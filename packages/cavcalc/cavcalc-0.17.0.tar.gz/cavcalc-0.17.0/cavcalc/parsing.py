from collections import namedtuple
import os

import numpy as np

from .handler import Handler
from .parameter import ARG_PARAM_MAP, TARGET_PARAM_MAP
from .units import SI_DISTANCE_MAP, SI_FREQ_MAP, units_convert, check_units_validity
from .utilities import quit_print
from . import __version__

# v is the quantity stored in the given units
# calcv is this quantity converted for computation
# purposes into the standard (e.g. metres for distances,
# Hz for frequencies etc.)
PhysicalQuantity = namedtuple("PhysicalQuantity", "v calcv units")

# fromvar is either 'x' or 'y'
# var is the variable corresponding to a data range
# condition is the type of condition (e.g. '=')
# value is the value of the condition in the given units
# -> this units field is grabbed from the x-axis variable units
ConditionArgument = namedtuple("ConditionArgument", "fromvar var condition value units")


def units(string):
    def check(u_str):
        if (
            u_str in SI_DISTANCE_MAP
            or u_str in SI_FREQ_MAP
            or u_str.lower() in ("deg", "degrees", "rad", "rads", "radians")
        ):
            return u_str
        quit_print(f"ERROR: Invalid output units: {u_str}")

    all_units = string.split(" ")
    if len(all_units) == 1:
        return check(string)
    else:
        rtn = []
        for u_str in all_units:
            rtn.append(check(u_str))
        return rtn


def _parse_data_range(string, ptype):
    if ptype in ("linspace", "range"):
        args_and_units = (string.split("(")[1]).split(")")
        args = args_and_units[0].split(",")
        units_ = ""
        if len(args) != 3:
            quit_print(
                f"ERROR: Parsing range - expected 3 arguments to {ptype} in string: {string} "
                f"but got {len(args)}"
            )
        if len(args_and_units) > 1:
            units_ = args_and_units[1].strip()
        try:
            start = float(args[0])
            stop = float(args[1])
            if ptype == "linspace":
                num = int(args[2])
                quantity_in_specified_units = np.linspace(start, stop, num)
            else:
                step = float(args[2])
                quantity_in_specified_units = np.arange(start, stop, step)

            if quantity_in_specified_units.size == 2:
                quit_print(
                    "Data ranges of size 2 are currently not supported due "
                    "to the conflict with upper/lower quadrant computations. "
                    "This is a non-trivial issue and so will be fixed at a later date."
                )

            quantity_in_standard_units = units_convert(
                quantity_in_specified_units, units_
            )
            return PhysicalQuantity(
                quantity_in_specified_units, quantity_in_standard_units, units_
            )
        except ValueError:
            quit_print(f"ERROR: Unable to parse args of {ptype} in string: {string}")
    else:
        args = string.split(" ")
        units_ = ""
        if ptype == "datarange_units":
            units_ = args[-1]
        try:
            start = float(args[0])
            stop = float(args[1])
            num = int(args[2])
            quantity_in_specified_units = np.linspace(start, stop, num)

            if quantity_in_specified_units.size == 2:
                quit_print(
                    "Data ranges of size 2 are currently not supported due "
                    "to the conflict with upper/lower quadrant computations. "
                    "This is a non-trivial issue and so will be fixed at a later date."
                )

            quantity_in_standard_units = units_convert(
                quantity_in_specified_units, units_
            )
            return PhysicalQuantity(
                quantity_in_specified_units, quantity_in_standard_units, units_
            )
        except ValueError:
            quit_print(f"ERROR: Unable to parse args in string: {string}")


def float_file_range(string):
    """Returns a np.array of data loaded from the
    file with name `string` if it exists, a np.array
    of data initialised from a user-defined range if
    specified or a single value for the float conversion
    of `string` otherwise."""
    # first try opening argument as a file...
    if os.path.isfile(string):
        data = None
        if string.endswith(".npy"):  # load from numpy array file
            data = np.load(string)
        else:  # load from text/csv file
            data = np.loadtxt(string)
        if data is None:
            quit_print(f"Unable to parse file {string}")
        else:
            if data.size == 2:
                quit_print(
                    "Data ranges of size 2 are currently not supported due "
                    "to the conflict with upper/lower quadrant computations. "
                    "This is a non-trivial issue and so will be fixed at a later date."
                )
        return data
    # ... then try parsing as a range...
    nargs = len(string.split(" "))
    if "linspace" in string.lower():
        return _parse_data_range(string, "linspace")
    elif "range" in string.lower():
        return _parse_data_range(string, "range")
    elif nargs == 3:
        return _parse_data_range(string, "datarange")
    elif nargs == 4:
        return _parse_data_range(string, "datarange_units")
    # ... if that fails then attempt to convert
    # the argument to a floating point number
    unit_start_idx = len(string)
    poss_exp = False
    for i, char in enumerate(string):
        try:
            if char == "." or char == "-":
                continue
            if char == "e":
                poss_exp = True
                continue
            _ = float(char)
        except ValueError:
            if not i and not poss_exp:
                quit_print(
                    f"{string} must be a number (with optional units) or refer "
                    "to a file of 1D data."
                )
            unit_start_idx = i
            break
    # now store the number and units
    quantity_in_specified_units = float(string[:unit_start_idx])
    specified_units = string[unit_start_idx:]
    quantity_in_standard_units = units_convert(
        quantity_in_specified_units, specified_units
    )
    return PhysicalQuantity(
        quantity_in_specified_units, quantity_in_standard_units, specified_units
    )


