# -*- coding: utf-8 -*-
#! /usr/bin/python
"""
Thie imas-compatibility module of tofu

Default parameters and input checking

"""

# Built-ins
import sys
import os
import itertools as itt
import copy
import functools as ftools
import getpass
import inspect
import warnings
import traceback

# Standard
import numpy as np
import matplotlib as mpl
import datetime as dtm

# tofu
pfe = os.path.join(os.path.expanduser('~'), '.tofu', '_imas2tofu_def.py')
if os.path.isfile(pfe):
    # Make sure we load the user-specific file
    # sys.path method
    # sys.path.insert(1, os.path.join(os.path.expanduser('~'), '.tofu'))
    # import _scripts_def as _defscripts
    # _ = sys.path.pop(1)
    # importlib method
    import importlib.util
    spec = importlib.util.spec_from_file_location("_defimas2tofu", pfe)
    _defimas2tofu = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_defimas2tofu)
else:
    try:
        import tofu.imas2tofu._def as _defimas2tofu
    except Exception as err:
        from . import _def as _defimas2tofu

# imas
try:
    import imas
except Exception as err:
    raise Exception('imas not available')

__all__ = ['MultiIDSLoader',
           'load_Config', 'load_Plasma2D',
           'load_Cam', 'load_Data',
           '_save_to_imas']


# public imas user (used for checking if can be saved)
_IMAS_USER_PUBLIC = 'imas_public'

# Default IMAS parameters (default for loading)
_IMAS_USER = 'imas_public'
_IMAS_SHOT = 0
_IMAS_RUN = 0
_IMAS_OCC = 0
_IMAS_TOKAMAK = 'west'
_IMAS_VERSION = '3'
_IMAS_SHOTR = -1
_IMAS_RUNR = -1
_IMAS_DIDD = {'shot': _IMAS_SHOT, 'run': _IMAS_RUN,
              'refshot': _IMAS_SHOTR, 'refrun': _IMAS_RUNR,
              'user': _IMAS_USER, 'tokamak': _IMAS_TOKAMAK,
              'version': _IMAS_VERSION}

# Root tofu path (for saving repo in IDS)
_ROOT = os.path.abspath(os.path.dirname(__file__))
_ROOT = _ROOT[:_ROOT.index('tofu')+len('tofu')]


#############################################################
#############################################################
#           IdsMultiLoader
#############################################################


