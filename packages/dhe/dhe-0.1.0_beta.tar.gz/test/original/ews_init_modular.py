"""Modular version of ews_init"""

from math import log, exp, sqrt, pi as pi_
from .pascal_defs import Vektor, Vektor10, \
    Matrix6, Matrix, KMatrix, VektorRad,\
    Def_Sondendurchmesser,\
    Def_lambdaFill, Def_lambdaSole, Def_Ra, Def_Rb, \
    Def_Sicherheit2

# pylint: disable=consider-using-in, no-else-return, too-many-statements, R0801


def Polynom(g1: float, g2: float, g3: float, g4: float,
            g5: float, Sondenabstand: float,
            g_Sondenabstand: float):
    # var
    #    pivot,BH,g10,g20,g30,g40,g50,ExA,ExB : float
    #    g,i,j                                  : int

    x = Vektor10()
    y = Vektor10()
    w = Vektor10()
    A = Matrix6()
    Ainv = Matrix6()

    g10 = g1
    g20 = g2
    g30 = g3
    g40 = g4
    g50 = g5
    if abs(Sondenabstand - g_Sondenabstand) > 0.05:
        #  Extrapolation der g-Function
        BH = Sondenabstand / g_Sondenabstand
        if BH < 0.4:
            _ErrorMldg = 1
        uMin = -4
        ExA = g5 - 6.29
        ExB = -log((g3 - 6.29) / (g5 - 6.6)) / 27
        g10 = Max(4.82 + ExA / BH * exp(-BH * ExB * 343), 4.82)
        if abs(g10 - 4.82) < 1.5:
            g10 = 4.82
        else:
            g10 = (g10 + 4.82) / 2
        g20 = Max(5.69 + ExA / BH * exp(-BH * ExB * 125), 5.69)
        g30 = Max(6.29 + ExA / BH * exp(-BH * ExB * 27), 6.29)
        g40 = Max(6.57 + ExA / BH * exp(-BH * ExB), 6.57)
        g50 = Max(6.6 + ExA / BH, 6.6)
        #  e Extrapolation g-Function
    # Berechnet die g-function aus 4 Stuetztstellen g1,g2,g3,g4
    x[1] = -4
    x[2] = -2
    x[3] = 0
    x[4] = 2.5
    x[5] = 3
    x[6] = min(-4.5, (-4 - (g10 - 4.82) / 2))
    uMin = max((x[6] + 0.5), -6)
    y[1] = g10
    y[2] = g20
    y[3] = g30
    y[4] = g40
    y[5] = g50 * 0.99
    y[6] = (log(0.5 / 0.0005) + 0.5 * x[6]) * 0.95
    y[4] = (y[4] + y[5]) / 2 * 0.99
    for i in range(1, 6 + 1):
        A[i, 1] = 1
        for j in range(2, 6 + 1):
            A[i, j] = A[i, j - 1] * x[i]

    # invertiert die 6 x 6 Matrix A nach der Diagonalen-Methode
    for i in range(1, 6 + 1):
        for j in range(1, 6 + 1):
            Ainv[i, j] = A[i, j]
    for g in range(1, 6 + 1):
        pivot = Ainv[g, g]
        for j in range(1, 6 + 1):
            Ainv[g, j] = Ainv[g, j] * (-1) / pivot
        for i in range(1, 6 + 1):
            for j in range(1, 6 + 1):
                if (i != g) and (j != g):
                    Ainv[i, j] = Ainv[g, j] * Ainv[i, g] + Ainv[i, j]
            Ainv[i, g] = Ainv[i, g] / pivot

        Ainv[g, g] = 1 / pivot
        # e invertieren
        # w = Ainv * y
    for i in range(1, 6 + 1):
        w[i] = 0
    for i in range(1, 6 + 1):
        for j in range(1, 6 + 1):
            w[i] = w[i] + Ainv[i, j] * y[j]

    return uMin, w[1:7]


def Max(x1: float, x2: float) -> float:
    if x1 > x2:
        return x1
    else:
        return x2


