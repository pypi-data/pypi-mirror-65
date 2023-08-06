import time
from dataclasses import asdict
import numpy

from . import zip_header
from . import rs
# pylint: disable=no-name-in-module
from ..model import T_brine_calc_method, GCone, GFunc

from ..c_dhe_full import (  # pylint: disable=import-error
    calc_P as _c_calc_P,
    T_BRINE_METHOD_DYNAMIC as C_T_BRINE_METHOD_DYNAMIC, \
    T_BRINE_METHOD_STATIONARY as C_T_BRINE_METHOD_STATIONARY, \
    GConeParameters, GFuncParameters
)

T_brine_mode_map = {
    T_brine_calc_method.dynamic: C_T_BRINE_METHOD_DYNAMIC,  # pylint: disable=no-member
    T_brine_calc_method.stationary: C_T_BRINE_METHOD_STATIONARY  # pylint: disable=no-member
}

g_map = {
    GFunc: GFuncParameters,
    GCone: GConeParameters
}


def c_env(env):
    out = env
    out.g_method = g_map[type(env.g_method)](**asdict(env.g_method))
    out.T_brine_method = T_brine_mode_map[env.T_brine_method]
    return out


def calc_P(t: numpy.ndarray, P: numpy.ndarray,
           dhe, env, precision: float = 0.05):
    """ Load is defined by power """
    #_t = numpy.arange(t[0], t[-1]+dt, dt)
    #P = numpy.interp(_t, t, P)

    cpu_t0 = time.clock()
    data = _c_calc_P(t=t, P=P,
                     dhe=dhe,
                     env=c_env(env),
                     precision=precision)

    print(f"Ran c_calc_P in {time.clock() - cpu_t0} s")
    return zip_header(t, P, data)


T_brine = rs.T_brine
T_brine_static = rs.T_brine_static
