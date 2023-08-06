from .pascal_defs import Vektor10, Vektor, Matrix


def TBRINE(T: Matrix,
           TDown: Vektor,
           TUp: Vektor,
           TSink: float,
           L0: float,
           L, La: Vektor10,
           Zeitschritt: int, subdt: int, substep: int,
           QWand: Vektor,
           mcpSole: float, mcpSoleUp: float, mcpSoleDown: float,
           DimAxi: int,
           stationaer: bool,
           KoaxialSonde: bool
           ) -> float:
    # var i, k: integer
    #    TOut, dt2, Lm0, Lm1, LmMin, L0mcpdt, Nichtad: float
    SummeT = Vektor()
    Td = Vektor()
    Tu = Vektor()
    dTa = Vektor()
    dt2 = Zeitschritt * 60 / subdt / substep  # [s]
    TDown[0] = TSink
    TOut = 0
    L0mcpdt = L0 / mcpSole * dt2
    for i in range(1, DimAxi + 1):
        SummeT[i] = 0
    for _step in range(1, substep + 1):
        if KoaxialSonde:  # KoaxialSonde: Neu 10.1.2000
            for i in range(1, DimAxi + 1):
                Td[i] = (T[i, 1] - TDown[i]) * L[i] / mcpSoleDown * dt2
                if stationaer:
                    TDown[i] = (L[i] * T[i, 1] + L0 * TDown[i - 1] +
                                La[i] * TUp[1 + DimAxi - i]) / (L[i] + L0 + La[i])
                else:
                    dTa[i] = (TUp[1 + DimAxi - i] - TDown[i])
                    TDown[i] = TDown[i] + \
                        (TDown[i - 1] - TDown[i]) * L0 / mcpSoleDown * dt2 \
                        + dTa[i] * La[i] / mcpSoleDown * dt2 + Td[i]
                Td[i] = (T[i, 1] - TDown[i]) * L[i] / mcpSoleDown * dt2
            TUp[0] = TDown[DimAxi]
            for i in range(1, DimAxi + 1):
                if stationaer:
                    TUp[i] = (La[1 + DimAxi - i] * TDown[1 + DimAxi - i] +
                              L0 * TUp[i - 1]) / (La[1 + DimAxi - i] + L0)
                else:
                    TUp[i] = TUp[i] + (TUp[i - 1] - TUp[i]) * \
                        L0 / mcpSoleUp * dt2 \
                        - dTa[1 + DimAxi - i] * \
                        La[1 + DimAxi - i] / mcpSoleUp * dt2
                    # dTa[1 + DimAxi - 1] -> dTa[1 + DimAxi - i]
            for i in range(1, DimAxi + 1):
                SummeT[i] = SummeT[i] + Td[i]
            TOut = TOut + TUp[DimAxi]
        # Koaxialsonde: # Ende des neuen Teils
        else:  # doppel - U - Sonde
            for i in range(1, DimAxi + 1):
                Td[i] = (T[i, 1] - TDown[i]) * L[i] / 2 / mcpSole * dt2
                if stationaer:
                    TDown[i] = (L[i] / 2 * T[i, 1] + L0 *
                                TDown[i - 1]) / (L[i] / 2 + L0)
                else:
                    TDown[i] = TDown[i] + \
                        (TDown[i - 1] - TDown[i]) * L0mcpdt + Td[i]
                Td[i] = (T[i, 1] - TDown[i]) * L[i] / 2 / mcpSole * dt2
            TUp[0] = TDown[DimAxi]
            for i in range(1, DimAxi + 1):
                Tu[i] = (T[1 + DimAxi - i, 1] - TUp[i]) * \
                    L[1 + DimAxi - i] / 2 / mcpSole * dt2
                if stationaer:
                    TUp[i] = (L[1 + DimAxi - i] / 2 * T[1 + DimAxi - i, 1] +
                              L0 * TUp[i - 1]) / (L[1 + DimAxi - i] / 2 + L0)
                else:
                    TUp[i] = TUp[i] + \
                        (TUp[i - 1] - TUp[i]) * L0mcpdt + Tu[i]
                Tu[i] = (T[1 + DimAxi - i, 1] - TUp[i]) * \
                    L[1 + DimAxi - i] / 2 / mcpSole * dt2
            for i in range(1, DimAxi + 1):
                SummeT[i] = SummeT[i] + Td[i] + Tu[1 + DimAxi - i]
            TOut = TOut + TUp[DimAxi]
        #(*** Ende Doppel - U - Sonde ** ***********************)
    if KoaxialSonde:
        for i in range(1, DimAxi + 1):
            QWand[i] = SummeT[i] * mcpSoleDown
    else:
        for i in range(1, DimAxi + 1):
            QWand[i] = SummeT[i] * mcpSole
    TOut = TOut / substep
    return TOut
