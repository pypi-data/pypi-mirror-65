#!/usr/bin/env python3

import unittest
import numpy

from dhe.backends.py import pressure_decay
from .original.pressure_decay import pressure_decay as pressure_decay_original


class TestPressureDecay(unittest.TestCase):
    def test_pressure_decay(self):

        Phi_m = numpy.array([0.001, 0.01, 0.1, 1., 10.])
        nu_brine = 0.00000415
        rho_brine = 1050.
        D = 0.026
        d = 0
        L = 100.

        p0, laminar_0 = pressure_decay(Phi_m[0], nu_brine, rho_brine, D, d, L)
        p, laminar = pressure_decay(Phi_m, nu_brine, rho_brine, D, d, L)
        p_ref = numpy.empty_like(p)
        laminar_ref = numpy.empty_like(laminar)
        for i, phi in enumerate(Phi_m):
            p_ref[i], laminar_ref[i] = pressure_decay_original(
                phi, nu_brine, rho_brine, D, d, L)
        numpy.testing.assert_array_almost_equal(p, p_ref)
        numpy.testing.assert_array_almost_equal(laminar, laminar_ref)
        self.assertEqual(p0, p[0])
        self.assertEqual(laminar_0, laminar[0])


if __name__ == '__main__':
    unittest.main()
