# Mixed utilities
#
# Author: F. Mertens

import os
import re
import sys
import shutil
import itertools

import numpy as np

import tables as h5_tables
from casacore import tables

import astropy.time as at


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class FlagManager(object):

    def __init__(self, time, freqs, flag):
        self.time = time
        self.freqs = freqs
        self.flag = flag

    @staticmethod
    def load_from_ms(ms_file):
        print(f'Loading flag from MS {ms_file} ...')
        with tables.table(ms_file, readonly=True) as t:
            flag = t.getcol('FLAG')
            time = t.getcol('TIME')
            freqs, _ = get_ms_freqs(t)

        return FlagManager(time, freqs, flag)

    def save_to_ms(self, ms_file):
        print(f'Saving flag to MS {ms_file} ...')
        with tables.table(ms_file, readonly=False) as t:
            current_flag = t.getcol('FLAG')
            assert current_flag.shape == self.flag.shape
            t.putcol('FLAG', self.flag)

    @staticmethod
    def reset(ms_file):
        print(f'Reseting flag in MS {ms_file} ...')
        with tables.table(ms_file, readonly=False) as t:
            current_flag = t.getcol('FLAG')
            t.putcol('FLAG', np.zeros_like(current_flag, dtype=bool))

    @staticmethod
    def load(h5_file):
        print(f'Loading flag file {h5_file} ...')
        with h5_tables.open_file(h5_file, 'r') as h5:
            flag = h5.root.flag.flag.read()
            freqs = h5.root.flag.freqs.read()
            time = h5.root.flag.time.read()

        return FlagManager(time, freqs, flag)

    def save(self, h5_file):
        print(f'Saving flag file {h5_file} ...')
        with h5_tables.open_file(h5_file, 'w') as h5:
            group = h5.create_group("/", 'flag', 'Flag cube')
            h5.create_array(group, 'flag', self.flag, "Flags")
            h5.create_array(group, 'freqs', self.freqs, "Frequencies (Hz)")
            h5.create_array(group, 'time', self.time, "Time")


def save_flag(ms_file, flag_file):
    FlagManager.load_from_ms(ms_file).save(flag_file)


def restore_flag(ms_file, flag_file):
    FlagManager.load(flag_file).save_to_ms(ms_file)


def bold(s):
    return color.BOLD + s + color.END


def red(s):
    return color.RED + s + color.END


def yellow(s):
    return color.YELLOW + s + color.END


def format_table(data, header=None, min_col_size=8, max_col_size=None):
    ''' Return a table formatted version of data'''

    if len(data) == 0:
        dim = len(header)
    else:
        dim = len(data[0])
    if header:
        assert len(header) == dim
        data = [header] + [None] + data
    col_size = [min_col_size] * dim
    for i, line in enumerate(data):
        if line is None:
            # header delimitation
            continue
        assert len(line) == dim, "Dimension incorrect (%s != %s)" % (len(line), dim)
        new_line = [""] * dim
        for j in range(dim):
            s = str(line[j]).strip()
            if max_col_size is not None and len(s) > max_col_size:
                iws = s.rfind(" ", 0, max_col_size)
                if iws != -1 and iws > 0:
                    s, new_line[j] = s[:iws].strip(), s[iws:].strip()
            n = len(s) + 1
            data[i][j] = s
            if n > col_size[j]:
                col_size[j] = n
        if sum([len(k) for k in new_line]) > 0:
            data.insert(i + 1, new_line)
    res = ""
    for line in data:
        if line is None:
            res += "-" * (sum(col_size) + dim) + "\n"
            continue
        for i in range(dim):
            res += "%-*s" % (col_size[i], str(line[i])[:col_size[i]])
            res += '|'
        res += "\n"
    return res


def alphanum(s):
    return "".join(filter(str.isalnum, s))


def n_digits(i):
    return len(str(i))


def expend_num_ranges(s):
    r = re.split(r'\[([0-9-,]+)\]', s)
    for i in range(1, len(r), 2):
        if ',' in r[i]:
            r[i] = r[i].split(',')
        elif '-' in r[i]:
            s, e = r[i].split('-')
            n = max(n_digits(s), n_digits(e))
            r[i] = [str(k).rjust(n, '0') for k in range(int(s), int(e) + 1)]
    for i in range(0, len(r), 2):
        r[i] = [r[i]]
    for el in itertools.product(*r):
        yield ''.join(el)


def get_ms_freqs(ms_table):
    t_spec_win = tables.table(ms_table.getkeyword('SPECTRAL_WINDOW'), readonly=True, ack=False)
    freqs = t_spec_win.getcol('CHAN_FREQ').squeeze()
    chan_widths = t_spec_win.getcol('CHAN_WIDTH').squeeze()
    t_spec_win.close()

    return freqs, chan_widths


def get_info_from_ms_files(files):
    t_start = []
    t_end = []
    t_total = 0

    for file in files:
        t = tables.table(file, ack=False)
        time = t.getcol('TIME')
        t_start.append(time[0])
        t_end.append(time[-1])
        t_int = t.getcol('INTERVAL')[0]
        t_total += time[-1] - time[0]
        freqs, chan_widths = get_ms_freqs(t)
        n_chan = len(freqs)
        chan_width = chan_widths.mean()

    t_start = min(t_start)
    t_end = max(t_end)

    return {'start_time': t_start, 'end_time': t_end, 'int_time': t_int,
            'total_time': t_total, 'n_channels': n_chan, 'chan_width': chan_width}


def rm_if_exist(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)


def mkdir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def abspath(p):
    return os.path.abspath(os.path.expanduser(p))


def is_file(f):
    return os.path.isfile(os.path.expanduser(f))


def all_same(l):
    return not l or l.count(l[0]) == len(l)


def all_in_other(l, other):
    return all(elem in other for elem in l)


def get_lst(obs_mjd, longitude=6.57):
    return at.Time(obs_mjd, scale='utc', format='mjd').sidereal_time('mean', longitude=longitude).value


def is_in_lst_bin(lst, lst_s, lst_e):
    if lst_s == lst_e:
        return False
    if lst_e > lst_s:
        return (lst >= lst_s) and (lst < lst_e)
    return (lst >= lst_s) or (lst < lst_e)


def cinput(prompt):
    print(yellow(prompt), end='', flush=True)
    sys.stdout.flush()
    return input()


def ask(prompt, check_fct=False, check_re=False, check_list=False, default=None):
    ok = False
    while not ok:
        ok = True
        s = cinput(prompt + " ")
        if default is not None and s.strip() == '':
            return default
        if check_fct:
            ok = check_fct(s)
        if check_re:
            ok = re.match(check_re, s)
        if check_list:
            ok = bool(s in check_list)
        if not ok:
            print("Incorrect input\n")
    return s


def askbool(prompt, default=False):
    if not default:
        choice = " (Yes/[No])"
    else:
        choice = " ([Yes]/No)"

    def check_bool(v):
        return v.lower() in ["yes", "true", "y", "1", "no", "n", "false", "0"]

    ret = ask(prompt + choice, check_fct=check_bool, default=str(default))
    return ret.lower() in ["yes", "true", "1", "y"]
