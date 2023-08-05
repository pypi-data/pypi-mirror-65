"""
Function for computing target parameter(s) from arbritrary number of
physical arguments.
"""

import argparse
import numpy as np

from .parameter import Parameter
from .parameter import ARG_PARAM_MAP, TARGET_PARAM_MAP
from .parameter import param_to_command_arg
from .parsing import add_parser_arguments, handle_parser_namespace
from .units import standard_units_from_param
from .utilities import CavCalcError

_SHORTARG_PARAM = {
    "w": Parameter.BEAMSIZE,
    "w0": Parameter.WAISTSIZE,
    "g": Parameter.CAV_GFACTOR,
    "gouy": Parameter.GOUY,
    "div": Parameter.DIVERGENCE,
    "FSR": Parameter.FSR,
    "fsr": Parameter.FSR,
    "FWHM": Parameter.FWHM,
    "fwhm": Parameter.FWHM,
    "finesse": Parameter.FINESSE,
    "pole": Parameter.POLE,
    "modesep": Parameter.MODESEP,
    "w1": Parameter.BEAMSIZE_ITM,
    "w2": Parameter.BEAMSIZE_ETM,
    "g1": Parameter.GFACTOR_ITM,
    "g2": Parameter.GFACTOR_ETM,
    "gs": Parameter.GFACTOR_SINGLE,
    "L": Parameter.CAV_LENGTH,
    "R1": Parameter.REFLECTIVITY_ITM,
    "R2": Parameter.REFLECTIVITY_ETM,
    "wl": Parameter.WAVELENGTH,
    "Rc": Parameter.ROC,
    "Rc1": Parameter.ROC_ITM,
    "Rc2": Parameter.ROC_ETM,
}