class MultiIDSLoader(object):
    """ Class for handling multi-ids possibly from different idd

    For each desired ids (e.g.: core_profile, ece, equilibrium...), you can
    specify a different idd (i.e.: (shot, run, user, tokamak, version))

    The instance will remember from which idd each ids comes from.
    It provides a structure to keep track of these dependencies
    Also provides methods for opening idd and getting ids and closing idd

    """



    ###################################
    #       Default class attributes
    ###################################

    _def = {'isget':False,
            'ids':None, 'occ':0, 'needidd':True}
    _defidd = _IMAS_DIDD

    _lidsnames = [k for k in dir(imas) if k[0] != '_']
    _lidsk = ['tokamak', 'user', 'version',
              'shot', 'run', 'refshot', 'refrun']

    # Known short version of signal str
    _dshort = _defimas2tofu._dshort
    _didsdiag = _defimas2tofu._didsdiag
    _lidsplasma = ['equilibrium', 'core_profiles', 'core_sources',
                   'edge_profiles', 'edge_sources']

    _lidsdiag = sorted([kk for kk,vv in _didsdiag.items() if 'sig' in vv.keys()])
    _lidssynth = sorted([kk for kk,vv in _didsdiag.items() if 'synth' in vv.keys()])
    _lidslos = list(_lidsdiag)
    for ids_ in _lidsdiag:
        if _didsdiag[ids_]['geomcls'] not in ['CamLOS1D']:
            _lidslos.remove(ids_)

    for ids_ in _lidssynth:
        for kk,vv in _didsdiag[ids_]['synth']['dsynth'].items():
            if type(vv) is str:
                vv = [vv]
            for ii in range(0,len(vv)):
                v0, v1 = vv[ii].split('.')
                if v0 not in _didsdiag[ids_]['synth']['dsig'].keys():
                    _didsdiag[ids_]['synth']['dsig'][v0] = [v1]
                elif v1 not in _didsdiag[ids_]['synth']['dsig'][v0]:
                    _didsdiag[ids_]['synth']['dsig'][v0].append(v1)
            _didsdiag[ids_]['synth']['dsynth'][kk] = vv

    for ids in _lidslos:
        dlos = {}
        strlos = 'line_of_sight'
        if ids == 'reflectometer_profile':
            strlos += '_detection'
        dlos['los_pt1R'] = {'str':'channel[chan].%s.first_point.r'%strlos}
        dlos['los_pt1Z'] = {'str':'channel[chan].%s.first_point.z'%strlos}
        dlos['los_pt1Phi'] = {'str':'channel[chan].%s.first_point.phi'%strlos}
        dlos['los_pt2R'] = {'str':'channel[chan].%s.second_point.r'%strlos}
        dlos['los_pt2Z'] = {'str':'channel[chan].%s.second_point.z'%strlos}
        dlos['los_pt2Phi'] = {'str':'channel[chan].%s.second_point.phi'%strlos}
        _dshort[ids].update( dlos )

    # Computing functions

    def _events(names, t):
        ustr = 'U{}'.format(np.nanmax(np.char.str_len(np.char.strip(names))))
        return np.array([(nn, tt)
                         for nn, tt in zip(*[np.char.strip(names), t])],
                        dtype=[('name', ustr), ('t', np.float)])

    def _RZ2array(ptsR, ptsZ):
        return np.array([ptsR, ptsZ]).T

    def _losptsRZP(*pt12RZP):
        return np.swapaxes([pt12RZP[:3], pt12RZP[3:]], 0, 1).T

    def _add(a0, a1):
        return np.abs(a0 + a1)

    def _eqB(BT, BR, BZ):
        return np.sqrt(BT**2 + BR**2 + BZ**2)

    def _icmod(al, ar, axis=0):
        return np.sum(al - ar, axis=axis)

    def _icmodadd(al0, ar0, al1, ar1, al2, ar2, axis=0):
        return (np.sum(al0 - ar0, axis=axis)
                + np.sum(al1 - ar1, axis=axis)
                + np.sum(al2 - ar2, axis=axis))

    def _rhopn1d(psi):
        return np.sqrt((psi - psi[:, 0:1]) / (psi[:, -1] - psi[:, 0])[:, None])

    def _rhopn2d(psi, psi0, psisep):
        return np.sqrt(
            (psi - psi0[:, None]) / (psisep[:, None] - psi0[:, None]))

    def _rhotn2d(phi):
        return np.sqrt(np.abs(phi) / np.nanmax(np.abs(phi), axis=1)[:, None])

    def _eqSep(sepR, sepZ, npts=100):
        nt = len(sepR)
        assert len(sepZ) == nt
        sep = np.full((nt,npts,2), np.nan)
        pts = np.linspace(0,100,npts)
        for ii in range(0,nt):
            ptsii = np.linspace(0,100,sepR[ii].size)
            sep[ii,:,0] = np.interp(pts, ptsii, sepR[ii])
            sep[ii,:,1] = np.interp(pts, ptsii, sepZ[ii])
        return sep
    def _eqtheta(axR, axZ, nodes, cocos=11):
        theta = np.arctan2(nodes[:,0][None,:] - axZ[:,None],
                           nodes[:,1][None,:] - axR[:,None])
        if cocos == 1:
            theta = -theta
        return theta

    def _rhosign(rho, theta):
        ind = np.cos(theta) < 0.
        rho[ind] = -rho[ind]
        return rho

    def _lamb(lamb_up, lamb_lo):
        return 0.5*(lamb_up + lamb_lo)

    _dcomp = {
              'pulse_schedule':
              {'events':{'lstr':['events_names','events_times'], 'func':_events}},

              'wall':
              {'wall':{'lstr':['wallR','wallZ'], 'func':_RZ2array}},

              'equilibrium':
              {'ax':{'lstr':['axR','axZ'], 'func':_RZ2array},
               'sep':{'lstr':['sepR','sepZ'],
                      'func':_eqSep, 'kargs':{'npts':100}},
               '2dB':{'lstr':['2dBT', '2dBR', '2dBZ'], 'func':_eqB,
                      'dim':'B', 'quant':'B', 'units':'T'},
               '1drhopn':{'lstr':['1dpsi','psiaxis','psisep'], 'func':_rhopn2d,
                          'dim':'rho', 'quant':'rhopn', 'units':'adim.'},
               '2drhopn':{'lstr':['2dpsi','psiaxis','psisep'], 'func':_rhopn2d,
                          'dim':'rho', 'quant':'rhopn', 'units':'adim.'},
               '2drhotn':{'lstr':['2dphi'], 'func':_rhotn2d,
                          'dim':'rho', 'quant':'rhotn', 'units':'adim.'},
               'x0':{'lstr':['x0R','x0Z'], 'func':_RZ2array},
               'x1':{'lstr':['x1R','x1Z'], 'func':_RZ2array},
               'strike0':{'lstr':['strike0R','strike0Z'], 'func':_RZ2array},
               'strike1':{'lstr':['strike1R','strike1Z'], 'func':_RZ2array},
               '2dtheta':{'lstr':['axR','axZ','2dmeshNodes'],
                          'func':_eqtheta, 'kargs':{'cocos':11}}},

              'core_profiles':
             {'1drhopn':{'lstr':['1dpsi'], 'func':_rhopn1d,
                         'dim':'rho', 'quant':'rhopn', 'units':'adim.'}},

              'core_sources':
             {'1drhopn':{'lstr':['1dpsi'], 'func':_rhopn1d,
                         'dim':'rho', 'quant':'rhopn', 'units':'adim.'},
              '1dprad':{'lstr':['1dbrem','1dline'], 'func':_add,
                        'dim':'vol. emis.', 'quant':'prad', 'unit':'W/m3'}},

             'magnetics':
             {'bpol_pos':{'lstr':['bpol_R', 'bpol_Z'], 'func':_RZ2array},
              'floop_pos':{'lstr':['floop_R', 'floop_Z'], 'func':_RZ2array}},

             'ic_antennas': {
                'power0': {'lstr': ['power0mod_fwd', 'power0mod_reflect'],
                           'func': _icmod, 'kargs': {'axis': 0}, 'pos': True},
                'power1': {'lstr': ['power1mod_fwd', 'power1mod_reflect'],
                           'func': _icmod, 'kargs': {'axis': 0}, 'pos': True},
                'power2': {'lstr': ['power2mod_fwd', 'power2mod_reflect'],
                           'func': _icmod, 'kargs': {'axis': 0}, 'pos': True},
                'power': {'lstr': ['power0mod_fwd', 'power0mod_reflect',
                                   'power1mod_fwd', 'power1mod_reflect',
                                   'power2mod_fwd', 'power2mod_reflect'],
                          'func': _icmodadd, 'kargs': {'axis': 0},
                          'pos': True}},

             'ece':
             {'rhotn_sign':{'lstr':['rhotn','theta'], 'func':_rhosign,
                            'units':'adim.'}},

             'bremsstrahlung_visible':
             {'lamb': {'lstr': ['lamb_up', 'lamb_lo'], 'func': _lamb,
                       'dim': 'distance',
                       'quantity': 'wavelength',
                       'units': 'm'}}
            }

    _lstr = ['los_pt1R', 'los_pt1Z', 'los_pt1Phi',
             'los_pt2R', 'los_pt2Z', 'los_pt2Phi']
    for ids in _lidslos:
        _dcomp[ids] = _dcomp.get(ids, {})
        _dcomp[ids]['los_ptsRZPhi'] = {'lstr':_lstr, 'func':_losptsRZP}


    # Uniformize
    _lids = set(_dshort.keys()).union(_dcomp.keys())
    for ids in _lids:
        _dshort[ids] = _dshort.get(ids, {})
        _dcomp[ids] = _dcomp.get(ids, {})

    # All except (for when sig not specified in get_data())
    _dall_except = {}
    for ids in _lidslos:
        _dall_except[ids] = _lstr
    _dall_except['equilibrium'] = ['axR','axZ','sepR','sepZ',
                                   '2dBT','2dBR','2dBZ',
                                   'x0R','x0Z','x1R','x1Z',
                                   'strike0R','strike0Z', 'strike1R','strike1Z']
    _dall_except['magnetics'] = ['bpol_R', 'bpol_Z', 'floop_R', 'floop_Z']
    _dall_except['ic_antennas'] = ['power0mod_launched', 'power0mod_reflected',
                                   'power1mod_launched', 'power1mod_reflected',
                                   'power2mod_launched', 'power2mod_reflected']


    # Preset

    _dpreset = {
                'overview':
                {'wall':None,
                 'pulse_schedule':None,
                 'equilibrium':None},

                'plasma2d':
                {'wall':['domainR','domainZ'],
                 'equilibrium':['t','ax','sep'],
                 'core_profiles':['t','1dTe','1dne','1dzeff','1drhotn','1dphi'],
                 'core_sources':['t','1dprad'],
                 'edge_profiles':['t'],
                 'edge_sources':['t']},

                'ece':
                {'wall':['domainR','domainZ'],
                 'ece':None,
                 'core_profiles':['t','Te','ne']}
               }

    _IDS_BASE = ['wall', 'pulse_schedule']


    ###################################
    ###################################
    #       Methods
    ###################################


    def __init__(self, preset=None, dids=None, ids=None, occ=None, idd=None,
                 shot=None, run=None, refshot=None, refrun=None,
                 user=None, tokamak=None, version=None,
                 ids_base=None, synthdiag=None, get=None, ref=True):
        """ A class for handling multiple ids loading from IMAS

        IMAS provides access to a database via a standardized structure (idd
        and ids). This class is a convenient tool to interact with IMAS.

        idd: An IMAS data dictionnary (idd) is like a 'shotfile', it contains
            all data for a given shot, in a given version.
            An idd is identified by:
                - user:     the name of the user to whom the idd belongs.
                            Indeed, each idd can e stored in an official
                            centralized database identified by a generic user
                            name (e.g.: 'public') or locally on a personnal
                            database identified by your own user name.
                            An idd stored locally on the database of user A can
                            be read by other users if they provide the
                            user name 'A'.
                - tokamak:  the name of the experiment (e.g.: 'ITER')
                - shot:     the shot number
                - run:      It's the 'version' of the shotfile.
                            Indeed, IMAS allows to store both experimental and
                            simulation data. A given experimental data can
                            exist in several versions (more or less filtered or
                            treated) and the same goes for simulation data (the
                            same simulation can be run with different sets of
                            parameters, or with a different code).
                            For a given shot, several runs can exist

        ids: Once the idd has been chosen, it contains all the available data
            in the form of IMAS data Structures (ids).
            Each ids contains a 'family' or 'group' of data. It has an explicit
            name to indicate what that group is.
            There are typically diagnostic ids (e.g.: 'barometry',
            'intereferometer', 'soft_x_rays', ...) that contain all data
            produced by these diagnostics (with their time bases, units...),
            advanced data treatment ids (e.g.: 'equilibrium'...) and simulation
            ids (e.g.: 'core_profiles', 'edge_sources'...)

        In a typical use case, you would want to load all data from several ids
        from the same idd (e.g.: from the official centralized idd of a shot
        that contains official, validated data).
        But for some analysis, you may want to load different ids from
        different idd (e.g.: to compare official experimental data of a
        diagnostics to synthetic data computed from the core profiles produced
        by a simulation and interpolated via an equilibrium produced by a
        third-party code).

        This class provides an easy interface to access several ids from
        several idd (or a unique idd of course).


        Example
        -------

        # Tis will load 2 ids from the same public idd
        # But we know we will need to add another ids from a different idd
        # So we instanciate the class and secpify get=False to postpone the
        # data loading itself until we have added all we need
        import tofu as tf
        user = 'imas_public'
        ids = ['interferometer', 'polarimeter']
        multi = tf.imas2tofu.MultiIDSLoader(shot=55583, user=user,
                                            tokamak='west', ids=ids, get=False)

        # This will ad an ids from a different idd and automatically load
        # ('get') everything
        multi.add_ids('bolometer', shot=55583, user='myusername',
                      tokamak='west')

        # To have an overview of what your multi instance contains, type
        multi

        """
        super(MultiIDSLoader, self).__init__()

        # Initialize dicts
        self._init_dict()

        # Check and format inputs
        if dids is None:
            self.add_idd(idd=idd,
                         shot=shot, run=run, refshot=refshot, refrun=refrun,
                         user=user, tokamak=tokamak, version=version, ref=ref)
            lidd = list(self._didd.keys())
            assert len(lidd) <= 1
            idd = lidd[0] if len(lidd) > 0 else None
            self.add_ids(preset=preset, ids=ids, occ=occ, idd=idd, get=False)
            if ids_base is None:
                if not all([iids in self._IDS_BASE
                            for iids in self._dids.keys()]):
                    ids_base = True
            if ids_base is True:
                self.add_ids_base(get=False)
            if synthdiag is None:
                synthdiag = False
            if synthdiag is True:
                self.add_ids_synthdiag(get=False)
            if get is None and (len(self._dids) > 0 or preset is not None):
                get = True
        else:
            self.set_dids(dids)
            if get is None:
                get = True
        self._set_fsig()
        if get is True:
            self.open_get_close()

    def _init_dict(self):
        self._didd = {}
        self._dids = {}
        self._refidd = None
        self._preset = None

    def set_dids(self, dids=None):
        didd, dids, refidd = self._get_diddids(dids)
        self._dids = dids
        self._didd = didd
        self._refidd = refidd


    @classmethod
    def _get_diddids(cls, dids, defidd=None):

        # Check input
        assert type(dids) is dict
        assert all([type(kk) is str for kk in dids.keys()])
        assert all([kk in cls._lidsnames for kk in dids.keys()])
        if defidd is None:
            defidd = cls._defidd
        didd = {}

        # Check ids
        for k, v in dids.items():

            lc0 = [v is None or v == {}, type(v) is dict, hasattr(v, 'ids_properties')]
            assert any(lc0)
            if lc0[0]:
                dids[k] = {'ids':None}
            elif lc0[-1]:
                dids[k] = {'ids':v}
            dids[k]['ids'] = dids[k].get('ids', None)
            v = dids[k]

            # Implement possibly missing default values
            for kk, vv in cls._def.items():
                dids[k][kk] = v.get(kk, vv)
            v = dids[k]

            # Check / format occ and deduce nocc
            assert type(dids[k]['occ']) in [int, list]
            dids[k]['occ'] = np.r_[dids[k]['occ']].astype(int)
            dids[k]['nocc'] = dids[k]['occ'].size
            v = dids[k]

            # Format isget / get
            for kk in ['isget']:    #, 'get']:
                assert type(v[kk]) in [bool, list]
                v[kk] = np.r_[v[kk]].astype(bool)
                assert v[kk].size in set([1,v['nocc']])
                if v[kk].size < v['nocc']:
                    dids[k][kk] = np.repeat(v[kk], v['nocc'])
            v = dids[k]

            # Check / format ids
            lc = [v['ids'] is None, hasattr(v['ids'], 'ids_properties'),
                  type(v['ids']) is list]
            assert any(lc)
            if lc[0]:
                dids[k]['needidd'] = True
            elif lc[1]:
                assert v['nocc'] == 1
                dids[k]['ids'] = [v['ids']]
                dids[k]['needidd'] = False
            elif lc[2]:
                assert all([hasattr(ids, 'ids_properties') for ids in v['ids']])
                assert len(v['ids']) == v['nocc']
                dids[k]['needidd'] = False
            v = dids[k]

            # ----------------
            # check and open idd, populate didd
            # ----------------
            idd = v.get('idd', None)
            if idd is None:
                dids[k]['idd'] = None
                continue
            kwargs = {}
            if type(idd) is dict:
                idd, kwargs = None, idd
            diddi = cls._checkformat_idd(idd=idd, **kwargs)

            name = list(diddi.keys())[0]
            didd[name] = diddi[name]
            dids[k]['idd'] = name


        # --------------
        #   Now use idd for ids without idd needing one
        # --------------

        # set reference idd, if any
        lc = [(k,v['needidd']) for k,v in dids.items()]
        lc0, lc1 = zip(*lc)
        refidd = None
        if any(lc1):
            if len(didd) == 0:
                msg = "The following ids need an idd to be accessible:\n"
                msg += "    - "
                msg += "    - ".join([lc0[ii] for ii in range(0,len(lc0))
                                      if lc1[ii]])
                raise Exception(msg)
            refidd = list(didd.keys())[0]

        # set missing idd to ref
        need = False
        for k, v in dids.items():
            lc = [v['needidd'], v['idd'] is None]
            if all(lc):
                dids[k]['idd'] = refidd

        return didd, dids, refidd


    #############
    # properties

    @property
    def dids(self):
        return self._dids
    @property
    def didd(self):
        return self._didd
    @property
    def refidd(self):
        return self._refidd

    #############
    #############
    # methods
    #############


    #############
    # shortcuts

    @staticmethod
    def _getcharray(ar, col=None, sep='  ', line='-', just='l', msg=True):
        c0 = ar is None or len(ar) == 0
        if c0:
            return ''
        ar = np.array(ar, dtype='U')

        if ar.ndim == 1:
            ar = ar.reshape((1, ar.size))

        # Get just len
        nn = np.char.str_len(ar).max(axis=0)
        if col is not None:
            if len(col) not in ar.shape:
                msg = ("len(col) should be in np.array(ar, dtype='U').shape:\n"
                       + "\t- len(col) = {}\n".format(len(col))
                       + "\t- ar.shape = {}".format(ar.shape))
                raise Exception(msg)
            if len(col) != ar.shape[1]:
                ar = ar.T
                nn = np.char.str_len(ar).max(axis=0)
            nn = np.fmax(nn, [len(cc) for cc in col])

        # Apply to array
        fjust = np.char.ljust if just == 'l' else np.char.rjust
        out = np.array([sep.join(v) for v in fjust(ar,nn)])

        # Apply to col
        if col is not None:
            arcol = np.array([col, [line*n for n in nn]], dtype='U')
            arcol = np.array([sep.join(v) for v in fjust(arcol,nn)])
            out = np.append(arcol,out)

        if msg:
            out = '\n'.join(out)
        return out

    @staticmethod
    def _shortcuts(obj, ids=None, return_=False,
                   verb=True, sep='  ', line='-', just='l'):
        if ids is None:
            if hasattr(obj, '_dids'):
                lids = list(obj._dids.keys())
            else:
                lids = list(obj._dshort.keys())
        elif ids == 'all':
            lids = list(obj._dshort.keys())
        else:
            lc = [type(ids) is str, type(ids) is list and all([type(ss) is str
                                                               for ss in ids])]
            assert any(lc), "ids must be an ids name or a list of such !"
            if lc[0]:
                lids = [ids]
            else:
                lids = ids
        lids = sorted(set(lids).intersection(obj._dshort.keys()))

        short = []
        for ids in lids:
            lks = obj._dshort[ids].keys()
            if ids in obj._dcomp.keys():
                lkc = obj._dcomp[ids].keys()
                lk = sorted(set(lks).union(lkc))
            else:
                lk = sorted(lks)
            for kk in lk:
                if kk in lks:
                    ss = obj._dshort[ids][kk]['str']
                else:
                    ss = 'f( %s )'%(', '.join(obj._dcomp[ids][kk]['lstr']))
                short.append((ids, kk, ss))

        if verb:
            col = ['ids', 'shortcut', 'long version']
            msg = obj._getcharray(short, col, sep=sep, line=line, just=just)
            print(msg)
        if return_:
            return short

    @classmethod
    def get_shortcutsc(cls, ids=None, return_=False,
                       verb=True, sep='  ', line='-', just='l'):
        """ Display and/or return the builtin shortcuts for imas signal names

        By default (ids=None), only display shortcuts for stored ids
        To display all possible shortcuts, use ids='all'
        To display shortcuts for a specific ids, use ids=<idsname>

        These shortcuts can be customized (with self.set_shortcuts())
        They are useful for use with self.get_data()

        """
        return cls._shortcuts(cls, ids=ids, return_=return_, verb=verb,
                              sep=sep, line=line, just=just)

    def get_shortcuts(self, ids=None, return_=False,
                      verb=True, sep='  ', line='-', just='l'):
        """ Display and/or return the builtin shortcuts for imas signal names

        By default (ids=None), only display shortcuts for stored ids
        To display all possible shortcuts, use ids='all'
        To display shortcuts for a specific ids, use ids=<idsname>

        These shortcuts can be customized (with self.set_shortcuts())
        They are useful for use with self.get_data()

        """
        return self._shortcuts(self, ids=ids, return_=return_, verb=verb,
                               sep=sep, line=line, just=just)

    def set_shortcuts(self, dshort=None):
        """ Set the dictionary of shortcuts

        If None, resets to the class's default dict
        """
        dsh = copy.deepcopy(self.__class__._dshort)
        if dshort is not None:
            c0 = type(dshort) is dict
            c1 = c0 and all([k0 in self._lidsnames and type(v0) is dict
                             for k0,v0 in dshort.items()])
            c2 = c1 and all([all([type(k1) is str and type(v1) in {str,dict}
                                  for k1,v1 in v0.items()])
                             for v0 in dshort.values()])
            if not c2:
                msg = "Arg dshort should be a dict with valid ids as keys:\n"
                msg += "    {'ids0': {'shortcut0':'long_version0',\n"
                msg += "              'shortcut1':'long_version1'},\n"
                msg += "     'ids1': {'shortcut2':'long_version2',...}}"
                raise Exception(msg)

            for k0,v0 in dshort.items():
                for k1,v1 in v0.items():
                    if type(v1) is str:
                        dshort[k0][k1] = {'str':v1}
                    else:
                        assert 'str' in v1.keys() and type(v1['str']) is str

            for k0, v0 in dshort.items():
                dsh[k0].update(dshort[k0])
        self._dshort = dsh
        self._set_fsig()

    def update_shortcuts(self, ids, short, longstr):
        assert ids in self._dids.keys()
        assert type(short) is str
        assert type(longstr) is str
        self._dshort[ids][short] = {'str':longstr}
        self._set_fsig()

    #############
    # preset

    @classmethod
    def _getpreset(cls, obj=None, key=None, return_=False,
                   verb=True, sep='  ', line='-', just='l'):
        if obj is None:
            obj = cls
        if key is None:
            lkeys = list(obj._dpreset.keys())
        else:
            lc = [type(key) is str, type(key) is list and all([type(ss) is str
                                                               for ss in key])]
            assert any(lc), "key must be an vali key of self.dpreset or a list of such !"
            if lc[0]:
                lkeys = [key]
            else:
                lkeys = key

        preset = []
        for key in lkeys:
            lids = sorted(obj._dpreset[key].keys())
            for ii in range(0,len(lids)):
                s0 = key if ii == 0 else ''
                if obj._dpreset[key][lids[ii]] is None:
                    s1 = sorted(obj._dshort[lids[ii]].keys())
                else:
                    s1 = obj._dpreset[key][lids[ii]]
                    assert type(s1) in [str,list]
                    if type(s1) is str:
                        s1 = [s1]
                s1 = ', '.join(s1)
                preset.append((s0,lids[ii],s1))

        if verb:
            col = ['preset', 'ids', 'shortcuts']
            msg = obj._getcharray(preset, col, sep=sep, line=line, just=just)
            print(msg)
        if return_:
            return preset

    def get_preset(self, key=None, return_=False,
                   verb=True, sep='  ', line='-', just='l'):
        """ Display and/or return the builtin shortcuts for imas signal names

        By default (ids=None), only display shortcuts for stored ids
        To display all possible shortcuts, use ids='all'
        To display shortcuts for a specific ids, use ids=<idsname>

        These shortcuts can be customized (with self.set_shortcuts())
        They are useful for use with self.get_data()

        """
        return self._getpreset(obj=self, key=key, return_=return_, verb=verb,
                               sep=sep, line=line, just=just)

    def set_preset(self, dpreset=None):
        """ Set the dictionary of preselections

        If None, resets to the class's default dict
        """
        dpr = copy.deepcopy(self.__class__._dpreset)
        if dpreset is not None:
            c0 = type(dpreset) is dict
            c1 = c0 and all([type(k0) is str and type(v0) is dict
                             for k0,v0 in dpreset.items()])
            c2 = c1 and all([[(k1 in self._lidsnames
                               and (type(v1) in [str,list] or v1 is None))
                              for k1,v1 in v0.items()]
                             for v0 in dpreset.values()])
            c3 = True and c2
            for k0,v0 in dpreset.items():
                for v1 in v0.values():
                    if type(v1) is str:
                        dpreset[k0][k1] = [v1]
                    c3 = c3 and all([ss in self._dshort[k1].keys()
                                     for ss in dpreset[k0][k1]])
            if not c3:
                msg = "Arg dpreset should be a dict of shape:\n"
                msg += "    {'key0': {'ids0': ['shortcut0','shortcut1',...],\n"
                msg += "              'ids1':  'shortcut2'},\n"
                msg += "     'key1': {'ids2':  'shortcut3',\n"
                msg += "              'ids3':  None}}\n\n"
                msg += "  i.e.: each preset (key) is a dict of (ids,value)"
                msg += "        where value is either:\n"
                msg += "            - None: all shortuc of ids are taken\n"
                msg += "            - str : a valid shortut\n"
                msg += "            - list: a list of valid shortcuts"
                raise Exception(msg)

            for k0, v0 in dpreset.keys():
                dpr[k0].update(dpreset[k0])
        self._dpreset = dpr

    def update_preset(self, key, ids, lshort):
        assert ids in self._dshort.keys()
        assert lshort is None or type(lshort) in [str,list]
        if type(lshort) is str:
            lshort = [lshort]
        if lshort is not None:
            assert all([ss in self._dshort[ids].keys() for ss in lshort])
        self._dpreset[key][ids] = lshort




    #############
    # ids getting

    def _checkformat_get_idd(self, idd=None):
        lk = self._didd.keys()
        lc = [idd is None, type(idd) is str and idd in lk,
              hasattr(idd,'__iter__') and all([ii in lk for ii in idd])]
        assert any(lc)
        if lc[0]:
            lidd = lk
        elif lc[1]:
            lidd = [idd]
        else:
            lidd = idd
        return lidd

    def _checkformat_get_ids(self, ids=None):
        """ Return a list of tuple (idd, lids) """
        lk = self._dids.keys()
        lc = [ids is None, type(ids) is str and ids in lk,
              hasattr(ids,'__iter__') and all([ii in lk for ii in ids])]
        assert any(lc)
        if lc[0]:
            lids = lk
        elif lc[1]:
            lids = [ids]
        else:
            lids = ids
        lidd = sorted(set([self._dids[ids]['idd'] for ids in lids]))
        llids = [(idd, sorted([ids for ids in lids
                               if self._dids[ids]['idd'] == idd]))
                for idd in lidd]
        return llids

    def _open(self, idd=None):
        lidd = self._checkformat_get_idd(idd)
        for k in lidd:
            if self._didd[k]['isopen'] == False:
                if not all([ss in self._didd[k]['params'].keys()
                            for ss in ['user','tokamak','version']]):
                    msg = "idd cannot be opened with user, tokamak, version !\n"
                    msg += "    - name : %s"%k
                    raise Exception(msg)
                args = (self._didd[k]['params']['user'],
                        self._didd[k]['params']['tokamak'],
                        self._didd[k]['params']['version'])
                self._didd[k]['idd'].open_env( *args )
                self._didd[k]['isopen'] = True

    def _get(self, idsname=None, occ=None, llids=None, verb=True,
             sep='  ', line='-', just='l'):

        lerr = []
        if llids is None:
            llids = self._checkformat_get_ids(idsname)
        if len(llids) == 0:
            return lerr

        if verb:
            msg0 = ['Getting ids', '[occ]'] + self._lidsk
            lmsg = []

        docc = {}
        for ii in range(0,len(llids)):
            docc[ii] = {jj:{'oc':None, 'indok':None}
                        for jj in range(0,len(llids[ii][1]))}
            for jj in range(0,len(llids[ii][1])):
                ids = llids[ii][1][jj]
                occref = self._dids[ids]['occ']
                if occ is None:
                    oc = occref
                else:
                    oc = np.unique(np.r_[occ].astype(int))
                    oc = np.intersect1(oc, occref)
                docc[ii][jj]['oc'] = oc
                docc[ii][jj]['indoc'] = np.array([(occref==oc[ll]).nonzero()[0][0]
                                                  for ll in range(0,len(oc))])
                if verb:
                    msg = [ids, str(oc)]
                    if jj == 0:
                        msg += [str(self._didd[llids[ii][0]]['params'][kk])
                                for kk in self._lidsk]
                    else:
                        msg += ['"' for _ in self._lidsk]
                    lmsg.append(msg)

        if verb:
            msgar = self._getcharray(lmsg, col=msg0,
                                     sep=sep, line=line, just=just, msg=False)
            print('\n'.join(msgar[:2]))

        nline = 0
        for ii in range(0,len(llids)):
            for jj in range(0,len(llids[ii][1])):
                ids = llids[ii][1][jj]
                oc = docc[ii][jj]['oc']
                indoc = docc[ii][jj]['indoc']

                # if ids not provided
                if self._dids[ids]['ids'] is None:
                    idd = self._didd[self._dids[ids]['idd']]['idd']
                    self._dids[ids]['ids'] = [getattr(idd, ids) for ii in oc]
                    self._dids[ids]['needidd'] = False

                if verb:
                    print(msgar[2+nline])

                try:
                    for ll in range(0,len(oc)):
                        if self._dids[ids]['isget'][indoc[ll]] == False:
                            self._dids[ids]['ids'][indoc[ll]].get( oc[ll] )
                            self._dids[ids]['isget'][indoc[ll]] = True
                    done = 'ok'
                except Exception as err:
                    done = 'error !'
                    lerr.append(err)
                    if verb:
                        print('        => failed !')

                nline += 1

        return lerr


    def _close(self, idd=None):
        lidd = self._checkformat_get_idd(idd)
        for k in lidd:
            self._didd[k]['idd'].close()
            self._didd[k]['isopen'] = False

    def get_list_notget_ids(self):
        lids = [k for k,v in self._dids.items() if np.any(v['isget'] == False)]
        return lids

    def open_get_close(self, ids=None, occ=None, verb=True):
        """ Force data loading

        If at instanciation or when using method add_ids() you specified option
        get = False, then the latest added ids may not have been loaded.

        This method forces a refresh and loads all ids contained in the instance

        The name comes from:
            - open (all the idd)
            - get (all the ids)
            - close (all the idd)
        """
        llids = self._checkformat_get_ids(ids)
        lidd = [lids[0] for lids in llids]
        self._open(idd=lidd)
        lerr = self._get(occ=occ, llids=llids)
        self._close(idd=lidd)
        if verb and len(lerr) > 0:
            for err in lerr:
                warnings.warn(str(err))


    #---------------------
    # Methods for adding / removing idd / ids
    #---------------------

    @classmethod
    def _checkformat_idd(cls, idd=None,
                         shot=None, run=None, refshot=None, refrun=None,
                         user=None, tokamak=None, version=None,
                         isopen=None, ref=None, defidd=None):
        lc = [idd is None, shot is None]
        if not any(lc):
            msg = "You cannot provide both idd and shot !"
            raise Exception(msg)

        if all(lc):
            didd = {}
            return didd
        if defidd is None:
            defidd = cls._defidd

        if lc[0]:
            assert type(shot) in [int,np.int_]
            params = dict(shot=int(shot), run=run, refshot=refshot, refrun=refrun,
                          user=user, tokamak=tokamak, version=version)
            for kk,vv in defidd.items():
                if params[kk] is None:
                    params[kk] = vv
            idd = imas.ids(params['shot'], params['run'],
                           params['refshot'], params['refrun'])
            isopen = False

        elif lc[1]:
            assert hasattr(idd,'close'), "idd does not seem to be data entry !"
            params = {'shot':idd.shot, 'run':idd.run,
                      'refshot':idd.getRefShot(), 'refrun':idd.getRefRun()}
            expIdx = idd.expIdx
            if not (expIdx == -1 or expIdx > 0):
                msg = "Status of the provided idd could not be determined:\n"
                msg += "    - idd.expIdx : %s   (should be -1 or >0)\n"%str(expIdx)
                msg += "    - (shot, run): %s\n"%str((idd.shot, idd.run))
                raise Exception(msg)
            if isopen is not None:
                if isopen != (expIdx > 0):
                    msg = "Provided isopen does not match observed value:\n"
                    msg += "    - isopen: %s\n"%str(isopen)
                    msg += "    - expIdx: %s"%str(expIdx)
                    raise Exception(msg)
            isopen = expIdx > 0

        if 'user' in params.keys():
            name = [params['user'], params['tokamak'], params['version']]
        else:
            name = [str(id(idd))]
        name += ['{:06.0f}'.format(params['shot']),
                 '{:05.0f}'.format(params['run'])]
        name = '_'.join(name)
        didd = {name:{'idd':idd, 'params':params, 'isopen':isopen}}
        return didd


    def set_refidd(self, idd=None):
        if len(self._didd.keys()) == 0:
            assert idd is None
        else:
            assert idd in self._didd.keys()
        self._refidd = idd

    def add_idd(self, idd=None,
                shot=None, run=None, refshot=None, refrun=None,
                user=None, tokamak=None, version=None,
                ref=None, return_name=False):
        assert ref in [None, True]
        # didd
        didd = self._checkformat_idd(idd=idd,
                                     shot=shot, run=run,
                                     refshot=refshot, refrun=refrun,
                                      user=user, tokamak=tokamak,
                                      version=version)
        self._didd.update(didd)
        name = list(didd.keys())[0]

        # ref
        if ref is None:
            ref = self._refidd  is None
        if ref == True and len(didd.keys())>0:
            self.set_refidd(name)
        if return_name:
            return name

    def remove_idd(self, idd=None):
        """Remove an idd and all its dependencies (ids) """
        if idd is not None:
            if not idd in self._didd.keys():
                msg = "Please provide the name (str) of a valid idd\n"
                msg += "Currently available idd are:\n"
                msg += "    - %s"%str(sorted(self._didd.keys()))
                raise Exception(msg)
            lids = [k for k,v in self._dids.items() if v['idd']==idd]
            del self._didd[idd]
            for ids in lids:
                del self._dids[ids]

    def get_idd(self, idd=None):
        if idd is None and len(self._didd.keys()) == 1:
            idd = list(self._didd.keys())[0]
        assert idd in self._didd.keys()
        return self._didd[idd]['idd']

    def _checkformat_ids_synthdiag(self, ids=None):
        lc = [ids is None, isinstance(ids, str), isinstance(ids, list),
              hasattr(ids, 'ids_properties')]
        if not any(lc):
            msg = ("Provided ids not understood!\n"
                   + "\t- provided: {}".format(str(ids)))
            raise Exception(msg)

        lidssynth = [kk for kk, vv in self._didsdiag.items()
                     if 'synth' in vv.keys()]
        if lc[0]:
            ids = sorted(set(self._dids.keys()).intersection(lidssynth))
        elif lc[1]:
            ids = [ids]
        elif lc[3]:
            ids = [ids.__class__.__name__]

        ids = sorted(
            set(ids).intersection(lidssynth).intersection(self._dids.keys()))
        if len(ids) == 0:
            msg = ("The provided ids must be:\n"
                   + "\t- an ids name (str)\n"
                   + "\t- a list of ids names\n"
                   + "\t- an ids instance\n"
                   + "\t- None\n"
                   + "And it must:\n"
                   + "\t- Already be added (cf. self.dids.keys())\n"
                   + "\t- Be a diagnostic ids with tabulated 'synth'")
            # Turn to warning? => see user feedback
            raise Exception(msg)
        return ids

    def get_inputs_for_synthsignal(self, ids=None, verb=True, returnas=False):
        """ Return and / or print a dict of the default inputs for desired ids

        Synthetic signal for a given diagnostic ids is computed from
        signal that comes from other ids (e.g. core_profiles, equilibrium...)
        For some diagnostics, the inputs required are already tabulated in
        self._didsdiag[<ids>]['synth']

        This method simply shows this already tabulated information
        Advanced users may edit this hidden dictionnary to their needs

        """
        assert returnas in [False, True, dict, list]
        ids = self._checkformat_ids_synthdiag(ids)

        # Deal with real case
        if len(ids) == 1:
            out = self._didsdiag[ids[0]]['synth']
            lids = sorted(out.get('dsig', {}).keys())
            if verb:
                dmsg = ("\n\t-" +
                        "\n\t-".join([
                            kk+':\n\t\t'+'\n\t\t'.join(vv)
                            for kk, vv in out.get('dsig', {}).items()]))
                extra = {kk: vv for kk, vv in out.items()
                         if kk not in ['dsynth', 'dsig']}
                msg = ("For computing synthetic signal for ids {}".format(ids)
                       + dmsg + '\n'
                       + "\t- Extra parameters (if any):\n"
                       + "\t\t{}\n".format(extra))
                print(msg)
            if returnas is True:
                returnas = dict
        else:
            out = None
            lids = sorted(set(itt.chain.from_iterable([
                self._didsdiag[idsi]['synth'].get('dsig', {}).keys()
                for idsi in ids])))
            if verb:
                print(lids)
            if returnas is True:
                returnas = list
        if returnas is dict:
            return out
        elif returnas is list:
            return lids

    def _checkformat_ids(self, ids, occ=None, idd=None, isget=None,
                         synthdiag=False):

        # Check value and make dict if necessary
        lc = [type(ids) is str,
              type(ids) is list,
              hasattr(ids, 'ids_properties'),
              ids is None and synthdiag is True]
        if not any(lc):
            msg = "Arg ids must be either:\n"
            msg += "    - str : valid ids name\n"
            msg += "    - a list of such\n"
            msg += "    - an ids itself\n"
            msg += "  Provided: %s\n"%str(ids)
            msg += "  Conditions: %s"%str(lc)
            raise Exception(msg)

        # Synthdiag-specific
        if synthdiag is True:
            ids = self.get_inputs_for_synthsignal(ids=ids, verb=False,
                                                  returnas=list)
            lc[1] = True

        # Prepare dids[name] = {'ids':None/ids, 'needidd':bool}
        dids = {}
        if lc[0] or lc[1]:
            if lc[0]:
                ids = [ids]
            for ids_ in ids:
                if not ids_ in self._lidsnames:
                    msg = "ids %s matched no known imas ids !"%ids_
                    msg += "  => Available ids are:\n"
                    msg += repr(self._lidsnames)
                    raise Exception(msg)
            for k in ids:
                dids[k] = {'ids':None, 'needidd':True, 'idd':idd}
            lids = ids
        elif lc[2]:
            dids[ids.__class__.__name__] = {'ids':ids,
                                            'needidd':False, 'idd':idd}
            lids = [ids.__class__.__name__]
        nids = len(lids)

        # Check / format occ and deduce nocc
        if occ is None:
            occ = 0
        lc = [type(occ) in [int,np.int], hasattr(occ,'__iter__')]
        assert any(lc)
        if lc[0]:
            occ = [np.r_[occ].astype(int) for _ in range(0,nids)]
        else:
            if len(occ) == nids:
                occ = [np.r_[oc].astype(int) for oc in occ]
            else:
                occ = [np.r_[occ].astype(int) for _ in range(0,nids)]
        for ii in range(0,nids):
            nocc = occ[ii].size
            dids[lids[ii]]['occ'] = occ[ii]
            dids[lids[ii]]['nocc'] = nocc
            if dids[lids[ii]]['ids'] is not None:
                dids[lids[ii]]['ids'] = [dids[lids[ii]]['ids']]*nocc

        # Format isget / get
        for ii in range(0,nids):
            nocc = dids[lids[ii]]['nocc']
            if dids[lids[ii]]['ids'] is None:
                isgeti = np.zeros((nocc,), dtype=bool)
            if dids[lids[ii]]['ids'] is not None:
                if isget is None:
                    isgeti = np.r_[False]
                elif type(isget) is bool:
                    isgeti = np.r_[bool(isget)]
                elif hasattr(isget,'__iter__'):
                    if len(isget) == nids:
                        isgeti = np.r_[isget[ii]]
                    else:
                        isgeti = np.r_[isget]

            assert isgeti.size in [1,nocc]
            if isgeti.size < nocc:
                isgeti = np.repeat(isgeti,nocc)
            dids[lids[ii]]['isget'] = isgeti

        return dids

    def add_ids(self, ids=None, occ=None, idd=None, preset=None,
                shot=None, run=None, refshot=None, refrun=None,
                user=None, tokamak=None, version=None,
                ref=None, isget=None, get=None):
        """ Add an ids (or a list of ids)

        Optionally specify also a specific idd to which the ids will be linked
        The ids can be provided as such, or by name (str)

        """

        if get is None:
            get = False if preset is None else True

        # preset
        if preset is not None:
            if preset not in self._dpreset.keys():
                msg = "Available preset values are:\n"
                msg += "    - %s\n"%str(sorted(self._dpreset.keys()))
                msg += "    - Provided: %s"%str(preset)
                raise Exception(msg)
            ids = sorted(self._dpreset[preset].keys())
        self._preset = preset

        # Add idd if relevant
        if hasattr(idd, 'close') or shot is not None:
            name = self.add_idd(idd=idd,
                                shot=shot, run=run,
                                refshot=refshot, refrun=refrun,
                                user=user, tokamak=tokamak,
                                version=version, ref=ref, return_name=True)
            idd = name

        if idd is None and ids is not None:
            if self._refidd is None:
                msg = "No idd was provided (and ref idd is not clear) !\n"
                msg += "Please provide an idd either directly or via \n"
                msg += "args (shot, user, tokamak...)!\n"
                msg += "    - %s"%str([(k,v.get('ref',None))
                                       for k,v in self._didd.items()])
                raise Exception(msg)
            idd = self._refidd
        elif idd is not None:
            assert idd in self._didd.keys()

        # Add ids
        if ids is not None:
            dids = self._checkformat_ids(ids, occ=occ, idd=idd, isget=isget)

            self._dids.update(dids)
            if get:
                self.open_get_close()

    def add_ids_base(self, occ=None, idd=None,
                     shot=None, run=None, refshot=None, refrun=None,
                     user=None, tokamak=None, version=None,
                     ref=None, isget=None, get=None):
        """ Add th list of ids stored in self._IDS_BASE

        Typically used to add a list of common ids without having to re-type
        them every time
        """
        self.add_ids(ids=self._IDS_BASE, occ=occ, idd=idd,
                     shot=shot, run=run, refshot=refshot, refrun=refrun,
                     user=user, tokamak=tokamak, version=version,
                     ref=ref, isget=isget, get=get)

    def add_ids_synthdiag(self, ids=None, occ=None, idd=None,
                          shot=None, run=None, refshot=None, refrun=None,
                          user=None, tokamak=None, version=None,
                          ref=None, isget=None, get=None):
        """ Add pre-tabulated input ids necessary for calculating synth. signal

        The necessary input ids are given by self.get_inputs_for_synthsignal()

        """
        if get is None:
            get = True
        ids = self.get_inputs_for_synthsignal(ids=ids, verb=False,
                                              returnas=list)
        self.add_ids(ids=ids, occ=occ, idd=idd, preset=None,
                     shot=shot, run=run, refshot=refshot, refrun=refrun,
                     user=user, tokamak=tokamak, version=version,
                     ref=ref, isget=isget, get=get)

    def remove_ids(self, ids=None, occ=None):
        """ Remove an ids (optionally remove only an occurence)

        If all the ids linked to an idd are removed, said idd is removed too

        """
        if ids is not None:
            if not ids in self._dids.keys():
                msg = "Please provide the name (str) of a valid ids\n"
                msg += "Currently available ids are:\n"
                msg += "    - %s"%str(sorted(self._dids.keys()))
                raise Exception(msg)
            occref = self._dids[ids]['occ']
            if occ is None:
                occ = occref
            else:
                occ = np.unique(np.r_[occ].astype(int))
                occ = np.intersect1d(occ, occref, assume_unique=True)
            idd = self._dids[ids]['idd']
            lids = [k for k,v in self._dids.items() if v['idd']==idd]
            if lids == [ids]:
                del self._didd[idd]
            if np.all(occ == occref):
                del self._dids[ids]
            else:
                isgetref = self._dids[ids]['isget']
                indok = np.array([ii for ii in range(0,occref.size)
                                  if occref[ii] not in occ])
                self._dids[ids]['ids'] = [self._dids[ids]['ids'][ii]
                                              for ii in indok]
                self._dids[ids]['occ'] = occref[indok]
                self._dids[ids]['isget'] = isgetref[indok]
                self._dids[ids]['nocc'] = self._dids[ids]['occ'].size

    def get_ids(self, ids=None, occ=None):
        if ids is None and len(self._dids.keys()) == 1:
            ids = list(self._dids.keys())[0]
        assert ids in self._dids.keys()
        if occ is None:
            occ = self._dids[ids]['occ'][0]
        else:
            assert occ in self._dids[ids]['occ']
        indoc = np.where(self._dids[ids]['occ'] == occ)[0][0]
        return self._dids[ids]['ids'][indoc]


    #---------------------
    # Methods for showing content
    #---------------------

    def get_summary(self, sep='  ', line='-', just='l',
                    table_sep=None, verb=True, return_=False):
        """ Summary description of the object content as a np.array of str """
        if table_sep is None:
            table_sep = '\n\n'

        # -----------------------
        # idd
        a0 = []
        if len(self._didd) > 0:
            c0 = ['idd', 'user', 'tokamak', 'version',
                  'shot', 'run', 'refshot', 'refrun', 'isopen', '']
            for k0,v0 in self._didd.items():
                lu = ([k0] + [str(v0['params'][k]) for k in c0[1:-2]]
                      + [str(v0['isopen'])])
                ref = '(ref)' if k0==self._refidd else ''
                lu += [ref]
                a0.append(lu)
            a0 = np.array(a0, dtype='U')

        # -----------------------
        # ids
        if len(self._dids) > 0:
            c1 = ['ids', 'idd', 'occ', 'isget']
            llids = self._checkformat_get_ids()
            a1 = []
            for (k0, lk1) in llids:
                for ii in range(0,len(lk1)):
                    idd = k0 if ii == 0 else '"'
                    a1.append([lk1[ii], idd,
                               str(self._dids[lk1[ii]]['occ']),
                               str(self._dids[lk1[ii]]['isget'])])
            a1 = np.array(a1, dtype='U')
        else:
            a1 = []


        # Out
        if verb or return_ in [True,'msg']:
            if len(self._didd) > 0:
                msg0 = self._getcharray(a0, c0,
                                        sep=sep, line=line, just=just)
            else:
                msg0 = ''
            if len(self._dids) > 0:
                msg1 = self._getcharray(a1, c1,
                                        sep=sep, line=line, just=just)
            else:
                msg1 = ''
            if verb:
                msg = table_sep.join([msg0,msg1])
                print(msg)
        if return_ != False:
            if return_ == True:
                out = (a0, a1, msg0, msg1)
            elif return_ == 'array':
                out = (a0, a1)
            elif return_ == 'msg':
                out = table_sep.join([msg0,msg1])
            else:
                lok = [False, True, 'msg', 'array']
                raise Exception("Valid return_ values are: %s"%str(lok))
            return out

    def __repr__(self):
        if hasattr(self, 'get_summary'):
            return self.get_summary(return_='msg', verb=False)
        else:
            return object.__repr__(self)

    #---------------------
    # Methods for returning data
    #---------------------

    def _checkformat_getdata_ids(self, ids):
        msg = ("Arg ids must be either:\n"
               + "\t- None: if self.dids only has one key\n"
               + "\t- str: a valid key of self.dids\n\n"
               + "  Provided : {}\n".format(ids)
               + "  Available: {}\n".format(str(list(self._dids.keys())))
               + "  => Consider using self.add_ids({})".format(str(ids)))

        lc = [ids is None, type(ids) is str]
        if not any(lc):
            raise Exception(msg)

        if lc[0]:
            if len(self._dids.keys()) != 1:
                raise Exception(msg)
            ids = list(self._dids.keys())[0]
        elif lc[1]:
            if ids not in self._dids.keys():
                raise Exception(msg)
        return ids

    def _checkformat_getdata_sig(self, sig, ids):
        msg = "Arg sig must be a str or a list of str !\n"
        msg += "  More specifically, a list of valid ids nodes paths"
        lks = list(self._dshort[ids].keys())
        lkc = list(self._dcomp[ids].keys())
        lk = set(lks).union(lkc)
        if ids in self._dall_except.keys():
            lk = lk.difference(self._dall_except[ids])
        lc = [sig is None, type(sig) is str, type(sig) is list]
        if not any(lc):
            raise Exception(msg)
        if lc[0]:
            sig = list(lk)
        elif lc[1]:
            sig = [sig]
        elif lc[2]:
            if any([type(ss) is not str for ss in sig]):
                raise Exception(msg)
        nsig = len(sig)

        # Check each sig is either a key / value[str] to self._dshort
        comp = np.zeros((nsig,),dtype=bool)
        for ii in range(0,nsig):
            lc0 = [sig[ii] in lks,
                   [sig[ii] == self._dshort[ids][kk]['str'] for kk in lks]]
            c1 = sig[ii] in lkc
            if not (lc0[0] or any(lc0[1]) or c1):
                msg = "Each provided sig must be either:\n"
                msg += "    - a valid shortcut (cf. self.shortcuts()\n"
                msg += "    - a valid long version (cf. self.shortcuts)\n"
                msg += "\n  Provided sig: %s for ids %s"%(str(sig), ids)
                raise Exception(msg)
            if c1:
                comp[ii] = True
            else:
                if not lc0[0]:
                    sig[ii] = lks[lc0[1].index(True)]
        return sig, comp

    def _checkformat_getdata_occ(self, occ, ids):
        msg = "Arg occ must be a either:\n"
        msg += "    - None: all occurences are used\n"
        msg += "    - int: occurence to use (in self.dids[ids]['occ'])\n"
        msg += "    - array of int: occurences to use (in self.dids[ids]['occ'])"
        lc = [occ is None, type(occ) is int, hasattr(occ,'__iter__')]
        if not any(lc):
            raise Exception(msg)
        if lc[0]:
            occ = self._dids[ids]['occ']
        else:
            occ = np.r_[occ].astype(int).ravel()
            if any([oc not in self._dids[ids]['occ'] for oc in occ]):
                raise Exception(msg)
        return occ

    def _checkformat_getdata_indch(self, indch, nch):
        msg = "Arg indch must be a either:\n"
        msg += "    - None: all channels used\n"
        msg += "    - int: channel to use (index)\n"
        msg += "    - array of int: channels to use (indices)\n"
        msg += "    - array of bool: channels to use (indices)\n"
        lc = [indch is None,
              type(indch) is int,
              hasattr(indch,'__iter__') and type(indch) is not str]
        if not any(lc):
            raise Exception(msg)
        if lc[0]:
            indch = np.arange(0,nch)
        elif lc[1] or lc[2]:
            indch = np.r_[indch].ravel()
            lc = [indch.dtype == np.int, indch.dtype == np.bool]
            if not any(lc):
                raise Exception(msg)
            if lc[1]:
                indch = np.nonzero(indch)[0]
            assert np.all((indch>=0) & (indch<nch))
        return indch

    def _checkformat_getdata_indt(self, indt):
        msg = "Arg indt must be a either:\n"
        msg += "    - None: all channels used\n"
        msg += "    - int: times to use (index)\n"
        msg += "    - array of int: times to use (indices)"
        lc = [type(indt) is None, type(indt) is int, hasattr(indt,'__iter__')]
        if not any(lc):
            raise Exception(msg)
        if lc[1] or lc[2]:
            indt = np.r_[indt].rave()
            lc = [indt.dtype == np.int]
            if not any(lc):
                raise Exception(msg)
            assert np.all(indt>=0)
        return indt

    @staticmethod
    def _prepare_sig(sig):
        if '[' in sig:
            # Get nb and ind
            ind0 = 0
            while '[' in sig[ind0:]:
                ind1 = ind0 + sig[ind0:].index('[')
                ind2 = ind0 + sig[ind0:].index(']')
                sig = sig.replace(sig[ind1+1:ind2], sig[ind1+1:ind2].replace('.','/'))
                ind0 = ind2+1
        return sig

    @staticmethod
    def _get_condfromstr(sid, sig=None):
        lid0, id1 = sid.split('=')
        lid0 = lid0.split('.')

        if '.' in id1 and id1.replace('.','').isdecimal():
            id1 = float(id1)
        elif id1.isdecimal():
            id1 = int(id1)
        elif '.' in id1:
            msg = "Not clear how to interpret the following condition:\n"
            msg += "    - sig: %s\n"%sig
            msg += "    - condition: %s"%sid
            raise Exception(msg)
        return lid0, id1

    @classmethod
    def _get_fsig(cls, sig):

        # break sig in list of elementary nodes
        sig = cls._prepare_sig(sig)
        ls0 = sig.split('.')
        sig = sig.replace('/','.')
        ls0 = [ss.replace('/','.') for ss in ls0]
        ns = len(ls0)

        # For each node, identify type (i.e. [])
        lc = [all([si in ss for si in ['[',']']]) for ss in ls0]
        dcond, seq, nseq, jj = {}, [], 0, 0
        for ii in range(0,ns):
            nseq = len(seq)
            if lc[ii]:
                # there is []
                if nseq > 0:
                    dcond[jj] = {'type':0, 'lstr': seq}
                    seq = []
                    jj += 1

                # Isolate [strin]
                ss = ls0[ii]
                strin = ss[ss.index('[')+1:-1]

                # typ 0 => no dependency
                # typ 1 => dependency ([],[time],[chan],[int])
                # typ 2 => selection ([...=...])
                cond, ind, typ = None, None, 1
                if '=' in strin:
                    typ = 2
                    cond = cls._get_condfromstr(strin, sig=sig)
                elif strin in ['time','chan']:
                    ind = strin
                elif strin.isnumeric():
                    ind = [int(strin)]
                dcond[jj] = {'str':ss[:ss.index('[')], 'type':typ,
                             'ind':ind, 'cond':cond}
                jj += 1
            else:
                seq.append(ls0[ii])
                if ii == ns-1:
                    dcond[jj] = {'type':0, 'lstr': seq}

        c0 = [v['type'] == 1 and (v['ind'] is None or len(v['ind'])>1)
             for v in dcond.values()]
        if np.sum(c0) > 1:
            msg = "Cannot handle mutiple iterative levels yet !\n"
            msg += "    - sig: %s"%sig
            raise Exception(msg)

        # Create function for getting signal
        def fsig(obj, indt=None, indch=None, stack=True, dcond=dcond):
            sig = [obj]
            nsig = 1
            for ii in dcond.keys():

                # Standard case (no [])
                if dcond[ii]['type'] == 0:
                    sig = [ftools.reduce(getattr, [sig[jj]]+dcond[ii]['lstr'])
                            for jj in range(0,nsig)]

                # dependency
                elif dcond[ii]['type'] == 1:
                    for jj in range(0,nsig):
                        sig[jj] = getattr(sig[jj],dcond[ii]['str'])
                        nb = len(sig[jj])
                        if dcond[ii]['ind'] == 'time':
                            ind = indt
                        elif dcond[ii]['ind'] == 'chan':
                            ind = indch
                        else:
                            ind = dcond[ii]['ind']

                        if ind is None:
                            ind = range(0,nb)
                        if nsig > 1:
                            assert type(ind) is not str and len(ind) == 1

                        if len(ind) == 1:
                            sig[jj] = sig[jj][ind[0]]
                        else:
                            assert nsig == 1
                            sig = [sig[0][ll] for ll in ind]
                            nsig = len(sig)

                # one index to be found
                else:
                    for jj in range(0,nsig):
                        sig[jj] = getattr(sig[jj], dcond[ii]['str'])
                        nb = len(sig[jj])
                        typ = type(ftools.reduce(getattr,
                                                 [sig[jj][0]]+dcond[ii]['cond'][0]))
                        if typ == str:
                            ind = [ll for ll in range(0,nb)
                                   if (ftools.reduce(getattr,
                                                     [sig[jj][ll]]+dcond[ii]['cond'][0]).strip()
                                       == dcond[ii]['cond'][1].strip())]
                        else:
                            ind = [ll for ll in range(0,nb)
                                   if (ftools.reduce(getattr,
                                                     [sig[jj][ll]]+dcond[ii]['cond'][0])
                                       == dcond[ii]['cond'][1])]
                        if len(ind) != 1:
                            msg = "No / several matching signals for:\n"
                            msg += "    - %s[]%s = %s\n"%(dcond[ii]['str'],
                                                          dcond[ii]['cond'][0],
                                                          dcond[ii]['cond'][1])
                            msg += "    - nb.of matches: %s"%str(len(ind))
                            raise Exception(msg)
                        sig[jj] = sig[jj][ind[0]]

            # Conditions for stacking / sqeezing sig
            lc = [(stack and nsig>1 and isinstance(sig[0],np.ndarray)
                   and all([ss.shape == sig[0].shape for ss in sig[1:]])),
                  stack and nsig>1 and type(sig[0]) in [int, float, np.int,
                                                        np.float, str],
                  (stack and nsig == 1 and type(sig) in
                   [np.ndarray,list,tuple])]

            if lc[0]:
                sig = np.atleast_1d(np.squeeze(np.stack(sig)))
            elif lc[1] or lc[2]:
                sig = np.atleast_1d(np.squeeze(sig))
            return sig

        return fsig

    def _set_fsig(self):
        for ids in self._dshort.keys():
            for k,v in self._dshort[ids].items():
                self._dshort[ids][k]['fsig'] = self._get_fsig(v['str'])

    def __get_data(self, ids, sig, occ, comp=False, indt=None, indch=None,
                   stack=True, isclose=True, flatocc=True, nan=True,
                   pos=None, warn=True):

        # get list of results for occ
        occref = self._dids[ids]['occ']
        indoc = np.array([np.nonzero(occref==oc)[0][0] for oc in occ])
        nocc = len(indoc)
        if comp:
            lstr = self._dcomp[ids][sig]['lstr']
            kargs = self._dcomp[ids][sig].get('kargs', {})
            ddata, _ = self._get_data(ids=ids, sig=lstr,
                                      occ=occ, indch=indch, indt=indt,
                                      stack=stack, flatocc=False, nan=nan,
                                      pos=pos, warn=warn)
            out = [self._dcomp[ids][sig]['func']( *[ddata[kk][nn]
                                                   for kk in lstr], **kargs )
                   for nn in range(0,nocc)]
            if pos is None:
                pos = self._dcomp[ids][sig].get('pos', False)

        else:
            out = [self._dshort[ids][sig]['fsig']( self._dids[ids]['ids'][ii],
                                                  indt=indt, indch=indch,
                                                  stack=stack )
                   for ii in indoc]
            if pos is None:
                pos = self._dshort[ids][sig].get('pos', False)

        if isclose:
            for ii in range(0,len(out)):
                if type(out[ii]) is np.ndarray and out[ii].ndim == 2:
                    if np.allclose(out[ii], out[ii][0:1,:]):
                        out[ii] = out[ii][0,:]
                    elif np.allclose(out[ii], out[ii][:,0:1]):
                        out[ii] = out[ii][:,0]
        if nan:
            for ii in range(0,len(out)):
                if type(out[ii]) is np.ndarray and out[ii].dtype == np.float:
                    out[ii][np.abs(out[ii]) > 1.e30] = np.nan

        if pos == True:
            for ii in range(0,len(out)):
                if type(out[ii]) is np.ndarray:
                    out[ii][out[ii] < 0] = np.nan


        if nocc == 1 and flatocc:
            out = out[0]
        return out

    def _get_data(self, ids=None, sig=None, occ=None,
                  indch=None, indt=None, stack=True,
                  isclose=None, flatocc=True, nan=True, pos=None, warn=True):

        # ------------------
        # Check format input

        # ids = valid self.dids.keys()
        ids = self._checkformat_getdata_ids(ids)

        # sig = list of str
        sig, comp = self._checkformat_getdata_sig(sig, ids)

        # occ = np.ndarray of valid int
        occ = self._checkformat_getdata_occ(occ, ids)
        indoc = np.where(self._dids[ids]['occ'] == occ)[0]

        # Check all occ have isget = True
        indok = self._dids[ids]['isget'][indoc]
        if not np.all(indok):
            msg = "All desired occurences shall have been gotten !\n"
            msg += "    - desired occ:   %s\n"%str(occ)
            msg += "    - available occ:   %s\n"%str(self._dids[ids]['occ'])
            msg += "    - isget: %s\n"%str(self._dids[ids]['isget'])
            msg += "  => Try running self.open_get_close()"
            raise Exception(msg)

        # check indch if ids has channels
        if hasattr(self._dids[ids]['ids'][indoc[0]], 'channel'):
            nch = len(getattr(self._dids[ids]['ids'][indoc[0]], 'channel'))
            indch = self._checkformat_getdata_indch(indch, nch)

        # ------------------
        # get data

        dout, dfail = {}, {}
        for ii in range(0, len(sig)):
            if isclose is None:
                isclose_ = sig[ii] == 't'
            else:
                isclose_ = isclose
            try:
                dout[sig[ii]] = self.__get_data(ids, sig[ii], occ,
                                                comp=comp[ii],
                                                indt=indt, indch=indch,
                                                stack=stack, isclose=isclose_,
                                                flatocc=flatocc, nan=nan,
                                                pos=pos, warn=warn)
            except Exception as err:
                dfail[sig[ii]] = str(err)
                if warn:
                    msg = '\n' + str(err) + '\n'
                    msg += '\tsignal {0}.{1} not loaded!'.format(ids, sig[ii])
                    warnings.warn(msg)
        return dout, dfail

    def get_data(self, ids=None, sig=None, occ=None,
                 indch=None, indt=None, stack=True,
                 isclose=None, flatocc=True, nan=True, pos=None, warn=True):
        """ Return a dict of the desired signals extracted from specified ids

        If the ids has a field 'channel', indch is used to specify from which
        channel data shall be loaded (all by default)

        Parameters
        ----------
        ids:        None / str
            ids from which the data should be loaded
            ids should be available (check self.get_summary())
            ids should be loaded if not available, using:
                - self.add_ids() to add the ids
                - self.open_get_close() to force loading if necessary
        sig:        None / str / list
            shortcuts of signals to be loaded from the ids
            Check available shortcuts using self.get_shortcuts(ids)
            You can add custom shortcuts if needed (cf. self.add_shortcuts())
            sig can be a single str (shortcut) or a list of such
        occ:        None / int
            occurence from which to load the data
        indch:      None / list / np.ndarray
            If the data has channels, this lists / array of int indices can be
            used to specify which channels to load from (all if None)
        indt:       None / list / np.ndarray
            If data is time-dependent, the list / array of int indices can be
            used to specify which time steps to load
        stack:      bool
            Flag indicating whether common data (e.g.: data from different
            channels) should be agregated / stacked into a single array
        isclose:    None / bool
            Flag indicating whether the agregated data is a collection of
            identical vectors, if which case it will be checked (np.isclose())
            and only a single vector will be kept
        flatocc:    bool
            By default, the data is returned as a list for each occurence
            If there is only one occ and flatocc = True, only the first element
            of the list is returned
        nan:        bool
            Flag indicating whether to check for abs(data) > 1.30
            All data is this case will be set to nan
            Due to the fact IMAS default value is 1.e49
        pos:        None / bool
            Flag indicating whether the data should be positive (negative
            values will be set to nan)
        warn:       bool
            Flag indicating whether to print warning messages for data could
            not be retrieved

        Return
        ------
        dout:   dict
            Dictionnary containing the loaded data

        """
        return self._get_data(ids=ids, sig=sig, occ=occ, indch=indch,
                              indt=indt, stack=stack, isclose=isclose,
                              flatocc=flatocc, nan=nan, pos=pos, warn=warn)[0]

    def get_data_all(self, dsig=None, stack=True,
                     isclose=None, flatocc=True, nan=True, pos=None):

        # dsig
        if dsig is None:
            if self._preset is not None:
                dsig = self._dpreset[self._preset]
            else:
                dsig = dict.fromkeys(self._dids.keys())
        else:
            assert type(dsig) is dict
        dout = dict.fromkeys(set(self._dids.keys()).intersection(dsig.keys()))

        lc = [ss for ss in dsig.keys() if ss not in dout.keys()]
        if len(lc) != 0:
            msg = "The following ids are asked but not available:\n"
            msg += "    - %s"%str(lc)
            raise Exception(msg)
        assert all([type(v) in [str,list] or v is None for v in dsig.values()])

        # Get data
        dfail = dict.fromkeys(dout.keys())
        anyerror = False
        for ids in dout.keys():
            try:
                dout[ids], dfail[ids] = self._get_data(ids, sig=dsig[ids],
                                                       stack=stack,
                                                       isclose=isclose,
                                                       flatocc=flatocc,
                                                       nan=nan,
                                                       pos=pos, warn=False)
                if len(dfail[ids]) > 0:
                    anyerror = True
            except Exception as err:
                del dout[ids]
                dfail[ids] = dict.fromkeys(dsig[ids].keys(), 'ids error')
                anyerror = True
        if anyerror:
            msg = "The following data could not be retrieved:"
            for ids, v0 in dfail.items():
                if len(v0) == 0:
                    continue
                msg += "\n\t- {}:".format(ids)
                for k1, v1 in v0.items():
                    msg += "\n\t\t{0}  : {1}".format(k1, v1.replace('\n', ' '))
            warnings.warn(msg)
        return dout

    def get_events(self, occ=None, verb=True, returnas=False):
        """ Return chronoligical events stored in pulse_schedule

        If verb = True              => print (default)
                  False             => don't print
        If returnas = list          => return as list of tuples (name, time)
                      np.ndarray    => return as np.ndarray
                      False         => don't return (default)
        """

        # Check / format inputs
        if verb is None:
            verb = True
        if returnas is None:
            returnas = False
        assert isinstance(verb, bool)
        assert returnas in [False, list, tuple]

        events = self.get_data('pulse_schedule',
                               sig='events', occ=occ)['events']
        name, time = zip(*events)
        ind = np.argsort(time)
        if verb:
            name, time = zip(*events[ind])
            msg = np.array([name, time], dtype='U').T
            msg = np.char.ljust(msg, np.nanmax(np.char.str_len(msg)))
            print(msg)
        if returnas is list:
            return events[ind].tolist()
        elif returnas is tuple:
            name, time = zip(*events[ind])
            return name, time



    #---------------------
    # Methods for exporting to tofu objects
    #---------------------

    @staticmethod
    def _check_shotExp_consistency(didd, lidd, tofustr='shot', imasstr='shot',
                                   err=True, fallback=0):
        crit = None
        for idd in lidd:
            v0 = didd[idd]
            if imasstr in v0['params']:
                if crit is None:
                    crit = v0['params'][imasstr]
                elif crit != v0['params'][imasstr]:
                    ss = '{} : {}'.format(idd, str(v0['params'][imasstr]))
                    msg = ("All idd refer to different {}!\n".format(imasstr)
                           + "\t- {}".format(ss))
                    if err:
                        raise Exception(msg)
                    else:
                        warnings.warn(msg)
        if crit is None:
            crit  = fallback
        return crit

    def _get_lidsidd_shotExp(self, lidsok,
                             errshot=True, errExp=True, upper=True):
        lids = set(lidsok).intersection(self._dids.keys())
        lidd = set([self._dids[ids]['idd'] for ids in lids])

        # shot (non-identical => error)
        shot = self._check_shotExp_consistency(self._didd, lidd,
                                               tofustr='shot', imasstr='shot',
                                               err=errshot, fallback=0)

        # Exp (non-identical => error)
        Exp = self._check_shotExp_consistency(self._didd, lidd,
                                              tofustr='Exp', imasstr='tokamak',
                                              err=errExp, fallback='Dummy')
        if upper:
            Exp = Exp.upper()
        return lids, lidd, shot, Exp


    @staticmethod
    def _checkformat_tlim(t, tlim=None):
        # Extract time indices and vector
        indt = np.ones((t.size,), dtype=bool)
        if tlim is not None:
            indt[(t<tlim[0]) | (t>tlim[1])] = False
        t = t[indt]
        indt = np.nonzero(indt)[0]
        nt = t.size
        return {'tlim':tlim, 'nt':nt, 't':t, 'indt':indt}

    def _get_t0(self, t0=None):
        if t0 is None:
            t0 = False
        elif t0 != False:
            if type(t0) in [int,float,np.int,np.float]:
                t0 = float(t0)
            elif type(t0) is str:
                t0 = t0.strip()
                c0 = (len(t0.split('.')) <= 2
                      and all([ss.isdecimal() for ss in t0.split('.')]))
                if 'pulse_schedule' in self._dids.keys():
                    events = self.get_data(ids='pulse_schedule',
                                           sig='events')['events']
                    if t0 in events['name']:
                        t0 = events['t'][np.nonzero(events['name'] == t0)[0][0]]
                    elif c0:
                        t0 = float(t0)
                    else:
                        msg = "Desired event name (%s) not available!\n"
                        msg += "    - available events:\n"
                        msg += str(events['name'])
                        raise Exception(msg)
                elif c0:
                    t0 = float(t0)
                else:
                    t0 = False
            else:
                t0 = False
            if t0 == False:
                msg = "t0 set to False because could not be interpreted !"
                warnings.warn(msg)
        return t0

    def to_Config(self, Name=None, occ=None,
                  description_2d=None, mobile=None, plot=True):
        """ Export the content of wall ids as a tofu Config object

        Choose the occurence (occ), and index (description_2d, cf. dd_doc) to
        be exported.
        Specify whether to pick from limiter or mobile
        If not specified, will be decided automatically from the content
        Optionally plot the result

        This requires that the wall ids was previously loaded.
        If not run:
            self.add_ids('wall')
        """
        lidsok = ['wall']

        # ---------------------------
        # Preliminary checks on data source consistency
        lids, lidd, shot, Exp = self._get_lidsidd_shotExp(lidsok,
                                                          errshot=False,
                                                          errExp=False,
                                                          upper=True)
        # ----------------
        #   Trivial case
        if 'wall' not in lids:
            if plot:
                msg = "ids 'wall' has not been loaded => Config not available!"
                raise Exception(msg)
            return None

        # ----------------
        #   Relevant case

        # Get relevant occ and description_2d
        ids = 'wall'
        # occ = np.ndarray of valid int
        occ = self._checkformat_getdata_occ(occ, ids)
        assert occ.size == 1, "Please choose one occ only !"
        occ = occ[0]
        indoc = np.nonzero(self._dids[ids]['occ'] == occ)[0][0]

        if description_2d is None:
            if len(self._dids[ids]['ids'][indoc].description_2d) >= 2:
                description_2d = 1
            else:
                description_2d = 0

        wall = self._dids[ids]['ids'][indoc].description_2d[description_2d]
        kwargs = dict(Exp=Exp, Type='Tor')

        import tofu.geom as mod

        # Get vessel
        nlim = len(wall.limiter.unit)
        nmob = len(wall.mobile.unit)
        # onelimonly = False

        # ----------------------------------
        # Relevant only if vessel is filled
        # try:
        #    if len(wall.vessel.unit) != 1:
        #        msg = "There is no / several vessel.unit!"
        #        raise Exception(msg)
        #    if len(wall.vessel.unit[0].element) != 1:
        #        msg = "There is no / several vessel.unit[0].element!"
        #        raise Exception(msg)
        #    if len(wall.vessel.unit[0].element[0].outline.r) < 3:
        #        msg = "wall.vessel polygon has less than 3 points!"
        #        raise Exception(msg)
        #    name = wall.vessel.unit[0].element[0].name
        #    poly = np.array([wall.vessel.unit[0].element[0].outline.r,
        #                     wall.vessel.unit[0].element[0].outline.z])
        # except Exception as err:
        #    # If vessel not in vessel, sometimes stored a a single limiter
        #    if nlim == 1:
        #        name = wall.limiter.unit[0].name
        #        poly = np.array([wall.limiter.unit[0].outline.r,
        #                         wall.limiter.unit[0].outline.z])
        #        onelimonly = True
        #    else:
        #        msg = ("There does not seem to be any vessel, "
        #               + "not in wall.vessel nor in wall.limiter!")
        #        raise Exception(msg)
        # cls = None
        # if name == '':
        #     name = 'ImasVessel'
        # if '_' in name:
        #     ln = name.split('_')
        #     if len(ln) == 2:
        #         cls, name = ln
        #     else:
        #         name = name.replace('_', '')
        # if cls is None:
        #     cls = 'Ves'
        # assert cls in ['Ves', 'PlasmaDomain']
        # ves = getattr(mod, cls)(Poly=poly, Name=name, **kwargs)

        # Determine if mobile or not
        lS = []
        # if onelimonly is False:
        if mobile is None:
            if nlim == 0 and nmob > 0:
                mobile = True
            elif nmob == 0 and nlim > 0:
                mobile = False
            elif nmob > nlim:
                msgw = 'wall.description_2[{}]'.format(description_2d)
                msg = ("\nids wall has less limiter than mobile units\n"
                       + "\t- len({}.limiter.unit) = {}\n".format(msgw, nlim)
                       + "\t- len({}.mobile.unit) = {}\n".format(msgw, nmob)
                       + "  => Choosing mobile by default")
                warnings.warn(msg)
                mobile = True
            elif nmob <= nlim:
                msgw = 'wall.description_2[{}]'.format(description_2d)
                msg = ("\nids wall has more limiter than mobile units\n"
                       + "\t- len({}.limiter.unit) = {}\n".format(msgw, nlim)
                       + "\t- len({}.mobile.unit) = {}\n".format(msgw, nmob)
                       + "  => Choosing limiter by default")
                warnings.warn(msg)
                mobile = False
        assert isinstance(mobile, bool)

        # Get PFC
        if mobile is True:
            units = wall.mobile.unit
        else:
            units = wall.limiter.unit
        nunits = len(units)

        if nunits == 0:
            msg = ("There is no unit stored !\n"
                   + "The required 2d description is empty:\n")
            ms = "len(idd.{}[occ={}].description_2d".format(ids, occ)
            msg += "{}[{}].limiter.unit) = 0".format(ms,
                                                     description_2d)
            raise Exception(msg)

        lS = [None for _ in units]
        for ii in range(0, nunits):
            try:
                if mobile is True:
                    outline = units[ii].outline[0]
                else:
                    outline = units[ii].outline
                poly = np.array([outline.r, outline.z])

                if units[ii].phi_extensions.size > 0:
                    pos, extent = units[ii].phi_extensions.T
                else:
                    pos, extent = None, None
                name = units[ii].name
                cls, mobi = None, None
                if name == '':
                    name = 'unit{:02.0f}'.format(ii)
                if '_' in name:
                    ln = name.split('_')
                    if len(ln) == 2:
                        cls, name = ln
                    elif len(ln) == 3:
                        cls, name, mobi = ln
                    else:
                        name = name.replace('_', '')
                if cls is None:
                    if ii == nunits - 1:
                        cls = 'Ves'
                    else:
                        cls = 'PFC'
                # mobi = mobi == 'mobile'
                lS[ii] = getattr(mod, cls)(Poly=poly, pos=pos,
                                           extent=extent,
                                           Name=name,
                                           **kwargs)
            except Exception as err:
                msg = ("PFC unit[{}] named {} ".format(ii, name)
                       + "could not be loaded!\n"
                       + str(err))
                raise Exception(msg)

        if Name is None:
            Name = wall.type.name
            if Name == '':
                Name = 'imas wall'

        config = mod.Config(lStruct=lS, Name=Name, **kwargs)

        # Output
        if plot:
            lax = config.plot()
        return config


    def _checkformat_Plasma2D_dsig(self, dsig=None):
        lidsok = set(self._lidsplasma).intersection(self._dids.keys())

        lscom = ['t']
        lsmesh = ['2dmeshNodes', '2dmeshFaces',
                  '2dmeshR', '2dmeshZ']

        lc = [dsig is None,
              type(dsig) is str,
              type(dsig) is list,
              type(dsig) is dict]
        assert any(lc)

        # Convert to dict
        if lc[0]:
            dsig = {}
            dsig = {ids: sorted(set(list(self._dshort[ids].keys())
                                    + list(self._dcomp[ids].keys())))
                    for ids in lidsok}
        elif lc[1] or lc[2]:
            if lc[1]:
                dsig = [dsig]
            dsig = {ids: dsig for ids in lidsok}

        # Check content
        dout = {}
        for k0, v0 in dsig.items():
            lkeysok = sorted(set(list(self._dshort[k0].keys())
                                 + list(self._dcomp[k0].keys())))
            if k0 not in lidsok:
                msg = "Only the following ids are relevant to Plasma2D:\n"
                msg += "    - %s"%str(lidsok)
                msg += "  => ids %s from dsig is ignored"%str(k0)
                warnings.warn(msg)
                continue
            lc = [v0 is None, type(v0) is str, type(v0) is list]
            if not any(lc):
                msg = "Each value in dsig must be either:\n"
                msg += "    - None\n"
                msg += "    - str : a valid shortcut\n"
                msg += "    - list of str: list of valid shortcuts\n"
                msg += "You provided:\n"
                msg += str(dsig)
                raise Exception(msg)
            if lc[0]:
                dsig[k0] = lkeysok
            if lc[1]:
                dsig[k0] = [dsig[k0]]
            if not all([ss in lkeysok for ss in dsig[k0]]):
                msg = "All requested signals must be valid shortcuts !\n"
                msg += "    - dsig[%s] = %s"%(k0, str(dsig[k0]))
                raise Exception(msg)

            # Check presence of minimum
            lc = [ss for ss in lscom if ss not in dsig[k0]]
            if len(lc) > 0:
                msg = "dsig[%s] does not have %s\n"%(k0,str(lc))
                msg += "    - dsig[%s] = %s"%(k0,str(dsig[k0]))
                raise Exception(msg)
            if any(['2d' in ss for ss in dsig[k0]]):
                for ss in lsmesh:
                    if ss not in dsig[k0]:
                        dsig[k0].append(ss)
            dout[k0] = dsig[k0]
        return dout


    @staticmethod
    def _checkformat_mesh_NodesFaces(nodes, indfaces, ids=None):

        # Check mesh type
        if indfaces.shape[1] == 3:
            mtype = 'tri'
        elif indfaces.shape[1] == 4:
            mtype = 'quad'
        else:
            msg = "Mesh seems to be neither triangular nor quadrilateral\n"
            msg += "  => unrecognized mesh type, not implemented yet"
            raise Exception(msg)

        # Check indexing !!!
        indmax = int(np.nanmax(indfaces))
        if indmax == nodes.shape[0]:
            indfaces = indfaces - 1
        elif indmax > nodes.shape[0]:
            msg = "There seems to be an indexing error\n"
            msg += "    - np.max(indfaces) = %s"%str(indmax)
            msg += "    - nodes.shape[0] = %s"%str(nodes.shape[0])
            raise Exception(msg)

        # Check for duplicates
        nnodes = nodes.shape[0]
        nfaces = indfaces.shape[0]
        nodesu, indnodesu = np.unique(nodes, axis=0, return_index=True)
        facesu, indfacesu = np.unique(indfaces, axis=0, return_index=True)
        facesuu = np.unique(facesu)
        lc = [nodesu.shape[0] != nnodes,
              facesu.shape[0] != nfaces,
              facesuu.size != nnodes or np.any(facesuu != np.arange(0,nnodes))]
        if any(lc):
            msg = "Non-valid mesh in ids %s:\n"%ids
            if lc[0]:
                noddup = [ii for ii in range(0,nnodes) if ii not in indnodesu]
                msg += "  Duplicate nodes: %s\n"%str(nnodes - nodesu.shape[0])
                msg += "    - nodes.shape: %s\n"%str(nodes.shape)
                msg += "    - unique nodes.shape: %s\n"%str(nodesu.shape)
                msg += "    - duplicate nodes indices: %s\n"%str(noddup)
            if lc[1]:
                dupf = [ii for ii in range(0,nfaces) if ii not in indfacesu]
                msg += "  Duplicate faces: %s\n"%str(nfaces - facesu.shape[0])
                msg += "    - faces.shape: %s\n"%str(indfaces.shape)
                msg += "    - unique faces.shape: %s"%str(facesu.shape)
                msg += "    - duplicate facess indices: %s\n"%str(dupf)
            if lc[2]:
                nfu = facesuu.size
                nodnotf = [ii for ii in range(0,nnodes) if ii not in facesuu]
                fnotn = [ii for ii in facesuu if ii < 0 or  ii >= nnodes]
                msg += "  Non-bijective nodes indices vs faces:\n"
                msg += "    - nb. nodes: %s\n"%str(nnodes)
                msg += "    - nb. unique nodes index in faces: %s\n"%str(nfu)
                msg += "    - nodes not in faces: %s\n"%str(nodnotf)
                msg += "    - faces ind not in nodes: %s\n"%str(fnotn)
            raise Exception(msg)

        # Test for unused nodes
        facesu = np.unique(indfaces)
        c0 = np.all(facesu>=0) and facesu.size == nnodes
        if not c0:
            indnot = [ii for ii in range(0,nnodes)
                      if ii not in facesu]
            msg = "Some nodes not used in mesh of ids %s:\n"%ids
            msg += "    - unused nodes indices: %s"%str(indnot)
            warnings.warn(msg)

        # Convert to triangular mesh if necessary
        if mtype == 'quad':
            # Convert to tri mesh (solution for unstructured meshes)
            indface = np.empty((indfaces.shape[0]*2,3), dtype=int)

            indface[::2,:] = indfaces[:,:3]
            indface[1::2,:-1] = indfaces[:,2:]
            indface[1::2,-1] = indfaces[:,0]
            indfaces = indface
            mtype = 'quadtri'
            ntri = 2
        else:
            ntri = 1


        # Check orientation
        x, y = nodes[indfaces,0], nodes[indfaces,1]
        orient = ((y[:,1]-y[:,0])*(x[:,2]-x[:,1])
                  - (y[:,2]-y[:,1])*(x[:,1]-x[:,0]))

        indclock = orient > 0.
        if np.any(indclock):
            nclock, ntot = indclock.sum(), indfaces.shape[0]
            msg = "Some triangles not counter-clockwise\n"
            msg += "  (necessary for matplotlib.tri.Triangulation)\n"
            msg += "    => %s/%s triangles reshaped"%(str(nclock),str(ntot))
            warnings.warn(msg)
            (indfaces[indclock,1],
             indfaces[indclock,2]) = indfaces[indclock,2], indfaces[indclock,1]
        return indfaces, mtype, ntri

    def inspect_ggd(self, ids):
        # TBF
        if ids not in self._dids.keys():
            msg = "The ggd of ids %s cannot be inspected:\n"%ids
            msg += "  => please add ids first (self.add_ids())"
            raise Exception(msg)

        lids = ['equilibrium', 'core_sources', 'edge_sources']
        if ids not in lids:
            msg = "The default structure of ggd in ids %s is not known"%ids
            raise Exception(msg)

        if ids == 'equilibrium':
            nt = len(grids_ggd)
            for ii in range(nt):
                nggd = len(grids_ggd[ii])
                for jj in range(0,ngrid):
                    ggd = grids_ggd[ii].grid[jj]
                    gtype = ggd.identifier.name
                    nspace = len(ggd.space)
                    for ll in range(0,nspace):
                        npts = ggd.space[ll].objects_per_dimension[0].object[0]

    @staticmethod
    def _checkformat_mesh_Rect(R, Z, datashape=None,
                               shapeRZ=None, ids=None):
        assert R.ndim in [1, 2]
        assert Z.ndim in [1, 2]
        shapeu = np.unique(np.r_[R.shape, Z.shape])
        if shapeRZ is None:
            shapeRZ = [None, None]
        if R.ndim == 1:
            assert np.all(np.diff(R) > 0.)
        else:
            lc = [np.all(np.diff(R[0, :])) > 0.,
                  np.all(np.diff(R[:, 0])) > 0.]
            assert np.sum(lc) == 1
            if lc[0]:
                R = R[0, :]
                if shapeRZ[1] is None:
                    shapeRZ[1] = 'R'
                assert shapeRZ[1] == 'R'
            else:
                R = R[:, 0]
                if shapeRZ[0] is None:
                    shapeRZ[0] = 'R'
                assert shapeRZ[0] == 'R'
        if Z.ndim == 1:
            assert np.all(np.diff(Z) > 0.)
        else:
            lc = [np.all(np.diff(Z[0, :])) > 0.,
                  np.all(np.diff(Z[:, 0])) > 0.]
            assert np.sum(lc) == 1
            if lc[0]:
                Z = Z[0, :]
                if shapeRZ[1] is None:
                    shapeRZ[1] = 'Z'
                assert shapeRZ[1] == 'Z'
            else:
                Z = Z[:, 0]
                if shapeRZ[0] is None:
                    shapeRZ[0] = 'Z'
                assert shapeRZ[0] == 'Z'

        if datashape is not None:
            if None in shapeRZ:
                pass
            shapeRZ = tuple(shapeRZ)

            if shapeRZ == ('R', 'Z'):
                assert datashape == (R.size, Z.size)
            elif shapeRZ == ('Z', 'R'):
                assert datashape == (Z.size, R.size)
            else:
                msg = "Inconsistent data shape !"
                raise Exception(msg)

        if None not in shapeRZ:
            shapeRZ = tuple(shapeRZ)
            assert shapeRZ in [('R', 'Z'), ('Z', 'R')]
        return R, Z, shapeRZ, 0

    # TBF
    def get_mesh_from_ggd(path_to_ggd, ggdindex=0):
        pass

    def _get_dextra(self, dextra=None, fordata=False, nan=True, pos=None):
        lc = [dextra == False, dextra is None,
              type(dextra) is str, type(dextra) is list, type(dextra) is dict]
        assert any(lc)

        if dextra is False:
            if fordata:
                return None
            else:
                return None, None

        elif dextra is None:
            dextra = {}
            if 'equilibrium' in self._dids.keys():
                dextra.update({'equilibrium': [('ip','k'), ('BT0','m'),
                                               ('axR',(0.,0.8,0.)),
                                               ('axZ',(0.,1.,0.)),
                                               'ax','sep','t']})
            if 'core_profiles' in self._dids.keys():
                dextra.update({'core_profiles': ['ip','vloop','t']})
            if 'lh_antennas' in self._dids.keys():
                dextra.update({'lh_antennas': [('power0',(0.8,0.,0.)),
                                               ('power1',(1.,0.,0.)),'t']})
            if 'ic_antennas' in self._dids.keys():
                dextra.update({'ic_antennas': [('power0',(0.,0.,0.8)),
                                               ('power1',(0.,0.,1.)),
                                               ('power2',(0.,0.,0.9)),'t']})
        if type(dextra) is str:
            dextra = [dextra]
        if type(dextra) is list:
            dex = {}
            for ee in dextra:
                lids = [ids for ids in self._dids.keys()
                        if ee in self._dshort[ids].keys()]
                if len(lids) != 1:
                    msg = "No / multiple matches:\n"
                    msg = "extra %s not available from self._dshort"%ee
                    raise Exception(msg)
                if lids[0] not in dex.keys():
                    dex = {lids[0]:[ee]}
                else:
                    dex[lids[0]].append(ee)
            dextra = dex

        if len(dextra) == 0:
            if fordata:
                return None
            else:
                return None, None

        if fordata:
            dout = {}
            for ids, vv in dextra.items():
                vs = [vvv if type(vvv) is str else vvv[0] for vvv in vv]
                vc = ['k' if type(vvv) is str else vvv[1] for vvv in vv]
                out = self.get_data(ids=ids, sig=vs, nan=nan, pos=pos)
                inds = [ii for ii in range(0,len(vs)) if vs[ii] in out.keys()]
                for ii in inds:
                    ss = vs[ii]
                    if ss == 't':
                        continue
                    if out[ss].size == 0:
                        continue
                    if ss in self._dshort[ids].keys():
                        dd = self._dshort[ids][ss]
                    else:
                        dd = self._dcomp[ids][ss]
                    label = dd.get('quant', 'unknown')
                    units = dd.get('units', 'a.u.')
                    key = '%s.%s'%(ids,ss)

                    if 'sep' == ss.split('.')[-1].lower():
                        out[ss] = np.swapaxes(out[ss], 1,2)

                    datastr = 'data'
                    if any([ss.split('.')[-1].lower() == s0 for s0 in
                            ['sep','ax','x']]):
                        datastr = 'data2D'

                    dout[key] = {'t': out['t'], datastr:out[ss],
                                 'label':label, 'units':units, 'c':vc[ii]}
            return dout

        else:
            d0d, dt0 = {}, {}
            for ids, vv in dextra.items():
                vs = [vvv if type(vvv) is str else vvv[0] for vvv in vv]
                vc = ['k' if type(vvv) is str else vvv[1] for vvv in vv]
                out = self.get_data(ids=ids, sig=vs, nan=nan, pos=pos)
                keyt = '%s.t'%ids
                any_ = False
                for ss in out.keys():
                    if ss == 't':
                        continue
                    if out[ss].size == 0:
                        continue
                    if ss in self._dshort[ids].keys():
                        dd = self._dshort[ids][ss]
                    else:
                        dd = self._dcomp[ids][ss]
                    dim = dd.get('dim', 'unknown')
                    quant = dd.get('quant', 'unknown')
                    units = dd.get('units', 'a.u.')
                    key = '%s.%s'%(ids,ss)

                    if 'sep' == ss.split('.')[-1].lower():
                        out[ss] = np.swapaxes(out[ss], 1,2)

                    d0d[key] = {'data':out[ss], 'name':ss,
                                'origin':ids, 'dim':dim, 'quant':quant,
                                'units':units, 'depend':(keyt,)}
                    any_ = True
                if any_:
                    dt0[keyt] = {'data':out['t'], 'name':'t',
                                 'origin':ids, 'depend':(keyt,)}
            return d0d, dt0



    def to_Plasma2D(self, tlim=None, dsig=None, t0=None,
                    Name=None, occ=None, config=None, out=object,
                    description_2d=None,
                    plot=None, plot_sig=None, plot_X=None,
                    bck=True, dextra=None, nan=True, pos=None, shapeRZ=None):
        """ Export the content of some ids as a tofu Plasma2D object

        Some ids typically contain plasma 1d (radial) or 2d (mesh) profiles
        They include for example ids:
            - core_profiles
            - core_sources
            - edge_profiles
            - edge_sources
            - equilibrium

        tofu offers a class for handling multiple profiles characterizing a
        plasma, it's called Plasma2D
        This method automatically identifies the ids that may contain profiles,
        extract all profiles (i.e.: all profiles identified by a shortcut, see
        self.get_shortcuts()) and export everything to a fresh Plasma2D
        instance.

        Parameters
        ----------
        tlim:   None / list
            Restrict the loaded data to a time interval with tlim
            if None, loads all time steps
        dsig:   None / dict
            Specify exactly which data (shortcut) should be loaded by ids
            If None, loads all available data
        t0:     None / float / str
            Specify a time to be used as origin:
                - None: absolute time vectors are untouched
                - float : the roigin of all time vectors is set to t0
                - str : the origin is taken from an event in ids pulse_schedule
        Name:   None / str
            Name to be given to the instance
            If None, a default Name is built
        occ:    None / int
            occurence to be used for loading the data
        config: None / Config
            Configuration (i.e.: tokamak geometry) to be used for the instance
            If None, created from the wall ids with self.to_Config().
        out:    type
            class with which the output shall be returned
                - object :  as a Plasma2D instance
                - dict:     as a dict
        description_2d: None / int
            description_2d index to be used if the Config is to be built from
            wall ids. See self.to_Config()
        plot:       None / bool
            Flag whether to plot the result
        plot_sig:   None / str
            shortcut of the signal to be plotted, if any
        plot_X:     None / str
            shortcut of the abscissa against which to plot the signal, if any
        bck:        bool
            Flag indicating whether to plot the grey envelop of the signal as a
            background, if plot is True
        dextra:     None / dict
            dict of extra signals (time traces) to be plotted, for context
        shapeRZ:    None / tuple
            If provided, tuple indicating the order of 2d data arrays
            associated to rectangular meshes
            Only necessary when shape cannot be infered from data shape
                - ('R', 'Z'): first dimension is R, second Z
                - ('Z', 'R'): the other way around

        Args nan and pos are fed to self.get_data()

        Return
        ------
        plasma:     dict / Plasma2D
            dict or Plasma2D instance depending on out

        """

        # dsig
        dsig = self._checkformat_Plasma2D_dsig(dsig)

        # plot arguments
        if plot is None:
            plot = not (plot_sig is None and plot_X is None)

        if plot == True:
            if plot_sig is None:
                lsplot = [ss for ss in list(dsig.values())[0]
                          if ('1d' in ss and ss != 't'
                              and all([sub not in ss
                                       for sub in ['rho','psi','phi']]))]
                if not (len(dsig) == 1 and len(lsplot) == 1):
                    msg = "Direct plotting only possible if\n"
                    msg += "sig_plot is provided, or can be derived from:\n"
                    msg += "    - unique ids: %s"%str(dsig.keys())
                    msg += "    - unique non-t, non-radius 1d sig: %s"%str(lsplot)
                    raise Exception(msg)
                plot_sig = lsplot
            if type(plot_sig) is str:
                plot_sig = [plot_sig]
            if plot_X is None:
                lsplot = [ss for ss in list(dsig.values())[0]
                          if ('1d' in ss and ss != 't'
                              and any([sub in ss
                                       for sub in ['rho','psi','phi']]))]
                if not (len(dsig) == 1 and len(lsplot) == 1):
                    msg = "Direct plotting only possible if\n"
                    msg += "X_plot is provided, or can be derived from:\n"
                    msg += "    - unique ids: %s"%str(dsig.keys())
                    msg += "    - unique non-t, 1d radius: %s"%str(lsplot)
                    raise Exception(msg)
                plot_X = lsplot
            if type(plot_X) is str:
                plot_X = [plot_X]

        # lids
        lids = sorted(dsig.keys())
        if Name is None:
            Name = 'custom'

        # ---------------------------
        # Preliminary checks on data source consistency
        _, _, shot, Exp = self._get_lidsidd_shotExp(lids, upper=True,
                                                    errshot=False,
                                                    errExp=False)
        # get data
        out0 = self.get_data_all(dsig=dsig)

        # -------------
        #   Input dicts

        # config
        if config is None:
            config = self.to_Config(Name=Name, occ=occ,
                                    description_2d=description_2d, plot=False)

        # dextra
        d0d, dtime0 = self._get_dextra(dextra)

        # dicts
        dtime = {} if dtime0 is None else dtime0
        d1d, dradius = {}, {}
        d2d, dmesh = {}, {}
        for ids in lids:
            # Hotfiw to avoid calling get_data a second time out0 -> out_
            # TBF in next release (ugly, sub-optimal...)

            # dtime
            out_ = {'t': out0[ids].get('t', None)}
            lc = [out_['t'] is not None,
                  out_['t'].size > 0,
                  0 not in out_['t'].shape]
            keyt, nt, indt = None, None, None
            if all(lc):
                nt = out_['t'].size
                keyt = '%s.t'%ids

                dtt = self._checkformat_tlim(out_['t'], tlim=tlim)
                dtime[keyt] = {'data':dtt['t'],
                               'origin':ids, 'name':'t'}
                indt = dtt['indt']
            else:
                nt = None

            # d1d and dradius
            lsig = [k for k in dsig[ids]
                    if '1d' in k and k in out0[ids].keys()]
            out_ = self.get_data(ids, lsig, indt=indt, nan=nan, pos=pos,
                                 warn=False)
            if len(out_) > 0:
                nref, kref = None, None
                for ss in out_.keys():
                    assert out_[ss].ndim in [1,2]
                    if out_[ss].ndim == 1:
                        out_[ss] = np.atleast_2d(out_[ss])
                    shape = out_[ss].shape
                    if 0 in shape or len(shape) == 0:
                        continue

                    if nt is None:
                        msg = "%s.'t' could not be retrieved\n"%ids
                        msg += "Assuming 't' is the first dimension of:\n"
                        msg += "    - %s.%s"%(ids,ss)
                        warnings.warn(msg)
                        nt = shape[0]
                        keyt = '%s.homemade'%ids
                        dtime[keyt] = {'data':np.arange(0,nt),
                                       'origin':ids, 'name':'homemade'}
                    else:
                        if nt not in shape:
                            msg = "Inconsistent shape with respect to 't'!\n"
                            msg += "    - %s.%s.shape = %s"%(ids,ss,str(shape))
                            msg += "    - One dim should be t.size = %s"%str(nt)
                            raise Exception(msg)
                    axist = shape.index(nt)
                    nr = shape[1-axist]
                    if axist == 1:
                        out_[ss] = out_[ss].T

                    if ss in self._dshort[ids].keys():
                        dim = self._dshort[ids][ss].get('dim', 'unknown')
                        quant = self._dshort[ids][ss].get('quant', 'unknown')
                        units = self._dshort[ids][ss].get('units', 'a.u.')
                    else:
                        dim = self._dcomp[ids][ss].get('dim', 'unknown')
                        quant = self._dcomp[ids][ss].get('quant', 'unknown')
                        units = self._dcomp[ids][ss].get('units', 'a.u.')
                    key = '%s.%s'%(ids,ss)

                    if nref is None:
                        dradius[key] = {'data': out_[ss], 'name': ss,
                                        'origin': ids, 'dim': dim,
                                        'quant': quant, 'units': units,
                                        'depend': (keyt, key)}
                        nref, kref = nr, key
                    else:
                        assert nr == nref
                        d1d[key] = {'data': out_[ss], 'name': ss,
                                    'origin': ids, 'dim': dim, 'quant': quant,
                                    'units': units, 'depend': (keyt, kref)}
                        assert out_[ss].shape == (nt, nr)

                    if plot:
                        if ss in plot_sig:
                            plot_sig[plot_sig.index(ss)] = key
                        if ss in plot_X:
                            plot_X[plot_X.index(ss)] = key

            # d2d and dmesh
            lsig = [k for k in dsig[ids]
                    if '2d' in k and k in out0[ids].keys()]
            lsigmesh = [k for k in lsig if 'mesh' in k]
            out_ = self.get_data(ids, sig=lsig, indt=indt, nan=nan, pos=pos,
                                 warn=False)

            cmesh = any([ss in out_.keys() for ss in lsigmesh])
            if len(out_) > 0:
                npts, datashape = None, None
                keym = '{}.mesh'.format(ids) if cmesh else None
                for ss in set(out_.keys()).difference(lsigmesh):
                    assert out_[ss].ndim in [1, 2, 3]
                    if out_[ss].ndim == 1:
                        out_[ss] = np.atleast_2d(out_[ss])
                    shape = out_[ss].shape
                    assert len(shape) >= 2
                    if np.sum(shape) > 0:
                        if nt not in shape:
                            assert nt == 1
                            assert len(shape) == 2
                            datashape = tuple(shape)
                            if shapeRZ is None:
                                msg = ("Please provide shapeRZ"
                                       + "indexing is ambiguous")
                                raise Exception(msg)
                            size = shape[0]*shape[1]
                            if shapeRZ == ('R', 'Z'):
                                out_[ss] = out_[ss].reshape((nt, size))
                            elif shapeRZ == ('Z', 'R'):
                                out_[ss] = out_[ss].reshape((nt, size),
                                                            order='F')
                            shape = out_[ss].shape
                        if len(shape) == 3:
                            assert nt == shape[0]
                            datashape = (shape[1], shape[2])
                            if shapeRZ is None:
                                msg = ("Please provide shapeRZ,"
                                       + " indexing is ambiguous")
                                raise Exception(msg)
                            size = shape[1]*shape[2]
                            if shapeRZ == ('R', 'Z'):
                                out_[ss] = out_[ss].reshape((nt, size))
                            elif shapeRZ == ('Z', 'R'):
                                out_[ss] = out_[ss].reshape((nt, size),
                                                            order='F')
                            shape = out_[ss].shape

                        axist = shape.index(nt)
                        if npts is None:
                            npts = shape[1-axist]
                        assert npts == shape[1-axist]
                        if axist == 1:
                            out_[ss] = out_[ss].T

                        if ss in self._dshort[ids].keys():
                            dim = self._dshort[ids][ss].get('dim', 'unknown')
                            quant = self._dshort[ids][ss].get('quant', 'unknown')
                            units = self._dshort[ids][ss].get('units', 'a.u.')
                        else:
                            dim = self._dcomp[ids][ss].get('dim', 'unknown')
                            quant = self._dcomp[ids][ss].get('quant', 'unknown')
                            units = self._dcomp[ids][ss].get('units', 'a.u.')
                        key = '%s.%s'%(ids,ss)

                        d2d[key] = {'data': out_[ss], 'name': ss,
                                    'dim': dim, 'quant': quant, 'units': units,
                                    'origin': ids, 'depend': (keyt, keym)}

                if cmesh:
                    lc = [all([ss in lsig for ss in ['2dmeshNodes',
                                                     '2dmeshFaces']]),
                          all([ss in lsig for ss in ['2dmeshR', '2dmeshZ']])]
                    if not np.sum(lc) == 1:
                        msg = ("2d mesh shall be provided either via:\n"
                               + "\t- '2dmeshR' and '2dmeshZ'\n"
                               + "\t- '2dmeshNodes' and '2dmeshFaces'")
                        raise Exception(msg)

                    # Nodes / Faces case
                    if lc[0]:
                        nodes = out_['2dmeshNodes']
                        indfaces = out_['2dmeshFaces']
                        func = self._checkformat_mesh_NodesFaces
                        indfaces, mtype, ntri = func(nodes, indfaces, ids=ids)
                        nnod, nfaces = int(nodes.size/2), indfaces.shape[0]
                        if npts is not None:
                            nft = int(nfaces/ntri)
                            if npts not in [nnod, nft]:
                                msg = "Inconsistent indices:\n"
                                msg += "\t- 2d profile {} npts\n".format(npts)
                                msg += "\t- mesh {} nodes\n".format(nnod)
                                msg += "\t       {} faces".format(nft)
                                raise Exception(msg)
                            ftype = 1 if npts == nnod else 0
                        else:
                            ftype = None
                        mpltri = mpl.tri.Triangulation(nodes[:, 0],
                                                       nodes[:, 1], indfaces)
                        dmesh[keym] = {'dim': 'mesh', 'quant': 'mesh',
                                       'units': 'a.u.', 'origin': ids,
                                       'depend': (keym,), 'name': mtype,
                                       'nodes': nodes, 'faces': indfaces,
                                       'type': mtype, 'ntri': ntri,
                                       'ftype': ftype, 'nnodes': nnod,
                                       'nfaces': nfaces, 'mpltri': mpltri}
                    # R / Z case
                    elif lc[1]:
                        func = self._checkformat_mesh_Rect
                        R, Z, shapeRZ, ftype = func(out_['2dmeshR'],
                                                    out_['2dmeshZ'],
                                                    datashape=datashape,
                                                    shapeRZ=shapeRZ, ids=ids)
                        dmesh[keym] = {'dim': 'mesh', 'quant': 'mesh',
                                       'units': 'a.u.', 'origin': ids,
                                       'depend': (keym,), 'name': 'rect',
                                       'R': R, 'Z': Z, 'shapeRZ': shapeRZ,
                                       'type': 'rect', 'ftype': ftype}

        # t0
        t0 = self._get_t0(t0)
        if t0 != False:
            for tt in dtime.keys():
                dtime[tt]['data'] = dtime[tt]['data'] - t0

        plasma = dict(dtime=dtime, dradius=dradius, dmesh=dmesh,
                      d0d=d0d, d1d=d1d, d2d=d2d,
                      Exp=Exp, shot=shot, Name=Name, config=config)

        # Instanciate Plasma2D
        if out == object or plot == True:
            import tofu.data as tfd
            plasma = tfd.Plasma2D( **plasma )
            if plot == True:
                plasma.plot(plot_sig, X=plot_X, bck=bck)

        return plasma


    def _checkformat_Cam_geom(self, ids=None, geomcls=None, indch=None):

        # Check ids
        idsok = set(self._lidsdiag).intersection(self._dids.keys())
        if ids is None and len(idsok) == 1:
            ids = next(iter(idsok))

        if ids not in self._dids.keys():
            msg = ("Provided ids should be available as a self.dids.keys()!\n"
                   + "\t- provided: {}\n".format(str(ids))
                   + "\t- available: {}".format(sorted(self._dids.keys())))
            raise Exception(msg)

        if ids not in self._lidsdiag:
            msg = "Requested ids is not pre-tabulated !\n"
            msg = "  => Be careful with args (geomcls, indch)"
            warnings.warn(msg)
        else:
            if geomcls is None:
                geomcls = self._didsdiag[ids]['geomcls']

        # Check data and geom
        import tofu.geom as tfg

        lgeom = [kk for kk in dir(tfg) if 'Cam' in kk]
        if geomcls not in [False] + lgeom:
            msg = "Arg geomcls must be in {}".format([False]+lgeom)
            raise Exception(msg)

        if geomcls is False:
            msg = "ids {} does not seem to be a ids with a camera".format(ids)
            raise Exception(msg)

        return geomcls

    def inspect_channels(self, ids=None, occ=None, indch=None, geom=None,
                         dsig=None, data=None, X=None, datacls=None,
                         geomcls=None, return_dict=None, return_ind=None,
                         return_msg=None, verb=None):
        # ------------------
        # Preliminary checks
        if return_dict is None:
            return_dict = False
        if return_ind is None:
            return_ind = False
        if return_msg is None:
            return_msg = False
        if verb is None:
            verb = True
        if occ is None:
            occ = 0
        if geom is None:
            geom = True
        compute_ind = return_ind or return_msg or verb

        # Check ids is relevant
        idsok = set(self._lidsdiag).intersection(self._dids.keys())
        if ids is None and len(idsok) == 1:
            ids = next(iter(idsok))

        # Check ids has channels (channel, gauge, ...)
        lch = ['channel', 'gauge', 'group', 'antenna',
               'pipe', 'reciprocating', 'bpol_probe']
        ind = [ii for ii in range(len(lch))
               if hasattr(self._dids[ids]['ids'][occ], lch[ii])]
        if len(ind) == 0:
            msg = "ids {} has no attribute with '[chan]' index!".format(ids)
            raise Exception(msg)
        nch = len(getattr(self._dids[ids]['ids'][0], lch[ind[0]]))
        if nch == 0:
            msg = ('ids {} has 0 channels:\n'.format(ids)
                   + '\t- len({}.{}) = 0\n'.format(ids, lch[ind[0]])
                   + '\t- idd: {}'.format(self._dids[ids]['idd']))
            raise Exception(msg)


        datacls, geomcls, dsig = self._checkformat_Data_dsig(ids, dsig,
                                                             data=data, X=X,
                                                             datacls=datacls,
                                                             geomcls=geomcls)
        if geomcls is False:
            geom = False

        # ------------------
        # Extract sig and shapes / values
        if geom == 'only':
            lsig = []
        else:
            lsig = sorted(dsig.values())
        lsigshape = list(lsig)
        if geom in ['only', True] and 'LOS' in geomcls:
            lkok = set(self._dshort[ids].keys()).union(self._dcomp[ids].keys())
            lsig += [ss for ss in ['los_ptsRZPhi', 'etendue',
                                   'surface', 'names']
                     if ss in lkok]

        out = self.get_data(ids, sig=lsig,
                            isclose=False, stack=False, nan=True,
                            pos=False)
        dout = {}
        for k0, v0 in out.items():
            if len(v0) != nch:
                if len(v0) != 1:
                    import pdb          # DB
                    pdb.set_trace()     # DB
                continue
            if isinstance(v0[0], np.ndarray):
                dout[k0] = {'shapes': np.array([vv.shape for vv in v0]),
                            'isnan': np.array([np.any(np.isnan(vv))
                                               for vv in v0])}
                if k0 == 'los_ptsRZPhi':
                    dout[k0]['equal'] = np.array([np.allclose(vv[0, ...],
                                                              vv[1, ...])
                                                 for vv in v0])
            elif type(v0[0]) in [int, float, np.int, np.float, str]:
                dout[k0] = {'value': np.asarray(v0).ravel()}
            else:
                typv = type(v0[0])
                k0str = (self._dshort[ids][k0]['str']
                         if k0 in self._dshort[ids].keys() else k0)
                msg = ("\nUnknown data type:\n"
                       + "\ttype({}) = {}".format(k0str, typv))
                raise Exception(msg)

        lsig = sorted(set(lsig).intersection(dout.keys()))
        lsigshape = sorted(set(lsigshape).intersection(dout.keys()))

        # --------------
        # Get ind, msg
        ind, msg = None, None
        if compute_ind:
            if geom in ['only', True] and 'los_ptsRZPhi' in out.keys():
                indg = ((np.prod(dout['los_ptsRZPhi']['shapes'], axis=1) == 0)
                        | dout['los_ptsRZPhi']['isnan']
                        | dout['los_ptsRZPhi']['equal'])
                if geom == 'only':
                    indok = ~indg
                    indchout = indok.nonzero()[0]
            if geom != 'only':
                shapes0 = np.concatenate([np.prod(dout[k0]['shapes'],
                                                  axis=1, keepdims=True)
                                          for k0 in lsigshape], axis=1)
                indok = np.all(shapes0 != 0, axis=1)
                if geom is True and 'los_ptsRZPhi' in out.keys():
                    indok[indg] = False
            if not np.any(indok):
                indchout = np.array([], dtype=int)
            elif geom != 'only':
                indchout = (np.arange(0, nch)[indok]
                            if indch is None else np.r_[indch][indok])
                lshapes = [dout[k0]['shapes'][indchout, :] for k0 in lsigshape]
                lshapesu = [np.unique(ss, axis=0) for ss in lshapes]
                if any([ss.shape[0] > 1 for ss in lshapesu]):
                    for ii in range(len(lshapesu)):
                        if lshapesu[ii].shape[0] > 1:
                            _, inv, counts = np.unique(lshapes[ii], axis=0,
                                                       return_counts=True,
                                                       return_inverse=True)
                            indchout = indchout[inv == np.argmax(counts)]
                            lshapes = [dout[k0]['shapes'][indchout, :]
                                       for k0 in lsigshape]
                            lshapesu = [np.unique(ss, axis=0)
                                        for ss in lshapes]

        if return_msg is True or verb is True:
            col = ['index'] + [k0 for k0 in dout.keys()]
            ar = ([np.arange(nch)]
                  + [['{} {}'.format(tuple(v0['shapes'][ii]), 'nan')
                      if v0['isnan'][ii] else str(tuple(v0['shapes'][ii]))
                      for ii in range(nch)]
                     if 'shapes' in v0.keys()
                     else v0['value'].astype(str) for v0 in dout.values()])
            msg = self._getcharray(ar, col, msg=True)
            if verb is True:
                indstr = ', '.join(map(str, indchout))
                msg += "\n\n => recommended indch = [{}]".format(indstr)
                print(msg)

        # ------------------
        # Return
        lv = [(dout, return_dict), (indchout, return_ind), (msg, return_msg)]
        lout = [vv[0] for vv in lv if vv[1] is True]
        if len(lout) == 1:
            return lout[0]
        elif len(lout) > 1:
            return lout

    @staticmethod
    def _compare_indch_indchr(indch, indchr, nch, indch_auto=None):
        if indch_auto is None:
            indch_auto = True
        if indch is None:
            indch = np.arange(0, nch)
        if not np.all(np.in1d(indch, indchr)):
            msg = ("indch has to be changed, some data may be missing\n"
                   + "\t- indch: {}\n".format(indch)
                   + "\t- indch recommended: {}".format(indchr)
                   + "\n\n  => check self.inspect_channels() for details")
            if indch_auto is True:
                indch = indchr
                warnings.warn(msg)
            else:
                raise Exception(msg)
        return indch

    def _to_Cam_Du(self, ids, lk, indch, nan=None, pos=None):
        Etendues, Surfaces, names = None, None, None
        out = self.get_data(ids, sig=list(lk), indch=indch,
                            nan=nan, pos=pos)
        if 'los_ptsRZPhi' in out.keys() and out['los_ptsRZPhi'].size > 0:
            oo = out['los_ptsRZPhi']
            D = np.array([oo[:,0,0]*np.cos(oo[:,0,2]),
                          oo[:,0,0]*np.sin(oo[:,0,2]), oo[:,0,1]])
            u = np.array([oo[:,1,0]*np.cos(oo[:,1,2]),
                          oo[:,1,0]*np.sin(oo[:,1,2]), oo[:,1,1]])
            u = (u-D) / np.sqrt(np.sum((u-D)**2, axis=0))[None,:]
            dgeom = (D, u)
            indnan = np.any(np.isnan(D), axis=0) | np.any(np.isnan(u), axis=0)
            if np.any(indnan):
                nunav, ntot = str(indnan.sum()), str(D.shape[1])
                msg = "Some lines of sight geometry unavailable in ids:\n"
                msg += "    - unavailable LOS: {0} / {1}\n".format(nunav, ntot)
                msg += "    - indices: {0}".format(str(indnan.nonzero()[0]))
                warnings.warn(msg)
        else:
            dgeom = None

        if 'etendue' in out.keys() and len(out['etendue']) > 0:
            Etendues = out['etendue']
        if 'surface' in out.keys() and len(out['surface']) > 0:
            Surfaces = out['surface']
        if 'names' in out.keys() and len(out['names']) > 0:
            names = out['names']
        return dgeom, Etendues, Surfaces, names



    def to_Cam(self, ids=None, indch=None, indch_auto=False,
               description_2d=None,
               Name=None, occ=None, config=None,
               plot=True, nan=True, pos=None):
        """ Export the content of a diagnostic ids as a tofu CamLos1D instance

        Some ids contain the geometry of a diagnostics
        They typically have a 'channels' field
        Generally in the form of a set of Lines of Sights (LOS)
        They include for example ids:
            - interferometer
            - polarimeter
            - bolometer
            - soft_x_rays
            - bremsstrahlung_visible
            - spectrometer_visible

        tofu offers a class for handling sets fo LOS as a camera: CamLOS1D
        This method extracts the geometry of the desired diagnostic (ids) and
        exports it as a CamLOS1D instance.

        Parameters
        ----------
        ids:   None / str
            Specify the ids (will be checked against known diagnostics ids)
            Should have a 'channels' field
            If None and a unique diagnostic ids has been added, set to this one
        Name:   None / str
            Name to be given to the instance
            If None, a default Name is built
        occ:    None / int
            occurence to be used for loading the data
        indch:  None / list / array
            If provided, array of int indices specifying which channels shall
            be loaded (fed to self.get_data())
        indch_auto: bool
            If True and indch is not provided, will try to guess which channels
            can be loaded. If possible all channels are loaded by default, but
            only if they have uniform data (same shape, i.e.: same time
            vectors). In case of channels with non-uniform data, will try to
            identify a sub-group of channels with uniform data
        config: None / Config
            Configuration (i.e.: tokamak geometry) to be used for the instance
            If None, created from the wall ids with self.to_Config().
        description_2d: None / int
            description_2d index to be used if the Config is to be built from
            wall ids. See self.to_Config()
        plot:       None / bool
            Flag whether to plot the result

        Args nan and pos are fed to self.get_data()

        Return
        ------
        cam:     CamLOS1D
            CamLOS1D instance

        """

        # Check ids
        idsok = set(self._lidslos).intersection(self._dids.keys())
        if ids is None and len(idsok) == 1:
            ids = next(iter(idsok))

        # dsig
        geom = self._checkformat_Cam_geom(ids)
        if Name is None:
            Name = 'custom'

        # ---------------------------
        # Preliminary checks on data source consistency
        _, _, shot, Exp = self._get_lidsidd_shotExp([ids], upper=True,
                                                    errshot=False,
                                                    errExp=False)
        # -------------
        #   Input dicts

        # config
        if config is None:
            config = self.to_Config(Name=Name, occ=occ,
                                    description_2d=description_2d, plot=False)

        # dchans
        dchans = {}
        if indch is not None:
            dchans['ind'] = indch

        # cam
        cam = None
        nchMax = len(self._dids[ids]['ids'][0].channel)
        Etendues, Surfaces = None, None
        if config is None:
            msg = "A config must be provided to compute the geometry !"
            raise Exception(msg)

        if 'LOS' in geom:
            # Check channel indices
            indchr = self.inspect_channels(ids, indch=indch,
                                           geom='only', return_ind=True,
                                           verb=False)
            indch = self._compare_indch_indchr(indch, indchr, nchMax,
                                               indch_auto=indch_auto)

            # Load geometrical data
            lk = ['los_ptsRZPhi', 'etendue', 'surface', 'names']
            lkok = set(self._dshort[ids].keys())
            lkok = lkok.union(self._dcomp[ids].keys())
            lk = list(set(lk).intersection(lkok))
            dgeom, Etendues, Surfaces, names = self._to_Cam_Du(ids, lk, indch,
                                                               nan=nan,
                                                               pos=pos)

            if names is not None:
                dchans['names'] = names

        import tofu.geom as tfg
        cam = getattr(tfg, geom)(dgeom=dgeom, config=config,
                                 Etendues=Etendues, Surfaces=Surfaces,
                                 Name=Name, Diag=ids, Exp=Exp,
                                 dchans=dchans)
        cam.Id.set_dUSR( {'imas-nchMax': nchMax} )

        if plot:
            cam.plot_touch(draw=True)
        return cam


    def _checkformat_Data_dsig(self, ids=None, dsig=None, data=None, X=None,
                               datacls=None, geomcls=None):

        # Check ids
        idsok = set(self._lidsdiag).intersection(self._dids.keys())
        if ids is None and len(idsok) == 1:
            ids = next(iter(idsok))

        if ids not in self._dids.keys():
            msg = "Provided ids should be available as a self.dids.keys() !"
            raise Exception(msg)

        if ids not in self._lidsdiag:
            msg = "Requested ids is not pre-tabulated !\n"
            msg = "  => Be careful with args (dsig, datacls, geomcls)"
            warnings.warn(msg)
        else:
            if datacls is None:
                datacls = self._didsdiag[ids]['datacls']
            if geomcls is None:
                geomcls = self._didsdiag[ids]['geomcls']
            if dsig is None:
                dsig = self._didsdiag[ids]['sig']
        if data is not None:
            assert type(data) is str
            dsig['data'] = data
        if X is not None:
            assert type(X) is str
            dsig['X'] = X

        # Check data and geom
        import tofu.geom as tfg
        import tofu.data as tfd

        if datacls is None:
            datacls = 'DataCam1D'
        ldata = [kk for kk in dir(tfd) if 'DataCam' in kk]
        if not datacls in ldata:
            msg = "Arg datacls must be in %s"%str(ldata)
            raise Exception(msg)
        lgeom = [kk for kk in dir(tfg) if 'Cam' in kk]
        if geomcls not in [False] + lgeom:
            msg = "Arg geom must be in %s"%str([False]+lgeom)
            raise Exception(msg)

        # Check signals
        c0 = type(dsig) is dict
        c0 = c0 and 'data' in dsig.keys()
        ls = ['t','X','lamb','data']
        c0 = c0 and all([ss in ls for ss in dsig.keys()])
        if not c0:
            msg = "Arg dsig must be a dict with keys:\n"
            msg += "    - 'data' : shortcut to the main data to be loaded\n"
            msg += "    - 't':       (optional) shortcut to time vector\n"
            msg += "    - 'X':       (optional) shortcut to abscissa vector\n"
            msg += "    - 'lamb':    (optional) shortcut to wavelengths\n"
            raise Exception(msg)

        dout = {}
        lok = set(self._dshort[ids].keys()).union(self._dcomp[ids].keys())
        for k, v in dsig.items():
            if v in lok:
                dout[k] = v

        return datacls, geomcls, dout



    def to_Data(self, ids=None, dsig=None, data=None, X=None, tlim=None,
                indch=None, indch_auto=False, Name=None, occ=None,
                config=None, description_2d=None,
                dextra=None, t0=None, datacls=None, geomcls=None,
                plot=True, bck=True, fallback_X=None, nan=True, pos=None,
                return_indch=False):
        """ Export the content of a diagnostic ids as a tofu DataCam1D instance

        Some ids contain the geometry and data of a diagnostics
        They typically have a 'channels' field
        They include for example ids:
            - interferometer
            - polarimeter
            - bolometer
            - soft_x_rays
            - bremsstrahlung_visible
            - spectrometer_visible
            - reflectometer_profile
            - ece
            - magnetics
            - barometry
            - neutron_diagnostics

        tofu offers a class for handling data: DataCam1D
        If available, this method also loads the geometry using self.to_Cam()
        on the same ids.
        But it will load the data even if no geometry (LOS) is available.
        This method extracts the data of the desired diagnostic (ids) and
        exports it as a DataCam1D instance.

        Parameters
        ----------
        ids:   None / str
            Specify the ids (will be checked against known diagnostics ids)
            Should have a 'channels' field
            If None and a unique diagnostic ids has been added, set to this one
        Name:   None / str
            Name to be given to the instance
            If None, a default Name is built
        occ:    None / int
            occurence to be used for loading the data
        indch:  None / list / array
            If provided, array of int indices specifying which channels shall
            be loaded (fed to self.get_data())
        indch_auto: bool
            If True and indch is not provided, will try to guess which channels
            can be loaded. If possible all channels are loaded by default, but
            only if they have uniform data (same shape, i.e.: same time
            vectors). In case of channels with non-uniform data, will try to
            identify a sub-group of channels with uniform data
        dsig:   None / dict
            Specify exactly which data (shortcut) should be loaded by ids
            If None, loads all available data
        data:   None / str
            If dsig is not provided, specify the shortcut of the data to be
            loaded (from channels)
        X:      None / str
            If dsig is not provided, specify the shortcut of the data to be
            used as abscissa
        tlim:   None / list
            Restrict the loaded data to a time interval with tlim
            if None, loads all time steps
        config: None / Config
            Configuration (i.e.: tokamak geometry) to be used for the instance
            If None, created from the wall ids with self.to_Config().
        description_2d: None / int
            description_2d index to be used if the Config is to be built from
            wall ids. See self.to_Config()
        dextra:     None / dict
            dict of extra signals (time traces) to be plotted, for context
        t0:     None / float / str
            Specify a time to be used as origin:
                - None: absolute time vectors are untouched
                - float : the roigin of all time vectors is set to t0
                - str : the origin is taken from an event in ids pulse_schedule
        datacls:    None / str
            tofu calss to be used for the data
                - None : determined from tabulated info (self._didsdiag[ids])
                - str  : should be a valid data class name from tofu.data
        geomcls:    None / False / str
            tofu class to be used for the geometry
                - False: geometry not loaded
                - None : determined from tabulated info (self._didsdiag[ids])
                - str  : should be a valid camera class name from tofu.geom
        fallback_X: None / float
            fallback value for X when X is nan
                X[np.isnan(X)] = fallback_X
            If None, set to 1.1*np.nanmax(X)

        return_indch:   bool
            Flag indicating whether to return also the indch
            Useful if indch was determined automatically by indch_auto
        plot:       None / bool
            Flag whether to plot the result
        bck:        bool
            Flag indicating whether to plot the grey envelop of the signal as a
            background, if plot is True

        Args nan and pos are fed to self.get_data()

        Return
        ------
        data:   DataCam1D
            DataCam1D instance
        indch:  np.ndarray
            int array of indices of the loaded channels, returned only if
            return_indch = True
        """

        # Check ids
        idsok = set(self._lidsdiag).intersection(self._dids.keys())
        if ids is None and len(idsok) == 1:
            ids = next(iter(idsok))

        # dsig
        datacls, geomcls, dsig = self._checkformat_Data_dsig(ids, dsig,
                                                             data=data, X=X,
                                                             datacls=datacls,
                                                             geomcls=geomcls)
        if Name is None:
            Name = 'custom'

        # ---------------------------
        # Preliminary checks on data source consistency
        _, _, shot, Exp = self._get_lidsidd_shotExp([ids], upper=True,
                                                    errshot=False,
                                                    errExp=False)
        # -------------
        #   Input dicts

        # config
        if config is None:
            config = self.to_Config(Name=Name, occ=occ,
                                    description_2d=description_2d, plot=False)

        # dchans
        if indch is not None:
            dchans = {'ind':indch}
        else:
            dchans = None

        # -----------
        # Get geom
        cam = None
        indchanstr = self._dshort[ids][dsig['data']]['str'].index('[chan]')
        chanstr = self._dshort[ids][dsig['data']]['str'][:indchanstr]
        nchMax = len(getattr(self._dids[ids]['ids'][0], chanstr))

        # Check channel indices
        indchr = self.inspect_channels(ids, indch=indch,
                                       geom=(geomcls is not False),
                                       return_ind=True,
                                       verb=False)
        indch = self._compare_indch_indchr(indch, indchr, nchMax,
                                           indch_auto=indch_auto)

        dgeom, names = None, None
        if geomcls is not False:
            Etendues, Surfaces = None, None
            if config is None:
                msg = "A config must be provided to compute the geometry !"
                raise Exception(msg)

            if 'LOS' in geomcls:
                lk_geom = ['los_ptsRZPhi', 'etendue', 'surface']
                lkok = set(self._dshort[ids].keys())
                lkok = lkok.union(self._dcomp[ids].keys())
                lk_geom = list(set(lk_geom).intersection(lkok))
                dgeom, Etendues, Surfaces, names = self._to_Cam_Du(
                    ids, lk_geom, indch, nan=nan, pos=pos)

        # ----------
        # Get time
        lk = sorted(dsig.keys())
        dins = dict.fromkeys(lk)
        t = self.get_data(ids, sig=dsig.get('t', 't'), indch=indch)['t']
        if len(t) == 0:
            msg = "The time vector is not available for %s:\n"%ids
            msg += "    - 't' <=> %s.%s\n"%(ids,self._dshort[ids]['t']['str'])
            msg += "    - 't' = %s"%str(t)
            raise Exception(msg)

        # ----------
        # Get data
        out = self.get_data(ids, sig=dsig['data'],
                            indch=indch, nan=nan, pos=pos)
        if len(out[dsig['data']]) == 0:
            msgstr = self._dshort[ids]['data']['str']
            msg = ("The data array is not available for {}:\n".format(ids)
                   + "    - 'data' <=> {}.{}\n".format(ids, msgstr)
                   + "    - 'data' = {}".format(out[dsig['data']]))
            raise Exception(msg)

        if names is not None:
            dchans['names'] = names

        if t.ndim == 2:
            assert np.all(np.isclose(t, t[0:1, :]))
            t = t[0, :]
        dins['t'] = t
        indt = self._checkformat_tlim(t, tlim=tlim)['indt']

        # -----------
        # Get data
        out = self.get_data(ids, sig=[dsig[k] for k in lk],
                            indt=indt, indch=indch, nan=nan, pos=pos)
        for kk in set(lk).difference('t'):
            # Arrange depending on shape and field
            if type(out[dsig[kk]]) is not np.ndarray:
                msg = "BEWARE : non-conform data !"
                raise Exception(msg)

            if out[dsig[kk]].size == 0 or out[dsig[kk]].ndim not in [1, 2, 3]:
                msg = ("\nSome data seem to have inconsistent shape:\n"
                       + "\t- out[{}].shape = {}".format(dsig[kk],
                                                         out[dsig[kk]].shape))
                raise Exception(msg)

            if out[dsig[kk]].ndim == 1:
                out[dsig[kk]] = np.atleast_2d(out[dsig[kk]])

            if out[dsig[kk]].ndim == 2:
                if dsig[kk] in ['X','lamb']:
                    if np.allclose(out[dsig[kk]], out[dsig[kk]][:,0:1]):
                        dins[kk] = out[dsig[kk]][:,0]
                    else:
                        dins[kk] = out[dsig[kk]]
                else:
                    dins[kk] = out[dsig[kk]].T

            elif out[dsig[kk]].ndim == 3:
                assert kk == 'data'
                dins[kk] = np.swapaxes(out[dsig[kk]].T, 1,2)

        # --------------------------
        # Format special ids cases
        if ids == 'reflectometer_profile':
            dins['X'] = np.fliplr(dins['X'])
            dins['data'] = np.fliplr(dins['data'])

        if 'validity_timed' in self._dshort[ids].keys():
            inan = self.get_data(ids, sig='validity_timed',
                                 indt=indt, indch=indch,
                                 nan=nan, pos=pos)['validity_timed'].T < 0.
            dins['data'][inan] = np.nan
        if 'X' in dins.keys() and np.any(np.isnan(dins['X'])):
            if fallback_X is None:
                fallback_X = 1.1*np.nanmax(dins['X'])
            dins['X'][np.isnan(dins['X'])] = fallback_X

        # Apply indt if was not done in get_data
        for kk,vv in dins.items():
            if (vv.ndim == 2 or kk == 't') and vv.shape[0] > indt.size:
                dins[kk] = vv[indt,...]

        # dlabels
        dins['dlabels'] = dict.fromkeys(lk)
        for kk in lk:
            dins['dlabels'][kk] = {'name':dsig[kk]}
            if dsig[kk] in self._dshort[ids].keys():
                dins['dlabels'][kk]['units'] = self._dshort[ids][dsig[kk]].get('units', 'a.u.')
            else:
                dins['dlabels'][kk]['units'] = self._dcomp[ids][dsig[kk]].get('units', 'a.u.')

        # dextra
        dextra = self._get_dextra(dextra, fordata=True)

        # t0
        t0 = self._get_t0(t0)
        if t0 != False:
            if 't' in dins.keys():
                dins['t'] = dins['t'] - t0
            if dextra is not None:
                for tt in dextra.keys():
                    dextra[tt]['t'] = dextra[tt]['t'] - t0

        # --------------
        # Create objects
        if geomcls is not False and dgeom is not None:
            import tofu.geom as tfg
            cam = getattr(tfg, geomcls)(dgeom=dgeom, config=config,
                                        Etendues=Etendues, Surfaces=Surfaces,
                                        Name=Name, Diag=ids, Exp=Exp,
                                        dchans=dchans)
            cam.Id.set_dUSR({'imas-nchMax': nchMax})

        import tofu.data as tfd
        conf = None if cam is not None else config
        Data = getattr(tfd, datacls)(Name=Name, Diag=ids, Exp=Exp, shot=shot,
                                     lCam=cam, config=conf, dextra=dextra,
                                     dchans=dchans, **dins)
        Data.Id.set_dUSR( {'imas-nchMax': nchMax} )

        if plot:
            Data.plot(draw=True, bck=bck)
        if return_indch is True:
            return Data, indch
        else:
            return Data


    def _get_synth(self, ids, dsig=None,
                   quant=None, ref1d=None, ref2d=None,
                   q2dR=None, q2dPhi=None, q2dZ=None):

        # Check quant, ref1d, ref2d
        dq = {'quant':quant, 'ref1d':ref1d, 'ref2d':ref2d,
              'q2dR':q2dR, 'q2dPhi':q2dPhi, 'q2dZ':q2dZ}
        for kk,vv in dq.items():
            lc = [vv is None, type(vv) is str, type(vv) in [list,tuple]]
            assert any(lc)
            if lc[0]:
                dq[kk] = self._didsdiag[ids]['synth']['dsynth'].get(kk, None)
            if type(dq[kk]) is str:
                dq[kk] = [dq[kk]]
            if dq[kk] is not None:
                for ii in range(0,len(dq[kk])):
                    v1 = tuple(dq[kk][ii].split('.'))
                    assert len(v1) == 2
                    assert v1[0] in self._lidsplasma
                    assert (v1[1] in self._dshort[v1[0]].keys()
                            or v1[1] in self._dcomp[v1[0]].keys())
                    dq[kk][ii] = v1

        # Check dsig
        if dsig is None:
            dsig = self._didsdiag[ids]['synth']['dsig']

        for k0,v0 in dsig.items():
            if type(v0) is not list:
                v0 = [v0]
            c0 = k0 in self._lidsplasma
            c0 = c0 and all([type(vv) is str for vv in v0])
            if not c0:
                msg = "Arg dsig must be a dict (ids:[shortcut1, shortcut2...])"
                raise Exception(msg)
            dsig[k0] = v0

        # Check dsig vs quant/ref1d/ref2d consistency
        for kk,vv in dq.items():
            if vv is None:
                continue
            for ii in range(0,len(vv)):
                if vv[ii][0] not in dsig.keys():
                    dsig[vv[ii][0]] = []
                if vv[ii][1] not in dsig[vv[ii][0]]:
                    dsig[vv[ii][0]].append(vv[ii][1])
                dq[kk][ii] = '%s.%s'%tuple(vv[ii])

        lq = self._didsdiag[ids]['synth']['dsynth'].get('fargs', None)
        if lq is not None:
            for qq in lq:
                q01 = qq.split('.')
                assert len(q01) == 2
                if q01[0] not in dsig.keys():
                    dsig[q01[0]] = [q01[1]]
                else:
                    dsig[q01[0]].append(q01[1])

        if dq['quant'] is None and dq['q2dR'] is None and lq is None:
            msg = "both quant and q2dR are not specified !"
            raise Exception(msg)
        return dsig, dq, lq


    def calc_signal(self, ids=None, dsig=None, tlim=None, t=None, res=None,
                    quant=None, ref1d=None, ref2d=None,
                    q2dR=None, q2dPhi=None, q2dZ=None,
                    Brightness=None, interp_t=None, newcalc=True,
                    indch=None, indch_auto=False, Name=None,
                    occ_cam=None, occ_plasma=None,
                    config=None, description_2d=None,
                    dextra=None, t0=None, datacls=None, geomcls=None,
                    bck=True, fallback_X=None, nan=True, pos=None,
                    plot=True, plot_compare=None, plot_plasma=None):
        """ Compute synthetic data for a diagnostics and export as DataCam1D

        Some ids typically contain plasma 1d (radial) or 2d (mesh) profiles
        They include for example ids:
            - core_profiles
            - core_sources
            - edge_profiles
            - edge_sources
            - equilibrium

        From these profiles, tofu can computed syntheic data for a diagnostic
        ids which provides a geometry (channels.line_of_sight).
        tofu extracts the geometry, and integrates the desired profile along
        the lines of sight (LOS), using 2D interpolation when necessary

        It requires:
            - a diagnostic ids with geometry (LOS)
            - an ids containing the 1d or 2d profile to be integrated
            - if necessary, an intermediate ids to interpolate the 1d profile
            to 2d (e.g.: equilibrium)

        For each ids, you need to specify:
            - profile ids:
                profile (signal) to be integrated
                quantity to be used for 1d interpolation
            - equilibrium / intermediate ids:
                quantity to be used for 2d interpolation
                    (shall be the same dimension as quantity for 1d interp.)

        This method is a combination of self.to_Plasma2D() (used for extracting
        profiles and equilibrium and for interpolation) and self.to_Cam() (used
        for extracting diagnostic geometry) and to_Data() (used for exportig
        computed result as a tofu DataCam1D instance.

        Args ids, dsig, tlim, occ_plasma (occ), nan, pos, plot_plasma (plot)
        are fed to to_Plasma2D()
        Args indch, indch_auto, occ_cam (occ), config, description_2d, are fed
        to to_Cam()
        Args Name, bck, fallback_X, plot, t0, dextra are fed to to_Data()

        Parameters
        ----------
        t:      None / float / np.ndarray
            time at which the synthetic signal shall be computed
            If None, computed for all available time steps
        res:    None / float
            absolute spatial resolution (sampling steps) used for Line-of-Sight
            intergation (in meters)
        quant:  None / str
            Shortcut of the quantity to be integrated
        ref1d:  None / str
            Shortcut of the quantity to be used as reference for 1d
            interpolation
        ref2d:  None / str
            Shortcut of the quantity to be used as reference for 2d
            interpolation
        q2dR:   None / str
            If integrating an anisotropic vector field (e.g. magnetic field)
                q2dR if the shortcut of the R-component of the quantity
        q2dPhi:   None / str
            If integrating an anisotropic vector field (e.g. magnetic field)
                q2dPhi if the shortcut of the Phi-component of the quantity
        q2dR:   None / str
            If integrating an anisotropic vector field (e.g. magnetic field)
                q2dZ if the shortcut of the Z-component of the quantity
        Brightness:     bool
            Flag indicating whether the result shall be returned as a
            Brightness (i.e.: line integral) or an incident flux (Brightness x
            Etendue), which requires the Etendue
        plot_compare:   bool
            Flag indicating whether to plot the experimental data against the
            computed synthetic data
        Return
        ------
        sig:     DataCam1D
            DataCam1D instance

        """

        # Check / format inputs
        if plot is None:
            plot = True

        if plot:
            if plot_compare is None:
                plot_compare = True
            if plot_plasma is None:
                plot_plasma = True

        # Get experimental data first if relevant
        # to get correct indch for comparison
        if plot and plot_compare:
            data, indch = self.to_Data(ids, indch=indch,
                                       indch_auto=indch_auto, t0=t0,
                                       config=config,
                                       description_2d=description_2d,
                                       return_indch=True, plot=False)

        # Get camera
        cam = self.to_Cam(ids=ids, indch=indch, indch_auto=indch_auto,
                          Name=None, occ=occ_cam,
                          config=config, description_2d=description_2d,
                          plot=False, nan=True, pos=None)

        # Get relevant parameters
        dsig, dq, lq = self._get_synth(ids, dsig, quant, ref1d, ref2d,
                                       q2dR, q2dPhi, q2dZ)

        # Get relevant plasma
        plasma = self.to_Plasma2D(tlim=tlim, dsig=dsig, t0=t0,
                                  Name=None, occ=occ_plasma,
                                  config=cam.config, out=object,
                                  plot=False, dextra=dextra, nan=True, pos=None)

        # Intermediate computation if necessary
        ani = False
        if ids == 'bremsstrahlung_visible':
            try:
                lamb = self.get_data(ids, sig='lamb')['lamb']
            except Exception as err:
                lamb = 5238.e-10
                msg = "bremsstrahlung_visible.lamb could not be retrived!\n"
                msg += "  => fallback to lamb = 5338.e-10 m (WEST case)"
                warnings.warn(msg)
            out = plasma.compute_bremzeff(Te='core_profiles.1dTe',
                                          ne='core_profiles.1dne',
                                          zeff='core_profiles.1dzeff',
                                          lamb=lamb)
            quant, _, units = out
            origin = 'f(core_profiles, bremsstrahlung_visible)'
            depend = ('core_profiles.t','core_profiles.1dTe')
            plasma.add_quantity(key='core_profiles.1dbrem', data=quant,
                                depend=depend, origin=origin, units=units,
                                dim=None, quant=None, name=None)
            dq['quant'] = ['core_profiles.1dbrem']

        elif ids == 'polarimeter':
            lamb = self.get_data(ids, sig='lamb')['lamb'][0]

            # Get time reference
            doutt, dtut, tref = plasma.get_time_common(lq)
            if t is None:
                t = tref

            # Add necessary 2dne (and time reference)
            ne2d, tne2d = plasma.interp_pts2profile(quant='core_profiles.1dne',
                                                    ref1d='core_profiles.1drhotn',
                                                    ref2d='equilibrium.2drhotn',
                                                    t=t, interp_t='nearest')
            # Add fanglev
            out = plasma.compute_fanglev(BR='equilibrium.2dBR',
                                         BPhi='equilibrium.2dBT',
                                         BZ='equilibrium.2dBZ',
                                         ne=ne2d, tne=tne2d, lamb=lamb)
            fangleRPZ, tfang, units = out

            plasma.add_ref(key='tfangleRPZ', data=tfang, group='time')

            origin = 'f(equilibrium, core_profiles, polarimeter)'
            depend = ('tfangleRPZ','equilibrium.mesh')

            plasma.add_quantity(key='2dfangleR', data=fangleRPZ[0,...],
                                depend=depend, origin=origin, units=units,
                                dim=None, quant=None, name=None)
            plasma.add_quantity(key='2dfanglePhi', data=fangleRPZ[1,...],
                                depend=depend, origin=origin, units=units,
                                dim=None, quant=None, name=None)
            plasma.add_quantity(key='2dfangleZ', data=fangleRPZ[2,...],
                                depend=depend, origin=origin, units=units,
                                dim=None, quant=None, name=None)

            dq['q2dR'] = ['2dfangleR']
            dq['q2dPhi'] = ['2dfanglePhi']
            dq['q2dZ'] = ['2dfangleZ']
            dq['Type'] = ['sca']
            ani = True

        for kk,vv in dq.items():
            c0 = [vv is None,
                  type(vv) is list and len(vv) == 1 and type(vv[0]) is str]
            if not any(c0):
                msg = "All in dq must be None or list of 1 string !\n"
                msg += "    - Provided: dq[%s] = %s"%(kk,str(vv))
                raise Exception(msg)
            if vv is not None:
                dq[kk] = vv[0]

        # Calculate synthetic signal
        if Brightness is None:
            Brightness = self._didsdiag[ids]['synth'].get('Brightness', None)
        dq['fill_value'] = 0.
        sig, units = cam.calc_signal_from_Plasma2D(plasma, res=res, t=t,
                                                   Brightness=Brightness,
                                                   newcalc=newcalc,
                                                   plot=False, **dq)

        sig._dextra = plasma.get_dextra(dextra)

        if ids == 'interferometer':
            sig = 2.*sig
        elif ids == 'polarimeter':
            # For polarimeter, the vect is along the LOS
            # it is not the direction of
            sig = -2.*sig

        # Safety check regarding Brightness
        _, _, dsig_exp = self._checkformat_Data_dsig(ids)
        kdata = dsig_exp['data']
        B_exp = self._dshort[ids][kdata].get('Brightness', None)
        err_comp = False
        if Brightness != B_exp:
            u_exp = self._dshort[ids][kdata].get('units')
            msg = ("\nCalculated synthetic and chosen experimental data "
                   + "do not seem directly comparable !\n"
                   + "\t- chosen experimental data: "
                   + "{}, ({}), Brightness = {}\n".format(kdata,
                                                          u_exp, B_exp)
                   + "\t- calculated synthetic data: "
                   + "int({}), ({}), Brightness = {}\n".format(dq['quant'],
                                                               units,
                                                               Brightness)
                   + "\n  => Consider changing data or Brigthness value")
            err_comp = True
            warnings.warn(msg)

        # plot
        if plot:
            if plot_compare:
                if err_comp:
                    raise Exception(msg)
                sig._dlabels = data.dlabels
                data.plot_compare(sig)
            else:
                sig.plot()
            if plot_plasma and dq['quant'] is not None and '1d' in dq['quant']:
                plasma.plot(dq['quant'], X=dq['ref1d'])
        return sig






