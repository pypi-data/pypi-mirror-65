#!/usr/bin/env python3

import unittest
import numpy

from dhe.core import P_profile
from .original.input_file_erzeugen import InputFileErzeugen


class TestTBrine(unittest.TestCase):

    def setUp(self):
        pass

    @staticmethod
    def test_P_profile():
        t_run_pas = numpy.array([0, 24, 22, 10, 5, 3, 2, 1, 1, 5, 10, 20, 23])
        t_run = t_run_pas[1:]
        P_DHE = 10000.
        Q_peek_feb = 15000.
        Delta_t_peek = 4

        profile_pas = []
        Delta_t_DHE_pas = numpy.array(float("NaN"))

        InputFileErzeugen(profile_pas, t_run_pas, 0., P_DHE,
                          0., Q_peek_feb, Delta_t_DHE_pas, Delta_t_peek, 0, 0)
        t_pas, P_pas = numpy.array(profile_pas)[:, [0, -1]].T
        Delta_t_DHE, t, P = P_profile(
            t_run, P_DHE, Q_peek_feb, Delta_t_peek)

        numpy.testing.assert_array_almost_equal(t // 3600, t_pas - 1)

        numpy.testing.assert_array_almost_equal(P, P_pas)
        numpy.testing.assert_array_almost_equal(Delta_t_DHE, Delta_t_DHE_pas)
