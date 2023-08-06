import time
import numpy

from . import py, T_brine_method
from ..model import T_brine_calc_method
from ..c_dhe import calc_P as _c_calc_P, C_DHE_T_BRINE_DYNAMIC, C_DHE_T_BRINE_STATIONARY  # pylint: disable=no-name-in-module

calc_P = py.calc_P


def _calc_P(t, P: numpy.ndarray, *, dim_ax, dt, U_brine,
            dhe, dhe_states, **kwargs):
    """ Load is defined by power """
    Q = numpy.empty((dhe[0]["g"].shape[0], dim_ax))
    Q[0] = 0.
    dhe_states = tuple(dict(T_U=state.T_U,
                            Q=Q.copy(), T_soil=state.T_soil)
                       for state in dhe_states)

    dhe = tuple(convert_dhe(d) for d in dhe)
    _t = numpy.arange(t[0], t[-1]+dt, dt)
    P = numpy.interp(_t, t, P)
    _U_brine = numpy.zeros_like(P)
    _U_brine[P > 0.] = U_brine
    cpu_t0 = time.clock()
    data = _c_calc_P(P=P,
                     U_brine=_U_brine,
                     dhe=dhe,
                     dhe_states=dhe_states,
                     **kwargs)
    print(f"Ran c_calc_P in {time.clock() - cpu_t0} s")
    return data


py._calc_P = _calc_P  # pylint: disable=protected-access


def convert_dhe(dhe: dict):
    ((B_off, L_off, method_off), (B_on, L_on, method_on)
     ) = dhe.pop("pump_dependent_parameters")
    dhe["T_soil_parameters_off"] = {
        "L": L_off,
        "T_brine_refresh": method_off.method,
        "T_soil_tensor": numpy.moveaxis(B_off, 0, -1).copy(),
        "T_brine_parameters": method_off.parameters
    }
    dhe["T_soil_parameters_on"] = {
        "L": L_on,
        "T_brine_refresh": method_on.method,
        "T_soil_tensor": numpy.moveaxis(B_on, 0, -1).copy(),
        "T_brine_parameters": method_on.parameters
    }
    return dhe


T_brine = T_brine_method(C_DHE_T_BRINE_DYNAMIC)


def T_brine_stationary(U_brine: float,
                       L: numpy.ndarray):
    """
    Stationary T_brine method

    U_brine: U_brinemcpdt = U_brine / U_brine * dt2
    """
    method = type('Method', (object,), {})()
    method.parameters = {"kappa_soil": L / (L + 2*U_brine),
                         "kappa_brine": U_brine / (0.5 * L + U_brine),
                         "L": L}
    method.method = C_DHE_T_BRINE_STATIONARY
    return method


py.T_brine_calc_method.items = {
    T_brine_calc_method.dynamic: T_brine,
    T_brine_calc_method.stationary: T_brine_stationary
}
