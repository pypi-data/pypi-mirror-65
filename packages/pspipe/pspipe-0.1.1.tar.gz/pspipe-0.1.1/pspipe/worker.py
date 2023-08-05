# Multi-process, multi-nodes process executors
#
# Authors: F.Mertens

import os
import time
import socket
import signal
import getpass
import asyncio
import datetime

import asyncssh
import progressbar

from . import utils

localhost_shortname = socket.gethostname().split('.', 1)[0]


def kill_remote(host, user, pid):
    os.system(f'ssh {user}@{host} "kill -TERM -{pid}"')


class Task(object):
    """Represent a task executed by the worker pool

    Attributes:
        name (str): Name of the task (set by the worker pool).
        command (str): Command
        output_file (str): Optional log file. None if not set.
        returncode (int): Return code. None if task was not executed.
    """

    def __init__(self, name, command, output_file=None, done_callback=None):
        self.name = name
        self.command = command
        self.output_file = output_file
        self.fd = None
        self.returncode = None
        self.process = None
        self.n_try = 0
        self.remote_host = None
        self.remote_user = None
        self.done_callback = done_callback

    def init_log(self):
        if self.output_file is not None:
            self.fd = open(self.output_file, 'w')
            self.fd.write(f'# Logging starting at {datetime.datetime.now()}\n')
            self.fd.write(f'# Input command: {self.command}\n\n')

    def set_process(self, process, remote_host=None, remote_user=None):
        self.process = process
        self.remote_host = remote_host
        self.remote_user = remote_user

    async def terminate(self):
        if self.process is not None:
            if hasattr(self.process, 'pid'):
                if self.remote_host is None:
                    self.log(f'Killing local process PID {self.process.pid}', 'local', err=True)
                    os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
                else:
                    self.log(f'Killing remote process PID {self.process.pid}', self.remote_host, err=True)
                    kill_remote(self.remote_host, self.remote_user, self.process.pid)

    def log(self, line, host, err=False):
        if isinstance(line, bytes):
            line = line.decode()
        if self.fd is not None:
            self.fd.write(line)
        line = line.strip()
        if err:
            line = utils.red(line)
        print(f'[{self.name}:{host}] {line}')

    async def log_stream(self, stream, host, err=False):
        async for line in stream:
            self.log(line, host, err=err)

    def close_log(self):
        if self.fd is not None:
            try:
                self.fd.write(f'\n\n# Logging stopped at {datetime.datetime.now()}\n')
                self.fd.close()
            except Exception:
                print(f'Error closing log file for task {self.name}. Ignoring.')


class SSHClient(asyncssh.SSHClient):

    def __init__(self):
        self.connected = False

    def connection_made(self, conn):
        self.connected = True
        print('Connection made to %s.' % conn.get_extra_info('peername')[0])

    def connection_lost(self, exc):
        if exc:
            print('SSH client error: ' + str(exc))
            raise exc
        self.connected = False


class Client(object):

    def __init__(self, host, user=None, force_sync=True):
        self.host = host
        self.user = user
        self.conn = None
        self.client = None
        self.starting = False
        self.started = asyncio.Event()
        self.closing = False
        self.force_sync = force_sync
        self.creating_session = asyncio.Lock()

    async def start(self):
        if not self.starting:
            self.starting = True
            print(f'Starting client {self.host} ...')
            try:
                self.conn, self.client = await asyncssh.create_connection(SSHClient, self.host, username=self.user)
            except Exception:
                raise
            finally:
                self.started.set()

    async def execute(self, task):
        if not self.connected():
            raise ConnectionError('Client not connected')

        async with self.creating_session:
            process = await self.conn.create_process('echo $$;' + task.command)
        task.set_process(process, remote_host=self.host, remote_user=self.user)

        process.pid = await process.stdout.readline()

        await task.log_stream(process.stdout, self.host)
        await task.log_stream(process.stderr, self.host, err=True)

        process.channel.close()
        task.returncode = process.returncode

        if self.force_sync:
            await self.conn.run('sync')
            await asyncio.sleep(1)

    def close(self):
        if self.conn is not None and not self.closing:
            self.closing = True
            self.conn.close()
            self.conn = None

    def connected(self):
        return self.client is not None and self.client.connected


