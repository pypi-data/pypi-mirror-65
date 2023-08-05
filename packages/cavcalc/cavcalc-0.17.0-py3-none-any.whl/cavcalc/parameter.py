"""
The physical parameter enumeration and convenience functions
for handling it.
"""

from enum import Enum, auto


class Parameter(Enum):
    """An enumeration containing each of the physical parameters
    associated with an optical cavity."""

    BEAMSIZE = auto()
    WAISTSIZE = auto()
    WAISTPOS = auto()
    GOUY = auto()
    DIVERGENCE = auto()
    FSR = auto()
    FWHM = auto()
    FINESSE = auto()
    POLE = auto()
    MODESEP = auto()
    BEAMSIZE_ITM = auto()
    BEAMSIZE_ETM = auto()
    GFACTOR_ITM = auto()
    GFACTOR_ETM = auto()
    GFACTOR_SINGLE = auto()
    CAV_GFACTOR = auto()
    CAV_LENGTH = auto()
    REFLECTIVITY_ITM = auto()
    REFLECTIVITY_ETM = auto()
    WAVELENGTH = auto()
    ROC = auto()
    ROC_ITM = auto()
    ROC_ETM = auto()
    EIGENMODE = auto()


PARAM_SYMBOL_MAP = {
    Parameter.BEAMSIZE: "$w$",
    Parameter.WAISTSIZE: "$w_0$",
    Parameter.WAISTPOS: "$z_0$",
    Parameter.CAV_GFACTOR: "$g$",
    Parameter.GOUY: r"$\psi$",
    Parameter.DIVERGENCE: r"$\theta$",
    Parameter.FSR: r"$\Delta \nu_{\mathrm{FSR}}$",
    Parameter.FWHM: "FWHM",
    Parameter.FINESSE: r"\mathcal{F}",
    Parameter.POLE: r"$\nu_p$",
    Parameter.MODESEP: r"$\delta f$",
    Parameter.BEAMSIZE_ITM: "$w_1$",
    Parameter.BEAMSIZE_ETM: "$w_2$",
    Parameter.GFACTOR_ITM: "$g_1$",
    Parameter.GFACTOR_ETM: "$g_2$",
    Parameter.GFACTOR_SINGLE: "$g_s$",
    Parameter.CAV_LENGTH: "$L$",
    Parameter.REFLECTIVITY_ITM: "$R_1$",
    Parameter.REFLECTIVITY_ETM: "$R_2$",
    Parameter.WAVELENGTH: r"$\lambda$",
    Parameter.ROC: "$R_C$",
    Parameter.ROC_ITM: "$R_{C,1}$",
    Parameter.ROC_ETM: "$R_{C,2}$",
    Parameter.EIGENMODE: "$q$",
}

ARG_PARAM_MAP = {
    "beamsize": Parameter.BEAMSIZE,
    "waistsize": Parameter.WAISTSIZE,
    "stability": Parameter.CAV_GFACTOR,
    "roundtripgouy": Parameter.GOUY,
    "divergence": Parameter.DIVERGENCE,
    "FSR": Parameter.FSR,
    "FWHM": Parameter.FWHM,
    "finesse": Parameter.FINESSE,
    "pole": Parameter.POLE,
    "modesep": Parameter.MODESEP,
    "beamsize_itm": Parameter.BEAMSIZE_ITM,
    "beamsize_etm": Parameter.BEAMSIZE_ETM,
    "stability_itm": Parameter.GFACTOR_ITM,
    "stability_etm": Parameter.GFACTOR_ETM,
    "stability_single": Parameter.GFACTOR_SINGLE,
    "length": Parameter.CAV_LENGTH,
    "itm_reflectivity": Parameter.REFLECTIVITY_ITM,
    "etm_reflectivity": Parameter.REFLECTIVITY_ETM,
    "wavelength": Parameter.WAVELENGTH,
    "curvature": Parameter.ROC,
    "curvature_itm": Parameter.ROC_ITM,
    "curvature_etm": Parameter.ROC_ETM,
}

TARGET_PARAM_MAP = {
    "w": Parameter.BEAMSIZE,
    "w1": Parameter.BEAMSIZE_ITM,
    "w2": Parameter.BEAMSIZE_ETM,
    "w0": Parameter.WAISTSIZE,
    "z0": Parameter.WAISTPOS,
    "g": Parameter.CAV_GFACTOR,
    "g1": Parameter.GFACTOR_ITM,
    "g2": Parameter.GFACTOR_ETM,
    "gs": Parameter.GFACTOR_SINGLE,
    "gouy": Parameter.GOUY,
    "div": Parameter.DIVERGENCE,
    "FSR": Parameter.FSR,
    "FWHM": Parameter.FWHM,
    "finesse": Parameter.FINESSE,
    "pole": Parameter.POLE,
    "modesep": Parameter.MODESEP,
    "Rc": Parameter.ROC,
    "Rc1": Parameter.ROC_ITM,
    "Rc2": Parameter.ROC_ETM,
    "eigenmode": Parameter.EIGENMODE,
    "all": None,
}


