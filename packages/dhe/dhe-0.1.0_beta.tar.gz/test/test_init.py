#!/usr/bin/env python3

import unittest
from math import pi as pi_
import numpy

from dhe.backends.py import g_poly, T_soil_evolution, r_grid, rz_grid, \
    alpha1, R_1, R_2, alpha0, T_soil_0, L_pump, C_matrix, optimal_n_steps
from dhe.model import BrineProperties
from .original.ews_init_modular import Polynom, _B, r_grid as r_grid_pas, \
    rz_grid as rz_grid_pas
from .original import pascal_defs
from .original.pascal_defs import Vektor, Matrix, VektorRad
from .original.pascal_defs import Def_Sondendurchmesser, \
    Def_Bohrdurchmesser, Def_Rechenradius, \
    Def_Gitterfaktor, Def_Jahresmitteltemp, \
    Def_Bodenerwaermung, \
    Def_cpErde, Def_rhoErde, Def_adiabat, Def_Rb, Def_lambdaFill, \
    Def_Sondenlaenge, Def_lambdaErde, Def_lambdaSole, \
    Def_cpFill, Def_rhoFill, Def_Sicherheit2, Def_Zeitschritt
from .original.ews_init_modular import alpha1 as alpha1_pas
from .original.ews_init_modular import resistances
from .original.ews_init_modular import Anfangstemp
from .original.ews_init_modular import L1run_matrix
from .original.ews_init_modular import C_matrix as C_matrix_pas
from .original.ews_init_modular import Optimaler_Zeitfaktor
from .original.calculateEWS import multiplizieren