#############################################################
#############################################################
#           Function-oriented interfaces to IdsMultiLoader
#############################################################


def load_Config(shot=None, run=None, user=None, tokamak=None, version=None,
                Name=None, occ=0, description_2d=None, plot=True):

    didd = MultiIDSLoader()
    didd.add_idd(shot=shot, run=run,
                 user=user, tokamak=tokamak, version=version)
    didd.add_ids('wall', get=True)

    return didd.to_Config(Name=Name, occ=occ,
                          description_2d=description_2d, plot=plot)


# occ ?
def load_Plasma2D(shot=None, run=None, user=None, tokamak=None, version=None,
                  tlim=None, occ=None, dsig=None, ids=None,
                  config=None, description_2d=None,
                  Name=None, t0=None, out=object, dextra=None,
                  plot=None, plot_sig=None, plot_X=None, bck=True):

    didd = MultiIDSLoader()
    didd.add_idd(shot=shot, run=run,
                 user=user, tokamak=tokamak, version=version)

    if dsig is dict:
        lids = sorted(dsig.keys())
    else:
        if type(ids) not in [str,list]:
            msg = "If dsig not provided => provide an ids to load Plasma2D!\n"
            msg += "  => Available ids for Plasma2D include:\n"
            msg += "     ['equilibrium',\n"
            msg += "      'core_profiles', 'core_sources'\n,"
            msg += "      'edge_profiles', edge_sources]"
            raise Exception(msg)
        lids = [ids] if type(ids) is str else ids
    lids.append('wall')
    if t0 != False and t0 != None:
        lids.append('pulse_schedule')

    didd.add_ids(ids=lids, get=True)

    return didd.to_Plasma2D(Name=Name, tlim=tlim, dsig=dsig, t0=t0,
                            occ=occ, config=config,
                            description_2d=description_2d, out=out,
                            plot=plot, plot_sig=plot_sig, plot_X=plot_X,
                            bck=bcki, dextra=dextra)


