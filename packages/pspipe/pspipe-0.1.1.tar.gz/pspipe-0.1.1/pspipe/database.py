# Database handler
#
# Author: F. Mertens

import os
import glob
import json
import fnmatch
from collections import OrderedDict

from . import attrmap
from .settings import Settings
from . import utils

import numpy as np

import astropy.time as at

from ps_eor import pspec, datacube, flagger, fgfit, psutil


OBS_ID_JSON_POSTFIX = '_obs_id.json'
IMG_REV_JSON = 'img_list.json'
OBS_VIS_REV_JSON = 'vis_list.json'

IMG_REV_TOML = 'img_config.toml'
OBS_VIS_REV_TOML = 'vis_config.toml'

all_stokes = ['I', 'V', 'Q', 'U']

obs_id_info_keys = ['start_time', 'end_time', 'int_time', 'total_time',
                    'n_channels', 'chan_width', 'is_sph', 'is_combined']


def even_odd_str(even, odd):
    if odd:
        return '_odd'
    if even:
        return '_even'
    return ''


def get_type_name(stokes_or_psf, even, odd):
    return stokes_or_psf.lower() + even_odd_str(even, odd)


def listdir_isdir(path, ignore=None):
    if not os.path.exists(path):
        return []
    return [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f)) and not f.startswith('.') and
            (ignore is None or f not in ignore)]


class Database(object):

    def __init__(self, settings_obj):
        self.settings = settings_obj

    def list_obs_ids(self):
        files = glob.glob(os.path.join(self.settings.get_path('data_dir'), 'obs_ids', f'*{OBS_ID_JSON_POSTFIX}'))
        return [os.path.basename(k).split(OBS_ID_JSON_POSTFIX)[0] for k in files]

    def filter_obs_ids(self, obs_id_str):
        all_obs_ids = self.list_obs_ids()
        return set(obs_id for k in obs_id_str.split(',') for obs_id in fnmatch.filter(all_obs_ids, k))

    def get_obs_id_meta_path(self, obs_id):
        return os.path.join(self.settings.get_path('data_dir'), 'obs_ids', obs_id + OBS_ID_JSON_POSTFIX)

    def get_obs_id_meta(self, obs_id):
        obs_id_meta_file = self.get_obs_id_meta_path(obs_id)
        if os.path.exists(obs_id_meta_file):
            return ObsIDMeta.load(obs_id_meta_file)
        return None

    def has_obs_id(self, obs_id):
        return os.path.exists(self.get_obs_id_meta_path(obs_id))

    def new_obs_id(self, obs_id, ms_files=None, **kargs):
        obs_id_meta_file = self.get_obs_id_meta_path(obs_id)
        os.makedirs(os.path.dirname(obs_id_meta_file), exist_ok=True)

        if ms_files is not None:
            obs_id_meta = ObsIDMeta.new_from_ms_list(obs_id_meta_file, obs_id, ms_files)
        else:
            obs_id_meta = ObsIDMeta.new(obs_id_meta_file, obs_id, **kargs)
        obs_id_meta.save()

        return obs_id_meta

    def new_obs_id_from_other(self, obs_id, other_obs_id_meta, **kargs):
        obs_id_meta_file = self.get_obs_id_meta_path(obs_id)
        os.makedirs(os.path.dirname(obs_id_meta_file), exist_ok=True)

        d = dict(other_obs_id_meta)
        d.update(kargs)
        del d['obs_id']

        obs_id_meta = ObsIDMeta.new(obs_id_meta_file, obs_id, **d)
        obs_id_meta.save()

        return obs_id_meta

    def has_image_revisions(self, img_rev):
        return img_rev in listdir_isdir(self.settings.get_path('data_dir'))

    def list_image_revisions(self):
        return [ImageRevision(Settings.load_with_defaults(k))
                for k in glob.glob(os.path.join(self.settings.get_path('data_dir'), '*', IMG_REV_TOML))]

    def get_image_revision(self, img_rev_name=None):
        img_rev_conf_file = ImageRevision(self.settings, img_rev_name).get_settings_path()
        if os.path.exists(img_rev_conf_file):
            return ImageRevision(Settings.load_with_defaults(img_rev_conf_file))
        if os.path.exists(os.path.dirname(img_rev_conf_file)):
            return ImageRevision(self.settings, img_rev_name=img_rev_name)
        return None

    def new_image_revision(self, img_rev_name=None):
        img_rev = ImageRevision(self.settings, img_rev_name=img_rev_name)
        img_rev.create()

        return img_rev

    def remove_obs_id(self, obs_id):
        for img_rev in self.list_image_revisions():
            img_rev.remove(obs_id)
        os.remove(self.get_obs_id_meta_path(obs_id))


