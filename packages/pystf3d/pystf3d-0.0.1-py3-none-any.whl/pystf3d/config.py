#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Config classes for weighting and inversion

:copyright:
    Wenjie Lei (lei@princeton.edu), 2016
:license:
    GNU Lesser General Public License, version 3 (LGPLv3)
    (http://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
from __future__ import print_function, division, absolute_import
import numpy as np
from .util import _float_array_to_str
from .constant import DEFAULT_SCALE_VECTOR, NM, NML, PARLIST


class WeightConfigBase(object):
    """
    Base class of weight config. Shouldn't be used for most cases.
    Since we introduce complex weighting strategies here, so I think
    it might be worth to seperate WeightConfig from the Config.
    """
    def __init__(self, mode, normalize_by_energy=False,
                 normalize_by_category=False):
        self.mode = mode.lower()
        self.normalize_by_energy = normalize_by_energy
        self.normalize_by_category = normalize_by_category

    def __repr__(self):
        string = "Weight Strategy:\n"
        string += "mode: %s\n" % self.mode
        string += "normalize_by_energy: %s\n" % self.normalize_by_energy
        string += "normalize_by_category: %s\n" % self.normalize_by_category
        return string

    def __str__(self):
        return self.__repr__()


class WeightConfig(WeightConfigBase):
    def __init__(self, normalize_by_energy=False,
                 normalize_by_category=False,
                 azi_bins=12, azi_exp_idx=0.5):
        WeightConfigBase.__init__(
            self, "classic", normalize_by_energy=normalize_by_energy,
            normalize_by_category=normalize_by_category)
        self.azi_bins = azi_bins
        self.azi_exp_idx = azi_exp_idx

    def __repr__(self):
        string = "Weight Strategy:\n"
        string += "mode: %s\n" % self.mode
        string += "normalize_by_energy: %s\n" % self.normalize_by_energy
        string += "normalize_by_category: %s\n" % self.normalize_by_category
        string += "Azimuth bins and exp index: %d, %f" % (self.azi_bins,
                                                          self.azi_exp_idx)
        return string


class DefaultWeightConfig(WeightConfigBase):
    """
    Weight config in original CMT3D packages
    """
    def __init__(self, normalize_by_energy=False, normalize_by_category=False,
                 comp_weight=None,
                 love_dist_weight=0.78, pnl_dist_weight=1.15,
                 rayleigh_dist_weight=0.55,
                 azi_exp_idx=0.5, azi_bins=12,
                 ref_dist=1.0):
        WeightConfigBase.__init__(self, "default",
                                  normalize_by_energy=normalize_by_energy,
                                  normalize_by_category=normalize_by_category)
        if comp_weight is None:
            self.comp_weight = {"Z": 2.0, "R": 1.0, "T": 2.0}
        else:
            self.comp_weight = comp_weight

        self.love_dist_weight = love_dist_weight
        self.pnl_dist_weight = pnl_dist_weight
        self.rayleigh_dist_weight = rayleigh_dist_weight
        self.azi_exp_idx = azi_exp_idx
        self.azi_bins = azi_bins
        self.ref_dist = ref_dist

    def __repr__(self):
        string = "Weight Strategy:\n"
        string += "mode: %s\n" % self.mode
        string += "normalize_by_energy: %s\n" % self.normalize_by_energy
        string += "normalize_by_category: %s\n" % self.normalize_by_category
        string += "component weight: %s\n" % self.comp_weight
        string += "pnl, rayleigh and love distance weights: %f, %f, %f\n" % (
            self.pnl_dist_weight, self.rayleigh_dist_weight,
            self.love_dist_weight)
        string += "number of azimuth bins: %d\n" % self.azi_bins
        string += "azimuth exponential index: %f\n" % self.azi_exp_idx
        return string


class Config(object):
    """
    Configuration for source inversion
    """

    def __init__(self, damping=0.0, station_correction=True,
                 weight_data=True, weight_config=None,
                 max_nl_iter,
                 bootstrap=True, bootstrap_repeat=300,
                 bootstrap_subset_ratio=0.4,
                 taper_type="tukey"):
        """
        :param npar: number of parameters to be inverted
        :param dlocation: location perturbation when calculated perturbed
            synthetic data, unit is degree
        :param ddepth: depth perturbation, unit is meter
        :param dmoment: moment perturbation, unit is dyne * cm
        :param scale_vector: the scaling vector for d***. If none, then
            it will use the default
        :param zero_trace: bool value of whether applies zero-trace constraint
        :param double_couple: bool value of whether applied double-couple
            constraint
        :param envelope_coef: the coefficient of envelope misfit function,
            should be within [0, 1]
        :param max_nl_iter: max number of non-linear iterations
        :param damping: damping coefficient
        :param station_correction: bool value of whether applies station
            correction
        :param weight_data: bool value of weighting data
        :param weight_config: the weighting configuration
        :param bootstrap: bool value of whether applied bootstrap method
        :param bootstrap_repeat: bootstrap iterations
        :param bootstrap_subset_ratio: the subset ratio for bootstrap runs
        :param taper_type: the taper type used for taper the seismograms
            in the windows
        :param dtx: Defines whether time shift is supposed to be
                    found or not
        :param dM0: Defines whether scalar Moment change is supposed
                    to be found or not
        """


        self.weight_data = weight_data
        self.weight_config = weight_config

        self.station_correction = station_correction

        if max_nl_iter <= 0:
            raise ValueError("max_nl_iter(%d) must be larger than 0"
                             % max_nl_iter)
        self.max_nl_iter = max_nl_iter
        self.damping = damping

        # scaled cmt perturbation
        self.bootstrap = bootstrap
        self.bootstrap_repeat = bootstrap_repeat
        self.bootstrap_subset_ratio = bootstrap_subset_ratio

        self.taper_type = taper_type

    def __repr__(self):
        npar = self.npar
        string = "="*10 + "  Config Summary  " + "="*10 + "\n"
        string += "Damping:%s\n" % self.damping
        string += "Max Iterations: %s\n" % self.max_nl_iter
        string += "Bootstrap:%s\n" % self.bootstrap
        if self.bootstrap:
            string += "Bootstrap repeat times: %d\n" % self.bootstrap_repeat
        string += "-" * 5 + "\nWeight Schema\n"
        string += "%s" % str(self.weight_config)
        return string
