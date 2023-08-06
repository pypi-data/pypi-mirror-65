import os
import importlib
from typing import Callable

from dataclasses import asdict

import numpy

from .model import DHEConfiguration, PCalculationMode, \
    PCalculationMonthlyLoadMode
from .enum_map import EnumMap

BACKEND = os.environ.get("BACKEND", "rs")
m = importlib.import_module("." + BACKEND, "dhe.backends")
calc_P = m.calc_P

profile_loader = EnumMap(Callable)
g_implementation = EnumMap(Callable)
T_brine_calc_method = EnumMap(Callable)


def calc(cfg: DHEConfiguration):
    mode_args = cfg.calculation_mode
    _loader, calc_method = profile_loader.items[type(mode_args)]
    loader_args = asdict(mode_args)
    routine_args = loader_args.pop("arguments", None)
    t, X = _loader(**loader_args)
    _t = numpy.arange(t[0], t[-1]+cfg.dt, cfg.dt)
    _X = numpy.interp(_t, t, X)
    return calc_method(_t, _X, cfg.dhe, cfg, **routine_args)


def unpack_load(*cols_names):
    def _load(load_file):
        return load_csv(load_file, cols_names)
    return _load


def load_csv(file_name, _colnames, delimiter=";"):
    return numpy.loadtxt(file_name, skiprows=1, delimiter=delimiter).T


profile_loader.item_with_key(PCalculationMode)(
    (unpack_load("t", "P"), calc_P))


def P_profile_tP(t_run, P_DHE, Q_peek_feb, Delta_t_peek):
    """ Load is defined by power determined by daily run time per month """
    _, t, P = P_profile(t_run, P_DHE, Q_peek_feb, Delta_t_peek)
    return t, P


profile_loader.item_with_key(
    PCalculationMonthlyLoadMode)((P_profile_tP, calc_P))


def P_profile(t_run: numpy.ndarray,
              P_DHE: float,
              Q_peek_feb: float,
              Delta_t_peek: int):
    """
    :param t_run: For each month: number of hours per day
       at which the pump is on
    :param P_DHE: Power [W] when pump is on
    :param Q_peek_feb: Power [W]
    :param Delta_t_peek: t [h]

    :return:
    """
    month_len = numpy.array(
        (0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31))
    month_start = 24 * numpy.cumsum(month_len)
    month_len = month_len[1:]
    idx_feb = 1

    n_hours = 24 * 365
    P = numpy.zeros(n_hours)
    P_month = tuple(P[m0:m1].reshape((-1, 24))
                    for m0, m1 in zip(month_start[:-1], month_start[1:]))
    t_run = numpy.minimum(numpy.round(t_run), 24)
    for P_m, t in zip(P_month, t_run):
        P_m[:, :t] = P_DHE
    P_month[idx_feb][month_len[idx_feb] - Delta_t_peek:, :] = Q_peek_feb
    t = numpy.arange(n_hours) * 3600.

    return numpy.sum(
        t_run * month_len + Delta_t_peek * (24 - t_run[idx_feb])), t, P


def save_result_csv(result, f, delimiter=";"):
    header, data = zip(*result)
    T_soil = data[-1][0]
    dim_rad, dim_ax = T_soil.shape[1:]
    data = data[:2] + tuple(d[0] for d in data[2:-1]) + \
        (T_soil.reshape((T_soil.shape[0], -1)),)
    header = header[:-1] + tuple(
        header[-1] + "[{},{}]".format(i, j)
        for i in range(dim_rad) for j in range(dim_ax))
    numpy.savetxt(f, numpy.c_[data], delimiter=delimiter,
                  header=delimiter.join(header), fmt="%g")
