from .pascal_defs import Matrix, KMatrix, Vektor
from .tbrine import TBRINE
from .boundary_gfunc import RandAussen_gfunc
from .boundary import RandAussen


def WriteStep(*_args):
    pass


def ReadStep(*_args):
    pass

# pylint: disable=consider-using-in, no-else-return, too-many-statements, too-many-nested-blocks, simplifiable-if-statement, line-too-long


def calculateEWS(Iteration: int, DimAxi: int, DimRad: int,
                 MonitorAxi: int, MonitorRad: int,
                 TEarthOld: Matrix,
                 TEarth: Matrix,
                 TUp: Vektor,
                 TupOld: Vektor,
                 TDownOld: Vektor,
                 TDown: Vektor,
                 Q0Old: Vektor,
                 Q0: Vektor,
                 TSourceOld: float,
                 TSource: float,
                 TSourceMin: float,
                 TSourceMax: float,
                 TSink: float,
                 TSinkMin: float,
                 TSinkMax: float,
                 QSource: float,
                 Massenstrom: float,
                 cpSole: float,
                 p: float,
                 laminar: bool,
                 readFile: bool,
                 simstep: int,
                 StepWrite: int,
                 einschwingen: bool,
                 Allsteps: bool,
                 writeFile: bool,
                 Leistung: bool,
                 gfunction: bool,
                 RepRandbed,
                 Zeitschritt,
                 Jahr,
                 numrows,
                 Starttemp: bool,
                 DeltaT,
                 subdt,
                 AnzahlSonden,
                 Rechenradius,
                 stationaer: bool,
                 mcpSole: float,
                 substep_run: int,
                 L1run,
                 substep_stop: int,
                 L1stop,
                 lambdaErde,
                 rhoErde,
                 cpErde,
                 Q,
                 T0,
                 B1, B2,
                 Tneu,
                 gpar6,
                 gpar5,
                 gpar4,
                 gpar3,
                 gpar2,
                 gpar1,
                 Sondenlaenge,
                 TMonitor,
                 u_min
                 ):
    QWand = Vektor()
    if Iteration == 0:
        for i in range(1, DimAxi + 1):
            for j in range(1, DimRad + 1):
                TEarthOld[i, j] = TEarth[i, j]
            TupOld[i] = TUp[i]
            TDownOld[i] = TDown[i]
            Q0Old[i] = Q0[i]
    else:
        for i in range(1, DimAxi + 1):
            for j in range(1, DimRad + 1):
                TEarth[i, j] = TEarthOld[i, j]
            TUp[i] = TupOld[i]
            TDown[i] = TDownOld[i]
            Q0[i] = Q0Old[i]

    if Iteration == 0:
        if not readFile:
            filestep = simstep - 1
        if simstep > 1:
            if ((not einschwingen) or Allsteps):
                if TSource < TSourceMin:
                    TSourceMin = TSource
                if TSource > TSourceMax:
                    TSourceMax = TSource
                if TSink < TSinkMin:
                    TSinkMin = TSink
                if TSink > TSinkMax:
                    TSinkMax = TSink
                if writeFile:
                    if ((simstep - 1) % StepWrite) == 0:
                        if Leistung:
                            if Massenstrom > 0.0001:
                                TSink = TSource - QSource * 1000 / Massenstrom / cpSole
                            else:
                                TSink = TSource
                        else:
                            QSource = (TSource - TSink) * \
                                Massenstrom * cpSole / 1000
                        WriteStep(filestep, Massenstrom, TSink, QSource, TSource,
                                  TEarth[MonitorAxi, MonitorRad], p, laminar)
        if readFile:
            ReadStep(filestep, Massenstrom, TSink, QSource)
        if DeltaT != 0:
            TSink = TSourceOld - DeltaT

    if Iteration > -1:
        Summe_TSource = 0
        if not Starttemp:
            Woche = (simstep + numrows * (Jahr - 1) -
                     1) // (10080 // Zeitschritt * RepRandbed) + 1
            simstepn = (simstep + numrows * (Jahr - 1)
                        ) % (10080 // Zeitschritt * RepRandbed)
        else:
            Woche = (simstep - 1) // (10080 // Zeitschritt * RepRandbed) + 1
            simstepn = (simstep) % (10080 // Zeitschritt * RepRandbed)
        if simstepn == 0:
            simstepn = 10080 // RepRandbed // Zeitschritt
        # Rechengebiet = Rechenradius - Bohrdurchmesser / 2
        L0 = cpSole * Massenstrom / AnzahlSonden
        if Massenstrom > 0.00001:
            Pumpelauft = True
        else:
            Pumpelauft = False
        for idt in range(1, subdt + 1):
            # calculate brine Temperature
            if Pumpelauft:
                TSource[()] = TBRINE(TEarth, TDown, TUp, TSink, L0, L1run, None, Zeitschritt, subdt,
                                     substep_run, QWand, mcpSole, None, None, DimAxi, stationaer, False)
                for i in range(1, DimAxi + 1):
                    TEarth[i, 0] = TEarth[i, 1] - QWand[i] / \
                        L1run[i] / Zeitschritt / 60 * subdt
            else:
                TSource[()] = TBRINE(TEarth, TDown, TUp, 0, 0, L1stop, None, Zeitschritt, subdt,
                                     substep_stop, QWand, mcpSole, None, None, DimAxi, stationaer, False)
                for i in range(1, DimAxi + 1):
                    TEarth[i, 0] = TEarth[i, 1] - \
                        QWand[i] / L1stop / Zeitschritt / 60 * subdt
            # print("[]", QWand[1:-1] / Zeitschritt / 60 * subdt)
            for i in range(1, DimAxi + 1):
                # calculate temperature at outer boudary condition at each RepRandBed
                Q0[i] = (Q0[i] * ((simstepn - 1) * subdt + (idt - 1)) +
                         QWand[i] * subdt / Zeitschritt / 60) / ((simstepn - 1) * subdt + idt)
                if Iteration == 0:
                    if idt == subdt:
                        if ((simstep + numrows * (Jahr - 1)) * Zeitschritt) % (60 * 24 * 7 * RepRandbed) == 0:
                            Q[i, Woche] = Q0[i]
                            if gfunction:
                                TRT = RandAussen_gfunc(i, Woche,
                                                       #Zeitschritt, (simstep + numrows * (Jahr - 1)),
                                                       RepRandbed, Q, cpErde[i], rhoErde[i],
                                                       lambdaErde[i], Rechenradius,
                                                       Sondenlaenge,
                                                       gpar1, gpar2, gpar3, gpar4, gpar5, gpar6,
                                                       DimAxi, uMin=u_min)
                            else:
                                TRT = RandAussen(i, Woche,
                                                 #Zeitschritt, (simstep + numrows * (Jahr - 1)),
                                                 RepRandbed,
                                                 Q, cpErde[i], rhoErde[i], lambdaErde[i],
                                                 Rechenradius, Sondenlaenge, DimAxi)
                            TEarth[i, DimRad + 1] = T0[i] + TRT
                # calulate earth temperature
                if Pumpelauft:
                    multiplizieren(B1, TEarth, Tneu, i, DimRad)
                else:
                    multiplizieren(B2, TEarth, Tneu, i, DimRad)
                for j in range(1, DimRad + 1):
                    TEarth[i, j] = Tneu[i, j]
            Summe_TSource = Summe_TSource + TSource

        # avarage source temperature *)
        TSource[()] = Summe_TSource / subdt
        TSourceOld[()] = TSource
        TMonitor[()] = TEarth[MonitorAxi, MonitorRad]


def multiplizieren(M: KMatrix, w: Matrix, y: Matrix, k: int, DimRad: int):
   #    ***********    y = M x w       ************
    y[k, 0] = w[k, 0]
    y[k, DimRad + 1] = w[k, DimRad + 1]
    for i in range(1, DimRad + 1):
        y[k, i] = 0
        for j in range(DimRad + 2):
            y[k, i] = y[k, i] + M[k, i, j] * w[k, j]
