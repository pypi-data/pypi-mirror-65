import numpy as np

from .utilities import quit_print


def get_label(p_id):
    from .parameter import Parameter

    label_map = {
        Parameter.BEAMSIZE: "Beam radius on mirrors",
        Parameter.WAISTSIZE: "Waist radius $w_0$ of cavity eigenmode",
        Parameter.WAISTPOS: "Waist position $z_0$ of cavity eigenmode",
        Parameter.CAV_GFACTOR: "Cavity stability factor $g$",
        Parameter.GOUY: "Round-trip Gouy phase",
        Parameter.DIVERGENCE: "Divergence angle",
        Parameter.FSR: "Free spectral range",
        Parameter.FWHM: "Full-Width at Half-Maximum",
        Parameter.FINESSE: "Finesse",
        Parameter.POLE: "Pole frequency",
        Parameter.MODESEP: "Mode separation frequency",
        Parameter.BEAMSIZE_ITM: "Beam radius on ITM",
        Parameter.BEAMSIZE_ETM: "Beam radius on ETM",
        Parameter.GFACTOR_ITM: "Stability factor $g_1$",
        Parameter.GFACTOR_ETM: "Stability factor $g_2$",
        Parameter.GFACTOR_SINGLE: "Stability factor of both mirrors $g_s$",
        Parameter.CAV_LENGTH: "Cavity length",
        Parameter.REFLECTIVITY_ITM: "ITM reflectivity",
        Parameter.REFLECTIVITY_ETM: "ETM reflectivity",
        Parameter.WAVELENGTH: "Wavelength",
        Parameter.ROC: "Radius of curvature of mirrors",
        Parameter.ROC_ITM: "Radius of curvature of ITM",
        Parameter.ROC_ETM: "Radius of curvature of ETM",
    }
    return label_map[p_id]


def density_plot(
    x,
    y,
    z,
    xlabel=None,
    ylabel=None,
    zlabel=None,
    xlim=None,
    ylim=None,
    zlim=None,
    log=False,
    cmap="cividis",
    show=True,
    filename=None,
):
    import matplotlib.pyplot as plt
    from matplotlib import cm
    import matplotlib.colors as colors

    fig, axes = plt.subplots()

    extent = [x.min(), x.max(), y.min(), y.max()]

    try:
        cmap = cm.get_cmap(cmap)
    except ValueError as e:
        quit_print(str(e))

    if log:
        z_valid = z[~np.isnan(z)]
        norm = colors.LogNorm(vmin=z_valid.min(), vmax=z_valid.max())
    elif zlim is not None:
        norm = colors.Normalize(vmin=zlim[0], vmax=zlim[1])
    else:
        norm = None

    surf = axes.imshow(
        z, extent=extent, origin="lower", aspect="auto", cmap=cmap, norm=norm
    )

    if xlim is not None:
        axes.set_xlim(xlim)
    if ylim is not None:
        axes.set_ylim(ylim)

    if zlabel is not None:
        plt.colorbar(surf, ax=axes, label=zlabel, fraction=0.046, pad=0.04)

    if xlabel is not None:
        axes.set_xlabel(xlabel)
    if ylabel is not None:
        axes.set_ylabel(ylabel)

    fig.tight_layout()

    if filename is not None:
        fig.savefig(filename)

    if show:
        plt.show()

    return fig, axes


def plot(
    x,
    y,
    xline=None,
    yline=None,
    xlabel=None,
    ylabel=None,
    legend=None,
    xlim=None,
    ylim=None,
    logx=False,
    logy=False,
    show=True,
    filename=None,
):
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots()

    plotting_func = axes.plot
    if logx and logy:
        plotting_func = axes.loglog
    elif logx:
        plotting_func = axes.semilogx
    elif logy:
        plotting_func = axes.semilogy

    if xline is not None:
        axes.axvline(x=xline, color="r", linestyle="--")
    if yline is not None:
        axes.axhline(
            y=yline,
            color="r",
            linestyle="--",
            label=f"{xlabel} = {xline:0.3f}\n{ylabel} = {yline:0.3f}",
        )
    if legend is not None:
        plotting_func(x, y, label=legend)
        axes.legend()
    else:
        plotting_func(x, y)

    if xlim is not None:
        axes.set_xlim(xlim)
    if ylim is not None:
        axes.set_ylim(ylim)

    if xlabel is not None:
        axes.set_xlabel(xlabel)
    if ylabel is not None:
        axes.set_ylabel(ylabel)

    fig.tight_layout()

    if filename is not None:
        fig.savefig(filename)
    if show:
        plt.show()
    return fig, axes