def condition_t(string):
    delim = "="
    if "=" not in string:
        quit_print(f"Unrecognised condition in string: {string}")
    # now split around the correct character(s)
    var_and_condition = string.split(delim)
    var = var_and_condition[0]
    val = var_and_condition[1]
    try:
        val = float(val)
    except ValueError:
        quit_print(f"The value of the condition: {val} must be a number.")
    # empty string for units initially, as we will grab the units of the
    # x-axis later on in handle_parser_namespace
    return ConditionArgument(var, var, delim, val, "")


def limits_t(string):
    lo_hi_s = string.split(" ")
    if len(lo_hi_s) == 1:
        quit_print('Expected limits specified as "<low> <high>".')
    lo_s, hi_s = lo_hi_s
    try:
        lo = float(lo_s)
    except ValueError:
        quit_print(f"Lower limit: {lo_s} must be convertible to a number.")
    try:
        hi = float(hi_s)
    except ValueError:
        quit_print(f"Upper limit: {hi_s} must be convertible to a number.")
    return lo, hi


def add_parser_arguments(parser):
    _add_target_arguments(parser)
    _add_physical_parameter_arguments(parser)
    _add_plotting_arguments(parser)
    _add_file_arguments(parser)
    _add_misc_arguments(parser)


def _add_target_arguments(parser):
    target_group = parser.add_argument_group(
        "Compute targets", "Arguments related to the target parameter to compute."
    )
    target_group.add_argument(
        "compute",
        choices=list(TARGET_PARAM_MAP.keys()),
        help="Choice of parameter to compute. Default is all for computing all available "
        "parameters from the given input values.",
        nargs="?",
        default="all",
    )
    target_group.add_argument(
        "-u",
        "--units",
        help="Units of output. If the compute target is all then you can pass multiple "
        'output units here - e.g: -u "cm deg kHz" to give output distances in '
        " cm, angles/phase in degrees and frequencies in kHz. Note that if this option "
        "is specified then it will override the associated unit option in the config file.",
        type=units,
    )