def load_Cam(shot=None, run=None, user=None, tokamak=None, version=None,
             ids=None, indch=None, config=None, description_2d=None,
             occ=None, Name=None, plot=True):

    didd = MultiIDSLoader()
    didd.add_idd(shot=shot, run=run,
                 user=user, tokamak=tokamak, version=version)

    if type(ids) is not str:
        msg = "Please provide ids to load Cam !\n"
        msg += "  => Which diagnostic do you wish to load ?"
        raise Exception(msg)

    lids = ['wall',ids]
    didd.add_ids(ids=lids, get=True)

    return didd.to_Cam(ids=ids, Name=Name, indch=indch,
                       config=config, description_2d=description_2d,
                       occ=occ, plot=plot)


def load_Data(shot=None, run=None, user=None, tokamak=None, version=None,
              ids=None, datacls=None, geomcls=None, indch_auto=True,
              tlim=None, dsig=None, data=None, X=None, indch=None,
              config=None, description_2d=None,
              occ=None, Name=None, dextra=None,
              t0=None, plot=True, bck=True):

    didd = MultiIDSLoader()
    didd.add_idd(shot=shot, run=run,
                 user=user, tokamak=tokamak, version=version)

    if type(ids) is not str:
        msg = "Please provide ids to load Data !\n"
        msg += "  => Which diagnostic do you wish to load ?"
        raise Exception(msg)

    lids = ['wall',ids]
    if dextra is None and plot:
        lids.append('equilibrium')
    if t0 != False and t0 != None:
        lids.append('pulse_schedule')

    didd.add_ids(ids=lids, get=True)

    return didd.to_Data(ids=ids, Name=Name, tlim=tlim, t0=t0,
                        datacls=datacls, geomcls=geomcls,
                        dsig=dsig, data=data, X=X, indch=indch,
                        config=config, description_2d=description_2d,
                        occ=occ, dextra=dextra,
                        plot=plot, bck=bck, indch_auto=indch_auto)


