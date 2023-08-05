import numpy as np


def modesep_adjust(rtgouy, L):
    """Compute the mode-separation frequency taking into account
    the value of the round-trip Gouy phase.
    """
    from ..functions.general import fsr

    if not isinstance(rtgouy, np.ndarray):  # single value
        if rtgouy > np.pi:
            return (1 - 0.5 * rtgouy / np.pi) * fsr(L).v
        return 0.5 * rtgouy / np.pi * fsr(L).v

    nominal = 0.5 * rtgouy / np.pi * fsr(L).v
    idx_gouy_greater_pi = np.where(rtgouy > np.pi)
    if len(idx_gouy_greater_pi) == 1:  # one-dimension
        for idx in idx_gouy_greater_pi:
            nominal[idx] = fsr(L).v - nominal[idx]
    else:  # meshgrid
        for idx_i, idx_j in zip(idx_gouy_greater_pi[0], idx_gouy_greater_pi[1]):
            if isinstance(L, np.ndarray) and L.ndim == 2:
                nominal[idx_i][idx_j] = fsr(L[idx_i][idx_j]).v - nominal[idx_i][idx_j]
            else:
                nominal[idx_i][idx_j] = fsr(L).v - nominal[idx_i][idx_j]

    return nominal


def find_nearest(x, v):
    return np.argmin(np.abs(x - v))


def mirror_refl_abcd(Rc):
    return np.array([[1.0, 0.0], [-2.0 / Rc, 1.0]])


def space_abcd(L):
    return np.array([[1.0, L], [0.0, 1.0]])


def abcd(L, Rc1, Rc2):
    return space_abcd(L) @ mirror_refl_abcd(Rc2) @ space_abcd(L) @ mirror_refl_abcd(Rc1)
