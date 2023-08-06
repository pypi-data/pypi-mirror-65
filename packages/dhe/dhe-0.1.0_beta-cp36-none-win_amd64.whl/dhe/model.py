import os
from enum import Enum, auto
from typing import Sequence, Tuple, Union

from dataclasses import dataclass, field

from .deserialize import deserialize
from .serialize import serialize
from .io_formats import JSON
from .translations import __


class Unit:
    def __init__(self, name, scale=1.):
        self.name = name
        self.scale = scale

    def __str__(self):
        return self.name


class UnitsMeta(type):
    def __getitem__(cls, name):
        if name is None:
            return None
        u = cls._registred_units.get(name)
        if u is None:
            u = Unit(name)
            cls._registred_units[name] = u
        return u


class Units(metaclass=UnitsMeta):
    m = Unit("m", 1.)
    _registred_units = {"m": m}


class Path(str):
    pass


class AutoNameEnum(Enum):
    def _generate_next_value_(name, _start, _count, _last_values):  # pylint: disable=no-self-argument
        return name

    def __str__(self):
        return self.value


class T_brine_calc_method(AutoNameEnum):
    dynamic = auto()
    stationary = auto()


metadata_rho = dict(help=__("Density"), unit=Units["kg/m^3"])
metadata_c = dict(help=__("Specific heat"), unit=Units["J/kg/K"])
metadata_lambda = dict(help=__("Heat conductivity"), unit=Units["W/m/K"])


@dataclass
class MaterialProperties:
    rho: float = field(metadata=metadata_rho)
    c: float = field(metadata=metadata_c)
    lambda_: float = field(metadata=metadata_lambda)


metadata_nu = dict(
    help=__("Kinematic viscosity of brine"), unit=Units["m^2/s"])


@dataclass
class FluidProperties(MaterialProperties):
    nu: float = field(metadata=metadata_nu)


@dataclass
class FillProperties(MaterialProperties):
    __doc__ = __("Backfill properties")
    rho: float = field(default=1180.,
                       metadata=metadata_rho)
    c: float = field(default=3040.,
                     metadata=metadata_c)
    lambda_: float = field(default=0.81,
                           metadata=metadata_lambda)


brine_doc = __("""Specific heat:
    H2O: 4200 J/kg/K
    33 % Etylen glycol: 3800 J/kg/K
Kinematic viscosity:
    H2O: 0.00000175 m^2/s
    33 % Ethylene glycol: ~ 0.000006 m^2/s
""")


@dataclass
class BrineProperties(FluidProperties):
    __doc__ = __("Brine properties") + "\n\n" + brine_doc
    rho: float = field(default=1050., metadata=metadata_rho)
    c: float = field(default=3875., metadata=metadata_c)
    lambda_: float = field(default=0.449, metadata=metadata_lambda)
    nu: float = field(default=0.415E-5, metadata=metadata_nu)


@dataclass
class SoilLayerProperties(MaterialProperties):
    __doc__ = __("""Soil layer properties""")
    rho: float = field(default=2600., metadata=metadata_rho)
    c: float = field(default=1000., metadata=metadata_c)
    lambda_: float = field(default=2., metadata=metadata_lambda)
    d: float = field(default=float("inf"), metadata=dict(
        help=__("Thickness of layer"), unit=Units["m"]))


@dataclass
class PCalculationArgs:
    precision: float = field(default=0.05, metadata=dict(
        help=__(
            "Termination criterion for"
            "T_brine computation routine")))


@dataclass
class PCalculationMode:
    __doc__ = __("""Input: P""")
    load_file: Path = field(default="", metadata=dict(
        help=__("Input file")))
    arguments: PCalculationArgs = PCalculationArgs()