#############################################################
#############################################################
#           save_to_imas object-specific functions
#############################################################


#--------------------------------
#   Generic functions
#--------------------------------

def _open_create_idd(shot=None, run=None, refshot=None, refrun=None,
                     user=None, tokamak=None, version=None, verb=True):

    # Check idd inputs and get default values
    didd = dict(shot=shot, run=run, refshot=refshot, refrun=refrun,
                user=user, tokamak=tokamak, version=version)
    for k, v in didd.items():
        if v is None:
            didd[k] = _IMAS_DIDD[k]
    didd['shot'] = int(didd['shot'])
    didd['run'] = int(didd['run'])
    assert all([type(didd[ss]) is str for ss in ['user','tokamak','version']])

    # Check existence of database
    path = os.path.join('~', 'public', 'imasdb', didd['tokamak'], '3', '0')
    path = os.path.realpath(os.path.expanduser(path))

    if not os.path.exists(path):
        msg = "IMAS: The required imas ddatabase does not seem to exist:\n"
        msg += "         - looking for : %s\n"%path
        if user == getpass.getuser():
            msg += "       => Maybe run imasdb %s (in shell) ?"%tokamak
        raise Exception(msg)

    # Check existence of file
    filen = 'ids_{0}{1:04d}.datafile'.format(didd['shot'], didd['run'])
    shot_file = os.path.join(path, filen)

    idd = imas.ids(didd['shot'], didd['run'])
    if os.path.isfile(shot_file):
        if verb:
            msg = "IMAS: opening shotfile %s"%shot_file
            print(msg)
        idd.open_env(didd['user'], didd['tokamak'], didd['version'])
    else:
        if user == _IMAS_USER_PUBLIC:
            msg = "IMAS: required shotfile does not exist\n"
            msg += "      Shotfiles with user=%s are public\n"%didd['user']
            msg += "      They have to be created centrally\n"
            msg += "       - required shotfile: %s"%shot_file
            raise Exception(msg)
        else:
            if verb:
                msg = "IMAS: creating shotfile %s"%shot_file
                print(msg)
            idd.create_env(didd['user'], didd['tokamak'], didd['version'])

    return idd, shot_file