def _add_physical_parameter_arguments(parser):
    physical_group = parser.add_argument_group(
        "Physical parameters",
        "Arguments which are the dependencies of the target parameter function. All of "
        "these arguments can be specified as <value>[<units>] (single value, units optional), "
        '"<start> <stop> <num> [<units>]" (range of values, units optional), '
        '"linspace(<start>, <stop>, <num>) [<units>]" (range of values, units optional) or '
        '"range(<start>, <stop>, <step>) [<units>]" (range of values, units optional). All '
        "distances default to metres, angles and phases to radians, if no units are specified.",
    )
    physical_group.add_argument(
        "-L", "--length", help="Length of the cavity.", type=float_file_range
    )
    physical_group.add_argument(
        "-wl",
        "--wavelength",
        help="Wavelength of the beam, defaults to 1064nm.",
        type=float_file_range,
        default=PhysicalQuantity(1064, 1064e-9, "nm"),
    )
    physical_group.add_argument(
        "-w",
        "--beamsize",
        help="Radius of the beam at both mirrors for a symmetric cavity.",
        type=float_file_range,
    )
    physical_group.add_argument(
        "-g",
        "--stability",
        help="Overall cavity stability factor.",
        type=float_file_range,
    )
    physical_group.add_argument(
        "-g1",
        "--stability_itm",
        help="Stability factor of the first cavity mirror.",
        type=float_file_range,
    )
    physical_group.add_argument(
        "-g2",
        "--stability_etm",
        help="Stability factor of the second cavity mirror.",
        type=float_file_range,
    )
    physical_group.add_argument(
        "-gs",
        "--stability_single",
        help="Stability factor of both cavity mirrors. Use this instead of "
        "-g1 or -g2 for symmetric cavity calculations.",
        type=float_file_range,
    )
    physical_group.add_argument(
        "-gouy", "--roundtripgouy", help="Round-trip Gouy phase.", type=float_file_range
    )
    physical_group.add_argument(
        "-div", "--divergence", help="Divergence angle.", type=float_file_range
    )
    physical_group.add_argument(
        "-R1",
        "--itm_reflectivity",
        help="Reflectivity of the first cavity mirror.",
        type=float_file_range,
    )
    physical_group.add_argument(
        "-R2",
        "--etm_reflectivity",
        help="Reflectivity of the second cavity mirror.",
        type=float_file_range,
    )
    physical_group.add_argument(
        "-T1",
        "--itm_transmission",
        help="Transmission of the first cavity mirror. NOTE: this argument is only "
        "used to compute itm_reflectivity.",
        type=float_file_range,
    )
    physical_group.add_argument(
        "-T2",
        "--etm_transmission",
        help="Transmission of the second cavity mirror. NOTE: this argument is only "
        "used to compute etm_reflectivity.",
        type=float_file_range,
    )
    physical_group.add_argument(
        "-L1",
        "--itm_loss",
        help="Loss of the first cavity mirror. NOTE: this argument is only "
        "used (with itm_transmission) to compute itm_reflectivity.",
        type=float_file_range,
    )
    physical_group.add_argument(
        "-L2",
        "--etm_loss",
        help="Loss of the second cavity mirror. NOTE: this argument is only "
        "used (with etm_transmission) to compute itm_reflectivity.",
        type=float_file_range,
    )
    physical_group.add_argument(
        "-Rc",
        "--curvature",
        help="Radius of curvature of both mirrors for a symmetric cavity.",
        type=float_file_range,
    )
    physical_group.add_argument(
        "-Rc1",
        "--curvature_itm",
        help="Radius of curvature of the first cavity mirror.",
        type=float_file_range,
    )
    physical_group.add_argument(
        "-Rc2",
        "--curvature_etm",
        help="Radius of curvature of the second cavity mirror.",
        type=float_file_range,
    )


def _add_file_arguments(parser):
    file_group = parser.add_argument_group(
        "File options", "Arguments for writing results to files"
    )
    file_group.add_argument(
        "-out",
        "--outputfile",
        help="Name of file to output computed data to.",
        type=str,
    )


def _add_misc_arguments(parser):
    misc_group = parser.add_argument_group(
        "Miscellaneous options",
        "Arguments for display formatting and information about cavcalc.",
    )
    misc_group.add_argument(
        "-V",
        "--version",
        help="Current version of cavcalc.",
        action="version",
        version=f"cavcalc v{__version__}",
    )
    misc_group.add_argument(
        "--dps",
        help="Number of decimal places to display computed results to.",
        type=int,
    )


def _add_plotting_arguments(parser):
    plotting_group = parser.add_argument_group(
        "Plotting options", "Arguments for generating plots."
    )
    plotting_group.add_argument(
        "--plot",
        dest="plot",
        action="store_true",
        help="Plot the target data on linear scales.",
    )
    plotting_group.add_argument(
        "--cmap",
        dest="cmap",
        help="matplotlib colormap to use for the generated image plot.",
        type=str,
    )
    plotting_group.add_argument(
        "--find",
        dest="find",
        help="Find the point(s) at which some condition is satisfied. Format as e.g. "
        '--find "y=<value>" to find the point in the data range corresponding to '
        "where the target parameter is nearest to the given value.",
        type=condition_t,
    )
    plotting_group.add_argument(
        "--logxplot",
        dest="semilogx",
        action="store_true",
        help="Plot the target data with log-scale x-axis.",
    )
    plotting_group.add_argument(
        "--logyplot",
        dest="semilogy",
        action="store_true",
        help="Plot the target data with log-scale y-axis.",
    )
    plotting_group.add_argument(
        "--logplot",
        dest="loglog",
        action="store_true",
        help="Plot the target data on a log-log scale.",
    )
    plotting_group.add_argument(
        "--saveplot", help="Save the figure with the specified name."
    )
    plotting_group.add_argument(
        "--xlim", dest="xlim", help="Limits of x-axis.", type=limits_t
    )
    plotting_group.add_argument(
        "--ylim", dest="ylim", help="Limits of y-axis.", type=limits_t
    )
    plotting_group.add_argument(
        "--zlim", dest="zlim", help="Limits of z-axis.", type=limits_t
    )
    parser.set_defaults(
        plot=False, semilogx=False, semilogy=False, loglog=False, cmap="cividis"
    )


