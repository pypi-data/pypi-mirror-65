from collections import namedtuple
import warnings

import numpy as np

from .functions import general
from .functions import symmetric as symm
from .functions import asymmetric as asymm
from .output import Output

from . import plotting

from .parameter import (
    ARG_PARAM_MAP,
    PARAM_SYMBOL_MAP,
    TARGET_PARAM_MAP,
    Parameter,
    is_angle,
    is_distance,
    is_frequency,
    param_for_printing,
    param_to_command_arg,
    param_to_config_type,
)
from .units import SI_DISTANCE_MAP, SI_FREQ_MAP, standard_units_from_param
from .utilities import dummy_return, find_nearest, save_result, quit_print, bug

from . import CONFIG

SingularComputable = namedtuple("SingularComputable", "function arg_calcvs arg_ts")


class Handler(object):
    def __init__(self, args, command_line=True):
        self.args = args
        self.cl = command_line

        self.target = self.args.compute
        self.compute_all = self.args.compute == "all"

        self.units_str = ""
        if not self.compute_all:
            self.ptarget = TARGET_PARAM_MAP[self.target]

            std_units_of_target = standard_units_from_param(self.ptarget)

            self.units = self.args.units
            self.units_map = None
            if self.args.units is not None:
                if std_units_of_target == "m":
                    if self.args.units not in SI_DISTANCE_MAP:
                        quit_print(
                            "ERROR: Invalid output units given for " f"{self.target}",
                            self.cl,
                        )

                    self.units_map = SI_DISTANCE_MAP
                elif std_units_of_target == "Hz":
                    if self.args.units not in SI_FREQ_MAP:
                        quit_print(
                            "ERROR: Invalid output units given for " f"{self.target}",
                            self.cl,
                        )

                    self.units_map = SI_FREQ_MAP
                elif std_units_of_target == "radians":
                    if args.units.lower() in ("deg", "degrees"):
                        self.units = (np.degrees, "degrees")
                    elif args.units.lower() in ("rad", "rads", "radians"):
                        self.units = (dummy_return, "radians")
                    else:
                        quit_print(
                            "ERROR: Invalid output units given for " f"{self.target}",
                            self.cl,
                        )
            else:
                config_type = param_to_config_type(self.ptarget)
                if config_type is None:
                    self.units = std_units_of_target
                else:
                    config_units = CONFIG["units"].get(config_type)
                    if is_angle(self.ptarget):
                        if config_units.lower() in ("deg", "degrees"):
                            self.units = (np.degrees, "degrees")
                        elif config_units.lower() in ("rad", "rads", "radians"):
                            self.units = (dummy_return, "radians")
                    else:
                        self.units = config_units
                        if is_distance(self.ptarget):
                            self.units_map = SI_DISTANCE_MAP
                        elif is_frequency(self.ptarget):
                            self.units_map = SI_FREQ_MAP

            if isinstance(self.units, str):
                self.units_str = self.units
            else:
                if not isinstance(self.units, tuple) or not isinstance(
                    self.units[1], str
                ):
                    bug(
                        "\nBug encountered! Unrecognised type of parsed units"
                        f"passed to handler: {self.units}",
                        self.cl,
                    )

                self.units_str = self.units[1]
        else:
            if self.args.units is not None:
                print(
                    "WARNING: -u option is not yet supported for a compute target of all, ignoring "
                    "it and using units from config file for now."
                )

            self.units = {}
            for k, v in CONFIG["units"].items():
                v_ = v.strip()
                if k == "gouy" or k == "divergence":
                    if v_.lower() in ("deg", "degrees"):
                        self.units[k] = (np.degrees, "degrees")
                    else:
                        self.units[k] = (dummy_return, "radians")
                else:
                    self.units[k] = v.strip()

        self.symmetric = not (
            self.args.stability_itm is not None
            or self.args.stability_etm is not None
            or self.args.curvature_itm is not None
            or self.args.curvature_etm is not None
        )

        self.all_funcs_map = {}
        func_maps = [
            general.FUNC_DEPENDENCIES_MAP,
            symm.FUNC_DEPENDENCIES_MAP,
            asymm.FUNC_DEPENDENCIES_MAP,
        ]
        for fm in func_maps:
            self.all_funcs_map.update(fm)

        self.func_dependency_map = {}
        if self.symmetric:
            func_maps.remove(asymm.FUNC_DEPENDENCIES_MAP)
        else:
            func_maps.remove(symm.FUNC_DEPENDENCIES_MAP)
        for fm in func_maps:
            self.func_dependency_map.update(fm)

        self.given_physical_args = self.all_specified_physical_args()
        self.chained_args = {}

        if not self.compute_all:
            self.all_reqd_params = self.all_required_arguments()

        self.chain_triggered = set()

    def constant_args(self):
        constants = []
        for pname, val in self.given_physical_args.items():
            if not isinstance(val.v, np.ndarray):
                constants.append((pname, val.v, val.units))

        return constants

    def array_args(self):
        arrays = []
        for pname, val in self.given_physical_args.items():
            if isinstance(val.v, np.ndarray):
                arrays.append((pname, val.v, val.units))

        return arrays

    def all_specified_physical_args(self):
        given = {}

        for argname, value in vars(self.args).items():
            if value is not None and argname in ARG_PARAM_MAP.keys():
                given[ARG_PARAM_MAP[argname]] = value

        return given

    def specified(self):
        given = {}

        given.update(self.given_physical_args)
        given.update(self.chained_args)

        return given

    def all_required_arguments(self, ptarget=None):
        all_reqd = []

        if ptarget is None:
            ptarget = self.ptarget

        for _, (reqd_params, return_param) in self.all_funcs_map.items():
            if return_param == ptarget:
                all_reqd.append(reqd_params)

        return all_reqd

    def all_functions_from_target(self, ptarget=None):
        targets = {}

        if ptarget is None:
            ptarget = self.ptarget

        for func, (reqd_params, return_param) in self.func_dependency_map.items():
            if return_param == ptarget:
                targets[func] = (reqd_params, return_param)

        return targets

    def all_targets_in_dependency_map(self):
        targets = set()

        for _, return_param in self.func_dependency_map.values():
            targets.add(return_param)

        return targets

    def filter_computable(self, targets_map):
        to_compute = None
        arguments = None
        args_for_doplot = []

        for func, (reqd_params, _) in targets_map.items():
            params_diff = set(reqd_params).difference(self.given_physical_args.keys())
            if not params_diff:
                to_compute = func
                arguments = (self.given_physical_args[p].calcv for p in reqd_params)
                for p in reqd_params:
                    args_for_doplot.append(
                        (
                            self.given_physical_args[p].v,
                            p,
                            self.given_physical_args[p].units,
                        )
                    )
                break

        if to_compute is None:
            return self.chained_target(targets_map)

        return SingularComputable(to_compute, arguments, args_for_doplot)

    def filter_computables(self):
        to_compute = {}
        targets_to_compute = set()

        # Here we want to find all the functions of each target type that we CAN compute
        # from the given args and add them to our computables container to avoid adding
        # the wrong function later on during chained target calls
        if self.compute_all:
            specified_ = self.specified()
            all_targets = self.all_targets_in_dependency_map()
            for target in all_targets:
                if target in self.given_physical_args:
                    continue

                funcs_from_target = self.all_functions_from_target(target)

                for func, (reqd_params, return_param) in funcs_from_target.items():
                    pdiff = set(reqd_params).difference(specified_.keys())
                    if not pdiff:
                        to_compute[func] = (
                            (specified_[p].calcv for p in reqd_params),
                            return_param,
                        )
                        targets_to_compute.add(return_param)
                        break

        for func, (reqd_params, return_param) in self.func_dependency_map.items():
            if func in to_compute or return_param in targets_to_compute:
                continue

            specified = self.specified()

            params_diff = set(reqd_params).difference(specified.keys())

            if not params_diff:
                if func not in to_compute:
                    if self.compute_all and return_param in self.given_physical_args:
                        continue

                    to_compute[func] = (
                        (specified[p].calcv for p in reqd_params),
                        return_param,
                    )
                    targets_to_compute.add(return_param)
            else:
                if func not in self.chain_triggered and return_param not in specified:
                    self.chain_triggered.add(func)
                    sc = self.chained_target(
                        self.all_functions_from_target(return_param)
                    )
                    if sc is not None and sc.function not in to_compute:
                        to_compute[sc.function] = (sc.arg_calcvs, return_param)
                        targets_to_compute.add(return_param)

        return to_compute

    def chained_target(self, targets):
        from .parsing import PhysicalQuantity

        computables = self.filter_computables()

        func_result = {}
        # see if any of the return parameters in our computable functions
        # are in the required parameters of the target function map...
        for _, (reqd_params, _) in targets.items():
            for func, (values, rtn_param) in computables.items():
                if rtn_param in reqd_params:
                    try:
                        vals = [val for val in values]
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore", category=RuntimeWarning)

                            try:
                                # FIXME losing is_dual information here, need to pass it on
                                result, _ = func(*vals)
                                func_result[rtn_param] = result
                            except ZeroDivisionError:
                                quit_print(
                                    "ERROR: Division by zero occurred in function: "
                                    f"{func}",
                                    self.cl,
                                )
                    except Exception as e:
                        func_params = tuple(
                            param_to_command_arg(p).strip("-") for p in reqd_params
                        )
                        fp = ", ".join(func_params)
                        bug(
                            "\nBug encountered! The following error occurred:"
                            f'\n\n\t"{e}"\n\nwhen calling {func.__name__}({fp}) '
                            f"with:\n\t{vals}.",
                            self.cl,
                        )

            if func_result:
                break

        # ... if not then we've hit the end of the road and cannot compute
        # the target parameter from any combination of input arguments
        if not func_result:
            return None

        args_for_plot = []
        # make new entries in the given map from the results of this function call
        for param, values in func_result.items():
            self.chained_args[param] = PhysicalQuantity(values, values, "")

        # finally get the function to compute using the new given args dictionary
        func_to_compute = None
        arguments = None

        specified = self.specified()

        for target_func, (reqd_params, _) in targets.items():
            params_diff = set(reqd_params).difference(specified.keys())

            if not params_diff:
                func_to_compute = target_func
                arguments = (specified[p].calcv for p in reqd_params)

                # grab all the required parameters for the function to be computed
                # as well as the parameter which started the chained calls
                needed_args = list(reqd_params) + list(
                    set(specified.keys()).difference(reqd_params)
                )

                for p in needed_args:
                    if p in func_result:
                        continue

                    args_for_plot.append((specified[p].v, p, specified[p].units))
                break

        return SingularComputable(func_to_compute, arguments, args_for_plot)

    def find_conditions(self, result):
        if self.args.find is None:
            return None

        if self.args.find.fromvar == "x":
            if self.args.find.condition == "=":
                idx = find_nearest(
                    vars(self.args)[self.args.find.var].v, self.args.find.value
                )
                return result[idx]
        else:
            if self.args.find.condition == "=":
                idx = find_nearest(result, self.args.find.value)
                return vars(self.args)[self.args.find.var].v[idx]

    def print_found_conditions(self, found):
        if found is None:
            return

        afind = self.args.find
        if afind.fromvar == "x":
            print(
                f"At {afind.var} = {afind.value} {afind.units}, "
                f"{self.target} = {found} {self.units_str}"
            )
        else:
            print(
                f"At {self.target} = {afind.value} {self.units_str}, "
                f"{afind.var} = {found} {afind.units}"
            )

    def _print_result(self, result, computable, is_dual):
        if not isinstance(result, np.ndarray) or result.size == 2:
            print("Given [{}SYMMETRIC CAVITY]:".format("" if self.symmetric else "A"))

            for argvals, argparam, argunits in computable.arg_ts:
                if not argunits:
                    argunits = standard_units_from_param(argparam)
                print(f"\t{param_for_printing(argparam)} = {argvals} {argunits}")

            print("\nComputed:")
            # TODO some cleaning up here - move common printing code to separate function
            if self.args.dps is None:
                if not is_dual:
                    print(
                        f"\t{param_for_printing(self.ptarget)} = "
                        f"{result} {self.units_str}"
                    )
                else:
                    print(
                        f"\t{param_for_printing(self.ptarget)}:\n"
                        f"\t\tLower Quadrant = {result[0]} {self.units_str}, "
                        f"Upper Quadrant = {result[1]} {self.units_str}"
                    )
            else:
                if not is_dual:
                    print(
                        f"\t{param_for_printing(self.ptarget)} = "
                        f"{np.round(result, self.args.dps)} {self.units_str}"
                    )
                else:
                    print(
                        f"\t{param_for_printing(self.ptarget)}:\n"
                        f"\t\tLower Quadrant = {np.round(result[0], self.args.dps)} {self.units_str}, "
                        f"Upper Quadrant = {np.round(result[1], self.args.dps)} {self.units_str}"
                    )
        else:
            if not self.args.plot and self.args.outputfile is None:
                quit_print(
                    "NOTE: Use --plot to display the computed results and/or "
                    "--out to save these results to a file."
                )

    def run(self):
        out = None
        if self.compute_all:
            out = self.__run_all_target()
        else:
            out = self.__run_singular_target()

        self.chain_triggered.clear()
        self.chained_args.clear()

        return out

    def __run_singular_target(self):
        targets_map = self.all_functions_from_target()

        computable = self.filter_computable(targets_map)

        if computable is None or computable.function is None:
            msg = f"ERROR: Incorrect usage. To compute {self.target} I require one of:"
            for reqd_params in self.all_reqd_params:
                msg += "\n\t"
                for param in reqd_params:
                    if param == Parameter.WAVELENGTH:
                        wl_v = self.args.wavelength.v
                        wl_u = self.args.wavelength.units
                        msg += f"[-wl = {wl_v} {wl_u}]"
                    else:
                        msg += param_to_command_arg(param)
                    if param != reqd_params[-1]:
                        msg += " AND "
            msg += (
                "\nOR a combination of parameters which allows one of "
                "the above sets to be computed."
            )
            quit_print(msg, self.cl)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)

            try:
                result, is_dual = computable.function(*computable.arg_calcvs)
                if isinstance(self.units, tuple):
                    result = self.units[0](result)
                else:
                    if self.units_map is not None:
                        result /= self.units_map[self.units]
            except ZeroDivisionError:
                quit_print(
                    "ERROR: Division by zero occurred in function: "
                    f"{computable.function}",
                    self.cl,
                )

        if not self.cl:
            given_dict = {}
            for argvals, argparam, argunits in computable.arg_ts:
                if not argunits:
                    argunits = standard_units_from_param(argparam)
                given_dict[argparam] = (argvals, argunits)

            return Output(
                self.ptarget,
                {self.ptarget: (result, self.units_str, is_dual)},
                given_dict,
            )

        found = self.find_conditions(result)
        self.print_found_conditions(found)
        xylines = None
        if found is not None:
            if self.args.find.fromvar == "y":
                xylines = (found, self.args.find.value)
            else:
                xylines = (self.args.find.value, found)

        self.__plot((result, self.ptarget, self.units_str), xylines, *computable.arg_ts)

        save_result(result, self.args.outputfile)
        self._print_result(result, computable, is_dual)

    def __run_all_target(self):
        computables = self.filter_computables()

        if self.cl:
            print("Given [{}SYMMETRIC CAVITY]:".format("" if self.symmetric else "A"))
        else:
            results = {}
            given = {}

        for pname, val in self.given_physical_args.items():
            given_units_str = val.units

            if not val.units:
                given_units_str = standard_units_from_param(pname)

            if self.cl:
                print(f"\t{param_for_printing(pname)} = {val.v} {given_units_str}")
            else:
                given[pname] = (val.v, given_units_str)

        if self.cl:
            print("\nComputed:")

        done = {}
        for func, (args, rtn_param) in computables.items():
            if rtn_param in self.given_physical_args:
                continue

            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=RuntimeWarning)

                try:
                    result, is_dual = func(*args)
                except ZeroDivisionError:
                    quit_print(
                        "ERROR: Division by zero occurred in function: " f"{func}",
                        self.cl,
                    )

            if rtn_param in done:
                prev_func, prev_result = done[rtn_param]
                if type(result) == type(prev_result):
                    if not np.allclose(result, prev_result):
                        func_params = tuple(
                            param_to_command_arg(p).strip("-")
                            for p in self.func_dependency_map[func][0]
                        )
                        prev_func_params = tuple(
                            param_to_command_arg(p).strip("-")
                            for p in self.func_dependency_map[prev_func][0]
                        )

                        fp = ", ".join(func_params)
                        pfp = ", ".join(prev_func_params)

                        msg = (
                            "\nBug encountered! Differing results when computing "
                            f'"{param_for_printing(rtn_param)}" using two different methods:\n\n'
                            f"\tf({fp}) = {result}\n"
                            f"\tf({pfp}) = {prev_result}"
                        )
                        bug(msg, self.cl)
                continue

            config_type = param_to_config_type(rtn_param)
            if is_distance(rtn_param):
                result /= SI_DISTANCE_MAP[self.units[config_type]]
                ustr = self.units[config_type]
            elif is_angle(rtn_param):
                result = self.units[config_type][0](result)
                ustr = self.units[config_type][1]
            elif is_frequency(rtn_param):
                result /= SI_FREQ_MAP[self.units[config_type]]
                ustr = self.units[config_type]
            else:
                ustr = standard_units_from_param(rtn_param)

            if self.cl:
                # TODO some cleaning up here - move common printing code to separate function
                if self.args.dps is None:
                    if not is_dual:
                        print(f"\t{param_for_printing(rtn_param)} = {result} {ustr}")
                    else:
                        print(
                            f"\t{param_for_printing(rtn_param)}:\n"
                            f"\t\tLower Quadrant = {result[0]} {ustr}, "
                            f"Upper Quadrant = {result[1]} {ustr}"
                        )
                else:
                    if not is_dual:
                        print(
                            f"\t{param_for_printing(rtn_param)} = "
                            f"{np.round(result, self.args.dps)} {ustr}"
                        )
                    else:
                        print(
                            f"\t{param_for_printing(rtn_param)}:\n"
                            f"\t\tLower Quadrant = {np.round(result[0], self.args.dps)} {ustr}, "
                            f"Upper Quadrant = {np.round(result[1], self.args.dps)} {ustr}"
                        )
            else:
                results[rtn_param] = (result, ustr, is_dual)

            done[rtn_param] = func, result

        if not self.cl:
            return Output("all", results, given)

    def __plot(self, result, xylines, *args):
        if not self.args.plot:
            return

        # perform some checks first
        const_params = []
        arraylike_args = []
        for p, p_id, p_u in args:
            if isinstance(p, np.ndarray):
                arraylike_args.append((p, p_id, p_u))
            else:
                const_params.append((p, p_id, p_u))

        if xylines is None:
            xylines = (None, None)

        # image plot
        if len(arraylike_args) == 2:
            X, X_PID, X_units = arraylike_args[0]
            Y, Y_PID, Y_units = arraylike_args[1]
            Z, Z_PID, Z_units = result

            axes_labels = []
            for p_id, p_u in [(X_PID, X_units), (Y_PID, Y_units), (Z_PID, Z_units)]:
                label = plotting.get_label(p_id)
                if p_u:
                    label += f" [{p_u}]"
                axes_labels.append(label)

            return plotting.density_plot(
                X,
                Y,
                Z,
                xlabel=axes_labels[0],
                ylabel=axes_labels[1],
                zlabel=axes_labels[2],
                xlim=self.args.xlim,
                ylim=self.args.ylim,
                zlim=self.args.zlim,
                log=self.args.loglog,
                cmap=self.args.cmap,
                filename=self.args.saveplot,
            )

        # normal plot
        y, y_param_id, y_units = result
        ylabel = plotting.get_label(y_param_id)
        if y_units:
            ylabel += f" [{y_units}]"

        fname = [self.args.saveplot, self.args.saveplot]

        # some computations yield results array of shape (2, n) due to
        # upper/lower quadrants of cavity stability -> take care of this here
        if len(y.shape) == 1:
            y = [y]
        else:
            if y.shape[0] != 2:
                bug(
                    f"\nBug encountered! Unrecognised result dimensions: {y.shape} "
                    f'when trying to plot "{param_for_printing(y_param_id)}".',
                    self.cl,
                )
            else:
                if self.args.saveplot is not None:
                    split_ext = self.args.saveplot.split(".")
                    fname = [
                        split_ext[0] + "_lowerquad." + split_ext[1],
                        split_ext[0] + "_upperquad." + split_ext[1],
                    ]

        for i, yi in enumerate(y):
            legend = plotting.get_label(y_param_id)
            if len(y) > 1:
                legend += " (lower quad)" if not i else " (upper quad)"
            if const_params:
                legend += "{}with ".format("\n" if len(const_params) > 1 else " ")
                legend += ", ".join(
                    [
                        "{} = {} {}".format(
                            PARAM_SYMBOL_MAP[p_id],
                            p,
                            p_u if p_u else standard_units_from_param(p_id),
                        )
                        for p, p_id, p_u in const_params
                    ]
                )

            for param, param_id, param_units in args:
                if isinstance(param, np.ndarray):
                    xlabel = plotting.get_label(param_id)
                    if param_units:
                        xlabel += f" [{param_units}]"

                    plotting.plot(
                        param,
                        yi,
                        xline=xylines[0],
                        yline=xylines[1],
                        xlabel=xlabel,
                        ylabel=ylabel,
                        legend=legend,
                        xlim=self.args.xlim,
                        ylim=self.args.ylim,
                        logx=self.args.semilogx,
                        logy=self.args.semilogy,
                        filename=fname[i],
                    )
                    break