def calculate(target="all", **kwargs):
    """Calculates a target parameter from an arbitrary number of physical arguments.

    If no `target` is specified then the default behaviour is to calculate all computable
    parameters from the given arguments.

    .. note::

        .. rubric:: Targets

        Here is a list of all valid targets.

        * "all" -- all computable parameters from the given arguments.
        * "w" -- beam radius on both cavity mirrors.
        * "w1" -- beam radius on first cavity mirror.
        * "w2" -- beam radius on second cavity mirror.
        * "w0" -- beam radius at the cavity waist.
        * "z0" -- position of beam waist from first cavity mirror.
        * "g" -- stability factor of cavity.
        * "g1" -- stability factor of first mirror.
        * "g2" -- stability factor of second mirror.
        * "gs" -- stability factor of both cavity mirrors.
        * "gouy" -- round-trip gouy phase of the cavity.
        * "div" -- divergence angle of the cavity eigenmode.
        * "FSR" -- free spectral range of the cavity.
        * "FWHM" -- full-width at half maximum of cavity resonance.
        * "finesse" - cavity finesse.
        * "pole" -- pole frequency of the cavity.
        * "modesep" -- mode separation frequency of the cavity.
        * "Rc" -- radius of curvature of both cavity mirrors.
        * "Rc1" -- radius of curvature of first mirror.
        * "Rc2" -- radius of curvature of second mirror.
        * "eigenmode" -- eigenmode of the cavity.

        .. rubric:: Keyword arguments

        This is the list of valid `kwargs` which can be passed to this function. Each argument
        here represents a physical parameter.

        * L -- length of the cavity.
        * wl -- Wavelength of the laser beam.
        * R1 -- reflectivity of the first mirror.
        * R2 -- reflectivity of the second mirror.
        * Rc -- radius of curvature of both cavity mirrors.
        * Rc1 -- radius of curvature of first mirror.
        * Rc2 -- radius of curvature of second mirror.
        * g -- stability factor of cavity.
        * gs -- stability factor of both cavity mirrors.
        * g1 -- stability factor of first mirror.
        * g2 -- stability factor of second mirror.
        * w -- beam radius on both cavity mirrors.
        * w1 -- beam radius on first cavity mirror.
        * w2 -- beam radius on second cavity mirror.
        * w0 -- beam radius at the cavity waist.
        * gouy -- round-trip gouy phase of the cavity.
        * div -- divergence angle of the cavity eigenmode.
        * FSR (or fsr) -- free spectral range of the cavity.
        * FWHM (or fwhm) -- full-width at half maximum of cavity resonance.
        * finesse - cavity finesse.
        * pole -- pole frequency of the cavity.
        * modesep -- mode separation frequency of the cavity.

        Each quantity above can be specified as:

        * A single value which then has standard SI units (e.g. metres for a distance, radians for an angle).
        * A :class:`numpy.ndarray` of values each of which then has standard SI units as above.
        * (If the parameter is *not* a dimensionless quantity) A tuple where:
            * the first element is either a single value or a :class:`numpy.ndarray` of values.
            * the second element is a string representing valid units for the given parameter.

    Parameters
    ----------
    target : str or :class:`.Parameter`, optional
        The target parameter to compute, can be specified as a string (see note above) or
        a constant of the enum :class:`.Parameter`. Defaults to `"all"` so that the function
        computes all the parameters it can from the given inputs.

    **kwargs
        See the note above for details.

    Returns
    -------
    out : :class:`.Output`
        The output object containing the results and methods for plotting them.

    Examples
    --------

    Compute the finesse of a cavity given the reflectivities of the mirrors::

        out = cc.calculate("finesse", R1=0.9, R2=0.99)
        print(out)

    giving::

        Given:
            Reflectivity of ITM = 0.9
            Reflectivity of ETM = 0.99

        Computed:
            Finesse = 54.42678433441527

    Calculate the cavity eigenmode given the length of the cavity and the stability factors of the mirrors::

        out = cc.calculate("eigenmode", L=(4, 'km'), gs=-0.9)
        print(out)

    yielding::

        Given:
            Cavity length = 4.0 km
            Wavelength of beam = 1064 nm
            Stability g-factor of both ITM & ETM = -0.9
            Round-trip Gouy phase = 5.3811316835870615 radians

        Computed:
            Eigenmode = (-2000.0000000000002+458.83146774112333j)

    Determine everything we can from the cavity length and radii of curvature of the mirrors::

        out = cc.calculate(L=(10, 'km), Rc1=(5.1, 'km'), Rc2=5345)
        print(out)

    resulting in::

        Given:
            Cavity length = 10.0 km
            Wavelength of beam = 1064 nm
            Radius of curvature of ITM = 5.1 km
            Radius of curvature of ETM = 5345.0 m

        Computed:
            FSR = 14989.6229 Hz
            Radius of beam at ITM = 8.93350457718444 cm
            Radius of beam at ETM = 9.383153657378871 cm
            Radius of beam at waist = 1.8897287744504574 cm
            Position of beam waist (from first cavity mirror) = 4871.794871794872 m
            Round-trip Gouy phase = 312.3384194061712 degrees
            Stability g-factor of ITM = -0.9607843137254901
            Stability g-factor of ETM = -0.8709073900841908
            Stability g-factor of cavity = 0.836754159100497
            Mode separation frequency = 1984.5253331095876 Hz
            Eigenmode = (-4871.794871794871+1054.404368971903j)
    """
    if (
        target not in TARGET_PARAM_MAP.keys()
        and target not in TARGET_PARAM_MAP.values()
    ):
        raise CavCalcError(f"Unrecognised target: {target} in call to calculate.")

    command = [target]
    for arg, value in kwargs.items():
        if (
            arg not in ARG_PARAM_MAP.keys()
            and arg not in ARG_PARAM_MAP.values()
            and arg not in _SHORTARG_PARAM.keys()
        ):
            raise CavCalcError(
                f"Unrecognised argument: {arg} in arguments to calculate."
            )

        if arg in ARG_PARAM_MAP.keys():
            parg = ARG_PARAM_MAP[arg]
        elif arg in _SHORTARG_PARAM.keys():
            parg = _SHORTARG_PARAM[arg]
        else:
            parg = arg

        if not isinstance(value, tuple):
            v_in_spec_units, units_str = value, standard_units_from_param(parg)
        else:
            if len(value) != 2:
                raise CavCalcError(
                    f"Expected tuple of size 2 for argument: {arg} but got size: {len(value)}."
                )
            v_in_spec_units, units_str = value

        # form the command
        if isinstance(v_in_spec_units, np.ndarray):
            start = np.min(v_in_spec_units)
            stop = np.max(v_in_spec_units)
            num = v_in_spec_units.size

            if num == 2:
                raise CavCalcError(
                    "Data ranges of size 2 are currently not supported due "
                    "to the conflict with upper/lower quadrant computations. "
                    "This is a non-trivial issue and so will be fixed at a later date."
                )

            command.append(f"{param_to_command_arg(parg)}")
            command.append(f"{start} {stop} {num} {units_str}")
        else:
            command.append(f"{param_to_command_arg(parg)}")
            command.append(f"{v_in_spec_units}{units_str}")

    parser = argparse.ArgumentParser()
    # add all the available arguments
    add_parser_arguments(parser)
    # parse the args provided into a Namespace
    args = parser.parse_args(command)
    return handle_parser_namespace(args, from_command_line=False)
