from collections import namedtuple
from functools import wraps
from itertools import combinations

import numpy as np

from .. import CONFIG

PhysicalReturn = namedtuple("PhysicalReturn", "v dual")


class CavCalcError(Exception):
    pass


def physical_return_dispatcher(dual=False):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            values = function(*args, **kwargs)
            return PhysicalReturn(values, dual)

        return wrapper

    return decorator


def construct_grids(**kwargs):
    """Constructs N-dimensional meshgrids from the arguments
    provided.

    If a combination of parameters in the keyword-arguments are
    all of type :class:`numpy.ndarray`, then a meshgrid is formed
    from these arguments. The dictionary returned from this function
    contains the parameter names with updated values (i.e. grids).

    Note that for each combination, if any of the parameters in the
    combo are not :class:`numpy.ndarray` instances then the entry in
    the returned dictionary for these parameters is unchanged from
    the value passed in.

    Parameters
    ----------
    kwargs : keyword-arguments
        Parameters with their value(s).

    Returns
    -------
    formed : dict
        A new dictionary with updated values from `kwargs`, or just
        `kwargs` itself if the number of array-like values in `kwargs`
        is less than two.
    """
    n_arrays = sum(isinstance(v, np.ndarray) for v in kwargs.values())
    if n_arrays < 2:  # cannot form any meshgrids with fewer than 2 arrays
        return kwargs

    combos = list(combinations(kwargs.items(), n_arrays))

    values = {}
    for kv_pairs in combos:
        ks = [kvp[0] for kvp in kv_pairs]  # parameter names
        vs = [kvp[1] for kvp in kv_pairs]  # parameter values

        if all(isinstance(v, np.ndarray) for v in vs):
            vs = np.meshgrid(*vs)
            for k, v in zip(ks, vs):
                values[k] = v
        else:
            for k, v in zip(ks, vs):
                if k not in values:
                    values[k] = v

    return values


def dummy_return(value):
    return value


def both_arraylike(x, y):
    return isinstance(x, np.ndarray) and isinstance(y, np.ndarray)


def save_result(result, filename):
    """Save an array of data to either a .npy file or txt file,
    depending upon `filename`."""
    if filename is None:
        return
    if filename.endswith(".npy"):
        np.save(filename, result)
    else:
        np.savetxt(filename, result)


def quit_print(msg, from_command_line=True):
    if from_command_line:
        print(msg)
        exit(-1)
    else:
        raise CavCalcError(msg)


def bug(msg, from_command_line):
    if "bug_reporting" in CONFIG and CONFIG["bug_reporting"].getboolean("report"):
        # TODO send an email with contents = msg
        pass

    quit_print(msg, from_command_line)
