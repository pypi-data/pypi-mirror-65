#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Signal Processing utilities used for the 
source time function inversion."""

import numpy as np
from numpy.fft import fft, ifft, fftfreq, fftshift
from scipy import signal

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


def forward(green, src):
    """ Convolution of set of Green's functions

    :param green: Green's function
    :param src:
    :return:
    """
    # Get frequency spectrum of source time function
    SRC = fft(src)

    # Get frequency spectra of Green's functions
    GRE = fft(green, axis=1)

    # Convolve the two and return matrix containing the synthetic
    syn = np.real(ifft(GRE*SRC, axis=1))

    return syn


def compute_gradient_newton(resid, green, lamb):
    """ Compute Gradient using the waterlevel deconvolution which computes
    the Newton Step.

    :param resid: residual
    :param green: green's function
    :param lamb: waterlevel scaling
    :return:
    """

    # FFT of residuals and green functions
    RES = fft(resid, axis=1)
    GRE = fft(green, axis=1)

    # Compute gradient (full wavelet estimation)
    num = np.sum(RES * np.conj(GRE), axis=0)
    den = np.sum(GRE * np.conj(GRE), axis=0)

    # Waterlevel?
    wl = lamb * np.max(np.abs(den))
    grad = np.real(ifft(num / (den + wl)))

    # Step value
    hmax = 1

    return grad, hmax


def compute_gradient_sd(resid, green):
    """ Compute the Gradient using the steepest decent method
    :param resid:
    :param green:
    :return:
    """

    # FFT of residuals and green functions
    RES = fft(resid, axis=1)
    GRE = fft(green, axis=1)

    # Compute gradient (full wavelet estimation)
    num = np.sum(RES * np.conj(GRE), axis=0)
    den = np.sum(GRE * np.conj(GRE), axis=0)

    # Waterlevel?
    tau = 1/np.max(np.abs(den))
    grad = np.real(ifft(num * tau))

    # Step value
    hmax = 1

    return grad, hmax
