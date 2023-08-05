"""
Physical parameter functions associated with symmetric
optical cavities.
"""

import cmath
import numpy as np

from ..parameter import Parameter
from ..utilities import construct_grids, modesep_adjust
from ..utilities.maths import abcd
from ..utilities.misc import physical_return_dispatcher

## gsingle refers to the g-factor of a single mirror of the
## cavity, gcav is the overall g-factor of the cavity where
## gcav = gsingle * gsingle
##
## note that gsingle is the g-factor of BOTH cavity mirrors
## as this file represents equations for symmetric cavities

### Beam radius relations


@physical_return_dispatcher()
def w_of_gsingle(L, wl, gsingle):
    values = construct_grids(L=L, wl=wl, gsingle=gsingle)
    L = values["L"]
    wl = values["wl"]
    gsingle = values["gsingle"]

    return np.sqrt(L * wl / np.pi * np.sqrt(1 / (1 - gsingle * gsingle)))


@physical_return_dispatcher()
def w_of_gcav(L, wl, gcav):
    values = construct_grids(L=L, wl=wl, gcav=gcav)
    L = values["L"]
    wl = values["wl"]
    gcav = values["gcav"]

    return np.sqrt(L * wl / np.pi * np.sqrt(1 / (1 - gcav)))


@physical_return_dispatcher()
def w_of_rtgouy(L, wl, rtgouy):
    values = construct_grids(L=L, wl=wl, rtgouy=rtgouy)
    L = values["L"]
    wl = values["wl"]
    rtgouy = values["rtgouy"]

    return np.sqrt(L * wl / (np.pi * np.sin(rtgouy * 0.5)))


@physical_return_dispatcher()
def w_of_divang(L, wl, theta):
    values = construct_grids(L=L, wl=wl, theta=theta)
    L = values["L"]
    wl = values["wl"]
    theta = values["theta"]

    factor_L_wl = (L * np.pi / (2 * wl)) ** 2 * np.power(np.tan(theta), 4)
    one_minus_gsqd = 1 - ((1 - factor_L_wl) / (1 + factor_L_wl)) ** 2
    return np.sqrt(L * wl / np.pi * np.sqrt(1 / one_minus_gsqd))


@physical_return_dispatcher()
def w0_of_gsingle(L, wl, gsingle):
    values = construct_grids(L=L, wl=wl, gsingle=gsingle)
    L = values["L"]
    wl = values["wl"]
    gsingle = values["gsingle"]

    return np.sqrt(0.5 * L * wl / np.pi * np.sqrt((1 + gsingle) / (1 - gsingle)))


@physical_return_dispatcher(dual=True)
def w0_of_gcav(L, wl, gcav):
    return w0_of_gsingle(L, wl, gsingle_of_gcav(gcav).v).v


@physical_return_dispatcher()
def w0_of_rtgouy(L, wl, rtgouy):
    values = construct_grids(L=L, wl=wl, rtgouy=rtgouy)
    L = values["L"]
    wl = values["wl"]
    rtgouy = values["rtgouy"]

    inner_sqrt_term = np.sqrt((1 + np.cos(0.5 * rtgouy)) / (1 - np.cos(0.5 * rtgouy)))
    return np.sqrt(0.5 * L * wl / np.pi * inner_sqrt_term)


@physical_return_dispatcher()
def z0_symmetric(L):
    return 0.5 * L


## RoC relations


@physical_return_dispatcher()
def roc_of_gsingle(L, gsingle):
    values = construct_grids(L=L, gsingle=gsingle)
    L = values["L"]
    gsingle = values["gsingle"]

    return L / (1 - gsingle)


## Stability relations

### singular


@physical_return_dispatcher()
def gsingle_of_roc(L, Rc):
    values = construct_grids(L=L, Rc=Rc)
    L = values["L"]
    Rc = values["Rc"]

    return 1 - L / Rc


@physical_return_dispatcher(dual=True)
def gsingle_of_w(L, wl, w):
    values = construct_grids(L=L, wl=wl, w=w)
    L = values["L"]
    wl = values["wl"]
    w = values["w"]

    mag = np.sqrt(1 - (L * wl / (np.pi * w * w)) ** 2)
    return np.array([-mag, mag])


@physical_return_dispatcher()
def gsingle_of_rtgouy(rtgouy):
    return np.cos(0.5 * rtgouy)


@physical_return_dispatcher()
def gsingle_of_divang(L, wl, theta):
    values = construct_grids(L=L, wl=wl, theta=theta)
    L = values["L"]
    wl = values["wl"]
    theta = values["theta"]

    factor_L_wl = (L * np.pi / (2 * wl)) ** 2 * np.power(np.tan(theta), 4)
    return (1 - factor_L_wl) / (1 + factor_L_wl)


@physical_return_dispatcher(dual=True)
def gsingle_of_gcav(gcav):
    mag = np.sqrt(gcav)
    return np.array([-mag, mag])


### cavity


@physical_return_dispatcher()
def gcav_of_roc(L, Rc):
    return gsingle_of_roc(L, Rc).v ** 2