def check_arraylike_args(args, from_command_line):
    n_arrays = 0
    for _, value in vars(args).items():
        if isinstance(value, PhysicalQuantity):
            if isinstance(value.v, np.ndarray):
                n_arrays += 1
    if not n_arrays and args.plot:
        quit_print(
            "Incorrect usage. A parameter must be a range or data from a file "
            "in order to plot the results."
        )
    if n_arrays > 2:
        quit_print(
            "Cannot compute results for more than two array-like arguments.",
            from_command_line,
        )


def check_physical_parameters(args, from_command_line):
    for argname, value in vars(args).items():
        if value is not None and argname in ARG_PARAM_MAP.keys():
            check_units_validity(ARG_PARAM_MAP[argname], value.units)

    if args.itm_transmission is not None and args.itm_reflectivity is not None:
        quit_print(
            "Incorrect usage. Cannot specify both input mirror reflectivity and transmission.",
            from_command_line,
        )
    if args.etm_transmission is not None and args.etm_reflectivity is not None:
        quit_print(
            "Incorrect usage. Cannot specify both end mirror reflectivity and transmission.",
            from_command_line,
        )

    if args.itm_reflectivity is not None and args.itm_loss is not None:
        print("WARNING: ignoring argument -L1 as -R1 has already been specified.")
    if args.etm_reflectivity is not None and args.etm_loss is not None:
        print("WARNING: ignoring argument -L2 as -R2 has already been specified.")

    if args.itm_transmission is not None:
        R1 = 1 - args.itm_transmission.v
        if args.itm_loss is not None:
            R1 -= args.itm_loss.v
        args.itm_reflectivity = PhysicalQuantity(R1, R1, "")
    if args.etm_transmission is not None:
        R2 = 1 - args.etm_transmission.v
        if args.etm_loss is not None:
            R2 -= args.etm_loss.v
        args.etm_reflectivity = PhysicalQuantity(R2, R2, "")

    if args.itm_reflectivity is not None:
        if np.any(args.itm_reflectivity.v < 0.0) or np.any(
            args.itm_reflectivity.v > 1.0
        ):
            quit_print(
                "ITM reflectivity R1 is invalid. Value(s) "
                "must satisfy 0 <= R1 <= 1.",
                from_command_line,
            )
    if args.etm_reflectivity is not None:
        if np.any(args.etm_reflectivity.v < 0.0) or np.any(
            args.etm_reflectivity.v > 1.0
        ):
            quit_print(
                "ETM reflectivity R2 is invalid. Value(s) "
                "must satisfy 0 <= R2 <= 1.",
                from_command_line,
            )


def asymmetric_sanity_checks(args, from_command_line):
    if args.stability is not None and (
        args.stability_itm is not None
        or args.stability_etm is not None
        or args.stability_single is not None
    ):
        quit_print(
            "Incorrect usage. Cavity g-factor and g-factor of one/both mirrors cannot "
            "be specified simultaneously. To specify an asymmetric "
            "cavity please use both g1 and g2 (do not give a value for g), to specify a "
            "symmetric cavity please use either g or gs (g is then gs*gs where "
            "gs = g1 =  g2).",
            from_command_line,
        )

    if args.curvature is not None and (
        args.curvature_itm is not None or args.curvature_etm is not None
    ):
        quit_print(
            "Incorrect usage. Symmetric curvature Rc and individual (asymmetric), Rc1 and Rc2, "
            "curvatures cannot be specified simulataneously. To specify an asymmetric cavity "
            "please use both Rc1 and Rc2 (do not give a value for Rc). To specify a symmetric "
            "cavity please use either Rc or one of Rc1 or Rc2 (Rc is then Rc = Rc1 = Rc2).",
            from_command_line,
        )


def handle_parser_namespace(args, from_command_line=True):
    if isinstance(args.units, list) and args.compute != "all":
        quit_print(
            "Incorrect usage. Multiple output units can only be "
            "specified for a compute target of all."
        )

    # check that the user hasn't specified an illogical
    # combination of symmetric and asymmetric parameters
    asymmetric_sanity_checks(args, from_command_line)

    # check the number of arguments specified as data
    # ranges or files of input data
    check_arraylike_args(args, from_command_line)

    # physical parameter sanity checks
    check_physical_parameters(args, from_command_line)

    # do some re-initialising of args.find by setting
    # args.find.var to the data range argument
    if args.find is not None:
        valid_find = False
        for argname, value in vars(args).items():
            if isinstance(value, PhysicalQuantity):
                if isinstance(value.v, np.ndarray):
                    args.find = ConditionArgument(
                        args.find.fromvar,
                        argname,
                        args.find.condition,
                        args.find.value,
                        value.units,
                    )
                    valid_find = True
                    break
        if not valid_find:
            quit_print(
                "Variable of condition passed to --find must be "
                "initialised with a range of data or file."
            )

    handler = Handler(args, from_command_line)
    return handler.run()
