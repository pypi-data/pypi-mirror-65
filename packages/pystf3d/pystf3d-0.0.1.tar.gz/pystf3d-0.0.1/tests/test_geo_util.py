#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest
from pystf3d.geo_util import locations2degrees
import numpy as np

class TestGeoUtils(unittest.TestCase):
    """Test the functions in geo_utils module."""


    def test_locations2degree(self):
        """Tests the locations2degree function"""

        # Set Test locations
        lat1 = 0
        lon1 = 0
        lat2 = 5
        lon2 = 0

        deg = locations2degrees(lat1, lon1, lat2, lon2)

        np.testing.assert_almost_equal(deg, 5)

        # Set Test locations
        lat1 = 0
        lon1 = 0
        lat2 = 0
        lon2 = 5

        deg = locations2degrees(lat1, lon1, lat2, lon2)

        np.testing.assert_almost_equal(deg, 5)