from .pascal_defs import Vektor12

# pylint: disable=line-too-long


def InputFileErzeugen(Inputfile,
                      Laufzeit: Vektor12,
                      Massenstrom: float,
                      Sondenleistung: float,
                      TSink: float, QSpitzeFeb: float,
                      # var
                      Sondenlaufzeit: float,
                      DauerLastSpitze: int,
                      Zeitschritt: int,
                      numrows: int):
    """ Erzeugen eines Inputfiles mit stuendlichem Lastprofil """
    # var k     : integer;
    #    l     : string;
    #    t,t1 : text;
    Monatslaenge = (None, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

    # def Monatslaenge(Month: int) -> integer:
    # var i: integer;
    # case Month of 1 : i:= 31; 2 : i:= 28; 3 : i:= 31; 4 : i:= 30;
    #   5 : i:= 31; 6 : i:= 30; 7 : i:= 31; 8 : i:= 31;
    #   9 : i:= 30; 10 : i:= 31; 11 : i:= 30; 12 : i:= 31;   end;
    # Monatslaenge = i  # Tage
    # end;
    _Monatsbeginn = (None, 0, 31, 59, 90, 120, 151,
                     181, 212, 243, 273, 304, 334)

    def Monatsbeginn(Month: int) -> int:
        return 1 + 24 * _Monatsbeginn[Month]

    # Function Monatsbeginn(Month : integer):integer;
    # var i: integer;
    # begin
    #  case Month of 1 : i:= 0;     2 : i:= 31;    3 : i:= 59;  4 : i:= 90;
    # 5 : i:= 120; 6 : i:= 151; 7 : i:= 181; 8 : i:= 212;
    # 9 : i:= 243; 10 : i:= 273; 11 : i:= 304; 12 : i:= 334;      end;
    # Monatsbeginn:=1+24*i; (* Stunden *)
    # end;

    def Entzugsprofil(  # var
            t, Monat: int, Laufzeit: Vektor12, m: float, Q: float):
      # var Tag,j : integer;
        for Tag in range(1, Monatslaenge[Monat] + 1):                    # Januar
            if Laufzeit[Monat] > 24:
                Laufzeit[Monat] = 24
            for j in range(1, round(Laufzeit[Monat]) + 1):
                if Monat == 2:
                    if Tag > (Monatslaenge[Monat] - DauerLastSpitze):
                        writeln(t, Monatsbeginn(Monat) - 1 + 24 *
                                (Tag - 1) + j, "\t", m, "\t", TSink, "\t", QSpitzeFeb)
                    else:
                        writeln(
                            t, Monatsbeginn(Monat) - 1 + 24 * (Tag - 1) + j, "\t", m, "\t", TSink, "\t", Q)
                else:
                    writeln(
                        t, Monatsbeginn(Monat) - 1 + 24 * (Tag - 1) + j, "\t", m, "\t", TSink, "\t", Q)
            if Laufzeit[Monat] < 24:
                for j in range(round(Laufzeit[Monat]) + 1, 25):
                    if Monat == 2:
                        if Tag > (Monatslaenge[Monat] - DauerLastSpitze):
                            writeln(t, Monatsbeginn(
                                Monat) - 1 + 24 * (Tag - 1) + j, "\t", m, "\t", TSink, "\t", QSpitzeFeb)
                        else:
                            writeln(t, Monatsbeginn(Monat) - 1 + 24 *
                                    (Tag - 1) + j, "\t", 0.0, "\t", TSink, "\t", 0.0)
                    else:
                        writeln(t, Monatsbeginn(Monat) - 1 + 24 *
                                (Tag - 1) + j, "\t", 0.0, "\t", TSink, "\t", 0.0)

    # Procedure InputFileErzeugen
    _Leistungsinput = True
    _Leistung = True
    Sondenlaufzeit[()] = 0
    for k in range(1, 13):
        Sondenlaufzeit[()] = Sondenlaufzeit + Laufzeit[k] * Monatslaenge[k] \
            + DauerLastSpitze * (24 - Laufzeit[2])
    ofile = OpenOutputFile(Inputfile, Zeitschritt, numrows)
    for k in range(1, 13):
        Entzugsprofil(ofile, k, Laufzeit, Massenstrom, Sondenleistung)
    close(ofile)


def writeln(t, *args):
    t.append(tuple(a for a in args if a != "\t"))


def OpenOutputFile(Inputfile, *_):
    return Inputfile


def close(*_):
    pass
