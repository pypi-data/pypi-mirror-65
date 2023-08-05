from enum import Enum
import numpy as np

from .parameter import (
    Parameter,
    is_angle,
    is_distance,
    is_frequency,
    param_to_command_arg,
)
from .utilities import quit_print

SI_DISTANCE_MAP = {
    "pm": 1e-12,
    "nm": 1e-9,
    "um": 1e-6,
    "mm": 1e-3,
    "cm": 1e-2,
    "m": 1,
    "km": 1e3,
}

SI_FREQ_MAP = {
    "pHz": 1e-12,
    "nHz": 1e-9,
    "uHz": 1e-6,
    "mHz": 1e-3,
    "Hz": 1,
    "kHz": 1e3,
    "MHz": 1e6,
    "GHz": 1e9,
    "THz": 1e12,
}


def check_units_validity(p, u):
    if is_angle(p) and u not in ("deg", "degrees", "rad", "rads", "radians", ""):
        quit_print(f"Invalid units: {u} given for argument: {param_to_command_arg(p)}")
    elif is_distance(p) and u not in SI_DISTANCE_MAP:
        if u:
            quit_print(
                f"Invalid units: {u} given for argument: {param_to_command_arg(p)}"
            )
    elif is_frequency(p) and u not in SI_FREQ_MAP:
        if u:
            quit_print(
                f"Invalid units: {u} given for argument: {param_to_command_arg(p)}"
            )
    elif not is_angle(p) and not is_distance(p) and not is_frequency(p):
        if u:
            quit_print(
                f"Invalid units: {u} given for argument: {param_to_command_arg(p)}"
            )


def standard_units_from_param(p):
    CONV = {
        Parameter.BEAMSIZE: "m",
        Parameter.WAISTSIZE: "m",
        Parameter.WAISTPOS: "m",
        Parameter.CAV_GFACTOR: "",
        Parameter.GOUY: "radians",
        Parameter.DIVERGENCE: "radians",
        Parameter.FSR: "Hz",
        Parameter.FWHM: "Hz",
        Parameter.FINESSE: "",
        Parameter.POLE: "Hz",
        Parameter.MODESEP: "Hz",
        Parameter.BEAMSIZE_ITM: "m",
        Parameter.BEAMSIZE_ETM: "m",
        Parameter.GFACTOR_ITM: "",
        Parameter.GFACTOR_ETM: "",
        Parameter.GFACTOR_SINGLE: "",
        Parameter.CAV_LENGTH: "m",
        Parameter.REFLECTIVITY_ITM: "",
        Parameter.REFLECTIVITY_ETM: "",
        Parameter.WAVELENGTH: "m",
        Parameter.ROC: "m",
        Parameter.ROC_ITM: "m",
        Parameter.ROC_ETM: "m",
        Parameter.EIGENMODE: "",
    }
    return CONV[p]


def units_convert(value, units):
    if not units:
        return value
    if units in SI_DISTANCE_MAP:
        return value * SI_DISTANCE_MAP[units]
    if units in SI_FREQ_MAP:
        return value * SI_FREQ_MAP[units]
    if units == "deg" or units == "degrees":
        return np.radians(value)
    if units == "rad" or units == "rads" or units == "radians":
        return value
    # should never get here anyway as units should always be checked in parsing.float_file_range
    # but leave for now just in case something slips through
    quit_print(f"Invalid units: {units}")
