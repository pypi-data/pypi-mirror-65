import time
from dataclasses import asdict
import numpy


from . import zip_header, T_brine_method
# pylint: disable=no-name-in-module
from ..model import T_brine_calc_method, GCone, GFunc

from ..dhe import (calc_P as _rs_calc_P,  # pylint: disable=import-error
                   T_BRINE_METHOD_DYNAMIC, T_BRINE_METHOD_STATIONARY,
                   GConeParameters, GFuncParameters)

T_brine_mode_map = {
    T_brine_calc_method.dynamic: T_BRINE_METHOD_DYNAMIC,
    T_brine_calc_method.stationary: T_BRINE_METHOD_STATIONARY
}

g_map = {
    GCone: GConeParameters,
    GFunc: GFuncParameters
}


def rs_env(env):
    out = env
    out.T_brine_method = T_brine_mode_map[env.T_brine_method]
    out.g_method = g_map[type(env.g_method)](**asdict(env.g_method))
    return out


def calc_P(t: numpy.ndarray, P: numpy.ndarray,
           dhe, env, precision: float = 0.05):
    """ Load is defined by power """
    #_t = numpy.arange(t[0], t[-1]+dt, dt)
    #P = numpy.interp(_t, t, P)

    cpu_t0 = time.clock()
    data = _rs_calc_P(t=t, P=P,
                      dhe=dhe,
                      env=rs_env(env),
                      precision=precision)

    print(f"Ran rs_calc_P in {time.clock() - cpu_t0} s")
    return zip_header(t, P, data)


T_brine = T_brine_method()


def T_brine_static(U_brine: float,
                   L: numpy.ndarray):
    """
    Static T_brine method

    U_brine: U_brinemcpdt = U_brine / U_brine * dt2
    """
    raise NotImplementedError("")
