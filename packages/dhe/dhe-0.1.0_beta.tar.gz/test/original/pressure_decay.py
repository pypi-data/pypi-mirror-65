from math import pi as pi_, log


def pressure_decay(Massenstrom: float, nu_brine: float, RhoSole: float,
                   Sondendurchmesser: float,
                   Dicke_Sondenrohr: float,
                   Sondenlaenge: float) -> (float, bool):
    Di = Sondendurchmesser - 2 * Dicke_Sondenrohr
    wi = Massenstrom / 2 / pi_ / (Di / 2)**2 / RhoSole
    Re = wi * Di / nu_brine
    laminar = False

    if Re > 0:
        if Re < 2300:
            Xi = 64 / Re
            laminar = True
        else:
            Xi = 1 / (1.82 * log(Re) / log(10) - 1.64)**2  # Petukhov, 1970
    else:
        Xi = 0
    return 0.5 * Sondenlaenge * Xi / Di * RhoSole * wi**2, laminar
