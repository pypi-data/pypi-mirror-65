"""
Sub-module containing the output object which stores results
from calls to :func:`.calculate`.
"""

import copy
from collections import namedtuple
import os

import numpy as np

from .parameter import (
    ARG_PARAM_MAP,
    PARAM_SYMBOL_MAP,
    TARGET_PARAM_MAP,
    param_for_printing,
)
from .plotting import get_label, plot, density_plot

from .utilities import CavCalcError

SingleQuantity = namedtuple("SingleQuantity", "v units")
DualQuantity = namedtuple("DualQuantity", "lower upper")


def is_dual(quantity):
    return isinstance(quantity, DualQuantity)


class Output:
    """Storage and manipulation of results computed via :func:`.calculate`."""

    def __init__(self, target, results, given):
        self.__target = target
        self.__results = {}
        for k, (v, u, dual) in results.items():
            if dual:
                self.__results[k] = DualQuantity(
                    lower=SingleQuantity(v[0], u), upper=SingleQuantity(v[1], u)
                )
            else:
                self.__results[k] = SingleQuantity(v, u)
        self.__given = {}
        for k, (v, u) in given.items():
            self.__given[k] = SingleQuantity(v, u)

        # fill the constant parameters and arraylike parameters lists
        self.__const_depends = {}
        self.__array_depends = {}
        for p, (v, v_u) in self.__given.items():
            if not isinstance(v, np.ndarray):
                self.__const_depends[p] = SingleQuantity(v, v_u)
            else:
                self.__array_depends[p] = SingleQuantity(v, v_u)

        # fill the constant parameters and arraylike results lists
        self.__const_results = {}
        self.__vector_results = {}
        self.__grid_results = {}
        for p, quantity in self.__results.items():
            if is_dual(quantity):
                v_lower, v_u = quantity[0]
                v_upper, _ = quantity[1]
            else:
                v_lower, v_u = quantity
                v_upper = v_lower

            if not isinstance(v_lower, np.ndarray) and not isinstance(
                v_upper, np.ndarray
            ):
                self.__const_results[p] = quantity
            else:
                if v_lower.ndim == 1 and v_upper.ndim == 1:
                    self.__vector_results[p] = quantity
                else:
                    self.__grid_results = quantity

    def __str__(self):
        s = "Given:"
        for p_id, (v, u) in self.__given.items():
            s += f"\n\t{param_for_printing(p_id)} = {v} {u}"

        s += "\n\nComputed:"
        for p_id, quantity in self.__results.items():
            if is_dual(quantity):
                v_lower, u = quantity[0]
                v_upper, _ = quantity[1]
                s += (
                    f"\n\t{param_for_printing(p_id)}:\n"
                    f"\t\tLower Quadrant = {v_lower} {u}, Upper Quadrant = {v_upper} {u}"
                )
            else:
                v, u = quantity
                s += f"\n\t{param_for_printing(p_id)} = {v} {u}"

        return s

    def print(self):
        print(str(self))

    @property
    def computed(self):
        """A list of all the computed parameters (only the parameters NOT the values).

        :getter: The computed parameters (read-only).
        """
        return list(self.__results.keys())

    def get(self):
        """The computed result(s).

        If compute target was `all` then returns a copy of the dictionary of parameter
        to result mappings. Otherwise returns the ``SingleQuantity`` corresponding to
        the computed parameter.

        Returns
        -------
        out : dict or SingleQuantity
            The result(s) of the computation.
        """
        if self.__target == "all":
            return copy.deepcopy(self.__results)
        return self.__results[self.__target]

    def constant_dependents(self, just_param=False):
        if just_param:
            return list(self.__const_depends.keys())
        return copy.deepcopy(self.__const_depends)

    def arraylike_dependents(self, just_param=False):
        if just_param:
            return list(self.__array_depends.keys())
        return copy.deepcopy(self.__array_depends)

    def constant_results(self, just_param=False):
        if just_param:
            return list(self.__const_results.keys())
        return copy.deepcopy(self.__const_results)

    def vector_results(self, just_param=False):
        if just_param:
            return list(self.__vector_results.keys())
        return copy.deepcopy(self.__vector_results)

    def grid_results(self, just_param=False):
        if just_param:
            return list(self.__grid_results.keys())
        return copy.deepcopy(self.__grid_results)

    def __getitem__(self, key):
        if key in TARGET_PARAM_MAP.keys() and key != "all":
            key = TARGET_PARAM_MAP[key]
        return self.__results[key]

    def plot(
        self,
        xparam=None,
        yparam=None,
        xlim=None,
        ylim=None,
        logx=False,
        logy=False,
        show=True,
        filename=None,
        style="cavcalc",
    ):
        "Plot a result from given arguments."
        if not self.__array_depends:
            raise CavCalcError(
                "None of the dependent parameters are arrays, cannot plot results."
            )
        if not self.__vector_results:
            raise CavCalcError(
                "None of the computed parameters are arrays, cannot plot results."
            )

        if xparam is None:
            if len(self.__array_depends) > 1:
                raise CavCalcError(
                    "Multiple dependent parameters are arrays, xparam must be "
                    "specified so that Output.plot knows what to plot."
                )

            xparam = list(self.__array_depends.keys())[0]

        if yparam is None:
            if len(self.__vector_results) > 1:
                raise CavCalcError(
                    "Multiple computed parameters are arrays, yparam must be "
                    "specified so that Output.plot knows what to plot."
                )

            yparam = list(self.__vector_results.keys())[0]

        # xparam is a string, try converting to the corresponding Parameter
        if xparam in ARG_PARAM_MAP.keys():
            xparam = ARG_PARAM_MAP[xparam]

        if xparam in self.__given.keys():
            xs, x_units = self.__given[xparam]
        else:
            raise CavCalcError(
                f"Parameter: {xparam} not in given dictionary of output."
            )

        # yparam is a string, try converting to the corresponding Parameter
        if yparam in TARGET_PARAM_MAP.keys():
            yparam = TARGET_PARAM_MAP[yparam]

        if yparam in self.__results.keys():
            y_quantity = self.__results[yparam]
        else:
            raise CavCalcError(
                f"Parameter: {yparam} not in results dictionary of output."
            )

        if style == "cavcalc":
            import matplotlib.pyplot as plt

            plt.style.use(
                os.path.join(
                    os.path.split(os.path.realpath(__file__))[0], "_default.mplstyle"
                )
            )

        if is_dual(y_quantity):
            ys_lower, y_units = y_quantity.lower
            ys_upper, _ = y_quantity.upper
            ys_quads = [ys_lower, ys_upper]
        else:
            ys, y_units = y_quantity
            ys_quads = [ys]

        nq = len(ys_quads)
        figs = []
        axes = []
        for i, y_values in enumerate(ys_quads):
            if xs.shape != y_values.shape:
                raise CavCalcError(
                    f"Unable to plot {yparam} against {xparam} - dimensions are incompatible. This "
                    f"typically indicates that {yparam} is not a function of {xparam}."
                )

            if nq == 2:
                quad_label = " [Lower] " if not i else " [Upper] "
            else:
                quad_label = ""
            legend = get_label(yparam) + quad_label + "\nwith "
            legend += ", ".join(
                [
                    f"{PARAM_SYMBOL_MAP[p]} = {v} {v_u}"
                    for p, (v, v_u) in self.__const_depends.items()
                ]
            )

            fig, ax = plot(
                xs,
                y_values,
                legend=legend,
                xlabel=get_label(xparam) + f" [{x_units}]",
                ylabel=get_label(yparam) + f" [{y_units}]",
                xlim=xlim,
                ylim=ylim,
                logx=logx,
                logy=logy,
                show=show,
                filename=filename,
            )
            figs.append(fig)
            axes.append(ax)

        if nq == 1:
            return figs[0], axes[0]

        return figs, axes

    def implot(
        self,
        xparam,
        yparam,
        zparam=None,
        xlim=None,
        ylim=None,
        zlim=None,
        cmap="cividis",
        filename=None,
        log=False,
        show=True,
        style="cavcalc",
    ):
        if len(self.__array_depends) < 2:
            raise CavCalcError(
                "Two of the dependent parameters must be arrays, cannot plot results."
            )
        if not self.__grid_results:
            raise CavCalcError(
                "None of the computed parameters have been evaluated on a grid, cannot plot results."
            )

        if zparam is None:
            if len(self.__grid_results) > 1:
                raise CavCalcError(
                    "Multiple computed parameters have been evaluated on grids, zparam must be "
                    "specified so that Output.implot knows what to plot."
                )

            zparam = list(self.__grid_results.keys())[0]

        # xparam is a string, try converting to the corresponding Parameter
        if xparam in ARG_PARAM_MAP.keys():
            xparam = ARG_PARAM_MAP[xparam]

        if xparam in self.__given.keys():
            xs, x_units = self.__given[xparam]
        else:
            raise CavCalcError(
                f"Parameter: {xparam} not in given dictionary of output."
            )

        # yparam is a string, try converting to the corresponding Parameter
        if yparam in ARG_PARAM_MAP.keys():
            yparam = ARG_PARAM_MAP[yparam]

        if yparam in self.__given.keys():
            ys, y_units = self.__given[yparam]
        else:
            raise CavCalcError(
                f"Parameter: {yparam} not in given dictionary of output."
            )

        # zparam is a string, try converting to the corresponding Parameter
        if zparam in TARGET_PARAM_MAP.keys():
            zparam = TARGET_PARAM_MAP[zparam]

        if zparam in self.__grid_results:
            z_quantity = self.__results[zparam]
        else:
            raise CavCalcError(
                f"Parameter: {zparam} not in results dictionary of output."
            )

        if style == "cavcalc":
            import matplotlib.pyplot as plt

            plt.style.use(
                os.path.join(
                    os.path.split(os.path.realpath(__file__))[0], "_default.mplstyle"
                )
            )

        if is_dual(z_quantity):
            zs_lower, z_units = z_quantity.lower
            zs_upper, _ = z_quantity.upper
            zs_quads = [zs_lower, zs_upper]
        else:
            zs, z_units = z_quantity
            zs_quads = [zs]

        nq = len(zs_quads)
        figs = []
        axes = []
        for i, z_values in enumerate(zs_quads):
            if nq == 2:
                quad_label = " [Lower] " if not i else " [Upper] "
            else:
                quad_label = ""

            fig, ax = density_plot(
                xs,
                ys,
                z_values,
                xlabel=get_label(xparam) + (f" [{x_units}]" if x_units else ""),
                ylabel=get_label(yparam) + (f" [{y_units}]" if y_units else ""),
                zlabel=get_label(zparam)
                + quad_label
                + (f" [{z_units}]" if z_units else ""),
                xlim=xlim,
                ylim=ylim,
                zlim=zlim,
                log=log,
                show=show,
                cmap=cmap,
                filename=filename,
            )
            figs.append(fig)
            axes.append(ax)

        if nq == 1:
            return figs[0], axes[0]

        return figs, axes