class ImageRevision(object):

    def __init__(self, settings_obj, img_rev_name=None):
        self.settings = settings_obj.copy()
        if img_rev_name is not None:
            self.settings.image.name = img_rev_name
        self.name = self.settings.image.name

    def create(self):
        os.makedirs(self.get_path(), exist_ok=True)
        self.settings.duplicate(self.get_settings_path())

    def exist(self):
        return os.path.exists(self.get_settings_path())

    def get_lst_bins(self, obs_id, return_time_index=False):
        lst_bins = OrderedDict()
        if not self.settings.image.lst_bins:
            return None

        obs_meta = Database(self.settings).get_obs_id_meta(obs_id)
        start, end, interval = self.settings.image.lst_bins

        s2day = lambda sec: sec / 3600. / 24.
        hr2int = lambda hr: int(hr * 3600. / obs_meta.int_time)

        start_lst = utils.get_lst(s2day(obs_meta.start_time), self.settings.longitude)
        end_lst = utils.get_lst(s2day(obs_meta.end_time), self.settings.longitude)

        start_index = 0
        start_lst_idx = 0
        bin_int = hr2int(interval)

        for i, (s, e) in enumerate(psutil.pairwise(np.arange(start, end + interval, interval))):
            if utils.is_in_lst_bin(s, start_lst, end_lst) and utils.is_in_lst_bin(e, start_lst, end_lst):
                lst_bins[i] = [s, e]
            if utils.is_in_lst_bin(start_lst, s, e):
                start_index = hr2int(abs(e - start_lst))
                start_lst_idx = i

        end_index = start_index + bin_int * len(lst_bins) + 1

        if return_time_index:
            lst_idx = lst_bins.keys()
            data_lst_idx = np.arange(start_lst_idx + 1, start_lst_idx + 1 + len(lst_idx)) % (max(lst_idx) + 1)

            return lst_bins, (start_index, end_index, bin_int), data_lst_idx

        return lst_bins

    def get_path(self):
        return os.path.join(self.settings.get_path('data_dir'), self.settings.image.name)

    def get_image_path(self, obs_id):
        return os.path.join(self.get_path(), 'images', obs_id)

    def get_meta_path(self, obs_id, lst_idx=None):
        lst_str = f'_t{int(lst_idx):03}' if lst_idx is not None else ''
        return os.path.join(self.get_image_path(obs_id), f'img_list{lst_str}.json')

    def get_settings_path(self):
        return os.path.join(self.get_path(), IMG_REV_TOML)

    def get_settings(self):
        return Settings.load_with_defaults(self.get_settings_path())

    def list_obs_ids(self):
        return listdir_isdir(os.path.join(self.get_path(), 'images'))

    def has_obs_id(self, obs_id):
        return obs_id in self.list_obs_ids()

    def new_obs_id(self, obs_id, lst_idx=None):
        img_meta = ImageRevisionMeta.new(self.get_meta_path(obs_id, lst_idx=lst_idx), obs_id, self.settings.image.name)
        os.makedirs(os.path.dirname(self.get_meta_path(obs_id, lst_idx=lst_idx)), exist_ok=True)
        img_meta.save()

        return img_meta

    def get_meta(self, obs_id, lst_idx=None):
        meta_file = self.get_meta_path(obs_id, lst_idx=lst_idx)
        if os.path.exists(meta_file):
            return ImageRevisionMeta.load(meta_file)
        return None

    def list_vis_revisions(self):
        return [VisRevision(Settings.load_with_defaults(k)) for k in
                glob.glob(os.path.join(self.get_path(), 'vis_cubes_u*_fov*', OBS_VIS_REV_TOML))]

    def get_vis_revision(self, **vis_kargs):
        vis_rev_conf_file = VisRevision(self.settings, **vis_kargs).get_settings_path()
        if os.path.exists(vis_rev_conf_file):
            return VisRevision(Settings.load_with_defaults(vis_rev_conf_file))
        if os.path.exists(os.path.basename(vis_rev_conf_file)):
            return VisRevision(self.settings, **vis_kargs)
        return VisRevision(self.settings, **vis_kargs)

    def new_vis_revision(self, **vis_kargs):
        vis_rev = VisRevision(self.settings, **vis_kargs)
        vis_rev.create()

        return vis_rev

    def remove(self, obs_id=None):
        if obs_id is not None:
            for vis_rev in self.list_vis_revisions():
                vis_rev.remove(obs_id)
            utils.rm_if_exist(os.path.dirname(self.get_meta_path(obs_id)))
        else:
            utils.rm_if_exist(self.get_path())