@dataclass
class PCalculationMonthlyLoadMode:
    __doc__ = __("""Input: mothly load""")
    P_DHE: float = field(metadata=dict(
        help=__("Heat extraction rate"),
        unit=Units["W"]))
    Q_peek_feb: float = field(metadata=dict(
        help=__("Peak of heat extraction rate at february"),
        unit=Units["W"]))
    Delta_t_peek: float = field(metadata=dict(
        help=__("Duration of peak"),
        unit=Units["h"]))
    t_run: Sequence[float] = field(metadata=dict(
        n=5,
        unit=Units["h"],
        help=__("For each month: number of hours, "
                "the DHE is running per day")))


brine_doc = __("""Specific heat:
    H2O: 4200 J/kg/K
    33 % Etylen glycol: 3800 J/kg/K
Kinematic viscosity:
    H2O: 0.00000175 m^2/s
    33 % Ethylene glycol: ~ 0.000006 m^2/s
""")


@dataclass
class SoilParameters:
    __doc__ = __("""Parameters used to compute initial soil temperature""")
    T_soil_mean: float = field(default=9.8, metadata=dict(
        help=__("Mean temperature of soil"),
        unit=Units["°C"]),
    )
    T_grad: float = field(default=0.03, metadata=dict(
        help=__("Axial gradient of temperature of soil"), unit=Units["K/m"]),
    )


@dataclass
class GFunc:
    __doc__ = __("""Boundary condition with g function""")
    g_coefs: Tuple[float, float, float, float, float] = field(
        default=(4.82, 5.69, 6.29, 6.57, 6.60), metadata=dict(
            help=__("Values of g function at ln(t/ts) = (-4, -2, 0, 2, 3)")))
    d_DHE: float = field(default=10., metadata=dict(
        help=__("Distance of DHE's"),
        unit=Units["m"]))
    d_DHE_ref: float = field(default=10., metadata=dict(
        unit=Units["m"],
        help=__("Distance of DHE's of the g function")))
    d_DHE_delta: float = field(default=0.05, metadata=dict(
        unit=Units["m"]))
    L: float = field(default=100.0, metadata=dict(
        help=__("Length of borehole"),
        unit=Units["m"]))
    go_const: float = 6.84


@dataclass
class GCone:
    __doc__ = __("""Boundary condition according to cone formula by Werner""")


@dataclass
class TSoil0Parameters:
    g_coefs: Tuple[float, float, float, float, float] = field(
        default=(
            4.82, 5.69, 6.29, 6.57, 6.60),
        metadata=dict(
            help=__(
                "Values of g function at "
                "ln(t/ts) = (-4, -2, 0, 2, 3)")))
    d_DHE: float = field(default=10., metadata=dict(
        help=__("Distance of DHE's"),
        unit=Units["m"]))


@dataclass
class DHE:
    x: float = field(default=0., metadata=dict(
        unit=Units["m"],
        help=__("x coordinate of the DHE")))
    y: float = field(default=0., metadata=dict(
        unit=Units["m"],
        help=__("y coordinate of the DHE")))
    L: float = field(default=100., metadata=dict(
        unit=Units["m"],
        help=__("Length of DHE")))
    D: float = field(default=0.026, metadata=dict(
        help=__("Diameter of DHE"),
        unit=Units["m"]))
    D_borehole: float = field(default=0.115, metadata=dict(
        help=__("Diameter of bore hole"),
        unit=Units["m"]))
    thickness: float = field(default=0., metadata=dict(
        help=__("Thickness of DHE pipe"),
        unit=Units["m"]))
    Ra: float = field(default=0.0, metadata=dict(
        help=__("Thermal pipe resistance"),
        unit=Units["Km/W"]))
    Rb: float = field(default=0.1, metadata=dict(
        help=__("Borehole thermal resistance"),
        unit=Units["Km/W"]))
    R1: float = field(default=0.0, metadata=dict(
        help=__("Thermal resistance"),
        unit=Units["Km/W"]))
    fill_properties: FillProperties = FillProperties()
    T_soil_0_parameters: TSoil0Parameters = TSoil0Parameters()
    brine_properties: BrineProperties = BrineProperties()

    Phi_m: float = field(default=0.4, metadata=dict(
        help=__("Mass throughput per DHE if pump is on"),
        unit=Units["kg/s"]))