def is_distance(p):
    l = [
        Parameter.BEAMSIZE,
        Parameter.WAISTSIZE,
        Parameter.WAISTPOS,
        Parameter.BEAMSIZE_ITM,
        Parameter.BEAMSIZE_ETM,
        Parameter.CAV_LENGTH,
        Parameter.WAVELENGTH,
        Parameter.ROC,
        Parameter.ROC_ITM,
        Parameter.ROC_ETM,
    ]
    return p in l


def is_frequency(p):
    l = [Parameter.FSR, Parameter.FWHM, Parameter.POLE, Parameter.MODESEP]
    return p in l


def is_angle(p):
    l = [Parameter.GOUY, Parameter.DIVERGENCE]
    return p in l


def param_to_config_type(p):
    CONV = {
        Parameter.BEAMSIZE: "beamsize",
        Parameter.BEAMSIZE_ITM: "beamsize",
        Parameter.BEAMSIZE_ETM: "beamsize",
        Parameter.WAISTSIZE: "beamsize",
        Parameter.CAV_LENGTH: "length",
        Parameter.WAISTPOS: "towaist",
        Parameter.ROC: "curvature",
        Parameter.ROC_ITM: "curvature",
        Parameter.ROC_ETM: "curvature",
        Parameter.GOUY: "gouy",
        Parameter.DIVERGENCE: "divergence",
        Parameter.FSR: "frequency",
        Parameter.FWHM: "frequency",
        Parameter.POLE: "frequency",
        Parameter.MODESEP: "frequency",
    }
    if p not in CONV:
        return None

    return CONV[p]


def param_for_printing(p):
    CONV = {
        Parameter.BEAMSIZE: "Radius of beam at mirrors",
        Parameter.WAISTSIZE: "Radius of beam at waist",
        Parameter.WAISTPOS: "Position of beam waist (from first cavity mirror)",
        Parameter.CAV_GFACTOR: "Stability g-factor of cavity",
        Parameter.GOUY: "Round-trip Gouy phase",
        Parameter.DIVERGENCE: "Divergence angle",
        Parameter.FSR: "FSR",
        Parameter.FWHM: "FWHM",
        Parameter.FINESSE: "Finesse",
        Parameter.POLE: "Pole frequency",
        Parameter.MODESEP: "Mode separation frequency",
        Parameter.BEAMSIZE_ITM: "Radius of beam at ITM",
        Parameter.BEAMSIZE_ETM: "Radius of beam at ETM",
        Parameter.GFACTOR_ITM: "Stability g-factor of ITM",
        Parameter.GFACTOR_ETM: "Stability g-factor of ETM",
        Parameter.GFACTOR_SINGLE: "Stability g-factor of both ITM & ETM",
        Parameter.CAV_LENGTH: "Cavity length",
        Parameter.REFLECTIVITY_ITM: "Reflectivity of ITM",
        Parameter.REFLECTIVITY_ETM: "Reflectivity of ETM",
        Parameter.WAVELENGTH: "Wavelength of beam",
        Parameter.ROC: "Radius of curvature of mirrors",
        Parameter.ROC_ITM: "Radius of curvature of ITM",
        Parameter.ROC_ETM: "Radius of curvature of ETM",
        Parameter.EIGENMODE: "Eigenmode",
    }
    return CONV[p]


def param_to_command_arg(p):
    CONV = {
        Parameter.CAV_LENGTH: "-L",
        Parameter.BEAMSIZE: "-w",
        Parameter.CAV_GFACTOR: "-g",
        Parameter.GFACTOR_SINGLE: "-gs",
        Parameter.GFACTOR_ITM: "-g1",
        Parameter.GFACTOR_ETM: "-g2",
        Parameter.GOUY: "-gouy",
        Parameter.DIVERGENCE: "-div",
        Parameter.REFLECTIVITY_ITM: "-R1",
        Parameter.REFLECTIVITY_ETM: "-R2",
        Parameter.ROC: "-Rc",
        Parameter.ROC_ITM: "-Rc1",
        Parameter.ROC_ETM: "-Rc2",
        Parameter.WAVELENGTH: "-wl",
    }
    return CONV[p]