def _B(L, C, dt, DimAxi, DimRad):
    def MultiMatrix(Ainv: KMatrix, F: KMatrix, B: KMatrix, DimAxi: int, DimRad: int):
        """    ***********     B = Ainv x F *****       """
        # var i,j,k,l      : int

        for l in range(1, DimAxi + 1):
            for k in range(0, DimRad + 1 + 1):
                for i in range(0, DimRad + 1 + 1):
                    B[l, k, i] = 0
                    for j in range(
                            0, DimRad + 1 + 1):
                        B[l, k, i] = B[l, k, i] + \
                            Ainv[l, k, j] * F[l, j, i]

    def invertieren(A: KMatrix, Ainv: KMatrix, DimAxi: int, DimRad: int):
        """ Diese Procedure invertiert die n x n Matrix A nach der Diagonalen-Methode,
        **************     Ainv = 1/A und n = DimRad+1 *************************** """
        # var
        #  pivot      : float
        #  g,i,j,k    : int
        for k in range(1, DimAxi + 1):
            for i in range(0, DimRad + 1 + 1):
                for j in range(0, DimRad + 1 + 1):
                    Ainv[k, i, j] = A[k, i, j]
            for g in range(0, DimRad + 1 + 1):
                pivot = Ainv[k, g, g]
                for j in range(0, DimRad + 1 +
                               1):
                    Ainv[k, g, j] = Ainv[k, g, j] * (-1) / pivot
                for i in range(0, DimRad + 1 + 1):
                    for j in range(0, DimRad + 1 + 1):
                        if (i != g) and (j != g):
                            Ainv[k, i, j] = Ainv[k, g, j] * \
                                Ainv[k, i, g] + Ainv[k, i, j]
                    Ainv[k, i, g] = Ainv[k, i, g] / pivot

                Ainv[k, g, g] = 1 / pivot

    def DefMatrixA(L: Matrix, C: Matrix, dt: float, A: KMatrix,
                   DimAxi: int, DimRad: int):
        # var i,j,k : int

        for i in range(1, DimAxi + 1):
            for j in range(0, DimRad + 1 + 1):
                for k in range(0, DimRad + 1 + 1):
                    A[i, j, k] = 0
            A[i, 0, 0] = 1
            A[i, DimRad + 1, DimRad + 1] = 1
            for j in range(1, DimRad + 1):
                A[i, j, j] = 2 * C[i, j] + dt * (L[i, j] + L[i, j + 1])
                A[i, j, j - 1] = -dt * L[i, j]
                A[i, j, j + 1] = -dt * L[i, j + 1]

    def DefMatrixF(L: Matrix, C: Matrix, dt: float, F: KMatrix,
                   DimAxi: int, DimRad: int):
        # var i,j,k : int
        for i in range(1, DimAxi + 1):
            for j in range(0, DimRad + 1 + 1):
                for k in range(0, DimRad + 1 + 1):
                    F[i, j, k] = 0
            F[i, 0, 0] = 1
            F[i, DimRad + 1, DimRad + 1] = 1
            for j in range(1, DimRad + 1):
                F[i, j, j] = 2 * C[i, j] - dt * (L[i, j] + L[i, j + 1])
                F[i, j, j - 1] = dt * L[i, j]
                F[i, j, j + 1] = dt * L[i, j + 1]
    #  Definition der Matrizen, wobei A * Tneu = F * Talt
    A1 = KMatrix()
    Ainv1 = KMatrix()
    F1 = KMatrix()
    B1 = KMatrix()
    DefMatrixA(L, C, dt, A1, DimAxi, DimRad)  # Pumpe laeuft
    DefMatrixF(L, C, dt, F1, DimAxi, DimRad)
    invertieren(A1, Ainv1, DimAxi, DimRad)
    MultiMatrix(Ainv1, F1, B1, DimAxi, DimRad)

    return B1


def hoch(a: float, b: float) -> float:  # a^b : float
    return exp(b * log(abs(a)))


def r_grid(Sondendurchmesser, Bohrdurchmesser, Rechengebiet, Gitterfaktor, DimRad):
    r = VektorRad()
    r[0] = Sondendurchmesser / 2
    r[1] = Bohrdurchmesser / 2
    Faktor = Rechengebiet * (1 - Gitterfaktor) / \
        (1 - hoch(Gitterfaktor, DimRad - 1))
    for i in range(2, DimRad + 1):
        r[i] = r[i - 1] + Faktor * hoch(Gitterfaktor, i - 2)
    return r


def rz_grid(r, DimRad):
    rz = VektorRad()
    for i in range(1, DimRad + 1):
        rz[i] = sqrt((r[i]**2 + r[i - 1]**2) / 2)
    rz[0] = r[0]
    rz[DimRad + 1] = r[DimRad]
    return rz


def C_matrix(DimAxi, DimRad, r, dl, cpErde, rhoErde, cpFill=3040., rhoFill=1180.):
    C = Matrix()
    for i in range(1, DimAxi + 1):
        C[i, 1] = cpFill * rhoFill * pi_ * (r[1]**2 - 4 * r[0]**2) * dl
        for j in range(2, DimRad + 1):
            C[i, j] = cpErde[i] * rhoErde[i] * \
                pi_ * (r[j]**2 - r[j - 1]**2) * dl
    return C