def _except_ids(ids, nt=None):
    traceback.print_exc(file=sys.stdout)
    if len(ids.time) > 0:
        if nt is None:
            ids.code.output_flag = -1
        else:
            ids.code.output_flag = -np.ones((nt,))
    else:
        ids.code.output_flag.resize(1)
        ids.code.output_flag[0] = -1


def _fill_idsproperties(ids, com, tfversion, nt=None):
    ids.ids_properties.comment = com
    ids.ids_properties.homogeneous_time = 1
    ids.ids_properties.provider = getpass.getuser()
    ids.ids_properties.creation_date = \
                      dtm.datetime.today().strftime('%Y%m%d%H%M%S')

    # Code
    # --------
    ids.code.name = "tofu"
    ids.code.repository = _ROOT
    ids.code.version = tfversion
    if nt is None:
        nt = 1
    ids.code.output_flag = np.zeros((nt,),dtype=int)
    ids.code.parameters = ""

def _put_ids(idd, ids, shotfile, occ=0, cls_name=None,
             err=None, dryrun=False, close=True, verb=True):
    idsn = ids.__class__.__name__
    if not dryrun and err is None:
        try:
            ids.put( occ )
        except Exception as err:
            msg = str(err)
            msg += "\n  There was a pb. when putting the ids:\n"
            msg += "    - shotfile: %s\n"%shotfile
            msg += "    - ids: %s\n"%idsn
            msg += "    - occ: %s\n"%str(occ)
            raise Exception(msg)
        finally:
            # Close idd
            if close:
                idd.close()

    # print info
    if verb:
        if err is not None:
            raise err
        else:
            if cls_name is None:
                cls_name = ''
            if dryrun:
                msg = "  => %s (not put) in %s in %s"%(cls_name,idsn,shotfile)
            else:
                msg = "  => %s put in %s in %s"%(cls_name,idsn,shotfile)
        print(msg)



