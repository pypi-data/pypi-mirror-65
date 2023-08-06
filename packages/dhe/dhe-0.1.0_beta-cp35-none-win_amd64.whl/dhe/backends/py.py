import warnings
import time
from math import pi as pi_, log, exp, sqrt
from typing import Callable, Tuple

from dataclasses import asdict, dataclass

import numpy

from numpy.lib.stride_tricks import as_strided
from scipy.linalg import solve_banded
from scipy.interpolate import interp1d

from .decorators import swallow_unneeded_arguments
from ..model import T_brine_calc_method as ifc_T_brine_calc_method, \
    DHEConfiguration, GCone, GFunc, DHE
from ..enum_map import EnumMap

profile_loader = EnumMap(Callable)
g_implementation = EnumMap(Callable)
T_brine_calc_method = EnumMap(Callable)


def calc_P(t: numpy.ndarray, P: numpy.ndarray,
           dhe, env, precision: float = 0.05):
    """ Load is defined by power """
    dim_ax = env.dim_ax

    t_boundary_refresh = numpy.arange(
        t[0], t[-1], env.dt_boundary_refresh)
    t_boundary_refresh += env.dt_boundary_refresh
    n_DHE = len(env.dhe)
    U_brine = sum(_d.brine_properties.c * _d.Phi_m for _d in dhe) / n_DHE
    dhe, dhe_states = zip(*(prepare_dhe_object(_dhe, env, t_boundary_refresh,
                                               U_brine=U_brine)
                            for _dhe in env.dhe))

    data = _calc_P(t=t, P=P,
                   dhe=dhe,
                   dhe_states=dhe_states,
                   Q_wall=numpy.zeros(dim_ax),
                   sum_Q0=numpy.empty(dim_ax),
                   n_boundary_refresh=int(
                       env.dt_boundary_refresh // env.dt),
                   dim_ax=dim_ax,
                   dt=env.dt,
                   U_brine=U_brine,
                   precision=precision)

    out = (("t", t), ("P", P)) + tuple(zip(
        ("T_sink", "T_source", "T_soil"),
        data
    ))
    return out


def T_evolution_parameters(
        dhe_config: DHEConfiguration,
        dhe: DHE, U_brine: float):
    dim_ax = dhe_config.dim_ax
    dim_rad = dhe_config.dim_rad
    dl = dhe.L / dim_ax  # m
    c_V_soil, lambda_soil = sample_soil_parameters(
        dhe_config.soil_layers, dhe.L, dim_ax)
    R_domain = dhe_config.R - 0.5 * dhe.D_borehole
    r = r_grid(dhe.D, dhe.D_borehole,
               R_domain, dim_rad, dhe_config.Gamma)
    rz = rz_grid(r)

    alpha = alpha1(dhe.brine_properties,
                   dhe.Phi_m / dhe.brine_properties.rho,
                   dhe.D, dhe.thickness)

    R1 = dhe.R1
    lambda_fill = dhe.fill_properties.lambda_
    c_V_fill = dhe.fill_properties.c * dhe.fill_properties.rho
    lambda_brine = dhe.brine_properties.lambda_
    if R1 <= 0.:
        R1 = R_1(dl, r, rz, alpha, lambda_fill,
                 dhe.Ra, dhe.Rb)
    R2 = R_2(dl, r, rz, lambda_fill, lambda_soil,
             dhe.Ra, dhe.Rb)
    L1_on = 1 / R1
    L1_off = 1 / \
        (R1 + (1. / alpha0(lambda_brine, dhe.D) - 1. / alpha) /
         (8 * pi_ * r[0] * dl))

    L_on, L_off = L_pump(dl, r, rz, L1_on, L1_off,
                         R2, dhe_config.adiabat, lambda_soil)
    # Heat capacity
    C = C_matrix(dl, r, c_V_fill=c_V_fill,
                 c_V_soil=c_V_soil)

    n_steps = optimal_n_steps(L_on, C, dhe_config.dt,
                              c=dhe_config.opt_n_steps_multiplier)
    dt_step = dhe_config.dt / n_steps

    C_brine = 2 * dhe.brine_properties.c \
        * dhe.brine_properties.rho \
        * pi_ * (0.5 * dhe.D)**2 * dl  # J/K
    Lm_min = C_brine / max(U_brine, L1_on)
    n_steps_on = int(dhe_config.n_steps_0 * dt_step / Lm_min) + 1
    n_steps_off = int(dhe_config.n_steps_0 * dt_step / C_brine * L1_off) + 1

    T_brine_method = swallow_unneeded_arguments(
        T_brine_calc_method.items[dhe_config.T_brine_method])
    T_brine_method_on = T_brine_method(
        dt=dt_step, dC_brine=C_brine,
        L=L_on[:, 0].copy(), n_sub_steps=n_steps_on,
        U_brine=U_brine)
    T_brine_method_off = T_brine_method(
        dt=dt_step, dC_brine=C_brine,
        L=L_off[:, 0].copy(), n_sub_steps=n_steps_off,  # pylint: disable=invalid-sequence-index
        U_brine=0.)
    return dict(
        L1_on=L1_on,
        n_steps=n_steps,
        pump_dependent_parameters=(
            (T_soil_evolution(L_off, C, dt_step),
             L_off[:, 0].copy(), T_brine_method_off),  # pylint: disable=invalid-sequence-index
            (T_soil_evolution(L_on, C, dt_step),
             L_on[:, 0].copy(), T_brine_method_on)
        )
    )


def prepare_dhe_object(dhe, dhe_config, t_boundary_refresh, U_brine):
    g_method = g_implementation.items[type(dhe_config.g_method)](
        **asdict(dhe_config.g_method))
    dim_ax = dhe_config.dim_ax
    c_V_soil, lambda_soil = sample_soil_parameters(
        dhe_config.soil_layers, dhe.L, dim_ax)
    g = g_method(
        t_boundary_refresh, c_V_soil=c_V_soil,
        lambda_soil=lambda_soil,
        r=dhe_config.R)
    dl = dhe.L / dim_ax  # m
    out = T_evolution_parameters(dhe_config, dhe, U_brine)
    out.update(
        dict(d_lambda_soil=lambda_soil * dl,
             g=g,
             x=dhe.x,
             y=dhe.y,
             L=dhe.L,
             R=dhe_config.R)
    )

    return out, DHEState(dhe, dhe_config, dl, c_V_soil,
                         lambda_soil, dim_t=g.shape[0])


@dataclass
class LowLevelDHE:
    x: float
    y: float
    R: float
    n_steps: int
    L: numpy.ndarray
    d_lambda_soil: numpy.ndarray
    g: numpy.ndarray
    L1_on: numpy.ndarray
    pump_dependent_parameters: Tuple[tuple, tuple]


class DHEState:
    def __init__(self, dhe, dhe_config, dl, c_V_soil, lambda_soil, dim_t: int):
        dim_ax = dhe_config.dim_ax
        dim_rad = dhe_config.dim_rad
        u_min, g_values = g_poly(dhe.T_soil_0_parameters.g_coefs,
                                 dhe.T_soil_0_parameters.d_DHE)
        R_domain = dhe_config.R - 0.5 * dhe.D_borehole
        r = r_grid(dhe.D, dhe.D_borehole,
                   R_domain, dim_rad, dhe_config.Gamma)
        rz = rz_grid(r)
        T_soil = T_soil_0(
            dhe_config.t0, g_values, dim_ax, dl, c_V_soil=numpy.mean(c_V_soil),
            lambda_soil=numpy.mean(lambda_soil),
            rz=rz, T_soil=dhe_config.soil_parameters.T_soil_mean,
            T_grad=dhe_config.soil_parameters.T_grad, u_min=u_min)
        T_U = numpy.empty((2, dim_ax))
        T_down, T_up = T_U
        T_down[()] = T_soil[0]
        T_up[::-1] = T_soil[0]
        self.T_U = T_U
        self.T_soil = T_soil
        self.Q = numpy.empty((dim_t, dim_ax))
        self.Q[0] = 0.


def sample_soil_parameters(layers, L_DHE, dim_ax):
    """Given dim_l layers :param layers: of soil with parameters
    (constant across single layers).
    Calculate values for a number of dim_ax equispaced layers
    of total thickness L_DHE. The output layers values are
    taken to be the length averages of the
    input layer values over the ranges of the output layers.

    :param L_DHE: Length of dhe [m]
    :param dim_ax:
    :return:
    """
    layer_data = numpy.array(
        [[layer.rho * layer.c, layer.lambda_] for layer in layers])
    d_soil = numpy.array([layer.d for layer in layers])

    l_DHE = numpy.linspace(0., L_DHE, dim_ax + 1)
    dim_l, dim_prm = layer_data.shape
    l_soil = numpy.empty(dim_l + 1)
    l_soil[1:] = numpy.cumsum(d_soil)
    if l_soil[-1] < L_DHE:
        warnings.warn(
            "L_DHE = {} exceeds lowest layer (L = {})."
            "The values of the lowest layer will be used "
            "as continuation.".format(L_DHE, l_soil[-1]))
    l_soil[0] = 0.
    if numpy.isinf(l_soil[-1]):
        l_soil[-1] = L_DHE
        d_soil = l_soil[1:] - l_soil[:-1]
    weighted_data = numpy.empty((dim_l + 1, dim_prm))
    weighted_data[1:] = numpy.cumsum(layer_data * d_soil[:, None], axis=0)
    weighted_data[0] = 0.
    I = interp1d(l_soil, weighted_data,
                 copy=False,
                 assume_sorted=True,
                 axis=0,
                 fill_value="extrapolate")(l_DHE)
    mean_values = (I[1:] - I[:-1]) / (L_DHE / dim_ax)
    return mean_values.T


def R_1(dl, r, rz, alpha, lambda_fill, Ra, Rb):
    """ Resistance R1 in bore hole """
    if (Ra > 0) and (Rb > 0):
        return Ra / (4 * dl)
    if Rb > 0:
        return Rb / dl - 1 / (2 * pi_ * dl * lambda_fill) * \
            log(r[1] / rz[1])
    return (1 / (alpha * r[0]) +
            log((r[1] - rz[1]) / r[0]) / lambda_fill) / (8 * pi_ * dl)


def R_2(dl, r, rz, lambda_fill, lambda_soil, Ra, Rb):
    """ Resistance R2 in bore hole """
    if Ra > 0. and Rb > 0.:
        return (Rb - 0.25 * Ra) / dl + \
            log(rz[2] / r[1]) / (2 * pi_ * dl * lambda_soil)
    return (log(r[1] / rz[1]) / lambda_fill +
            log(rz[2] / r[1]) / lambda_soil) / (2 * pi_ * dl)


def L_pump(dl, r, rz, L1_on, L1_off, R2, adiabat, lambda_soil) \
        -> Tuple[numpy.ndarray, numpy.ndarray]:
    """ Pump on / off """
    dim_ax = lambda_soil.size
    L_on = numpy.empty((dim_ax, r.size))  # r.size = dim_rad + 1
    L_on[..., 0] = L1_on
    L_on[..., 1] = 1. / R2
    L_on[..., -1] = (1 - adiabat) * 2 * pi_ * dl \
        * lambda_soil / log(r[-1] / rz[r.size - 1])
    L_on[..., 2:-1] = 2 * pi_ * dl * lambda_soil[..., None] \
        / numpy.log(rz[None, 3:-1] / rz[None, 2:-2])
    L_off = numpy.empty_like(L_on)
    L_off[..., 0] = L1_off
    L_off[..., 1:] = L_on[..., 1:]
    return L_on, L_off


def C_matrix(dl, r, c_V_fill, c_V_soil):
    dim_rad = r.size - 1
    dim_ax = c_V_soil.size
    C = numpy.empty((dim_ax, dim_rad))
    C[..., 0] = pi_ * c_V_fill * (r[1]**2 - 4 * r[0]**2) * dl
    C[..., 1:] = pi_ * dl * c_V_soil[:, None] \
        * (r[None, 2:]**2 - r[None, 1:-1]**2)
    return C


def T_evolution_big(L, C, dt_step):
    """
    Definition of matrices, where A T_new = F T_old
    => T_new = A^{-1} F T_old
    returns B = A^{-1} F
    """
    def _LC(L, C, dt):
        A = numpy.zeros((C.shape[0], C.shape[1] + 2, C.shape[1] + 2))
        A[:, 0, 0] = 1.
        A[:, -1, -1] = 1.
        diag_2d = as_strided(
            A, shape=A.shape[:-1],
            strides=(A.strides[0], A.strides[1] + A.strides[2]))
        diag_2d[:, 1:-1] = 2 * C + dt * (L[:, 1:] + L[:, :-1])
        off_diag_2d = as_strided(
            A.reshape(-1)[1:], shape=(2, A.shape[0], A.shape[1] - 1),
            strides=(A.strides[1] - A.strides[2],
                     A.strides[0], A.strides[1] + A.strides[2]))
        off_diag_2d[1, :, :-1] = -dt * L[:, :-1]
        off_diag_2d[0, :, 1:] = -dt * L[:, 1:]
        return A
    return numpy.linalg.solve(
        _LC(L, C, dt_step), _LC(L, C, -dt_step))


def T_soil_evolution(L, C, dt_step):
    """
    Returns B such that
    T_new[1:-1] = B T_old
    If (dim_ax, dim_rad+2) is the shape of T_old, then
    B has shape (dim_ax, dim_rad, dim_rad+2)
    """
    def _LC(L, C, dt, out=None, offset=0):
        dim_ax = C.shape[0]
        dim_rad = C.shape[1]
        if out is None:
            out = numpy.zeros((dim_ax, dim_rad, dim_rad))
        diag_2d = as_strided(
            out.reshape(-1)[offset:], shape=(dim_ax, dim_rad),
            strides=(out.strides[0], out.strides[1] + out.strides[2]))
        diag_2d[()] = 2 * C + dt * (L[:, 1:] + L[:, :-1])
        off_diag_2d = as_strided(
            out.reshape(-1)[1 + offset:], shape=(
                2, dim_ax, dim_rad - 1),
            strides=(out.strides[1] - out.strides[2],
                     out.strides[0],
                     out.strides[1] + out.strides[2]))
        off_diag_2d[()] = -dt * L[:, 1:-1]
        return out
    A = _LC(L, C, dt_step)
    F = numpy.zeros(A.shape[:2] + (A.shape[2] + 2,))
    _LC(L, C, -dt_step, out=F, offset=1)
    F[:, 0, 0] = 2 * dt_step * L[:, 0]
    F[:, -1, -1] = 2 * dt_step * L[:, -1]
    return numpy.linalg.solve(A, F)


def optimal_n_steps(L: numpy.ndarray, C: numpy.ndarray, dt, c=2.) -> int:
    """ Determine optimal value for n_steps """
    dt_min = min(numpy.min(C[:, i] / L[:, j])
                 for (i, j) in ((0, 0), (0, 1), (1, 1)))
    return int(c * dt // dt_min) or 1


def g_poly(g: tuple,
           d_DHE: float,
           d_DHE_ref: float = 10.,
           d_DHE_delta:
           float = 0.05):
    if abs(d_DHE - d_DHE_ref) > d_DHE_delta:
        # Extrapolation of the g function
        BH = d_DHE / d_DHE_ref
        if BH < 0.4:
            raise ValueError("BH out of bounds")
        ExA = g[4] - 6.29
        ExB = -numpy.log((g[2] - 6.29) / (g[4] - 6.6)) / 27
        g0 = numpy.array([4.82, 5.69, 6.29, 6.57, 6.6])
        g_exp = numpy.array([343, 125, 27, 1, 0])
        g = g0 + numpy.maximum(0., ExA / BH *
                               numpy.exp(-BH * ExB * g_exp))
        #  e Extrapolation g-Function
    # Calculates g function from 4 sampling points g1,g2,g3,g4
    x = numpy.array([-4, -2, 0, 2.5, 3., min(-4.5, (-4 - (g[0] - 4.82) / 2))])
    y = numpy.array([g[0], g[1], g[2], g[3], g[4] * 0.99,
                     (numpy.log(0.5 / 0.0005) + 0.5 * x[5]) * 0.95])
    A = numpy.empty((x.size, x.size))
    y[3] = (y[3] + y[4]) / 2 * 0.99
    A[:, 0] = 1.
    for i in range(1, x.size):
        A[:, i] = A[:, i - 1] * x
    u_min = max((x[5] + 0.5), -6)
    return u_min, numpy.linalg.solve(A, y)


def T_soil_0(t0, g_coefs, dim_ax, dl, c_V_soil, lambda_soil, rz,
             T_soil, q_drain: numpy.ndarray = 0.,
             T_grad: float = 0.03, **kwargs):
    """
    :param t0:
    :param g_coefs:
    :param dim_ax:
    :param dl:
    :param c_V_soil:
    :param lambda_soil:
    :param rz:
    :param T_soil: Mean of Temperature axial [K/m]
    :param T_grad: Gradient of Temperature axial [K/m]
    :param q_drain: Heat drained par layer. Shape: (dim_ax,) or ()
    :param kwargs:

    :return: numpy array of shape (dim_rad + 2, dim_ax)
    """

    if t0 == 0.:
        Rq = numpy.zeros_like(rz)[:, None]
    else:
        g = _g_func(g_coefs, L=dim_ax * dl, go_const=6.907755, **kwargs)(
            t0, c_V_soil, lambda_soil, r=rz)
        Rq = (g / (2 * pi_ * numpy.array(lambda_soil,
                                         copy=False).reshape((-1, 1)))).T
    q_drain = numpy.array(q_drain, copy=False)
    return T_soil + T_grad * dl * (numpy.arange(1., dim_ax + 1.) - 0.5) \
        - Rq * q_drain / dl


def r_grid(D_DHE, D_borehole, R, dim_rad, Gamma):
    """
    :param D_DHE:
    :param D_borehole:
    :param dim_rad:
    :param R: Domain of computation
    :param Gamma: Grid parameter
    :return:
    """
    r = numpy.empty(dim_rad + 1)
    r[0] = 0.5 * D_DHE
    r[1] = 0.5 * D_borehole
    c = R * (1 - Gamma) / \
        (1 - Gamma**(dim_rad - 1))
    r[2:] = r[1] + c * \
        numpy.cumsum(numpy.logspace(
            0, dim_rad - 2, num=dim_rad - 1, base=Gamma))
    return r


def rz_grid(r):
    rz = numpy.empty(r.size + 1)
    rz[1:-1] = numpy.sqrt(0.5 * (r[1:]**2 + r[:-1]**2))
    rz[0] = r[0]
    rz[-1] = r[-1]
    return rz


def alpha0(lambda_brine: float, D: float) -> float:
    """
    Heat transfer if pump is off
    """
    return 2. * lambda_brine / (D * (1 - sqrt(0.5)))


def alpha1(brine_properties, Phi: float,
           D_DHE: float, thickness_DHE: float) -> float:
    """Heat transfer brine backfill, when pump is on

    :param brine_properties:
    :param Phi:
    :param D_DHE:
    :param thickness_DHE: Thickness DHE pipe

    :return: alpha1
    """
    c_V_brine = brine_properties.c * brine_properties.rho
    nu_brine = brine_properties.nu
    lambda_brine = brine_properties.lambda_
    Di = D_DHE - 2 * thickness_DHE
    v = 2 * Phi / Di**2 / pi_
    Re = v * Di / nu_brine  # Reynolds number
    Pr = nu_brine * c_V_brine / lambda_brine  # Prandtl number
    #  Xi: pressure loss coefficient by Petukhov (1970)
    Xi = 1 / 1.82 * log(Re**2 / log(10) - 1.64)
    #  Stanton number by Petukhov (1970), valid for at turbulent speed
    K1 = 1 + 27.2 * Xi / 8
    K2 = 11.7 + 1.8 / Pr**(1 / 3)
    St = Xi / 8 / (K1 + K2 * sqrt(Xi / 8) *
                   (Pr**(2 / 3) - 1))  # Stanton number
    #  Stanton number by Petukhov at the border turbulence/transition zone
    Xi0 = 0.031437
    K10 = 1.106886
    St_0 = Xi0 / 8 / (K10 + K2 * sqrt(Xi0 / 8) * (Pr**(2 / 3) - 1))
    # Nusselt number on transition turbulence/transition zone:
    Nu_0 = St_0 * 10000 * Pr
    Nu_turbulent = St * Re * Pr  # Nusselt number for turbulent zone
    Nu_laminar = 4.36  # Nusselt number for laminar zone
    if Re >= 10000.:
        Nu = Nu_turbulent  # turbulent
    if Re <= 2300.:
        Nu = Nu_laminar  # laminar
        # Transition zone laminar/turbulent
    else:
        if Re < 10000.:
            Nu = Nu_laminar \
                * exp(log(Nu_0 / Nu_laminar) /
                      log(10000. / 2300.) * log(Re / 2300))
    return Nu * lambda_brine / Di


def _calc_P(t, P: numpy.ndarray, *, dim_ax, dt, U_brine,
            dhe, dhe_states, **kwargs):
    """ Load is defined by power """
    _t = numpy.arange(t[0], t[-1]+dt, dt)
    P = numpy.interp(_t, t, P)
    _U_brine = numpy.zeros_like(P)
    _U_brine[P > 0.] = U_brine

    dhe_state, = dhe_states
    dhe_state.T_soil = dhe_state.T_soil.T
    dhe_0, = dhe
    dhe_0 = LowLevelDHE(**dhe_0)

    cpu_t0 = time.clock()
    (T_sink, T_source, T_soil) = _py_calc_P(P=P,  # pylint: disable=missing-kwoa
                                            dim_ax=dim_ax,
                                            U_brine=_U_brine,
                                            dhe=dhe_0,
                                            dhe_state=dhe_state,
                                            **kwargs)

    print(f"Ran py_calc_P in {time.clock() - cpu_t0} s")
    return (T_sink[None, ...], T_source[None, ...], T_soil[None, ...])


def _py_calc_P(P, *,
               dim_ax,
               U_brine,
               dhe: LowLevelDHE,
               dhe_state: DHEState,
               precision=0.05,
               sum_Q0, Q_wall,
               n_boundary_refresh,
               out=None,
               **kwargs):
    """
    :param P:
    :param dim_ax:
    :param U_brine: U_brine = Phi_m * c_brine [W/K]
    :param dhe:
    :param dhe_state:
    :param precision:
    :param sum_Q0:
    :param Q_wall:
    :param n_boundary_refresh:
    :param out:
    :param kwargs:
    :return:
    """
    n_DHE = 1  # Only n_DHE = 1 supported
    T_soil, T_U, Q = (dhe_state.T_soil, dhe_state.T_U, dhe_state.Q)
    d_lambda_soil, g, L1_on, pump_dependent_parameters, n_steps \
        = (dhe.d_lambda_soil, dhe.g, dhe.L1_on,
           dhe.pump_dependent_parameters, dhe.n_steps)
    if out is None:
        out = numpy.empty((P.shape[0], 2 + numpy.prod(T_soil.shape)))
    out_T_sink = out[:, 0]
    out_T_source = out[:, 1]
    out_T_soil = out[:, 2:].reshape(P.shape + T_soil.shape)
    T_soil_old = numpy.empty_like(T_soil)
    T_U_old = numpy.empty_like(T_U)
    sum_Q0_old = numpy.empty_like(sum_Q0)
    T_sink = numpy.mean(T_soil[:, 1])
    T0 = numpy.empty(dim_ax)
    T0[:] = dhe_state.T_soil[:, -1].copy()
    for i, (Q_source, _U) in enumerate(zip(P, U_brine)):
        if _U > 0.:
            T_sink -= \
                Q_source * (1. / (n_DHE * L1_on) + 1. / _U)
            T_soil_old[:] = T_soil
            T_U_old[:] = T_U
            sum_Q0_old[:] = sum_Q0

        T_source = calc_sub_step(
            T_sink=T_sink, T_soil=T_soil,
            sum_Q0=sum_Q0, T_U=T_U,
            Q_wall=Q_wall, U_brine=_U,
            pump_dependent_parameters=pump_dependent_parameters,
            n_steps=n_steps,
            **kwargs)
        if _U:
            T_sink = T_source - Q_source / _U
            T_sink_ref = float("inf")
            while abs(T_sink - T_sink_ref) > precision:
                T_soil[:] = T_soil_old
                T_U[:] = T_U_old
                sum_Q0[:] = sum_Q0_old
                T_source = calc_sub_step(
                    T_sink=T_sink, T_soil=T_soil,
                    sum_Q0=sum_Q0, T_U=T_U,
                    Q_wall=Q_wall, U_brine=_U,
                    pump_dependent_parameters=pump_dependent_parameters,
                    n_steps=n_steps,
                    **kwargs)
                T_sink_ref = T_sink
                T_sink = T_source - Q_source / _U
                if abs(T_sink) > 100:
                    T_sink = -1
                    T_sink_ref = float("inf")
        else:
            T_sink = T_soil[0, 1]
            T_source = T_sink
        if i % n_boundary_refresh == 0 and i > 0:
            i_boundary = i // n_boundary_refresh
            Q[i_boundary] = sum_Q0 / (n_boundary_refresh * n_steps)
            T_soil[:, -1] = T0 + \
                Delta_T_boundary(g[:i_boundary],
                                 Q[:i_boundary + 1], d_lambda_soil)
            sum_Q0[()] = 0.

        out_T_sink[i] = T_sink
        out_T_source[i] = T_source
        out_T_soil[i] = T_soil

    return out_T_sink, out_T_source, out_T_soil


def calc_T(t, T_sink, U, *,
           T_soil, T_U, sum_Q0, Q, Q_wall, d_lambda_soil, g,
           n_boundary_refresh, n_steps,
           **kwargs):
    """
    :param t:
    :param T_sink:
    :param U: U = Phi_m * c_brine [W/K]
    :param T_soil:
    :param T_U:
    :param sum_Q0:
    :param Q:
    :param Q_wall:
    :param d_lambda_soil: lambda_soil * dl. shape: (dim_ax,) or ()
    :param g:
    :param n_boundary_refresh:
    :param n_steps:
    :param kwargs:
    :return:
    """
    out_Q_source = numpy.empty_like(T_sink)
    out_T_source = numpy.empty_like(T_sink)
    out_T_soil = numpy.empty((T_sink.shape[0],) + T_soil.shape)
    T0 = T_soil[:, -1].copy()
    for i, (_t, _T_sink, _U) in enumerate(zip(t, T_sink, U)):
        T_source = calc_sub_step(T_sink=T_sink, T_soil=T_soil,
                                 sum_Q0=sum_Q0, T_U=T_U,
                                 Q_wall=Q_wall, U_brine=_U,
                                 **kwargs)
        Q[i] = sum_Q0 / (n_boundary_refresh * n_steps)
        T_soil[:, -1] = T0 + Delta_T_boundary(g, Q[:i + 1], d_lambda_soil)
        out_Q_source[i] = (T_source - _T_sink) * _U

        out_T_source[i] = T_source
        out_T_soil[i] = T_soil
    return out_Q_source, out_T_source, out_T_soil


def calc_sub_step(T_soil, T_sink, sum_Q0,
                  n_steps,
                  Q_wall, T_U,
                  U_brine,
                  pump_dependent_parameters):
    """
    :param T_soil:
    :param T_sink:
    :param sum_Q0:
    :param Q_wall:
    :param U_brine:
    :param T_U:
    :param n_steps:
    :param pump_dependent_parameters:
    :param U_brine: U_brine = cp_brine * Phi_m / n_DHE
    :return:
    """
    B, L, T_brine_refresh = pump_dependent_parameters[U_brine > 0.]
    T_s = U_brine and T_sink
    T_source = 0.
    for _ in range(n_steps):
        # Calculate brine Temperature
        T_source += T_brine_refresh(T_soil[:, 1], T_U, Q_wall, T_sink=T_s)
        T_soil[:, 0] = T_soil[:, 1] - Q_wall / L
        sum_Q0 += Q_wall
        # Update soil temperature
        T_soil[:, 1:-1] = (B @ T_soil[:, :, None]).squeeze()
    T_source /= n_steps
    return T_source


@T_brine_calc_method.item_with_key(ifc_T_brine_calc_method.dynamic)
def T_brine(dt, n_sub_steps: int,
            dC_brine: float, U_brine: float,
            L: numpy.ndarray):
    """
    :param dt:
    :param n_sub_steps:
    :param dC_brine:
    :param L:
    :param U_brine: U_brine = Phi c_V_brine
    :param dC_brine: dC_brine = 2 c_V_brine pi r_DHE^2 dl
    :return:
    """

    dt_step = dt / n_sub_steps
    L0mcpdt = U_brine / dC_brine * dt_step
    lambda_brine = 0.5 * L / n_sub_steps
    L1mcpdt = lambda_brine * dt / dC_brine
    n = L.size
    N = n * 2

    def _T_brine(T_soil, T_U, Q_wall, T_sink: float) -> float:
        """
        :param T_soil:
        :param T_U: shape (2, n), T_U[0] is T_down, T_U[1] is T_up
        :param Q_wall: passed only to prevent reallocating [W/m]
        :param T_sink:
        :return: T_source
        """
        T_out = 0
        Q_wall[:] = 0.
        T_U_flat = T_U.reshape(-1)
        for _step in range(n_sub_steps):
            T_U_flat[0] += (T_sink - T_U_flat[0]) * L0mcpdt \
                + (T_soil[0] - T_U_flat[0]) * L1mcpdt[0]
            for i in range(1, n):
                T_U_flat[i] += (T_U_flat[i - 1] - T_U_flat[i]) * L0mcpdt \
                    + (T_soil[i] - T_U_flat[i]) * L1mcpdt[i]
            for i in range(n, N):
                T_U_flat[i] += (T_U_flat[i - 1] - T_U_flat[i]) * L0mcpdt \
                    + (T_soil[N - 1 - i] - T_U_flat[i]) * L1mcpdt[N - 1 - i]
            Q_wall += (2 * T_soil - T_U[0] - T_U[1, ::-1]) * lambda_brine
            T_out += T_U_flat[-1]
        T_out /= n_sub_steps
        return T_out
    _T_brine.method = _T_brine
    _T_brine.parameters = {"kappa_ax": L0mcpdt,
                           "kappa_rad": L1mcpdt,
                           "lambda_brine": lambda_brine,
                           "n_sub_steps": n_sub_steps}

    return _T_brine


# @T_brine_calc_method.item_with_key(ifc_T_brine_calc_method.T_brine)
def T_brine_banded(dt, n_sub_steps: int,
                   dC_brine: float, U_brine: float,
                   L: numpy.ndarray):
    """
    :param dt:
    :param n_sub_steps:
    :param dC_brine:
    :param L:
    :param U_brine: U_brine = Phi c_V_brine
    :param dC_brine: dC_brine = 2 c_V_brine pi r_DHE^2 dl
    :return:

    A t' = b
    T'[i] = L0*T'[i-1] + (1-L0 -L[i])*T[i] + Ts[i]*L[i]
    =>  T'[i] -L0*T'[i-1] = (1-L0 -L[i])*T[i] + Ts[i]*L[i]
    => A = diag(1,..,1) + lower_off_diag(-L0, ..., -L0)
       b = (1-L0 -L)*T + Ts*L + [T_sink*L0, 0, ..., 0]
    """
    dt_step = dt / n_sub_steps
    L0mcpdt = U_brine / dC_brine * dt_step
    lambda_brine = 0.5 * L / n_sub_steps
    L1mcpdt = lambda_brine * dt / dC_brine

    n = L.size
    A = numpy.empty((2, n))
    A[0] = 1.
    A[1, 0] = 0.
    A[1, 1:] = -L0mcpdt
    b1 = 1. - L0mcpdt - L1mcpdt
    b = numpy.empty_like(b1)

    def _T_brine(T_soil, T_U, Q_wall, T_sink: float) -> float:
        """
        :param T_soil:
        :param T_U: shape (2, n), T_U[0] is T_down, T_U[1] is T_up
        :param Q_wall: passed only to prevent reallocating [W/m]
        :param T_sink:
        :return: T_source
        """
        T_out = 0
        Q_wall[:] = 0.
        T_U_flat = T_U.reshape(-1)

        for _step in range(n_sub_steps):
            b[()] = b1*T_U_flat[:n] + T_soil*L1mcpdt
            b[0] += T_sink * L0mcpdt
            T_U_flat[:n] = solve_banded((1, 0), A, b, overwrite_b=True)
            b[()] = b1[::-1]*T_U_flat[n:] + T_soil[::-1]*L1mcpdt[::-1]
            b[0] += T_U_flat[n-1] * L0mcpdt
            T_U_flat[n:] = solve_banded((1, 0), A, b, overwrite_b=True)
            Q_wall += (2 * T_soil - T_U[0] - T_U[1, ::-1]) * lambda_brine
            T_out += T_U_flat[-1]
        T_out /= n_sub_steps
        return T_out
    _T_brine.method = _T_brine
    _T_brine.parameters = {"kappa_ax": L0mcpdt,
                           "kappa_rad": L1mcpdt,
                           "lambda_brine": lambda_brine,
                           "n_sub_steps": n_sub_steps}

    return _T_brine

@T_brine_calc_method.item_with_key(
    ifc_T_brine_calc_method.stationary)
def T_brine_stationary(U_brine: float,
                       L: numpy.ndarray):
    """
    Stationary T_brine method

    U_brine: U_brinemcpdt = U_brine / U_brine * dt2
    """
    def _T_brine(T_soil, T_U, Q_wall,
                 T_sink: float) -> float:
        """
        :param T_soil:
        :param T_U: shape (2, n), T_U[0] is T_down, T_U[1] is T_up
        :param Q_wall: passed only to prevent reallocating [W/m]
        :param T_sink:
        :return: T_source
        """
        T_U_flat = T_U.flat
        T_U_flat[0] = (0.5 * L[0] * T_soil[0] + U_brine * T_sink) \
            / (0.5 * L[0] + U_brine)
        N = T_U.size
        n = N // 2
        for i in range(1, n):
            T_U_flat[i] = (0.5 * L[i] * T_soil[i] +
                           U_brine * T_U_flat[i - 1]) \
                / (0.5 * L[i] + U_brine)
        for i in range(n, N):
            T_U_flat[i] = (0.5 * L[N - 1 - i] * T_soil[N - 1 - i] +
                           U_brine * T_U_flat[i - 1]) \
                / (0.5 * L[N - 1 - i] + U_brine)

        Q_wall[:] = (2 * T_soil - T_U[0] - T_U[1, ::-1]) * 0.5 * L
        return T_U[1, -1]
    _T_brine.method = _T_brine
    _T_brine.parameters = {"kappa_soil": L / (L + 2*U_brine),
                           "kappa_brine": U_brine / (0.5 * L + U_brine),
                           "L": L}
    return _T_brine


def T_brine_coax(T, T_up, T_down, Q_wall, dt_step, n_sub_steps: int,
                 U_brine_up: float, U_brine_down: float, L0: float,
                 L: numpy.ndarray,
                 La: numpy.ndarray,
                 T_sink: float) -> float:

    # TODO: finish
    # var i, k: integer
    #    TOut, dt2, Lm0, Lm1, LmMin, L0mcpdt, Nichtad: real
    #    Td, Tu, dTa, SummeT: Vektor
    T_down[0] = T_sink
    TOut = 0
    Q_wall[:] = 0.
    dTa = numpy.zeros_like(T_up)
    dim_ax = T.shape[0]
    kappa_down_0 = L0 / U_brine_down * dt_step
    kappa_up_0 = L0 / U_brine_up * dt_step
    kappa_down = L / U_brine_down * dt_step
    for _step in range(n_sub_steps):
        dTa[:] = (T_up - T_down) * La
        for i in range(1, dim_ax):
            T_down[i] += ((T_down[i - 1] - T_down[i]) * kappa_down_0 +
                          (T[i] - T_down[i]) * kappa_down[i] + dTa[i])

        T_up[-1] = T_down[-1]
        for i in range(2, dim_ax):
            T_up[-i] += ((T_up[-i + 1] - T_up[-i]) * kappa_up_0 -
                         dTa[-i])

        Q_wall += (T - T_down) * L
        TOut += T_up[0]

    TOut = TOut / n_sub_steps
    return TOut


def T_brine_coax_stat(T, T_U, Q_wall,
                      L0: float,
                      L: numpy.ndarray,
                      La: numpy.ndarray,
                      T_sink: float) -> float:

    # TODO: finish
    T_up = T_U[1, ::-1]
    T_down = T_U[0, :]
    N = T_up.shape[0]
    L_inv_up = 1. / (L0 + L + La)
    L_down = 1. / (L0 + L)
    a = L0 * L_inv_up[1:]
    b = La * L_inv_up
    b[0] = 0.
    c_inv = L_down / La
    c_inv[-1] = -1.
    d = L0 / L_down[:-1]
    bands = numpy.empty((3, N))
    upper = c_inv[:-1] * d
    bands[0, 1:] = upper
    bands[1] = c_inv
    bands[1, 1:] += upper
    bands[2, :-1] = a * c_inv[:-1]

    t_soil = numpy.empty(N)
    t_soil[1:] = T * L * L_inv_up[1:]
    t_soil[0] = T_sink
    T_up[:] = solve_banded(
        (1, 1), bands, t_soil, overwrite_b=True)

    T_down[:] = -c_inv * T_up[:]
    T_down[:-1] -= upper * T_up[1:]
    Q_wall[:] = (T - T_down) * L
    return T_up[0]


def Delta_T_boundary(g, q, d_lambda_soil):
    """Superposition of boundary conditions

    :param d_lambda_soil: lambda_soil * dl. shape: (dim_ax,) or ()
    :param q: Heat loss. shape: (dim_t+1, dim_ax)
    :param g: Values of the g function per time and height.
              shape: (dim_t, dim_ax)
    :return:
    """
    return numpy.sum((-q[:0:-1] + q[-2::-1]) * g, axis=0) \
        / (2 * pi_ * d_lambda_soil)


@g_implementation.item_with_key(GFunc)
def g_func(L: float, go_const=6.84, *, g_coefs, **kwargs):
    u_min, g_coefs = g_poly(g=g_coefs, **kwargs)
    return _g_func(g_coefs, u_min, L, go_const)


def _g_func(g_coefs: numpy.ndarray, u_min: float, L: float, go_const=6.84):
    """Boundary condition with g function

    :param g_coefs:
    :param u_min:
    :param L:
    :param go_const:
    :param L: Length of borehole
    :return:
    """
    def _gfunc(t: numpy.ndarray,
               c_V_soil: numpy.ndarray, lambda_soil: numpy.ndarray,
               r: numpy.ndarray):
        """Boundary condition with g function

        :param t: Array of time [s]
        :param c_V_soil: Volume specific heat of soil
        :param lambda_soil:
        :param r: Radius at which to calculate boundary conditions
        :return:
        """
        ts = numpy.array(L**2 / (9 * lambda_soil) * c_V_soil, copy=False)
        I = numpy.tensordot(t, 1. / ts, axes=0)
        u = numpy.empty_like(I)
        mask_I_0 = (I == 0.)
        u[~mask_I_0] = numpy.minimum(2.5, numpy.log(I[~mask_I_0]))
        u[mask_I_0] = 0.
        go = 0.5 * u + go_const
        _g = numpy.empty_like(go)
        mask_g = (u < u_min)
        _g[mask_g] = go[mask_g]
        u_part = u[~mask_g]
        # g_1 + g_2 u + g_3 u^2 + g_4 u^3 + g_5 u^4 + g_6 u^5
        _g[~mask_g] = g_coefs[0] + u_part * \
            (g_coefs[1] + u_part * (
                g_coefs[2] + u_part * (
                    g_coefs[3] + u_part * (
                        g_coefs[4] + u_part * g_coefs[5]))))
        mask_g = (u < -2.) & ((go - 0.3) > _g)
        _g[mask_g] = go[mask_g]
        log_r = numpy.log(r / (L * 0.0005))
        # Add r as an additional dimension
        return _g[(...,) + (None,) * log_r.ndim] - log_r
    return _gfunc


@g_implementation.item_with_key(GCone)
def g_cone():
    def _g_cone(t: numpy.ndarray,
                c_V_soil: numpy.ndarray, lambda_soil: numpy.ndarray,
                r: float):
        """ Boundary condition according to cone formula by Werner """
        u0 = r**2 * c_V_soil / (4 * lambda_soil)
        u = numpy.tensordot(1. / t, u0, axes=0)
        mask_u = u <= 1.
        u__1 = u[mask_u]
        if u__1.size == 0:
            return numpy.zeros(t.shape[0])
        W = numpy.empty(u.shape)
        W[~mask_u] = 0.
        _W = -0.5772 - numpy.log(u__1) + u__1
        sign = 1.
        _u = u__1.copy()
        j = 1
        fac = 1
        inaccuracy = numpy.full(_u.shape, True)
        while numpy.any(inaccuracy):
            sign = -sign
            _u *= u__1
            j += 1
            fac *= j
            delta = _u / (fac * j)
            new_inaccuracy = delta > 0.01 * numpy.abs(_W)
            _W[inaccuracy] += sign * delta[inaccuracy]
            inaccuracy = new_inaccuracy
        _W *= 0.5
        W[mask_u] = _W
        return W
    return _g_cone


def pressure_decay(Phi_m: numpy.ndarray, nu_brine: float, rho_brine: float,
                   D: float,
                   d: float,
                   L: float) -> Tuple[numpy.ndarray, numpy.ndarray]:
    """
    :param Phi_m:
    :param nu_brine:
    :param rho_brine:
    :param D: Diameter DHE pipe
    :param d: Thickness DHE pipe
    :param L: Length DHE
    :return:
    """
    Di = D - 2 * d
    wi = Phi_m / (2 * pi_ * (0.5 * Di)**2 * rho_brine)
    Re = wi * Di / nu_brine
    mask_positive = (Re > 0)
    laminar = mask_positive & (Re < 2300)
    Xi = numpy.zeros_like(Phi_m)
    Xi[laminar] = 64 / Re[laminar]
    Xi[mask_positive & ~laminar] = 1 / \
        (1.82 * numpy.log10(Re[mask_positive & ~laminar]
                            ) - 1.64)**2  # Petukhov, 1970
    return 0.5 * L * Xi / Di * rho_brine * wi**2, laminar
