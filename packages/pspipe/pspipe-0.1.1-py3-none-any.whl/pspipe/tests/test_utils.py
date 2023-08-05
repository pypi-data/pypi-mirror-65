import os
import numpy as np

from pspipe import utils

from unittest import mock


class MockTable(object):

    def __init__(self, data, keywords):
        self.data = data
        self.keywords = keywords

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def getcol(self, col):
        return self.data[col]

    def putcol(self, col, newdata):
        self.data[col] = newdata

    def getkeyword(self, col):
        return self.keywords[col]

    def close(self):
        pass


class MockTables(object):

    def __init__(self):
        self.tables = dict()

    def set(self, name, data, keywords=None):
        self.tables[name] = (data, keywords)

    def table(self, name, **karg):
        return MockTable(*self.tables[name])


def test_format_table():
    d = [[1, 2, 3], ]
    assert utils.format_table(d, min_col_size=2) == '1 |2 |3 |\n'
    assert utils.format_table(d, min_col_size=4) == '1   |2   |3   |\n'
    h = ['a', 'b', 'c']
    assert utils.format_table(d, h, min_col_size=4) == 'a   |b   |c   |\n---------------\n1   |2   |3   |\n'


def test_alphanum():
    assert utils.alphanum('|sd dd 12.s ') == 'sddd12s'


def test_expend_num_ranges():
    assert list(utils.expend_num_ranges('n[0-2],k[2,3]')) == ['n0,k2', 'n0,k3', 'n1,k2', 'n1,k3', 'n2,k2', 'n2,k3']
    assert list(utils.expend_num_ranges('nk[8-11]')) == ['nk08', 'nk09', 'nk10', 'nk11']


def test_all_same():
    assert utils.all_same([1, 1, 1])
    assert not utils.all_same([1, 1, 2])
    assert not utils.all_same([1, 2, 1])
    assert utils.all_same(['a', 'a', 'a'])
    assert not utils.all_same(['a', 'a', 'a', 1])


def test_all_in_other():
    assert utils.all_in_other([1, 2], list(range(10)))
    assert not utils.all_in_other([1, 2, 10], list(range(10)))


def test_is_in_lst_bin():
    assert utils.is_in_lst_bin(2, 1, 3)
    assert utils.is_in_lst_bin(2, 2, 3)
    assert not utils.is_in_lst_bin(2, 3, 3)
    assert not utils.is_in_lst_bin(3, 2, 3)
    assert not utils.is_in_lst_bin(3, 21, 3)
    assert utils.is_in_lst_bin(2, 21, 3)
    assert utils.is_in_lst_bin(21, 21, 3)


def test_get_info_from_ms_files():
    t = MockTables()
    t.set('a', {'TIME': np.arange(0, 16, 4), 'INTERVAL': np.ones(4) * 4}, {'SPECTRAL_WINDOW': 'sw'})
    t.set('b', {'TIME': np.arange(8, 22, 4), 'INTERVAL': np.ones(4) * 4}, {'SPECTRAL_WINDOW': 'sw'})
    t.set('c', {'TIME': np.arange(20, 40, 4), 'INTERVAL': np.ones(4) * 4}, {'SPECTRAL_WINDOW': 'sw'})
    t.set('sw', {'CHAN_FREQ': np.arange(100, 140, 10), 'CHAN_WIDTH': np.ones(10) * 4})

    with mock.patch.object(utils, 'tables', t):
        d = utils.get_info_from_ms_files(['a', 'b', 'c'])
        assert d['start_time'] == 0
        assert d['end_time'] == 36
        assert d['total_time'] == 12 + 12 + 16
        assert d['n_channels'] == 4
        assert d['chan_width'] == 4


def test_ask():
    with mock.patch.object(utils, 'input', lambda: 'A'):
        assert utils.ask('Q') == 'A'
    with mock.patch.object(utils, 'input', lambda: '\n'):
        assert utils.ask('Q', default='B') == 'B'
    with mock.patch.object(utils, 'input', lambda: 'a'):
        assert utils.ask('Q', check_list=['a', 'b']) == 'a'
    answers = ['a', 'd', 'c']
    with mock.patch.object(utils, 'input', lambda: answers.pop()):
        assert utils.ask('Q', check_list=['a', 'b']) == 'a'
    answers = ['true', 'a']
    with mock.patch.object(utils, 'input', lambda: answers.pop()):
        assert utils.askbool('Q')
    answers = ['N', 'a']
    with mock.patch.object(utils, 'input', lambda: answers.pop()):
        assert not utils.askbool('Q')
    with mock.patch.object(utils, 'input', lambda: '\n'):
        assert utils.askbool('Q', default=True)


def test_flag_manager(tmp_path):
    t = MockTables()
    time = np.arange(5)
    flag = np.array([0, 0, 1, 0, 1])
    freqs = np.arange(100, 140, 10)
    t.set('a', {'FLAG': flag, 'TIME': time}, {'SPECTRAL_WINDOW': 'sw'})
    t.set('b', {'FLAG': np.zeros(5), 'TIME': time}, {'SPECTRAL_WINDOW': 'sw'})
    t.set('sw', {'CHAN_FREQ': freqs, 'CHAN_WIDTH': np.ones(10) * 4})

    with mock.patch.object(utils, 'tables', t):
        fm = utils.FlagManager.load_from_ms('a')
        assert np.allclose(fm.time, time)
        assert np.allclose(fm.flag, flag)
        assert np.allclose(fm.freqs, freqs)

        fm.save(tmp_path / 'test.h5')

        fm2 = utils.FlagManager.load(tmp_path / 'test.h5')
        assert np.allclose(fm2.time, time)
        assert np.allclose(fm2.flag, flag)
        assert np.allclose(fm2.freqs, freqs)

        fm2.save_to_ms('b')

        fm3 = utils.FlagManager.load_from_ms('b')
        assert np.allclose(fm3.time, time)
        assert np.allclose(fm3.flag, flag)
        assert np.allclose(fm3.freqs, freqs)