@physical_return_dispatcher()
def gcav_of_gsingle(gsingle):
    return gsingle * gsingle


@physical_return_dispatcher()
def gcav_of_w(L, wl, w):
    return gsingle_of_w(L, wl, w).v[0] ** 2


@physical_return_dispatcher()
def gcav_of_rtgouy(rtgouy):
    return gsingle_of_rtgouy(rtgouy).v ** 2


@physical_return_dispatcher()
def gcav_of_divang(L, wl, theta):
    return gsingle_of_divang(L, wl, theta).v ** 2


# Round-trip Gouy phase relations


@physical_return_dispatcher()
def rtgouy_of_gsingle(gsingle):
    return 2 * np.arccos(gsingle)


@physical_return_dispatcher(dual=True)
def rtgouy_of_gcav(gcav):
    return rtgouy_of_gsingle(gsingle_of_gcav(gcav).v).v


@physical_return_dispatcher()
def rtgouy_of_w(L, wl, w):
    values = construct_grids(L=L, wl=wl, w=w)
    L = values["L"]
    wl = values["wl"]
    w = values["w"]

    return 2 * np.arcsin(L * wl / (np.pi * w * w))


@physical_return_dispatcher()
def rtgouy_of_divang(L, wl, theta):
    values = construct_grids(L=L, wl=wl, theta=theta)
    L = values["L"]
    wl = values["wl"]
    theta = values["theta"]

    factor_L_wl = (L * np.pi / (2 * wl)) ** 2 * np.power(np.tan(theta), 4)
    return 2 * np.arccos((1 - factor_L_wl) / (1 + factor_L_wl))


# Divergence angle relations


@physical_return_dispatcher()
def divang_of_gsingle(L, wl, gsingle):
    values = construct_grids(L=L, wl=wl, gsingle=gsingle)
    L = values["L"]
    wl = values["wl"]
    gsingle = values["gsingle"]

    return np.sqrt(2 * wl / (L * np.pi) * np.sqrt((1 - gsingle) / (1 + gsingle)))


@physical_return_dispatcher(dual=True)
def divang_of_gcav(L, wl, gcav):
    return divang_of_gsingle(L, wl, gsingle_of_gcav(gcav).v).v


@physical_return_dispatcher()
def divang_of_w(L, wl, w):
    values = construct_grids(L=L, wl=wl, w=w)
    L = values["L"]
    wl = values["wl"]
    w = values["w"]

    factor_wl_L = 2 * wl / (L * np.pi)
    inner_sqrt_term = np.sqrt(1 - (L * wl / (np.pi * w * w)) ** 2)
    return np.sqrt(factor_wl_L * np.sqrt((1 - inner_sqrt_term) / (1 + inner_sqrt_term)))


@physical_return_dispatcher()
def divang_of_rtgouy(L, wl, rtgouy):
    values = construct_grids(L=L, wl=wl, rtgouy=rtgouy)
    L = values["L"]
    wl = values["wl"]
    rtgouy = values["rtgouy"]

    factor_wl_L = 2 * wl / (L * np.pi)

    # if not isinstance(rtgouy, np.ndarray):
    # if rtgouy < np.pi:
    #    return np.sqrt(factor_wl_L * 1 / np.tan(0.25 * rtgouy))
    # return np.sqrt(factor_wl_L * np.tan(0.25 * rtgouy))

    nominal = np.sqrt(factor_wl_L * np.tan(0.25 * rtgouy))
    # idx_gouy_less_pi = np.where(rtgouy < np.pi)
    # if len(idx_gouy_less_pi) == 1: # 1D
    #    for idx in idx_gouy_less_pi:
    #        nominal[idx] /= np.tan(0.25 * rtgouy[idx])
    # else: # meshgrid
    #    for idx_i, idx_j in zip(idx_gouy_less_pi[0], idx_gouy_less_pi[1]):
    #        nominal[idx_i][idx_j] /= np.tan(0.25 * rtgouy[idx_i][idx_j])

    return nominal


# Mode separation frequency relations


@physical_return_dispatcher()
def modesep_of_rtgouy(L, rtgouy):
    values = construct_grids(L=L, rtgouy=rtgouy)
    L = values["L"]
    rtgouy = values["rtgouy"]

    return modesep_adjust(rtgouy, L)


@physical_return_dispatcher()
def modesep_of_gsingle(L, gsingle):
    values = construct_grids(L=L, gsingle=gsingle)
    L = values["L"]
    gsingle = values["gsingle"]

    rtgouy = rtgouy_of_gsingle(gsingle).v
    return modesep_adjust(rtgouy, L)


@physical_return_dispatcher(dual=True)
def modesep_of_gcav(L, gcav):
    rtgouy = rtgouy_of_gcav(gcav).v
    return modesep_adjust(rtgouy, L)


@physical_return_dispatcher()
def modesep_of_w(L, wl, w):
    rtgouy = rtgouy_of_w(L, wl, w).v
    return modesep_adjust(rtgouy, L)