class TestEWSInit(unittest.TestCase):
    def test_g_poly(self):
        g = (pascal_defs.Def_g1, pascal_defs.Def_g2,
             pascal_defs.Def_g3, pascal_defs.Def_g4, pascal_defs.Def_g5)
        uMin, w = Polynom(*g, Sondenabstand=pascal_defs.Def_Sondenabstand,
                          g_Sondenabstand=pascal_defs.Def_g_Sondenabstand)
        u_min, g_coefs = g_poly(g, pascal_defs.Def_Sondenabstand,
                                pascal_defs.Def_g_Sondenabstand)
        numpy.testing.assert_array_almost_equal(w, g_coefs)
        self.assertAlmostEqual(u_min, uMin)

    @staticmethod
    def test_r():
        DimRad = 5
        Rechengebiet = Def_Rechenradius - Def_Bohrdurchmesser / 2
        r_ref = r_grid_pas(Def_Sondendurchmesser, Def_Bohrdurchmesser,
                           Rechengebiet, Def_Gitterfaktor, DimRad)
        r = r_grid(Def_Sondendurchmesser, Def_Bohrdurchmesser,
                   Rechengebiet, DimRad, Def_Gitterfaktor)
        numpy.testing.assert_array_almost_equal(r, r_ref[:r.size])

    @staticmethod
    def test_rz():
        DimRad = 5
        r = numpy.array([0.013, 0.0575, 0.461 / 3, 0.346, 2.192 / 3, 1.5])
        r_ref = VektorRad()
        r_ref[:r.size] = r
        rz_ref = rz_grid_pas(r_ref, DimRad)
        rz = rz_grid(r)
        numpy.testing.assert_array_almost_equal(rz, rz_ref[:DimRad + 2])

    def test_alpha1(self):
        d_DHE = 0.
        D_DHE = 0.026
        Phi_m = 0.4
        brine_properties = BrineProperties(
            c=3875., rho=1050., nu=0.00000415, lambda_=0.449)
        alpha = alpha1(brine_properties, Phi_m / brine_properties.rho,
                       D_DHE, d_DHE)
        alpha_ref = alpha1_pas(brine_properties.nu, brine_properties.rho,
                               brine_properties.c, brine_properties.lambda_,
                               Phi_m, D_DHE, d_DHE)
        self.assertEqual(alpha, alpha_ref)

    def test_resistances(self):
        r = numpy.array([0.013, 0.0575, 0.461 / 3, 0.346, 2.192 / 3, 1.5])
        rz = rz_grid(r)
        DimAxi = 3
        dl = Def_Sondenlaenge / DimAxi
        alpha = 75.29384615384616
        lambdaErde = numpy.array(
            [float("NaN"), Def_lambdaErde, Def_lambdaErde + 0.1,
             Def_lambdaErde - 0.1])
        for Ra, Rb in ((0.01, Def_Rb), (0., Def_Rb), (0., 0.)):
            with self.subTest(R=(Ra, Rb)):
                R1 = R_1(dl, r, rz, alpha, Def_lambdaFill, Ra, Rb)
                R2 = R_2(dl, r, rz, Def_lambdaFill, lambdaErde[1:], Ra, Rb)
                L1run, L1stop, R1_ref, R2_ref = resistances(
                    DimAxi, 0., dl, r, rz, alpha, lambdaErde, Ra=Ra, Rb=Rb,
                    lambdaFill=Def_lambdaFill,
                    lambdaSole=Def_lambdaSole,
                    Sondendurchmesser=Def_Sondendurchmesser)
                self.assertAlmostEqual(R1, R1_ref)
                numpy.testing.assert_array_almost_equal(
                    R2, R2_ref[1:DimAxi + 1])
                L1_on = 1 / R1
                L1_off = 1 / \
                    (R1 + (1. / alpha0(Def_lambdaSole,
                                       Def_Sondendurchmesser) - 1. / alpha) /
                     (8 * pi_ * r[0] * dl))
                self.assertAlmostEqual(L1_on, L1run)
                self.assertAlmostEqual(L1_off, L1stop)

    def test_T_soil_0(self):
        u_min = -5.
        TMittel = Def_Jahresmitteltemp + Def_Bodenerwaermung
        r = numpy.array([0.013, 0.0575, 0.461 / 3, 0.346, 2.192 / 3, 1.5])
        rz = rz_grid(r)
        DimAxi = 3
        DimRad = 5
        dl = Def_Sondenlaenge / DimAxi
        T_grad = 0.03
        g = (pascal_defs.Def_g1, pascal_defs.Def_g2,
             pascal_defs.Def_g3, pascal_defs.Def_g4, pascal_defs.Def_g5)
        u_min, g_coefs = g_poly(g, pascal_defs.Def_Sondenabstand,
                                pascal_defs.Def_g_Sondenabstand)
        q_drain_pas = Vektor()
        q_drain = q_drain_pas[1:DimAxi + 1]
        q_drain[2] = 1.

        TEarth = Matrix()
        for y in (0, 1):
            with self.subTest(y=y):
                T_soil = T_soil_0(t0=y * 3600 * 24 * 365,
                                  g_coefs=g_coefs, dim_ax=DimAxi, dl=dl,
                                  c_V_soil=Def_rhoErde * Def_cpErde,
                                  lambda_soil=Def_lambdaErde, rz=rz,
                                  T_soil=TMittel, q_drain=q_drain,
                                  T_grad=T_grad, u_min=u_min).T
                Anfangstemp(TMittel=TMittel, TGrad=T_grad, dl=dl,
                            qEntzug=q_drain_pas,
                            TEarth=TEarth,
                            T0=Vektor(), TUp=Vektor(),
                            TUpold=Vektor(), TDown=Vektor(), TDownOld=Vektor(),
                            _TSource=None,
                            DimAxi=DimAxi, DimRad=DimRad, StartJahr=y,
                            gpar1=g_coefs[0],
                            gpar2=g_coefs[1],
                            gpar3=g_coefs[2],
                            gpar4=g_coefs[3],
                            gpar5=g_coefs[4],
                            gpar6=g_coefs[5],
                            lambdaErd=Def_lambdaErde, rhoErd=Def_rhoErde,
                            cpErd=Def_cpErde,
                            uMin=u_min, rz=rz, Sondenlaenge=Def_Sondenlaenge)
                numpy.testing.assert_array_almost_equal(
                    T_soil, TEarth[1:DimAxi + 1, :DimRad + 2])

    @staticmethod
    def test_L_pump():
        r = numpy.array([0.013, 0.0575, 0.461 / 3, 0.346, 2.192 / 3, 1.5])
        rz = rz_grid(r)
        DimAxi = 3
        DimRad = 5
        dl = Def_Sondenlaenge / DimAxi

        lambdaErde = numpy.array(
            [float("NaN"), Def_lambdaErde, Def_lambdaErde + 0.1,
             Def_lambdaErde - 0.1])
        R2_pas = numpy.array(
            [float("NaN"), 0.00460078, 0.00452098, 0.00468898])
        R2 = R2_pas[1:]
        L1_on = 40000. / 3
        L1_off = -2733.456633111457
        L_on, L_off = L_pump(dl, r, rz, L1_on, L1_off,
                             R2, Def_adiabat, lambdaErde[1:])
        L_on_ref, L_off_ref = L1run_matrix(
            DimAxi, DimRad, L1_on, L1_off, R2_pas, lambdaErde,
            r, rz, dl, adiabat=Def_adiabat)
        numpy.testing.assert_array_almost_equal(
            L_on, L_on_ref[1:DimAxi + 1, 1:DimRad + 2])
        numpy.testing.assert_array_almost_equal(
            L_off, L_off_ref[1:DimAxi + 1, 1:DimRad + 2])

    @staticmethod
    def test_C_matrix():
        DimAxi = 3
        DimRad = 5
        dl = Def_Sondenlaenge / DimAxi
        r = numpy.array([0.013, 0.0575, 0.461 / 3, 0.346, 2.192 / 3, 1.5])
        cpErde = numpy.array([float("NaN"), 1000., 1010., 990.])
        rhoErde = numpy.array([float("NaN"), 2600., 2500., 2600.])

        C_ref = C_matrix_pas(DimAxi, DimRad, r, dl, cpErde,
                             rhoErde, cpFill=Def_cpFill, rhoFill=Def_rhoFill)
        C = C_matrix(dl, r, c_V_fill=Def_cpFill * Def_rhoFill,
                     c_V_soil=cpErde[1:] * rhoErde[1:])
        numpy.testing.assert_array_almost_equal(
            C, C_ref[1:DimAxi + 1, 1:DimRad + 1])

    def test_optimal_n_steps(self):
        dt = Def_Zeitschritt * 60
        DimAxi = 3
        C = numpy.array([[9.88e+05, 5.52e+06, 2.61e+07, 1.12e+08, 4.67e+08],
                         [9.88e+05, 5.36e+06, 2.54e+07, 1.09e+08, 4.53e+08],
                         [9.88e+05, 5.47e+06, 2.59e+07, 1.11e+08, 4.62e+08]])
        L = numpy.array([[40000. / 3, 217.35444859, 500.965279, 552.124962,
                          578.11550952, 1744.47884119],
                         [40000. / 3, 221.19098072, 526.01354295,
                          579.7312101, 607.021285, 1831.70278325],
                         [40000. / 3, 213.26599815, 475.91701505,
                          524.5187139, 549.20973405, 1657.25489913]])
        C_pas = Matrix()
        L_pas = Matrix()
        C_pas[1:C.shape[0] + 1, 1:C.shape[1] + 1] = C
        L_pas[1:L.shape[0] + 1, 1:L.shape[1] + 1] = L
        optfak = Optimaler_Zeitfaktor(
            DimAxi, Def_Zeitschritt, L_pas, C_pas, Sicherheit2=Def_Sicherheit2)
        n_steps = optimal_n_steps(L, C, dt, c=Def_Sicherheit2)
        self.assertEqual(optfak, n_steps)

    @staticmethod
    def test_B():
        DimRad = 5
        DimAxi = 3
        dl = Def_Sondenlaenge / DimAxi
        L_pas = Matrix()
        L = L_pas[1:DimAxi + 1, 1:DimRad + 2]
        L[()] = [[40000. / 3, 217.35, 500.96, 552.12, 578.11, 1744.47],
                 [40000. / 3, 221.19, 526.01, 579.73, 607.02, 1831.70],
                 [40000. / 3, 213.26, 475.91, 524.51, 549.20, 1657.25]]
        r = numpy.array([0.013, 0.0575, 0.461 / 3, 0.346, 2.192 / 3, 1.5])
        r_ref = VektorRad()
        r_ref[:r.size] = r
        cpErde = numpy.array([float("NaN"), 1000., 1010., 990.])
        rhoErde = numpy.array([float("NaN"), 2600., 2500., 2600.])

        C_pas = C_matrix_pas(DimAxi, DimRad, r, dl, cpErde, rhoErde)
        C = C_pas[1:DimAxi + 1, 1:DimRad + 1]

        dt_step = 3600.
        B = T_soil_evolution(L, C, dt_step)
        B_pas = _B(L_pas, C_pas, dt_step, DimAxi, DimRad)
        numpy.testing.assert_array_almost_equal(
            B, B_pas[1:DimAxi + 1, 1:DimRad + 1, 0:DimRad + 2])

        T_old_pas = Matrix()
        T_new_pas = Matrix()
        T_old = T_old_pas[1:DimAxi + 1, :DimRad + 2]
        T_new_ref = T_new_pas[1:DimAxi + 1, :DimRad + 2]
        T_old[()] = 10. + 0.1 * numpy.arange(DimAxi)[:, None] \
            - 0.2 * numpy.arange(DimRad + 2)[None, :]
        for i in range(1, DimAxi + 1):
            multiplizieren(B_pas, T_old_pas, T_new_pas, i, DimRad)
        T_new = numpy.empty_like(T_old)
        T_new[:, 1:-1] = (B @ T_old[:, :, None]).squeeze()
        T_new[:, 0] = T_old[:, 0]
        T_new[:, -1] = T_old[:, -1]
        numpy.testing.assert_array_almost_equal(T_new, T_new_ref)
        T_new_ref[()] = 0.
        numpy.testing.assert_array_almost_equal(T_new_pas, 0.)


if __name__ == '__main__':
    unittest.main()