def _save_to_imas(obj, shot=None, run=None, refshot=None, refrun=None,
                  occ=None, user=None, tokamak=None, version=None,
                  dryrun=False, tfversion=None, verb=True, **kwdargs):

    dfunc = {'Struct': _save_to_imas_Struct,
             'Config': _save_to_imas_Config,
             'CamLOS1D': _save_to_imas_CamLOS1D,
             'DataCam1D': _save_to_imas_DataCam1D}


    # Preliminary check on object class
    cls = obj.__class__
    if cls not in dfunc.keys():
        parents = [cc.__name__ for cc in inspect.getmro(cls)]
        lc = [k for k,v in dfunc.items() if k in parents]
        if len(lc) != 1:
            msg = "save_to_imas() not implemented for class %s !\n"%cls.__name__
            msg += "Only available for classes and subclasses of:\n"
            msg += "    - " + "\n    - ".join(dfunc.keys())
            msg += "\n  => None / too many were found in parent classes:\n"
            msg += "    %s"%str(parents)
            raise Exception(msg)
        cls = lc[0]

    # Try getting imas info from tofu object
    if shot is None:
        try:
            shot = obj.Id.shot
        except Exception:
            msg = "Arg shot must be provided !\n"
            msg += "  (could not be retrieved from self.Id.shot)"
            raise Exception(msg)
    if tokamak is None:
        try:
            tokamak = obj.Id.Exp.lower()
        except Exception:
            msg = "Arg tokamak must be provided !\n"
            msg += "  (could not be retrieved from self.Id.Exp.lower())"
            raise Exception(msg)
    if cls in ['CamLOS1D', 'DataCam1D'] and kwdargs.get('ids',None) is None:
        try:
            kwdargs['ids'] = obj.Id.Diag.lower()
        except Exception:
            msg = "Arg ids must be provided !\n"
            msg += "  (could not be retrieved from self.Id.Diag.lower())"
            raise Exception(msg)

    # Call relevant function
    out = dfunc[cls]( obj, shot=shot, run=run, refshot=refshot,
                     refrun=refrun, occ=occ, user=user, tokamak=tokamak,
                     version=version, dryrun=dryrun, tfversion=tfversion,
                     verb=verb, **kwdargs)
    return out


