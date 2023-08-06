#!/usr/bin/env python
# -*- coding: utf-8 -*-

from obspy.geodetics import locations2degrees

def distance(lat1, lon1, lat2, lon2):
    """
    Given two points location by (latitude, longitude) and return
    the distance on sphere between two points, unit in degree
    :return: distance in degree
    """
    return locations2degrees(lat1, lon1, lat2, lon2)