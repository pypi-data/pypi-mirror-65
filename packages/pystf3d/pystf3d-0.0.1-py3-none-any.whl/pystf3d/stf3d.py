#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module that covers the function and classes that cover the 
inversion."""

import numpy as np
from .datacontainer import DataContainer
from .config import Config
from .signal import compute_gradient_newton, compute_gradient_sd
from .signal import forward

class STF3D(object):

    def __init__(self, datacontainer: DataContainer, config: Config)













































class STF(object):
    """Actual inversion class."""

    def __init__(self, observed, green, tapers, dt, maxT: float = 50, critical,
                 lamb=None, type="2"):
        """
        :param obs: observed traces
        :param G: Green's functions
        :param maxT: time after which STF is forced to zero
        :param crit: critical value for stopping the iteration
        :param dt: time sampling
        :param lamb: waterlevel for deconvolution if type 2 is chosen. Unused if
                     type is "1".
        :param type: string defining the type of landweber method. Type 1 is the
                     method using the steepest decent; type 2 is using a Newton
                     step.
        :return:
        """

        # Get data
        self.obs = observed
        self.green = green
        self.tapers = tapers  # Window measurements and weighting data
        self.dt = dt

        # Get parameters
        self.maxT = maxT
        self.critical = critical
        self.lamb = lamb  # Deconvolution method
        self.perc = 0.05  # Steepest descent
        self.type = type

        if self.type == "1":
            self.compute_gradient = compute_gradient_sd
        elif self.type == "2":
            self.compute_gradient = compute_gradient_newton
        else:
            raise ValueError('Type must be "1" or "2"')

        # Get informations about size and initialize src
        self.nr, self.nt = self.obs.shape
        self.src = np.zeros(self.nt)


        # Compute objective function and residual
        self.syn = forward(self.G, self.src)
        self.res = self.residual()
        self.chi = self.misfit()
        self.chi0 = self.chi

    def landweber(self):
        """Perform Landweber iterative source time function inversion."""

        # Compute the first gradient
        grad, alpha = self.compute_gradient(res, G, lamb)

        # Manage windowing tapered window in the future? e.g., tukey?
        itstop = int(np.floor(maxT / self.dt) + 1)
        Ptime = np.ones(nt)
        Ptime[itstop + 1: itstop + 31] = np.arange(30, 0, -1) / 30.
        Ptime[itstop + 31:] = 0.

        # Perform iterative deconvolution (inverse problem)
        self.it = 1
        chip = chi0
        # llb = 0.1

        # Initialize list to save iterations
        src_list = []
        chi_list = []

        while chi > crit * chi0 and it <= nt:

            # Regularized gradient
            gradreg = grad

            if type == "1":
                srctmp = src + gradreg
            else:
                srctmp = src + perc * gradreg

            # Window source time function --> zero after some time T
            srctmp = srctmp * Ptime

            # Enforce positivity
            srctmp[np.where(srctmp < 0)[0]] = 0

            # Compute misfit function and gradient
            syn = compute_synth(G, srctmp)
            res = obs - syn
            chi = 0.5 * np.sum(np.sum(res ** 2))
            grad, _ = compute_gradient(res, G, lamb)
            it = it + 1

            # Check convergence
            if chi > chip:
                print("NOT CONVERGING")
                break

            # Update
            # chi / chi0
            chip = chi
            src = srctmp

            chi_list.append(chi)
            src_list.append(src)

        # Final misfit function
        print(chi / chi0)
        print(it)

        return src, src_list, chi_list


    def residual(self):
        """Computes the residual between the observed data
        and the synthetic data."""

        return self.obs - self.syn

    def misfit(self, syn):
        """Computes the misfit between the observed data and
        the forward modeled synthetic data."""
        return 0.5 * np.sum(np.sum(self.residual() ** 2 * self.tapers))