class VisRevision(object):

    def __init__(self, settings_obj, img_rev_name=None, **vis_kargs):
        self.settings = settings_obj.copy()
        if img_rev_name is not None:
            self.settings.image.name = img_rev_name
        self.settings.vis_cube.update(vis_kargs)

    def create(self):
        os.makedirs(self.get_path(), exist_ok=True)
        self.settings.duplicate(self.get_settings_path())

    def exist(self):
        return os.path.exists(self.get_settings_path())

    def get_path(self):
        vis = self.settings.vis_cube
        vis_path = f'vis_cubes_u{vis.umin}-{vis.umax}_fov{vis.fov}'
        if 'tukey' not in vis.win_fct:
            vis_path += f'_{utils.alphanum(vis.win_fct)}'
        return os.path.join(self.settings.get_path('data_dir'), self.settings.image.name, vis_path)

    def get_h5_path(self, obs_id, lst_idx=None):
        if lst_idx is None:
            return os.path.join(self.get_path(), obs_id)
        return os.path.join(self.get_path(), obs_id, f't{int(lst_idx):03}')

    def get_result_path(self, obs_id, lst_idx=None):
        if lst_idx is None:
            return os.path.join(self.get_path(), 'results', obs_id)
        return os.path.join(self.get_path(), 'results', obs_id, f't{int(lst_idx):03}')

    def get_meta_path(self, obs_id, lst_idx=None):
        return os.path.join(self.get_h5_path(obs_id, lst_idx), 'vis_list.json')

    def get_settings_path(self):
        return os.path.join(self.get_path(), OBS_VIS_REV_TOML)

    def get_settings(self):
        return Settings.load_with_defaults(self.get_settings_path())

    def list_obs_ids(self):
        return listdir_isdir(self.get_path(), ['results'])

    def has_obs_id(self, obs_id):
        return obs_id in self.list_obs_ids()

    def new_obs_id(self, obs_id, lst_idx=None):
        img_meta = VisRevisionMeta.new(self.get_meta_path(obs_id, lst_idx=lst_idx), obs_id)
        os.makedirs(os.path.dirname(self.get_meta_path(obs_id, lst_idx=lst_idx)), exist_ok=True)
        img_meta.save()

        return img_meta

    def get_meta(self, obs_id, lst_idx=None):
        meta_file = self.get_meta_path(obs_id, lst_idx=lst_idx)
        if os.path.exists(meta_file):
            return VisRevisionMeta.load(meta_file)
        return None

    def get_data(self, obs_id, lst_idx=None):
        return ObsData(self, obs_id, lst_idx=lst_idx)

    def get_h5_file(self, obs_id, stokes, even=False, odd=False, lst_idx=None):
        vis = self.settings.vis_cube
        eo_str = even_odd_str(even, odd)
        w_str = utils.alphanum(vis.win_fct)[0]
        f = f'{obs_id}{eo_str}_{stokes}b{w_str}_fov{vis.fov}_u{vis.umin}-{vis.umax}.h5'

        return os.path.join(self.get_h5_path(obs_id, lst_idx=lst_idx), f)

    def remove(self, obs_id=None):
        if obs_id is not None:
            utils.rm_if_exist(os.path.dirname(self.get_meta_path(obs_id)))
        else:
            utils.rm_if_exist(self.get_path())


