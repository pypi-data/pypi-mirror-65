#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Plotting tools for the Source Time Function Inversion."""

import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'cm'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
matplotlib.rcParams['font.weight'] = 'bold'
matplotlib.rcParams["axes.labelweight"] = "bold"
matplotlib.rcParams['text.usetex'] = True


class PlotSTFDist(object):
    """Plots ditribution of Source Time Functions."""
    
    def __init__(Datacontaitns)