def L1run_matrix(DimAxi, DimRad, L1run, L1stop, R2, lambdaErde, r, rz, dl, adiabat=0.):
    L1 = Matrix()
    L2 = Matrix()
    Llast = Vektor()
    for i in range(1, DimAxi + 1):
        L1[i, 1] = L1run
        L1[i, 2] = 1 / R2[i]
        for j in range(3, DimRad + 1):
            L1[i, j] = 1 / (log(rz[j] / rz[j - 1]) /
                            2 / pi_ / lambdaErde[i] / dl)
        Llast[i] = (1 - adiabat) / (1 / 2 / pi_ / dl /
                                    lambdaErde[i] * log(r[DimRad] / rz[DimRad]))
        L1[i, DimRad + 1] = Llast[i]
    for i in range(1, DimAxi + 1):
        L2[i, 1] = L1stop
        for j in range(2, DimRad + 1 + 1):
            L2[i, j] = L1[i, j]
    return L1, L2


def resistances(DimAxi, R1, dl, r, rz, alpha, lambdaErde, lambdaSole=Def_lambdaSole,
                lambdaFill=Def_lambdaFill,
                Ra=Def_Ra, Rb=Def_Rb,
                Sondendurchmesser=Def_Sondendurchmesser):
    R2 = Vektor()
    if (Ra > 0) and (Rb > 0):
        R1 = Ra / 4 / dl
        for i in range(1, DimAxi + 1):
            R2[i] = (Rb - Ra / 4) / dl + 1 / 2 / pi_ / \
                dl * log(rz[2] / r[1]) / lambdaErde[i]
        L1run = 1 / R1
        L1stop = 1 / (R1 - 1 / 8 / pi_ / alpha / r[0] / dl +
                      1 / 8 / pi_ / alpha0(lambdaSole, Sondendurchmesser) / r[0] / dl)
    elif Rb > 0:
        R1 = Rb / dl - 1 / 2 / pi_ / dl * log(r[1] / rz[1]) / lambdaFill
        for i in range(1, DimAxi + 1):
            R2[i] = 1 / 2 / pi_ / dl * \
                (log(r[1] / rz[1]) / lambdaFill +
                 log(rz[2] / r[1]) / lambdaErde[i])
        L1run = 1 / R1
        L1stop = 1 / (R1 - 1 / 8 / pi_ / alpha / r[0] / dl +
                      1 / 8 / pi_ / alpha0(lambdaSole, Sondendurchmesser) / r[0] / dl)
        Ra = R1 * 4 * dl
    elif R1 > 0:
        for i in range(1, DimAxi + 1):
            R2[i] = 1 / 2 / pi_ / dl * \
                (log(r[1] / rz[1]) / lambdaFill +
                 log(rz[2] / r[1]) / lambdaErde[i])
        L1run = 1 / R1
        L1stop = 1 / (R1 - 1 / 8 / pi_ / alpha / r[0] / dl +
                      1 / 8 / pi_ / alpha0(lambdaSole, Sondendurchmesser) / r[0] / dl)
        Ra = R1 * 4 * dl
        Rb = R1 * dl + 1 / 2 / pi_ * log(r[1] / rz[1]) / lambdaFill
    else:
        R1 = 1 / 8 / pi_ / dl * \
            (1 / alpha / r[0] + log((r[1] - rz[1]) / r[0]) / lambdaFill)
        for i in range(1, DimAxi + 1):
            R2[i] = 1 / 2 / pi_ / dl * \
                (log(r[1] / rz[1]) / lambdaFill +
                 log(rz[2] / r[1]) / lambdaErde[i])
        L1run = 1 / R1
        L1stop = 8 / (1 / pi_ / alpha0(lambdaSole, Sondendurchmesser) / r[0] / dl +
                      log((r[1] - rz[1]) / r[0]) / pi_ / lambdaFill / dl)
        Ra = R1 * 4 * dl
        Rb = R1 * dl + 1 / 2 / pi_ * log(r[1] / rz[1]) / lambdaFill

    return L1run, L1stop, R1, R2


def alpha0(lambdaSole: float, Sondurchmesser: float) -> float:
    """  Waermeuebergang, wenn Pumpe steht """
    return lambdaSole / (Sondurchmesser / 2 * (1 - sqrt(0.5)))


