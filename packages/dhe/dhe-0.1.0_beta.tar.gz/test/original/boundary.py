""" Quellcode für die Berechnung der aeusseren Randbedingungen """

from math import log, pi, factorial
from .pascal_defs import MatrixQ


def RandAussen(k: int, Woche: int,
               RepRandbed: int,
               Q: MatrixQ,
               cpErd: float, rhoErd: float, lambdaErd: float,
               Rechenradius: float, Sondenlaenge: float,
               DimAxi: int):
    """ Diese Procedure berechnet die Randbedingung nach der Trichterformel
    von Werner """
    u0 = Rechenradius**2 * cpErd * rhoErd / (4 * lambdaErd)
    STrt0 = 4 * pi * lambdaErd * Sondenlaenge / DimAxi
    STrt = 0
    for i in range(1, Woche + 1):
        u = u0 / (i * 604800 * RepRandbed)
        if u > 1:
            STrt = 0
        else:
            W = -0.5772 - log(u)
            j = 1
            W_alt = W - (-1)**j * u**j / (j * factorial(j))
            W = W_alt
            while True:
                W_alt = W
                j = j + 1
                W = W - (-1)**j / j * u**j / (factorial(j))
                if abs(1 - W / W_alt) < 0.01:
                    break
            STrt = STrt + (-Q[k, Woche - i + 1] +
                           Q[k, Woche - i]) / STrt0 * W
    return STrt
