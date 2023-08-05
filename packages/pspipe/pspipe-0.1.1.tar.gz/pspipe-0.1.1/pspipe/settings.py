# Handle setting
#
# Author: F. Mertens

import os
import shutil
from collections import OrderedDict

import toml

import astropy.units as u

from ps_eor import datacube

from . import attrmap, utils


TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

DEFAULT_SETTINGS = os.path.join(TEMPLATE_DIR, 'default_settings.toml')

TEMPLATE_NAMES = ['a12', 'nenufar', 'hba']


class Settings(attrmap.AttrMap):

    def __init__(self, file, d):
        attrmap.AttrMap.__init__(self, d)
        self.set_file(file)

    def _build(self, obj):
        if isinstance(obj, attrmap.Mapping):
            obj = Settings(self.get_file(), obj)

        return obj

    def set_file(self, file):
        self._setattr('_file', os.path.abspath(file) if file else file)

    def get_file(self):
        return self._file

    def get_path(self, key):
        path = self.get(key)
        if path:
            path = os.path.expanduser(path)
            if not os.path.isabs(path):
                if self.get_file():
                    path = os.path.join(os.path.dirname(self.get_file()), path)
                else:
                    path = os.path.abspath(path)
        return path

    def validate_keys(self):
        sd = Settings.get_defaults()
        invalid_keys = set(self.all_keys()) - set(sd.all_keys())
        if invalid_keys:
            print(f'Warning: invalid keys: {",".join(invalid_keys)}')
            return False
        return True

    @staticmethod
    def load(file, check_args=True):
        s = Settings(file, toml.load(file, _dict=OrderedDict))
        if check_args:
            s.validate_keys()

        return s

    @staticmethod
    def load_with_defaults(file, check_args=True):
        c_file = Settings.load(file, check_args=check_args)
        c_default = Settings.get_defaults()

        if 'default_settings' in c_file and c_file.default_settings:
            c_default += Settings.load(c_file.get_path('default_settings'), check_args=check_args)

        s = c_default + c_file
        s.set_file(file)
        return s

    @staticmethod
    def get_defaults():
        return Settings.load(DEFAULT_SETTINGS, check_args=False)

    @staticmethod
    def load_from_string(s, check_args=True):
        if isinstance(s, list):
            s = '\n'.join(s)
        d = toml.loads(s)

        s = Settings(None, d)
        if check_args:
            s.validate_keys()

        return s

    def save(self, file=None, strip_parents_keys=False):
        if not file:
            file = self.get_file()
        if not file:
            print('Error: No target filename to save settings.')
        else:
            m = self._mapping.copy()
            if strip_parents_keys and os.path.isfile(self.get_path('default_settings')):
                s_parent = Settings.load(self.default_settings)
                m = m - s_parent
            with open(file, mode='w') as f:
                toml.dump(dict(m), f)

    def duplicate(self, out_file, copy_parset_files=False, strip_parents_keys=False, **config_modifiers):
        s_out = self.copy()
        s_out.set_file(out_file)
        s_out['default_settings'] = ''

        cur_dir = os.path.dirname(self.get_file()) if self.get_file() else os.getcwd()
        new_dir = os.path.dirname(s_out.get_file()) if s_out.get_file() else os.getcwd()

        if new_dir and not os.path.exists(new_dir):
            os.makedirs(new_dir)

        if cur_dir != new_dir:
            if not os.path.isabs(s_out.data_dir):
                s_out['data_dir'] = os.path.join(cur_dir, s_out.data_dir)
            for p, k, v in s_out.all_items():
                if isinstance(v, str) and v.endswith('.parset') and not os.path.isabs(v):
                    if copy_parset_files:
                        utils.mkdir(os.path.join(new_dir, os.path.dirname(v)))
                        shutil.copyfile(os.path.join(cur_dir, v), os.path.join(new_dir, v))
                    elif not os.path.isabs(v):
                        p[k.split('.')[-1]] = os.path.join(cur_dir, v)

        if config_modifiers:
            s_out = s_out + config_modifiers

        s_out.save(strip_parents_keys=strip_parents_keys)

        return s_out

    def validate_image(self, val_fct):
        val_fct(u.Unit(self.image.scale).is_equivalent((u.rad, u.s)), 'scale')
        val_fct(len(self.image.size.split()) == 2 and all(k.isdigit() for k in self.image.size.split()), 'size')
        val_fct(self.image.channels_out == 'all' or self.image.channels_out.isdigit(), 'channels_out')
        val_fct(isinstance(self.image.umin, (int, float)), 'umin')
        val_fct(isinstance(self.image.umax, (int, float)), 'umax')
        val_fct(utils.all_in_other(set(self.image.stokes), set('IQUV')), 'stokes')
        val_fct(isinstance(self.image.split_even_odd, bool), 'split_even_odd')
        val_fct(isinstance(self.image.time_start_index, int), 'time_start_index')
        val_fct(isinstance(self.image.time_end_index, int), 'time_end_index')
        if self.image.time_end_index or self.image.time_start_index:
            val_fct(self.image.time_end_index >= self.image.time_start_index, 'time_end_index')
        val_fct(isinstance(self.image.lst_bins, list) and len(self.image.lst_bins) in [0, 3], 'lst_bins')

    def validate_worker(self, val_fct):
        val_fct(isinstance(self.worker.max_concurrent, int), 'max_concurrent')
        val_fct(not self.worker.env_file or utils.is_file(self.worker.env_file), 'env_file')

    def validate_merge_ms(self, val_fct):
        val_fct(isinstance(self.merge_ms.apply_aoflagger, bool), 'apply_aoflagger')
        val_fct(isinstance(self.merge_ms.blmin, (int, float)), 'blmin')
        val_fct(isinstance(self.merge_ms.blmax, (int, float)), 'blmax')
        val_fct(isinstance(self.merge_ms.avg_timestep, int), 'avg_timestep')
        val_fct(isinstance(self.merge_ms.time_start_index, int), 'time_start_index')
        val_fct(isinstance(self.merge_ms.time_end_index, int), 'time_end_index')
        if self.merge_ms.time_end_index or self.merge_ms.time_start_index:
            val_fct(self.merge_ms.time_end_index >= self.merge_ms.time_start_index, 'time_end_index')

    def validate_vis_cube(self, val_fct):
        val_fct(isinstance(self.vis_cube.fov, (int, float)), 'fov')
        val_fct(isinstance(self.vis_cube.umin, (int, float)), 'umin')
        val_fct(isinstance(self.vis_cube.umax, (int, float)), 'umax')
        val_fct(len(datacube.get_window(datacube.WindowFunction.parse_winfct_str(self.vis_cube.win_fct), 3)) == 3,
                'win_fct')

    def validate_vis_to_sph(self, val_fct):
        val_fct(utils.is_file(self.vis_to_sph.pre_flag), 'pre_flag')

    def validate_combine(self, val_fct):
        val_fct(isinstance(self.combine.scale_with_noise, bool), 'scale_with_noise')
        val_fct(isinstance(self.combine.inhomogeneous, bool), 'inhomogeneous')
        val_fct(self.combine.weights_mode in ['full', 'uv', 'global'], 'weights_mode')
        val_fct(utils.is_file(self.combine.pre_flag), 'pre_flag')

    def validate_power_spectra(self, val_fct):
        val_fct(utils.is_file(self.power_spectra.eor_bin_list), 'eor_bin_list')
        val_fct(utils.is_file(self.power_spectra.ps_config), 'ps_config')
        val_fct(utils.is_file(self.power_spectra.flagger), 'flagger')

    def validate_gpr(self, val_fct):
        val_fct(utils.is_file(self.gpr.config_i), 'config_i')
        val_fct(utils.is_file(self.gpr.config_v), 'config_v')

    def validate_ssins(self, val_fct):
        val_fct(isinstance(self.ssins.apply_ssins, bool), 'apply_ssins')
        val_fct(isinstance(self.ssins.n_time_avg, list), 'n_time_avg')
        for k in ['percentage_freq_full_flag', 'percentage_time_full_flag', 'time_freq_threshold',
                  'baseline_threshold', 'snapshot_threshold']:
            val_fct(isinstance(self.ssins[k], float), k)

    def validate(self, module):
        try:
            assert module in self

            def val_fct(v, k, m=module):
                assert v, f'{m}.{k}={getattr(self, m)[k]} is invalid'
            getattr(self, f'validate_{module}')(val_fct)

        except AssertionError as error:
            print(f'Error: {error}')
            return False
        except ValueError as error:
            print(f'Error: {error}')
            return False

        return True


def get_template_path(template_name):
    assert template_name in TEMPLATE_NAMES

    return os.path.join(TEMPLATE_DIR, f'default_{template_name}.toml')