class LocalClient(object):

    def __init__(self, force_sync=True):
        self.host = 'local'
        self.started = asyncio.Event()
        self.force_sync = force_sync

    async def start(self):
        self.started.set()

    async def execute(self, task):
        process = await asyncio.create_subprocess_shell(task.command, stdout=asyncio.subprocess.PIPE,
                                                        stderr=asyncio.subprocess.PIPE, preexec_fn=os.setpgrp)
        task.set_process(process)

        await task.log_stream(process.stdout, self.host)
        await task.log_stream(process.stderr, self.host, err=True)

        task.returncode = await process.wait()

        if self.force_sync:
            os.sync()
            await asyncio.sleep(1)

    def connected(self):
        return self.started.is_set()

    def close(self):
        # nothing to do
        pass


class Worker(object):

    def __init__(self, client, name, pool, max_try=3):
        self.client = client
        self.name = name
        self.pool = pool
        self.running = True
        self.execute_start_time = None
        self.running_task = None
        self.max_try = max_try

    async def run(self):
        try:
            while True:
                task = await self.pool.queue.get()

                try:
                    task.init_log()
                    await self.client.start()
                    await self.client.started.wait()
                    self.execute_start_time = time.time()
                    self.running_task = task
                    await self.client.execute(task)

                    if task.done_callback is not None:
                        try:
                            task.done_callback()
                        except Exception as exc:
                            print(utils.red(f'Error executing return callback of task {self.name}: {str(exc)}'))
                            task.log(f'Error executing return callback of task {self.name}: {str(exc)}',
                                     self.client.host, err=True)
                except Exception as exc:
                    task.n_try += 1
                    if task.n_try < self.max_try:
                        await asyncio.sleep(1)
                        self.pool.queue.put_nowait(task)
                        print(utils.red(f'Error executing task {self.name}: {str(exc)}, will retry ...'))
                    else:
                        print(utils.red(f'Error executing task {self.name}: {str(exc)}'))
                        task.log(f'Error executing task {self.name}: {str(exc)}', self.client.host, err=True)
                    self.pool.queue.task_done()
                    self.running = False
                    break
                finally:
                    self.execute_start_time = None
                    self.running_task = None
                    task.close_log()

                self.pool.queue.task_done()
                self.pool.tasks_done.append(task)
                self.pool.pbar.update(len(self.pool.tasks_done))

        except asyncio.CancelledError:
            self.client.close()
        except Exception as exc:
            print(utils.red(f'Error in worker {self.name}: {str(exc)}'))
            raise
        finally:
            self.running = False


