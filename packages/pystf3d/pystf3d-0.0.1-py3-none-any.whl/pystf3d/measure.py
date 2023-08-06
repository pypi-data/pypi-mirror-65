#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Measurement util functions

:copyright:
    Wenjie Lei (lei@princeton.edu), 2016
:license:
    GNU Lesser General Public License, version 3 (LGPLv3)
    (http://www.gnu.org/licenses/lgpl-3.0.en.html)
"""
from __future__ import print_function, division, absolute_import
import numpy as np
from scipy.signal import hilbert

from .util import construct_taper, get_window_idx
from . import constant


def _envelope(array):
    return np.abs(hilbert(array))


def _xcorr_win_(arr1, arr2):
    """
    cross-correlation between arr1 and arr2 to get the max_cc_value
    and nshift
    """
    if len(arr1) != len(arr2):
        raise ValueError("Length of arr1(%d) and arr2(%d) must be the same"
                         % (len(arr1), len(arr2)))
    cc = np.correlate(arr1, arr2, mode="full")
    nshift = cc.argmax() - len(arr1) + 1
    # Normalized cross correlation.
    max_cc_value = \
        cc.max() / np.sqrt((arr1 ** 2).sum() * (arr2 ** 2).sum())
    return max_cc_value, nshift


def _power_l2_win_(arr1, arr2):
    """
    Power(L2 norm, square) ratio of arr1 over arr2, unit in dB.
    """
    if len(arr1) != len(arr2):
        raise ValueError("Length of arr1(%d) and arr2(%d) not the same"
                         % (len(arr1), len(arr2)))
    return 10 * np.log10(np.sum(arr1 ** 2) / np.sum(arr2 ** 2))


def _power_l1_win_(arr1, arr2):
    """
    Power(L1 norm, abs) ratio of arr1 over arr2, unit in dB
    """
    if len(arr1) != len(arr2):
        raise ValueError("Length of arr1(%d) and arr2(%d) not the same"
                         % (len(arr1), len(arr2)))
    return 10 * np.log10(np.sum(np.abs(arr1)) / np.sum(np.abs(arr2)))


def _cc_amp_(arr1, arr2):
    """
    Cross-correlation amplitude ratio
    """
    return 10 * np.log10(np.sum(arr1 * arr2) / np.sum(arr2 ** 2))


def _energy_(arr, taper=None):
    """
    Energy of an array
    """
    if taper is None:
        return np.sum(arr ** 2)
    else:
        return np.sum((taper * arr) ** 2)


def _diff_energy_(arr1, arr2, taper=None):
    """
    energy of two array difference
    """
    if taper is None:
        return np.sum((arr1 - arr2) ** 2)
    else:
        return np.sum((taper * (arr1 - arr2)) ** 2)


def correct_window_index(arr1, arr2, istart, iend):
    """
    Correct the window index based on cross-correlation shift
    """
    npts = min(len(arr1), len(arr2))
    max_cc, nshift = _xcorr_win_(arr1[istart:iend], arr2[istart:iend])
    istart_d = max(1, istart + nshift)
    iend_d = min(npts, iend + nshift)
    istart_s = max(1, istart_d - nshift)
    iend_s = min(npts, iend_d - nshift)
    if (iend_d - istart_d) != (iend_s - istart_s):
        raise ValueError("After correction, window length not the same: "
                         "[%d, %d] and [%d, %d]" % (istart_d, iend_d,
                                                    istart_s, iend_s))
    return istart_d, iend_d, istart_s, iend_s, max_cc, nshift


def measure_window(obsd_array, synt_array, istart, iend,
                   station_correction=True):
    """
    Make measurements on windows. If station_correction, correct window
    idx first based on cross-correlation time shift measurement.

    :param obsd: obsd data array
    :param synt: synt data array
    :param istart: start index of original window
    :param iend: end index of original window
    :param station_correction: station correction flag
    :return:
    """
    # correct window index if required
    if station_correction:
        istart_d, iend_d, istart_s, iend_s, max_cc, nshift = \
            correct_window_index(obsd_array, synt_array, istart, iend)
    else:
        max_cc, nshift = _xcorr_win_(obsd_array[istart:iend],
                                     synt_array[istart:iend])
        istart_d = istart
        iend_d = iend
        istart_s = istart
        iend_s = iend

    # make measurements
    _obs = obsd_array[istart_d: iend_d]
    _syn = synt_array[istart_s: iend_s]
    power_l1 = _power_l1_win_(_obs, _syn)
    power_l2 = _power_l2_win_(_obs, _syn)
    cc_amp_ratio = _cc_amp_(_obs, _syn)
    return nshift, max_cc, power_l1, power_l2, cc_amp_ratio


def calculate_variance_on_trace(obsd, synt, win_time, taper_type="tukey"):
    """
    Calculate the variance reduction on a pair of obsd and
    synt and windows

    :param obsd: observed data trace
    :type obsd: :class:`obspy.core.trace.Trace`
    :param synt: synthetic data trace
    :type synt: :class:`obspy.core.trace.Trace`
    :param win_time: [win_start, win_end]
    :type win_time: :class:`list` or :class:`numpy.array`
    :return:  waveform misfit reduction and observed data
    energy [v1, d1]
    :rtype: [float, float]
    """
    dt = synt.stats.delta
    win_time = np.array(win_time)
    num_wins = win_time.shape[0]

    v1_array = np.zeros(num_wins)
    d1_array = np.zeros(num_wins)
    tshift_array = np.zeros(num_wins)
    cc_array = np.zeros(num_wins)
    power_l1_array = np.zeros(num_wins)
    power_l2_array = np.zeros(num_wins)
    cc_amp_array = np.zeros(num_wins)

    for _win_idx in range(win_time.shape[0]):
        istart, iend = get_window_idx(win_time[_win_idx], obsd.stats.delta)

        istart_d, iend_d, istart_s, iend_s, _, _ = \
            correct_window_index(obsd.data, synt.data, istart, iend)

        nshift, cc, power_l1, power_l2, cc_amp_value = \
            measure_window(obsd, synt, istart, iend)

        taper = construct_taper(iend_d - istart_d, taper_type=taper_type)

        v1_array[_win_idx] = dt * _diff_energy_(obsd.data[istart_d:iend_d],
                                                synt.data[istart_s:iend_s],
                                                taper=taper)
        d1_array[_win_idx] = dt * _energy_(obsd.data[istart_d:iend_d],
                                           taper=taper)

        tshift_array[_win_idx] = nshift * dt
        cc_array[_win_idx] = cc
        power_l1_array[_win_idx] = power_l1
        power_l2_array[_win_idx] = power_l2
        cc_amp_array[_win_idx] = cc_amp_value

    var = {"v": v1_array, "d": d1_array, "tshift": tshift_array,
           "cc": cc_array, "power_l1": power_l1_array,
           "power_l2": power_l2_array, "cc_amp": cc_amp_array,
           "chi": v1_array/d1_array}
    return var


def compute_new_syn_on_trwin(datalist, parlist, dcmt_par, dm):
    """
    Compute new synthetic data based on gradient(datalist, and dcmt_par)
    and perturbation(dm). Be careful about dm here becuase dcmt_par has
    been scaled.

    :param datalist: dictionary of all data
    :param dm: CMTSolution perterbation, i.e.,
    (self.new_cmt_par-self.cmt_par)
    :return:
    """
    # get a dummy copy to keep meta data information
    datalist['new_synt'] = datalist['synt'].copy()

    npar = len(parlist)
    npts = datalist['synt'].stats.npts
    dt = datalist['synt'].stats.delta
    dsyn = np.zeros([npts, npar])

    for i in range(npar):
        if i < constant.NM:
            dsyn[:, i] = datalist[parlist[i]].data / dcmt_par[i]
        elif i < constant.NML:
            dsyn[:, i] = (datalist[parlist[i]].data
                          - datalist['synt'].data) / dcmt_par[i]
        elif i == constant.NML:
            dsyn[0:(npts - 1), i] = \
                -(datalist['synt'].data[1:npts]
                  - datalist[0:(npts - 1)]) / (dt * dcmt_par[i])
            dsyn[npts - 1, i] = dsyn[npts - 2, i]
        elif i == (constant.NML + 1):
            # not implement yet....
            raise ValueError("For npar == 10 or 11, not implemented yet")

    datalist['new_synt'].data = \
        datalist['synt'].data + np.dot(dsyn, dm[:npar])