class AbstractJsonMeta(attrmap.AttrMap):

    def __init__(self, file, d):
        attrmap.AttrMap.__init__(self, d)
        self._file = file

    @classmethod
    def load(cls, json_filename):
        with open(json_filename) as json_file:
            data = json.load(json_file)

        return cls(json_filename, data)

    def save(self):
        with open(self._file, 'w') as json_file:
            json.dump(self._mapping, json_file, indent=4)


class ObsIDMeta(AbstractJsonMeta):

    @staticmethod
    def new(file, obs_id, **kargs):
        assert utils.all_in_other(kargs, obs_id_info_keys + ['ms_files'])

        d = {'obs_id': obs_id, 'ms_files': []}
        d.update(dict.fromkeys(obs_id_info_keys, 0))
        d.update(kargs)
        return ObsIDMeta(file, d)

    def set_ms_files(self, ms_files):
        self.update(utils.get_info_from_ms_files(ms_files[0]))
        self['ms_files'] = ms_files
        self.save()

    @staticmethod
    def new_from_ms_list(file, obs_id, ms_files):
        assert ms_files

        meta = ObsIDMeta.new(file, obs_id)
        meta.set_ms_files(ms_files)

        return meta


class ImageRevisionMeta(AbstractJsonMeta):

    @staticmethod
    def new(file, obs_id, img_rev):
        return ImageRevisionMeta(file, {'obs_id': obs_id, 'img_rev': img_rev})

    def get_fits(self, stokes_or_psf, even=False, odd=False):
        assert (even != odd) or (even is False)
        assert stokes_or_psf in all_stokes + ['psf', None]

        name = get_type_name(stokes_or_psf, even, odd)

        return self[name]

    def get_stokes(self, stokes, even=False, odd=False):
        return (self.get_fits(stokes, even, odd), self.get_fits('psf', even, odd))

    def has_stokes(self, stokes, even=False, odd=False):
        return get_type_name(stokes, even, odd) in self

    def get_all_stokes(self):
        return set(k.split('_')[0] for k in self if k.split('_')[0].upper() in all_stokes)

    def get_fits_stat(self):
        return dict((k, len(v)) for k, v in self.items() if isinstance(v, list) and len(v) > 0)

    def add_fits(self, files, stokes_or_psf=None, even=False, odd=False):
        assert (even != odd) or (even is False)
        assert stokes_or_psf in all_stokes + ['psf', None]

        if stokes_or_psf is not None:
            name = get_type_name(stokes_or_psf, even=even, odd=odd)
            if name not in self:
                self[name] = []

            self[name].extend(files)
        else:
            for stokes in all_stokes:
                sfiles = fnmatch.filter(files, f'*{stokes}-image.fits')
                if sfiles:
                    self.add_fits(sfiles, stokes, even=even, odd=odd)
            psf_files = fnmatch.filter(files, f'*psf.fits')
            if psf_files:
                self.add_fits(psf_files, 'psf', even=even, odd=odd)


