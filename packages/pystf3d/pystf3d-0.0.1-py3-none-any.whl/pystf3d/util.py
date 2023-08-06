#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from obspy.geodetics import locations2degrees


def dump_json(content, filename):
    with open(filename, "w") as fh:
        json.dump(content, fh, indent=2, sort_keys=2)


def get_trwin_tag(trwin):
    """
    trwin.tag is usually the period band, so
    category would be like "27_60.BHZ", "27_60.BHR", "27_60.BHT",
    and "60_120.BHZ", "60_120.BHR", "60_120.BHT".
    """
    return "%s.%s" % (trwin.tags['obsd'], trwin.channel)

def check_trace_consistent(tr1, tr2, mode="part"):
    """
    Check if two traces are consistent with each other.
    If mode is 'part', only starttime and dt is compared
    If mode is 'full', npts is also compared
    """
    _options = ["part", "full"]
    if mode not in _options:
        raise ValueError("mode(%s) must be within %s" % (mode, _options))

    if not np.isclose(tr1.stats.delta, tr2.stats.delta):
        raise ValueError("DT of two traces are not the same: %f, %f"
                         % (tr1.stats.delta, tr2.stats.delta))

    if not np.isclose(tr1.stats.starttime - tr2.stats.starttime, 0):
        raise ValueError("Starttime of two traces not the same: %s, %s"
                         % (tr1.stats.starttime, tr2.stats.starttime))

    if mode == "full":
        if tr1.stats.npts != tr2.stats.npts:
            raise ValueError("NPTS not the same: %d, %d" % (tr1.stats.npts,
                                                            tr2.stats.npts))
    else:
        return


def construct_taper(npts, taper_type="tukey", alpha=0.2):
    """
    Construct taper based on npts

    :param npts: the number of points
    :param taper_type:
    :param alpha: taper width
    :return:
    """
    taper_type = taper_type.lower()
    _options = ['hann', 'boxcar', 'tukey']
    if taper_type not in _options:
        raise ValueError("taper type option: %s" % taper_type)
    if taper_type == "hann":
        taper = signal.hann(npts)
    elif taper_type == "boxcar":
        taper = signal.boxcar(npts)
    elif taper_type == "tukey":
        taper = signal.tukey(npts, alpha=alpha)
    else:
        raise ValueError("Taper type not supported: %s" % taper_type)
    return taper