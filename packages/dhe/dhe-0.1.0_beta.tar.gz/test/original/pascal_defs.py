import numpy
DimRadMax = 5
DimAxiMax = 4          # maximal 10 moeglich
MaxJahre = 9
Def_Zeitschritt = 60  # min
Def_Simulationsdauer = 8760  # h, totale Simulationszeit
Def_Sicherheit1 = 4  # Zeitschritt Sole, Empfohlen: 4
Def_Sicherheit2 = 2  # Zeitschritt Erde, Empfohlen: 2
Def_RepRandbed = 1  # Anzahl Wochen
Def_Sondendurchmesser = 0.026
Def_g1 = 4.82      # g-function bei ln(t/ts) = -4
Def_g2 = 5.69      # g-function bei ln(t/ts) = -2
Def_g3 = 6.29      # g-function bei ln(t/ts) = 0
Def_g4 = 6.57      # g-function bei ln(t/ts) = +2
Def_g5 = 6.60      # g-function bei ln(t/ts) = +3
Def_nueSole = 0.00000415  # Wasser: 0.00000175 m2/s
Def_AnzahlSonden = 1  # Anzahl Sonden
Def_Starttemp = False
Def_Sondenabstand = 10  # m, eff. Abstand der Sondenen
Def_g_Sondenabstand = 10  # m, Sondenabstand der g-function
Def_Sondenlaenge = 100  # m
Def_Gitterfaktor = 2.0  # Gitter in Erde, radial
Def_Bohrdurchmesser = 0.115  # m
Def_Rechenradius = 1.5  # m
Def_lambdaSole = 0.449  # W/mK
Def_lambdaFill = 0.81  # W/mK
Def_lambdaErde = 2.0  # W/mKx
Def_cpErde = 1000  # J/kgK
Def_rhoErde = 2600  # kg/m3
Def_cpSole = 3875  # J/kgK
Def_rhoSole = 1050  # kg/m3
Def_cpFill = 3040  # J/kgK
Def_rhoFill = 1180  # kg/m3
Def_adiabat = 0.0  # Anteil adiabater Randbed. 0..1
Def_Jahresmitteltemp = 9.0  # °C, Mittel Lufttemperatur
Def_Bodenerwaermung = 0.8  # °C, Boden waermer als Luft
Def_QSource = 5.0  # kW, Entzug (ohne Inputfile)
Def_DeltaT = 0.0       # C, Abkuehlung in der Waermepumpe
Def_Ra = 0.0  # Km/W, thermal pipe resistance Ra
Def_Rb = 0.1  # Km/W, borhole thermal resistance
Def_AnzahlSonden = 1  # Anzahl Sonden
Def_Massenstrom = 0.4  # kg/s, Solemassenstrom pro Sonde


def Vektor10(x=None):
    v = numpy.zeros(10)
    if x is not None:
        v[1:x.size + 1] = x
    return v


def Vektor12():
    return numpy.zeros(12, dtype=int)


def Vektor():
    return numpy.zeros(DimAxiMax + 1)


def Matrix():
    return numpy.zeros((DimAxiMax + 1, DimRadMax + 2))


def KMatrix():
    return numpy.zeros((DimAxiMax + 1, DimRadMax + 2, DimRadMax + 2))


def MatrixQ():
    return numpy.zeros((DimAxiMax + 1, 53 * MaxJahre + 1))


MatrixQ.py_data = lambda x, DimAxi: x[1:DimAxi]


def VektorRad():
    return numpy.zeros(DimRadMax + 2)


def Matrix6():
    return numpy.zeros((7, 7))