def alpha1(NueSole: float, rhoSole: float, cpSole: float, lambdaSole, Massenstrom: float,
           Sondurchmesser: float, Dicke_Sondenrohr: float) -> float:
    #  Function alpha1: Waermeuebergang Sole-Hinterfuellung, wenn Pumpe laeuft
    # var x,Geschw,Re,Pr,Nu_turbulent,Nu_laminar,
    #    Nu0,Nu,Di,St,Xi0,Xi,K1,K2,K10,St0       : float

    Di = Sondurchmesser - 2 * Dicke_Sondenrohr
    Geschw = 2 * Massenstrom / rhoSole / Di**2 / pi_
    Re = Geschw * Di / NueSole  # Reynoldszahl
    Pr = NueSole * rhoSole * cpSole / lambdaSole  # Prandtlzahl
    #  Xi = Druckverlustkoeffizient nach Petukhov (1970)
    Xi = 1 / 1.82 * log(Re**2 / log(10) - 1.64)
    #  Stantonzahl nach Petukhov (1970), gueltig fuer turbulenten Bereich
    K1 = 1 + 27.2 * Xi / 8
    K2 = 11.7 + 1.8 / hoch(Pr, 1 / 3)
    St = Xi / 8 / (K1 + K2 * sqrt(Xi / 8) *
                   (hoch(Pr, 2 / 3) - 1))  # Stantonzahl
    #  Stantonzahl nach Petukhov an der Grenze turbulent-Uebergangszone
    Xi0 = 0.031437
    K10 = 1.106886
    ST0 = Xi0 / 8 / (K10 + K2 * sqrt(Xi0 / 8) * (hoch(Pr, 2 / 3) - 1))
    Nu0 = ST0 * 10000 * Pr  # Nusseltzahl beim Uebergang turbulent-Uebergangszone
    Nu_turbulent = St * Re * Pr  # Nusseltzahl turbulente Zone
    Nu_laminar = 4.36  # Nusseltzahl laminare Zone
    if Re >= 10000:
        Nu = Nu_turbulent  # turbulent
    if Re <= 2300:
        Nu = Nu_laminar  # laminar
     # Uebergangszone laminar/turbulent
    else:
        if Re < 10000:
            Nu = Nu_laminar \
                * exp(log(Nu0 / Nu_laminar) / log(10000 / 2300) * log(Re / 2300))
    x = Nu * lambdaSole / Di
    return x


def Optimaler_Zeitfaktor(DimAxi, Zeitschritt, L: Matrix, C: Matrix, stationaer=False,
                         Sicherheit2=Def_Sicherheit2) -> int:
    # var i,Optfak                 : int
    #     Mindx,Mindt,Mindt2       : float

    Mindt = 3600
    for i in range(1, DimAxi + 1):
        Mindt2 = C[i, 1] / L[i, 2] / Sicherheit2
        if Mindt2 < Mindt:
            Mindt = Mindt2
        Mindt2 = C[i, 2] / L[i, 2] / Sicherheit2
        if Mindt2 < Mindt:
            Mindt = Mindt2
        if not stationaer:
            Mindt2 = C[i, 1] / L[i, 1] / Sicherheit2
        else:
            Mindt2 = C[i, 1] / L[i, 1] / Sicherheit2 * 1.0
        if Mindt2 < Mindt:
            Mindt = Mindt2

    Optfak = int(Zeitschritt * 60 / Mindt)
    if Optfak == 0:
        Optfak = 1
    return Optfak


def Anfangstemp(TMittel: float, TGrad: float, dl: float,
                qEntzug: Vektor,
                TEarth: Matrix,
                T0: Vektor, TUp: Vektor, TUpold: Vektor, TDown: Vektor, TDownOld: Vektor,
                _TSource: float,
                DimAxi: int, DimRad: int, StartJahr: int,
                gpar1, gpar2, gpar3, gpar4, gpar5, gpar6,
                lambdaErd, rhoErd, cpErd, uMin, rz, Sondenlaenge):
    """ Anfangstemp:    Ungestoerte Erde """
    # var i,j      : integer;
    # ts,u     : real;
    # go,g1    : real;
    g = VektorRad()
    Rq = VektorRad()
    ts = (dl * DimAxi)**2 / 9 / lambdaErd * rhoErd * cpErd
    if StartJahr > 0:
        u = log(StartJahr * 365) + log(24 * 3600) - log(ts)
    else:
        u = 0.
    if u > 2.5:
        u = 2.5
    go = 0.5 * u + 6.907755
    if u < uMin:
        g1 = go
    else:
        g1 = gpar1 + gpar2 * u + gpar3 * u**2 + gpar4 * u**3 +\
            gpar5 * u**4 + gpar6 * u**5
    if u < -2:
        if (go - 0.3) > g1:
            g1 = go
    for j in range(DimRad + 2):
        g[j] = g1 - log(rz[j] / dl / DimAxi / 0.0005)
        if StartJahr == 0:
            Rq[j] = 0
        else:
            Rq[j] = g[j] / 2 / pi_ / lambdaErd
    for i in range(1, DimAxi + 1):
        for j in range(DimRad + 2):
            TEarth[i, j] = TMittel + (i * dl - dl / 2) * TGrad - \
                qEntzug[i] / Sondenlaenge * DimAxi * Rq[j]
        T0[i] = TEarth[i, DimRad + 1]
        TUp[DimAxi - i + 1] = TEarth[i, 0]
        TUpold[DimAxi - i + 1] = TEarth[i, 0]
        TDown[i] = TEarth[i, 0]
        TDownOld[i] = TEarth[i, 0]