class WorkerPool(object):

    def __init__(self, hosts, name='Worker', max_tasks_per_worker=5,
                 env_source_file=None, user=None, max_time=None, force_sync=False):
        """Initiate a worker pool.

        Args:
            name (str): Name of the worker pool.
            hosts (list): List of host names, reachable via ssh (if not local host).
            max_tasks_per_worker (int, optional): Maximum number of tasks to execute concurrently on an host.
            env_source_file (str, optional): Name of a file to source before executing a task.
            user (str, optional): User to connect
        """
        if asyncio.get_event_loop().is_closed():
            asyncio.set_event_loop(asyncio.new_event_loop())

        if user is None:
            user = getpass.getuser()

        self.workers = []
        self.tasks = []
        self.queue = asyncio.Queue()
        self.tasks_done = []
        self.tasks_error = []
        self.tasks_timeout = []
        self.env_file = env_source_file
        self.max_time = max_time
        self.pbar = None
        self.name = name

        for host in hosts:
            if host == localhost_shortname:
                client = LocalClient(force_sync=force_sync)
            else:
                client = Client(host, user, force_sync=force_sync)
            for i in range(max_tasks_per_worker):
                worker = Worker(client, f'{client.host}:{i}', self)
                self.workers.append(worker)

    def add(self, command, name=None, output_file=None, done_callback=None):
        """Add a command to execute by a worker in the pool. Optionally output result in output_file.

        Args:
            command (str): Command to execute.
            name (str, optional): Name of the task. If not set it will be set by the worker pool
            output_file (str, optional): Optional filename to log output into.
        """
        if self.env_file is not None:
            command = "sh -c '. %s; %s'" % (self.env_file, command)
        if name is None:
            name = f'T{len(self.tasks)}'

        self.tasks.append(Task(name, command, output_file=output_file, done_callback=done_callback))

    async def _process_queue(self):
        for task in self.tasks:
            await self.queue.put(task)

        self.pbar.start(max_value=self.queue.qsize())

        futures = []
        for worker in self.workers:
            future = asyncio.ensure_future(worker.run())
            worker.future = future
            futures.append(future)
        futures.append(asyncio.ensure_future(self._monitor_queue()))

        # Wait until the queue is fully processed.
        await self.queue.join()

        # Cancel our worker tasks.
        for future in futures[::-1]:
            future.cancel()
        # Wait until all worker tasks are cancelled.
        await asyncio.gather(*futures, return_exceptions=False)

        self.pbar.finish(dirty=len(self.tasks_error) > 0 or self.queue.qsize() > 0)

    async def _monitor_queue(self, update_interval=2):
        try:
            while True:
                await asyncio.sleep(update_interval)
                self.pbar.update(len(self.tasks_done))
                active_workers = 0
                for w in self.workers:
                    if w.running:
                        active_workers += 1
                        if w.execute_start_time is not None and self.max_time is not None:
                            running_time = time.time() - w.execute_start_time
                            if running_time > (self.max_time + update_interval):
                                task = w.running_task
                                task.log(f'Task timeout: waited for {running_time:.2f} s', w.client.host, err=True)
                                task.log(f'Command was: {task.command}', w.client.host, err=True)
                                if task.n_try < w.max_try - 1:
                                    print(task.n_try, w.max_try)
                                    task.log('Will retry ...', w.client.host, err=True)
                                    self.queue.put_nowait(task)
                                    self.pbar.max_value += 1
                                    task.n_try += 1
                                await task.terminate()
                                await asyncio.sleep(1)

                if active_workers == 0:
                    print(f"No active workers, canceling all remaining tasks ...")
                    print(f"{self.queue.qsize()}")
                    for i in range(self.queue.qsize()):
                        self.tasks_error.append(self.queue.get_nowait())
                        self.queue.task_done()
                    print(f"{self.queue.qsize()}")

        except asyncio.CancelledError:
            pass

    def execute(self):
        """Execute all queue tasks.

        Returns:
            (list_done, list_error): Return a list of tasks executed successfully and tasks not executed.
        """
        widgets = [
            f"{utils.bold(self.name)}: ", progressbar.Percentage(), ' (',
            progressbar.SimpleProgress(), ')'
            ' ', progressbar.Bar(marker='|', left='[', right=']'),
            ' ', progressbar.Timer(),
            ' ', progressbar.ETA(),
        ]
        self.pbar = progressbar.ProgressBar(redirect_stdout=True, widgets=widgets)

        if not self.tasks:
            self.pbar.finish()
            return [], []

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._process_queue())

        return self.tasks_done, self.tasks_error

    def wait(self):
        self.execute()

    def close(self):
        pass


def main():
    # hosts = ['dawn.hpc.rug.nl'] * 2
    hosts = ['rug-laptop']
    # hosts = ['node101', 'node101']
    # hosts = ['rug-laptop', 'dawn.hpc.rug.nl', 'test']
    env_source_file = '/home/users/mertens/.activate_pspipe.sh'
    pool = WorkerPool(hosts, name='Reader', max_tasks_per_worker=2,
                      max_time=2, env_source_file=env_source_file)
    for i in range(4):
        # sleep_for = random.uniform(0.1, 1)
        sleep_for = 0.1
        if i == 3:
            sleep_for = 2
        pool.add(f'echo Task {i}; sleep {sleep_for}; echo Task {i}')  # , output_file=f'log/t{i}.log')
        # pool.add(f'dmesg|head; sleep 2; dmesg >&2', output_file=f't{i}.log')
        # pool.add('echo $(hostname) task %s' % i)
    done, err = pool.execute()
    print([k.returncode for k in done])


if __name__ == '__main__':
    main()