@dataclass
class DHEConfiguration:
    dim_ax: int = field(default=4, metadata=dict(
        help=__("Number of sampling points in axial direction"),
        unit=None))
    dim_rad: int = field(default=5, metadata=dict(
        help=__("Number of sampling points in radial direction"),
        unit=None))

    # lambda_DHE_pipe: float = field(metadata=dict(
    #                  help=__("Heat conductivity of DHE pipe"),
    #                  unit=Units["W/m/K"]))
    T_brine_method: T_brine_calc_method = field(
        default=T_brine_calc_method.dynamic,
        metadata=dict(
            help=__("Method for computing T_brine")))
    g_method: Union[GFunc, GCone] = field(default=GCone(), metadata=dict(
        help=__("""Method for computing boundary condition""")))

    soil_layers: Sequence[SoilLayerProperties] = field(
        default=(),
        metadata=dict(help=__("Soil layers")))

    calculation_mode: Union[PCalculationMode,
                            PCalculationMonthlyLoadMode] = field(
        default=PCalculationMode(), metadata=dict(
            help=__("""Calculation Mode""")))

    R: float = field(default=1.5, metadata=dict(
        help=__("Radius of calculation"),
        unit=Units["m"]))
    opt_n_steps_multiplier: float = field(default=2., metadata=dict(
        help=__("Multiplier for the n_steps variable")))
    Gamma: float = field(default=2.0, metadata=dict(
        help=__("Grid parameter for radial partition of "
                "domain of calculation"),
        unit=None))
    adiabat: float = field(default=0.0, metadata=dict(
        help=__("Fraction of adiabatic boundary contitions")))
    n_steps_0: int = field(default=4, metadata=dict(
        help=__("Factor for n_steps"),
        unit=Units["m"]))
    dt_boundary_refresh: float = field(default=7 * 24 * 3600., metadata=dict(
        help=__("Duration between two boundary condition refreshes"),
        unit=Units["s"]))
    dt: float = field(default=3600., metadata=dict(
        help=__("Sampling step"),
        unit=Units["s"]))
    t0: float = field(default=0., metadata=dict(
        unit=Units["s"]))
    soil_parameters: SoilParameters = SoilParameters()

    dhe: Sequence[DHE] = field(default=(DHE(),), metadata=dict(
        help=__("Parameterset for each DHE")))

    @classmethod
    def load(cls, f_name, fmt=JSON):
        cfg = deserialize(cls)(fmt.load(f_name))
        rel_file = getattr(cfg.calculation_mode, "load_file", None)
        if rel_file is not None:
            cfg.calculation_mode.load_file = absolute_path(
                rel_file, f_name)
        return cfg

    @classmethod
    def save(cls, val, f_name, fmt=JSON):
        abs_file = getattr(val.calculation_mode, "load_file", None)
        if abs_file is not None:
            val.calculation_mode.load_file = relative_path(
                abs_file, f_name)
        return fmt.save(serialize(cls)(val), f_name)

    # TODO: Delta_T_DHE, Rohrlochwiderstand - Rohrabstand (Shank spacing)


def absolute_path(f, reference):
    if not os.path.isabs(f):
        return os.path.join(os.path.dirname(reference), f)
    return f


def relative_path(f, reference, max_parent=1):
    base_dir = os.path.dirname(reference)
    rel = os.path.relpath(f, start=base_dir)
    n_descends = count_descends(rel)
    lowest_dir = os.path.realpath(os.path.join(base_dir, *([".."]*n_descends)))
    lowest_dir_parent = os.path.realpath(os.path.join(lowest_dir, ".."))
    if n_descends > max_parent or lowest_dir == lowest_dir_parent:
        return f
    return rel


def count_descends(path):
    def full_split(path):
        folder = path
        while folder:
            path, folder = os.path.split(path)
            yield folder
        if path:
            yield path
    return list(full_split(path)).count("..")
