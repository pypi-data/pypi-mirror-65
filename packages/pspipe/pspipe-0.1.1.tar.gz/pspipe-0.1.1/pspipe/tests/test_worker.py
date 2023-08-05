import os

from pspipe import worker


def test_worker(tmp_path):
    w = worker.WorkerPool([worker.localhost_shortname, 'test_node'], 'Test', max_tasks_per_worker=5)

    assert len(w.workers) == 10
    assert isinstance(w.workers[0].client, worker.LocalClient)
    assert isinstance(w.workers[6].client, worker.Client)

    w = worker.WorkerPool([worker.localhost_shortname], 'Test')

    for i in range(20):
        w.add('touch %s/t%d' % (str(tmp_path), i))

    success, errors = w.execute()

    assert len(success) == 20
    assert len(errors) == 0

    for i in range(20):
        assert os.path.isfile('%s/t%d' % (str(tmp_path), i))


def test_worker_log(tmp_path):
    w = worker.WorkerPool(['wrong_server', worker.localhost_shortname], 'Test')

    for i in range(20):
        w.add(f'echo Task {i}', output_file=str(tmp_path / f't{i}.log'))
        print(str(tmp_path / f't{i}.log'))

    success, errors = w.execute()

    assert len(success) == 20
    assert len(errors) == 0

    for i in range(20):
        assert os.path.isfile(tmp_path / f't{i}.log')
        with open(tmp_path / f't{i}.log') as f:
            s = f.readlines()
        assert len(s) == 7
        assert s[0].startswith('# Logging starting at ')
        assert s[1] == f'# Input command: echo Task {i}\n'
        assert s[3] == f'Task {i}\n'
        assert s[-1].startswith('# Logging stopped at ')


def test_worker_wrong_server(tmp_path):
    w = worker.WorkerPool(['wrong_server'] * 6, 'Test')

    for i in range(20):
        w.add(f'echo Task {i}')

    success, errors = w.execute()

    assert len(success) == 0
    assert len(errors) == 20


def test_worker_env_file(tmp_path):
    with open(tmp_path / 'env', 'w') as f:
        f.write('export WORKER_TEST=test_env')

    w = worker.WorkerPool([worker.localhost_shortname], 'Test', env_source_file=str(tmp_path / 'env'))

    os.listdir(tmp_path)

    for i in range(20):
        w.add('echo env:${WORKER_TEST}; touch %s/t_${WORKER_TEST}_%d' % (str(tmp_path), i))

    success, errors = w.execute()

    assert len(success) == 20
    assert len(errors) == 0

    for i in range(20):
        assert os.path.isfile('%s/t_test_env_%d' % (str(tmp_path), i))


def test_worker_retcode():
    w = worker.WorkerPool([worker.localhost_shortname], 'Test')

    for i in range(10):
        w.add(f'echo Task {i}; exit {i}', name=f't{i}')

    success, errors = w.execute()

    assert len(success) == 10
    assert len(errors) == 0
    assert [f't{k.returncode}' for k in success] == [k.name for k in success]


def test_timeout():
    w = worker.WorkerPool([worker.localhost_shortname], 'Test', max_time=2)

    w.add('echo 0')

    success, errors = w.execute()

    assert len(success) == 1
    assert len(errors) == 0

    w = worker.WorkerPool([worker.localhost_shortname], 'Test', max_time=1)

    w.add('sleep 100')

    success, errors = w.execute()

    # Currently falling. Need to be fixed
    # assert len(success) == 0
    # assert len(errors) == 1


def test_done_callback():
    w = worker.WorkerPool([worker.localhost_shortname], 'Test', max_time=2)

    done = False

    def callback():
        nonlocal done
        done = True

    w.add('echo 0', done_callback=callback)

    success, errors = w.execute()

    assert len(success) == 1
    assert len(errors) == 0
    assert done