class VisRevisionMeta(AbstractJsonMeta):

    @staticmethod
    def new(file, obs_id):
        return VisRevisionMeta(file, {'obs_id': obs_id})

    def add_h5(self, file, stokes, even=False, odd=False):
        self[get_type_name(stokes, even=even, odd=odd)] = file

    def get_stokes(self, stokes, even=False, odd=False):
        return self[get_type_name(stokes, even=even, odd=odd)]

    def has_stokes(self, stokes, even=False, odd=False):
        return get_type_name(stokes, even, odd) in self

    def get_all_stokes(self):
        return set(k.split('_')[0] for k in self if k.split('_')[0].upper() in all_stokes)


class ObsData(object):

    def __init__(self, vis_rev, obs_id, lst_idx=None):
        self.vis_rev = vis_rev
        self.obs_id = obs_id
        self.lst_idx = lst_idx
        self.settings = self.vis_rev.settings
        self.flag = None
        self.uvrange = None
        self.nfreqs = None
        self.data = {}
        self.all_stokes = {}
        for stokes in ['I', 'Q', 'U', 'V']:
            self.all_stokes[stokes.lower()] = stokes
            self.all_stokes[stokes.lower() + '_even'] = 'even_%s' % stokes
            self.all_stokes[stokes.lower() + '_odd'] = 'odd_%s' % stokes
            self.all_stokes[stokes.lower() + '_dt'] = 'dt_%s' % stokes
        self.ps_builder = pspec.PowerSpectraBuilder(self.settings.power_spectra.get_path('ps_config'),
                                                    self.settings.power_spectra.get_path('eor_bin_list'))

    def __getattr__(self, key):
        assert key in self.all_stokes.keys()
        return self.get_stokes(self.all_stokes[key])

    def __invalid_cache(self):
        self.data = {}

    def set_flag(self, flag):
        self.flag = flag
        self.__invalid_cache()

    def filter_uvrange(self, umin, umax):
        self.uvrange = [umin, umax]
        self.__invalid_cache()

    def average_freqs(self, nfreqs):
        self.nfreqs = nfreqs
        self.__invalid_cache()

    def do_flag(self, flagger_file=None, verbose_flagging=True, plot_flagging=True):
        if flagger_file is None:
            flagger_file = self.settings.power_spectra.get_path('flagger')
        flagger_runner = flagger.FlaggerRunner.load(flagger_file)
        flagger_runner.verbose = verbose_flagging
        flagger_runner.run(self.i, self.v)
        if plot_flagging:
            flagger_runner.plot()
        self.set_flag(flagger_runner.flag)

    def get_h5_file(self, stokes):
        return self.vis_rev.get_h5_file(self.obs_id, stokes, lst_idx=self.lst_idx)

    def get_stokes(self, stokes):
        if stokes not in self.data:
            path = self.get_h5_file(stokes)
            cube = datacube.CartDataCube.load(path)
            if self.uvrange is not None:
                cube.filter_uvrange(self.uvrange[0], self.uvrange[1])
            if self.nfreqs is not None:
                cube = cube.average_freqs(self.nfreqs)
            if self.flag is not None:
                cube = self.flag.apply(cube)
            self.data[stokes] = cube
        return self.data[stokes]

    def get_gpr_res(self, eor_bin, umin=50, umax=250, stokes='I'):
        path = os.path.join(os.path.dirname(self.get_h5_file(stokes)), f'eor{eor_bin}_u{umin}-{umax}')
        i_res = fgfit.GprForegroundResult.load(path, f'gpr_res_{stokes}')
        i_noise = datacube.CartDataCube.load(os.path.join(path, 'gpr_res_I.noise.h5'))
        i_res.noise = i_noise

        return i_res

    def get_ps_gen(self, **kargs):
        return self.ps_builder.get(self.i, **kargs)
