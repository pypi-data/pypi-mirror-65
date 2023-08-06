""" Quellcode für die Berechnung der aeusseren Randbedingungen """

from math import log, pi
from .pascal_defs import MatrixQ


def RandAussen_gfunc(k: int, Woche: int,
                     RepRandbed: int,
                     Q: MatrixQ,
                     cpErd: float, rhoErd: float, lambdaErd: float,
                     Rechenradius: float, Sondenlaenge: float,
                     gpar1: float, gpar2: float, gpar3: float, gpar4: float,
                     gpar5: float, gpar6: float,
                     DimAxi: int,
                     uMin: float):
    """ Diese Procedure berechnet die Randbedingung mit der g-Function """
    ts = Sondenlaenge**2 / 9 / lambdaErd * rhoErd * cpErd
    STrt = 0
    for i in range(1, Woche + 1):
        u = log(i / ts * 604800 * RepRandbed)
        #  Aenderung 2.10.02
        if u > 2.5:
            u = 2.5
        go = 0.5 * u + 6.84
        if u < uMin:
            g = go
        else:
            g = gpar1 + gpar2 * u + gpar3 * u**2 + gpar4 * u**3 \
                + gpar5 * u**4 + gpar6 * u ** 5
        if u < -2:
            if (go - 0.3) > g:
                g = go
        g = g - log(Rechenradius / Sondenlaenge / 0.0005)
        Rq = g / 2 / pi / lambdaErd
        STrt = STrt + (-Q[k, Woche - i + 1] + Q[k, Woche - i]
                       ) / Sondenlaenge * DimAxi * Rq
    return STrt
