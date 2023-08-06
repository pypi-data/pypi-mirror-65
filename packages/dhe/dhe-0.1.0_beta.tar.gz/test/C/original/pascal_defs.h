#ifndef __PASCAL_DEFS_H__
#define __PASCAL_DEFS_H__

#define DimRadMax 6
#define DimAxiMax 4          // maximal 10 moeglich
#define MaxJahre 9
#define Default -3
#define OpenFile -2
#define Initial -1
#define CloseFile -4         // Nur fuer Pascal - Version
#define Stoffdaten -5
#define ErzeugeLastprofil -6
#define Def_Sicherheit1 4         // Zeitschritt Sole, Empfohlen: 4
#define Def_Sicherheit2 2         // Zeitschritt Erde, Empfohlen: 2
#define Def_DimRad 5         // Radiale Unterteilung, Max: 5
#define Def_DimAxi 1         // Axiale Unterteilung, Max: 4
#define Def_cpSole 3875      // Wasser: 4200 J/kgK
                                            // 33%Etylenglykol: 3800 J/kgK
#define Def_cpFill 3040      // J/kgK
#define Def_cpErde 1000      // J/kgK
#define Def_rhoSole 1050.      // kg/m3
#define Def_rhoFill 1180      // kg/m3
#define Def_rhoErde 2600      // kg/m3
#define Def_lambdaSole 0.449     // W/mK
#define Def_lambdaFill 0.81      // W/mK
#define Def_lambdaErde 2.0       // W/mK
#define Def_nueSole 0.00000415// Wasser: 0.00000175 m2/s
                                            // 33%Ethylenglykol:ca0.000006 m2/s
#define Def_RepRandbed 1         // Anzahl Wochen
#define Def_Rechenradius 1.5       // m
#define Def_Gitterfaktor 2.0       // Gitter in Erde, radial
#define Def_AnzahlSonden 1         // Anzahl Sonden
#define Def_Sondenlaenge 100.       // m
#define Def_Sondendurchmesser 0.026     // m
#define Def_Dicke_Sondenrohr 0.000     // m
#define Def_Bohrdurchmesser 0.115     // m
#define Def_R1 0.0       // K/W, therm. Widerstand R1
#define Def_Ra 0.0       // Km/W, thermal pipe resistance Ra
#define Def_Rb 0.1       // Km/W, borhole thermal resistance
#define Def_Massenstrom 0.4       // kg/s, Solemassenstrom pro Sonde
#define Def_TGrad 0.03      // K/m, Temperaturgradient axial
#define Def_Jahresmitteltemp 9.0       // øC, Mittel Lufttemperatur
#define Def_Bodenerwaermung 0.8       // øC, Boden waermer als Luft
#define Def_DeltaT 0.0       // øC, Abkuehlung in der Waermepumpe
#define Def_TSource 0.0       // øC, Quellentemperatur
#define Def_TSink 4.0       // øC, Ruecklauftemp.(ohne Inputfile)
#define Def_QSource 5.0       // kW, Entzug (ohne Inputfile)
#define Def_Zeitschritt 60        // Min
#define Def_Simulationsdauer 8760      // h, totale Simulationszeit
#define Def_readFile true
#define Def_writeFile true
#define Def_Allsteps false     // Auch Einschwingen aufschreiben
#define Def_MonitorAxi 1
#define Def_MonitorRad 1
#define Def_Einschwingen false
#define Def_Leistungsinput false     // Entzugsleistung aus Inputfile
#define Def_Leistung false     // Rechnen mit Entzugsleistung
#define Def_stationaer false     // Stationaere Berechnung der Sole
#define Def_Genauigkeit 0.05      // øC, Iteration Leistungsberech.
#define Def_Sprache 'D'
#define Def_StepWrite 1         // Ausgabeschritte: 2 fuer jede 2te
#define Def_Jahr 1         // Beginn der Simulation
#define Def_adiabat 0.0       // Anteil adiabater Randbed. 0..1
#define Def_Druck true      // Wird der Druckabfall berechnet?
#define Def_g1 4.82      // g-function bei ln(t/ts) = -4
#define Def_g2 5.69      // g-function bei ln(t/ts) = -2
#define Def_g3 6.29      // g-function bei ln(t/ts) = 0
#define Def_g4 6.57      // g-function bei ln(t/ts) = +2
#define Def_g5 6.60      // g-function bei ln(t/ts) = +3
#define Def_gfunction true      // Randbedingung mit g-functions
#define Def_Sondenabstand 10        // m, eff. Abstand der Sondenen
#define Def_g_Sondenabstand 10        // m, Sondenabstand der g-function
#define Def_Starttemp false     // Erdreichtemp. abschaetzen
#define Def_LastYear 1         // Simulationsdauer in Jahren
#define Def_AlteInputfiles false     // Alter, kurzer Eingabefilekopf
#define Def_swewsInput false     // Liest Stoffwerte von SWEWS.DAT
#define Def_Laufzeit_Jan 12        // h, taegliche Sondenlaufziet Jan
#define Def_Laufzeit_Feb 11        // h, taegliche Sondenlaufziet Feb
#define Def_Laufzeit_Mar 9         // h, taegliche Sondenlaufziet Mar
#define Def_Laufzeit_Apr 7         // h, taegliche Sondenlaufziet Apr
#define Def_Laufzeit_Mai 3         // h, taegliche Sondenlaufziet Mai
#define Def_Laufzeit_Jun 2         // h, taegliche Sondenlaufziet Jun
#define Def_Laufzeit_Jul 2         // h, taegliche Sondenlaufziet Jul
#define Def_Laufzeit_Aug 2         // h, taegliche Sondenlaufziet Aug
#define Def_Laufzeit_Sep 3         // h, taegliche Sondenlaufziet Sep
#define Def_Laufzeit_Okt 7         // h, taegliche Sondenlaufziet Okt
#define Def_Laufzeit_Nov 9         // h, taegliche Sondenlaufziet Nov
#define Def_Laufzeit_Dez 11        // h, taegliche Sondenlaufziet Dez
#define Def_QSpitzeFeb 5         // kW, Spitzenentzug im Februar
#define Def_DauerLastspitze 4         // Tage, Dauer der Lastspitzen


typedef double Vektor[DimAxiMax];
typedef double Matrix[DimAxiMax][DimRadMax+1];
typedef double KMatrix[DimAxiMax][DimRadMax+1][DimRadMax+1];
typedef double MatrixQ[DimAxiMax][53*MaxJahre];
typedef double Vektor10[10];

#endif //__PASCAL_DEFS_H__