@physical_return_dispatcher()
def modesep_of_divang(L, wl, theta):
    rtgouy = rtgouy_of_divang(L, wl, theta).v
    return modesep_adjust(rtgouy, L)


@physical_return_dispatcher()
def eigenmode_of_Rc(L, Rc):
    if isinstance(L, np.ndarray) or isinstance(Rc, np.ndarray):
        print(
            "WARNING: Computing ABCD matrices over data ranges is not yet supported, "
            "setting eigenmode to None."
        )
        return None

    ABCD = abcd(L, Rc, Rc)

    C = ABCD[1][0]
    D_minus_A = ABCD[1][1] - ABCD[0][0]
    minus_B = -ABCD[0][1]

    sqrt_term = cmath.sqrt(D_minus_A * D_minus_A - 4 * C * minus_B)
    upper = 0.5 * (D_minus_A + sqrt_term) / C
    lower = 0.5 * (D_minus_A - sqrt_term) / C

    if np.imag(upper) > 0.0:
        return upper
    elif np.imag(lower) > 0.0:
        return lower


FUNC_DEPENDENCIES_MAP = {
    w_of_gsingle: (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.GFACTOR_SINGLE),
        Parameter.BEAMSIZE,
    ),
    w_of_gcav: (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.CAV_GFACTOR),
        Parameter.BEAMSIZE,
    ),
    w_of_rtgouy: (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.GOUY),
        Parameter.BEAMSIZE,
    ),
    w_of_divang: (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.DIVERGENCE),
        Parameter.BEAMSIZE,
    ),
    w0_of_gsingle: (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.GFACTOR_SINGLE),
        Parameter.WAISTSIZE,
    ),
    w0_of_gcav: (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.CAV_GFACTOR),
        Parameter.WAISTSIZE,
    ),
    w0_of_rtgouy: (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.GOUY),
        Parameter.WAISTSIZE,
    ),
    z0_symmetric: ((Parameter.CAV_LENGTH,), Parameter.WAISTPOS,),
    gsingle_of_roc: ((Parameter.CAV_LENGTH, Parameter.ROC), Parameter.GFACTOR_SINGLE),
    gsingle_of_w: (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.BEAMSIZE),
        Parameter.GFACTOR_SINGLE,
    ),
    gsingle_of_rtgouy: ((Parameter.GOUY,), Parameter.GFACTOR_SINGLE),
    gsingle_of_divang: (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.DIVERGENCE),
        Parameter.GFACTOR_SINGLE,
    ),
    gsingle_of_gcav: ((Parameter.CAV_GFACTOR,), Parameter.GFACTOR_SINGLE),
    gcav_of_roc: ((Parameter.CAV_LENGTH, Parameter.ROC), Parameter.CAV_GFACTOR),
    gcav_of_gsingle: ((Parameter.GFACTOR_SINGLE,), Parameter.CAV_GFACTOR),
    gcav_of_w: (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.BEAMSIZE),
        Parameter.CAV_GFACTOR,
    ),
    gcav_of_rtgouy: ((Parameter.GOUY,), Parameter.CAV_GFACTOR),
    gcav_of_divang: (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.DIVERGENCE),
        Parameter.CAV_GFACTOR,
    ),
    rtgouy_of_gsingle: ((Parameter.GFACTOR_SINGLE,), Parameter.GOUY,),
    rtgouy_of_gcav: ((Parameter.CAV_GFACTOR,), Parameter.GOUY,),
    rtgouy_of_w: (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.BEAMSIZE),
        Parameter.GOUY,
    ),
    rtgouy_of_divang: (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.DIVERGENCE),
        Parameter.GOUY,
    ),
    divang_of_gsingle: (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.GFACTOR_SINGLE),
        Parameter.DIVERGENCE,
    ),
    divang_of_gcav: (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.CAV_GFACTOR),
        Parameter.DIVERGENCE,
    ),
    divang_of_w: (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.BEAMSIZE),
        Parameter.DIVERGENCE,
    ),
    divang_of_rtgouy: (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.GOUY),
        Parameter.DIVERGENCE,
    ),
    modesep_of_rtgouy: ((Parameter.CAV_LENGTH, Parameter.GOUY), Parameter.MODESEP,),
    modesep_of_gsingle: (
        (Parameter.CAV_LENGTH, Parameter.GFACTOR_SINGLE),
        Parameter.MODESEP,
    ),
    modesep_of_gcav: (
        (Parameter.CAV_LENGTH, Parameter.CAV_GFACTOR),
        Parameter.MODESEP,
    ),
    modesep_of_w: (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.BEAMSIZE),
        Parameter.MODESEP,
    ),
    modesep_of_divang: (
        (Parameter.CAV_LENGTH, Parameter.WAVELENGTH, Parameter.DIVERGENCE),
        Parameter.MODESEP,
    ),
    roc_of_gsingle: ((Parameter.CAV_LENGTH, Parameter.GFACTOR_SINGLE), Parameter.ROC,),
    eigenmode_of_Rc: ((Parameter.CAV_LENGTH, Parameter.ROC), Parameter.EIGENMODE,),
}
