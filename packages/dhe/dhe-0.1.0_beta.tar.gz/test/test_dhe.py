#!/usr/bin/env python3

import unittest
import numpy

from dhe.backends.py import sample_soil_parameters
from dhe.model import SoilLayerProperties


class TestDHE(unittest.TestCase):

    def test_sample_soil_parameters(self):
        SoilLayer = SoilLayerProperties
        layers = [SoilLayer(d=1, rho=3., c=3., lambda_=0.),
                  SoilLayer(d=3., rho=2., c=3., lambda_=0.),
                  SoilLayer(d=2, rho=1., c=-1., lambda_=0.),
                  SoilLayer(d=1, rho=3., c=3., lambda_=0.)]
        resampled_data = sample_soil_parameters(layers, L_DHE=6., dim_ax=3)
        numpy.testing.assert_array_almost_equal(resampled_data.T,
                                                [
                                                    [7.5, 0.],
                                                    [6., 0.],
                                                    [-1., 0.]])

        with self.assertWarns(UserWarning):
            resampled_data = sample_soil_parameters(
                layers, 8., 2)
        numpy.testing.assert_array_almost_equal(resampled_data.T,
                                                [
                                                    [6.75, 0.],
                                                    [4., 0.]])
        resampled_data = sample_soil_parameters(
            [SoilLayer(d=float("inf"), rho=0., c=0., lambda_=0.)], 6., 2)
        numpy.testing.assert_array_almost_equal(resampled_data.T,
                                                [
                                                    [0., 0.],
                                                    [0., 0.]])


if __name__ == '__main__':
    unittest.main()