#--------------------------------
#   Class-specific functions
#--------------------------------

def _save_to_imas_Struct(obj,
                         shot=None, run=None, refshot=None, refrun=None,
                         occ=None, user=None, tokamak=None, version=None,
                         dryrun=False, tfversion=None, verb=True,
                         description_2d=None, description_typeindex=None,
                         unit=None, mobile=None):

    if occ is None:
        occ = 0
    if description_2d is None:
        description_2d = 0
    if description_typeindex is None:
        description_typeindex = 2
    description_typeindex = int(description_typeindex)
    if unit is None:
        unit = 0
    if mobile is None:
        mobile = False

    # Create or open IDS
    # ------------------
    idd, shotfile = _open_create_idd(shot=shot, run=run,
                                     refshot=refshot, refrun=refrun,
                                     user=user, tokamak=tokamak, version=version,
                                     verb=verb)

    # Fill in data
    # ------------------
    try:
        # data
        # --------
        idd.wall.description_2d.resize( description_2d + 1 )
        idd.wall.description_2d[description_2d].type.index = (
            description_typeindex)
        idd.wall.description_2d[description_2d].type.name = (
            '{}_{}'.format(obj.__class__.__name__, obj.Id.Name))
        idd.wall.description_2d[description_2d].type.description = (
            "tofu-generated wall. Each PFC is represented independently as a"
            + " closed polygon in tofu, which saves them as disjoint PFCs")
        if mobile is True:
            idd.wall.description_2d[description_2d].mobile.unit.resize(unit+1)
            node = idd.wall.description_2d[description_2d].mobile.unit[unit]
        else:
            idd.wall.description_2d[description_2d].limiter.unit.resize(unit+1)
            node = idd.wall.description_2d[description_2d].limiter.unit[unit]
        node.outline.r = obj._dgeom['Poly'][0,:]
        node.outline.z = obj._dgeom['Poly'][1,:]
        if obj.noccur > 0:
            node.phi_extensions = np.array([obj.pos, obj.extent]).T
        node.closed = True
        node.name = '%s_%s'%(obj.__class__.__name__, obj.Id.Name)


        # IDS properties
        # --------------
        com = "PFC contour generated:\n"
        com += "    - from %s"%obj.Id.SaveName
        com += "    - by tofu %s"%tfversion
        _fill_idsproperties(idd.wall, com, tfversion)
        err0 = None

    except Exception as err:
        _except_ids(idd.wall, nt=None)
        err0 = err

    finally:

        # Put IDS
        # ------------------
        _put_ids(idd, idd.wall, shotfile, 'wall', occ=occ,
                 cls_name='%s_%s'%(obj.Id.Cls,obj.Id.Name),
                 err=err0, dryrun=dryrun, verb=verb)


def _save_to_imas_Config(obj, idd=None, shotfile=None,
                         shot=None, run=None, refshot=None, refrun=None,
                         occ=None, user=None, tokamak=None, version=None,
                         dryrun=False, tfversion=None, close=True, verb=True,
                         description_2d=None, description_typeindex=None,
                         mobile=None):

    if occ is None:
        occ = 0
    if description_2d is None:
        description_2d = 0
    if mobile is None:
        mobile = False

    # Create or open IDS
    # ------------------
    if idd is None:
        idd, shotfile = _open_create_idd(shot=shot, run=run,
                                         refshot=refshot, refrun=refrun,
                                         user=user, tokamak=tokamak, version=version,
                                         verb=verb)
    assert type(shotfile) is str


    # Choose description_2d from config
    lS = obj.lStruct
    lcls = [ss.__class__.__name__ for ss in lS]
    lclsIn = [cc for cc in lcls if cc in ['Ves','PlasmaDomain']]
    nS = len(lS)

    if len(lclsIn) != 1:
        msg = "One (and only one) StructIn subclass is allowed / necessary !"
        raise Exception(msg)

    if description_typeindex is None:
        if nS == 1 and lcls[0] in ['Ves', 'PlasmaDomain']:
            description_typeindex = 0
        else:
            description_typeindex = 1
    assert description_typeindex in [0, 1]

    # Isolate StructIn and take out from lS
    ves = lS.pop(lcls.index(lclsIn[0]))
    nS = len(lS)

    # Fill in data
    # ------------------
    try:
        # data
        # --------
        idd.wall.description_2d.resize( description_2d + 1 )
        wall = idd.wall.description_2d[description_2d]
        wall.type.name = obj.Id.Name
        wall.type.index = description_typeindex
        wall.type.description = (
            "tofu-generated wall. Each PFC is represented independently as a"
            + " closed polygon in tofu, which saves them as disjoint PFCs")

        # Fill limiter / mobile
        if mobile is True:
            # resize nS + 1 for vessel
            wall.mobile.unit.resize(nS + 1)
            units = wall.mobile.unit
            for ii in range(0, nS):
                units[ii].outline.resize(1)
                units[ii].outline[0].r = lS[ii].Poly[0, :]
                units[ii].outline[0].z = lS[ii].Poly[1, :]
                if lS[ii].noccur > 0:
                    units[ii].phi_extensions = np.array([lS[ii].pos,
                                                         lS[ii].extent]).T
                units[ii].closed = True
                name = '{}_{}'.format(lS[ii].__class__.__name__,
                                      lS[ii].Id.Name)
                if lS[ii]._dgeom['move'] is not None:
                    name = name + '_mobile'
                units[ii].name = name

        else:
            # resize nS + 1 for vessel
            wall.limiter.unit.resize(nS + 1)
            units = wall.limiter.unit
            for ii in range(0, nS):
                units[ii].outline.r = lS[ii].Poly[0, :]
                units[ii].outline.z = lS[ii].Poly[1, :]
                if lS[ii].noccur > 0:
                    units[ii].phi_extensions = np.array([lS[ii].pos,
                                                         lS[ii].extent]).T
                units[ii].closed = True
                name = '{}_{}'.format(lS[ii].__class__.__name__,
                                      lS[ii].Id.Name)
                if lS[ii]._dgeom['move'] is not None:
                    name = name + '_mobile'
                units[ii].name = name

        # Add Vessel at the end
        ii = nS
        if ismobile:
            units[ii].outline.resize(1)
            units[ii].outline[0].r = ves.Poly[0, :]
            units[ii].outline[0].z = ves.Poly[1, :]
        else:
            units[ii].outline.r = ves.Poly[0, :]
            units[ii].outline.z = ves.Poly[1, :]
        units[ii].closed = True
        units[ii].name = '{}_{}'.format(ves.__class__.__name__,
                                        ves.Id.Name)

        # ----------------------------------
        # Fill vessel if needed
        # vesname = '{}_{}'.format(ves.__class__.__name__, ves.Id.Name)
        # wall.vessel.name = vesname
        # wall.vessel.index = 1
        # wall.vessel.description = (
        #     "tofu-generated vessel outline, with a unique unit / element")

        # wall.vessel.unit.resize(1)
        # wall.vessel.unit[0].element.resize(1)
        # element = wall.vessel.unit[0].element[0]
        # element.name = vesname
        # element.outline.r = ves.Poly[0, :]
        # element.outline.z = ves.Poly[1, :]
        # ----------------------------------

        # IDS properties
        # --------------
        com = "PFC contour generated:\n"
        com += "    - from {}".format(obj.Id.SaveName)
        com += "    - by tofu {}".format(tfversion)
        _fill_idsproperties(idd.wall, com, tfversion)
        err0 = None

    except Exception as err:
        _except_ids(idd.wall, nt=None)
        err0 = err

    finally:

        # Put IDS
        # ------------------
        _put_ids(idd, idd.wall, shotfile, occ=occ, err=err0, dryrun=dryrun,
                 cls_name='%s_%s'%(obj.Id.Cls,obj.Id.Name),
                 close=close, verb=verb)


def _save_to_imas_CamLOS1D( obj, idd=None, shotfile=None,
                           shot=None, run=None, refshot=None, refrun=None,
                           occ=None, user=None, tokamak=None, version=None,
                           dryrun=False, tfversion=None, close=True, verb=True,
                           ids=None, deep=True, restore_size=False,
                           config_occ=None, config_description_2d=None):

    if occ is None:
        occ = 0
    # Create or open IDS
    # ------------------
    if idd is None:
        idd, shotfile = _open_create_idd(shot=shot, run=run,
                                         refshot=refshot, refrun=refrun,
                                         user=user, tokamak=tokamak, version=version,
                                         verb=verb)
    assert type(shotfile) is str

    # Check choice of ids
    c0 = ids in dir(idd)
    c0 = c0 and hasattr(getattr(idd,ids), 'channel')
    if not c0:
        msg = "Please provide a valid value for arg ids:\n"
        msg += "  => ids should be a valid ids name\n"
        msg += "  => it should refer to an ids with tha attribute channeli\n"
        msg += "    - provided: %s"%ids
        raise Exception(msg)

    # First save dependencies
    if deep:
        _save_to_imas_Config(obj.config, idd=idd, shotfile=shotfile,
                             dryrun=dryrun, verb=verb, close=False,
                             occ=config_occ,
                             description_2d=config_description_2d)

    # Choose description_2d from config
    nch = obj.nRays
    assert nch > 0

    # Get first / second points
    D0 = obj.D
    RZP1 = np.array([np.hypot(D0[0,:],D0[1,:]),
                     D0[2,:],
                     np.arctan2(D0[1,:],D0[0,:])])
    D1 = D0 + obj._dgeom['kOut'][None,:]*obj.u
    RZP2 = np.array([np.hypot(D1[0,:],D1[1,:]),
                     D1[2,:],
                     np.arctan2(D1[1,:],D1[0,:])])

    # Get names
    lk = obj._dchans.keys()
    ln = [k for k in lk if k.lower() == 'name']
    if len(ln) == 1:
        ln = obj.dchans(ln[0])
    else:
        ln = ['ch%s'%str(ii) for ii in range(0,nch)]

    # Get indices
    lk = obj._dchans.keys()
    lind = [k for k in lk if k.lower() in ['ind', 'indch','index','indices']]
    if restore_size and len(lind) == 1:
        lind = obj.dchans[lind[0]]
    else:
        lind = np.arange(0,nch)

    # Check if info on nMax stored
    if restore_size and obj.Id.dUSR is not None:
        nchMax = obj.Id.dUSR.get('imas-nchMax', lind.max()+1)
    else:
        nchMax = lind.max()+1

    # Fill in data
    # ------------------
    try:
        # data
        # --------
        ids = getattr(idd,ids)
        ids.channel.resize( nchMax )
        for ii in range(0,lind.size):
            ids.channel[lind[ii]].line_of_sight.first_point.r = RZP1[0,ii]
            ids.channel[lind[ii]].line_of_sight.first_point.z = RZP1[1,ii]
            ids.channel[lind[ii]].line_of_sight.first_point.phi = RZP1[2,ii]
            ids.channel[lind[ii]].line_of_sight.second_point.r = RZP2[0,ii]
            ids.channel[lind[ii]].line_of_sight.second_point.z = RZP2[1,ii]
            ids.channel[lind[ii]].line_of_sight.second_point.phi = RZP2[2,ii]
            if obj.Etendues is not None:
                ids.channel[lind[ii]].etendue = obj.Etendues[ii]
            if obj.Surfaces is not None:
                ids.channel[lind[ii]].detector.surface = obj.Surfaces[ii]
            ids.channel[lind[ii]].name = ln[ii]


        # IDS properties
        # --------------
        com = "LOS-approximated camera generated:\n"
        com += "    - from %s"%obj.Id.SaveName
        com += "    - by tofu %s"%tfversion
        _fill_idsproperties(ids, com, tfversion)
        err0 = None

    except Exception as err:
        _except_ids(ids, nt=None)
        err0 = err

    finally:
        # Put IDS
        # ------------------
        _put_ids(idd, ids, shotfile, occ=occ,
                 cls_name='%s_%s'%(obj.Id.Cls,obj.Id.Name),
                 err=err0, dryrun=dryrun, close=close, verb=verb)


def _save_to_imas_DataCam1D( obj,
                            shot=None, run=None, refshot=None, refrun=None,
                            occ=None, user=None, tokamak=None, version=None,
                            dryrun=False, tfversion=None, verb=True,
                            ids=None, deep=True, restore_size=True, forceupdate=False,
                            path_data=None, path_X=None,
                            config_occ=None, config_description_2d=None):

    if occ is None:
        occ = 0
    # Create or open IDS
    # ------------------
    idd, shotfile = _open_create_idd(shot=shot, run=run,
                                     refshot=refshot, refrun=refrun,
                                     user=user, tokamak=tokamak, version=version,
                                     verb=verb)

    # Check choice of ids
    c0 = ids in dir(idd)
    c0 = c0 and hasattr(getattr(idd,ids), 'channel')
    if not c0:
        msg = "Please provide a valid value for arg ids:\n"
        msg += "  => ids should be a valid ids name\n"
        msg += "  => it should refer to an ids with tha attribute channel"
        raise Exception(msg)

    # Check path_data and path_X
    if not type(path_data) is str:
        msg = "path_data is not valid !\n"
        msg += "path_data must be a (str) valid path to a field in idd.%s"%ids
        raise Exception(msg)
    if not ( path_X is None or type(path_X) is str ):
        msg = "path_X is not valid !\n"
        msg += "path_X must be a (str) valid path to a field in idd.%s"%ids
        raise Exception(msg)

    # First save dependencies
    donersize = False
    if deep:
        if obj.config is not None:
            _save_to_imas_Config(obj.config, idd=idd, shotfile=shotfile,
                                 dryrun=dryrun, verb=verb, close=False,
                                 occ=config_occ,
                                 description_2d=config_description_2d)
        if obj.lCam is not None:
            if not len(obj.lCam) == 1:
                msg = "Geometry can only be saved to imas if unique CamLOS1D !"
                raise Exception(msg)
            _save_to_imas_CamLOS1D(obj.lCam[0], idd=idd, shotfile=shotfile,
                                   ids=ids, restore_size=restore_size,
                                   dryrun=True, verb=verb, close=False,
                                   occ=occ, deep=False)
            doneresize = True

    # Make sure data is up-to-date
    if forceupdate:
        obj._ddata['uptodate'] = False
        obj._set_ddata()

    # Choose description_2d from config
    nch = obj.nch
    assert nch > 0

    # Get names
    lk = obj._dchans.keys()
    ln = [k for k in lk if k.lower() == 'name']
    if len(ln) == 1:
        ln = obj.dchans(ln[0])
    else:
        ln = ['ch%s'%str(ii) for ii in range(0,nch)]

    # Get indices
    lk = obj._dchans.keys()
    lind = [k for k in lk if k.lower() in ['ind','index','indices']]
    if restore_size and len(lind) == 1:
        lind = obj.dchans(lind[0])
    else:
        lind = np.arange(0,nch)

    # Check if info on nMax stored
    if restore_size and obj.Id.dUSR is not None:
        nchMax = obj.Id.dUSR.get('imas-nchMax', lind.max()+1)
    else:
        nchMax = lind.max()+1

    # Fill in data
    # ------------------
    try:
        ids = getattr(idd,ids)

        # time
        ids.time = obj.t

        # data
        # --------
        if not doneresize:
            ids.channel.resize( nchMax )
        data, X = obj.data, obj.X

        lpdata = path_data.split('.')
        if path_X is not None:
            lpX = path_X.split('.')
        if not hasattr(ids.channel[lind[0]], lpdata[0]):
            msg = "Non-valid path_data:\n"
            msg += "    - path_data: %s\n"%path_data
            msg += "    - dir(ids.channel[%s]) = %s"%(str(lind[0]),
                                                      str(dir(ids.channel[lind[0]])))
            raise Exception(msg)
        if path_X is not None and not hasattr(ids.channel[lind[0]], lpX[0]):
            msg = "Non-valid path_X:\n"
            msg += "    - path_X: %s\n"%path_X
            msg += "    - dir(ids.channel[%s]) = %s"%(str(lind[0]),
                                                      str(dir(ids.channel[lind[0]])))
            raise Exception(msg)

        for ii in range(0,lind.size):
            setattr(ftools.reduce(getattr, [ids.channel[lind[ii]]] +
                                  lpdata[:-1]), lpdata[-1], data[:,ii])
            if path_X is not None:
                setattr(ftools.reduce(getattr, [ids.channel[lind[ii]]] +
                                      lpX[:-1]), lpX[-1], X[:,ii])
            ids.channel[ii].name = ln[ii]

        # IDS properties
        # --------------
        com = "LOS-approximated tofu generated signal:\n"
        com += "    - from %s\n"%obj.Id.SaveName
        com += "    - by tofu %s"%tfversion
        _fill_idsproperties(ids, com, tfversion)
        err0 = None

    except Exception as err:
        _except_ids(ids, nt=None)
        err0 = err

    finally:

        # Put IDS
        # ------------------
        _put_ids(idd, ids, shotfile, occ=occ,
                 cls_name='%s_%s'%(obj.Id.Cls,obj.Id.Name),
                 err=err0, dryrun=dryrun, verb=verb)
