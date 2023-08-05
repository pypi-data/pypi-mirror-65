.. _module:

Using as a Python module
========================

Whilst `cavcalc` is primarily a command line tool, it can also be used just as easily from within Python
in a more "programmatic" way. The recommended method for doing this is to use the single function interface
provided via :func:`.calculate`. This function works similarly to the command line interface, where a target
can be specified along with a variable number of keyword arguments corresponding to physical parameters. It then
returns a :class:`.Output` object which has a number of properties and methods for accessing the results and
plotting them against the parameters provided.

Note that for all examples shown here the import conventions::

    import cavcalc as cc
    import numpy as np

will be used.

Computing all available parameters
----------------------------------

Calculate everything we can from the cavity length and curvatures of the mirrors (note that
the ``target`` argument of :func:`.calculate` defaults to "all" so that all available
parameters get computed by default, just like the CLI behaviour):

>>> out = cc.calculate(L=(4, "km"), Rc1=1934, Rc2=2245)

Print the output:

>>> print(out)
Given:
        Cavity length = 4.0 km
        Wavelength of beam = 1064 nm
        Radius of curvature of ITM = 1934.0 m
        Radius of curvature of ETM = 2245.0 m
Computed:
        Eigenmode = (-1837.2153886417168+421.68018375440073j)
        Stability g-factor of cavity = 0.8350925761717987
        Stability g-factor of ETM = -0.7817371937639199
        Stability g-factor of ITM = -1.0682523267838677
        FSR = 37474.05725 Hz
        Radius of beam at ITM = 5.342106643304925 cm
        Radius of beam at ETM = 6.244807988323089 cm
        Radius of beam at waist = 1.1950538458990878 cm
        Position of beam waist (from first cavity mirror) = 1837.2153886417168 m
        Round-trip Gouy phase = 312.0813565565169 degrees
        Mode separation frequency = 4988.072188176179 Hz

You will notice here that the string representation of the :class:`.Output` object provides information
in a similar style to invoking `cavcalc` from the command line.

The `out` object here also acts like a Python dict, so that you can access individual parameters for example:

>>> out["w0"]
SingleQuantity(v=1.1950538458990878, units='cm')

This gives a ``SingleQuantity`` instance which is a `namedtuple` providing the value via the ``v`` attribute
and the units via the ``units`` attribute.

Note that if you provide arguments which result in two possible values for some parameters (i.e. representing
the upper and lower quadrants of the cavity stability plot), then these parameters will instead be ``DualQuantity``
instances where the ``upper`` and ``lower`` attributes are then themselves ``SingleQuantity`` objects:

>>> out = cc.calculate(L=4000, g=0.83)
>>> out["w0"]
DualQuantity(lower=SingleQuantity(v=1.208892924090748, units='cm'), upper=SingleQuantity(v=5.603171499316833, units='cm'))


Computing single parameters
---------------------------

If you are just interested in a single parameter, then a ``target`` can be given to :func:`.calculate`,
e.g:

>>> out = cc.calculate("w0", L=10, Rc=14.5)
>>> print(out)
Given:
        Cavity length = 10.0 m
        Wavelength of beam = 1064 nm
        Radius of curvature of mirrors = 14.5 m
Computed:
        Radius of beam at waist = 0.15278097598773807 cm


Evaluating parameters over data ranges
--------------------------------------

One can also specify parameter(s) as array-like arguments such that the target(s) are evaluated
over data ranges. Taking our singular target case from above for example:

>>> out = cc.calculate("w0", L=10, Rc=np.linspace(10, 20, 100))

this will compute the waist size of the cavity eigenmode for a 10 m long cavity over a range
of symmetric mirror curvatures :math:`R_c \in [10, 20]`.

You can then plot the result simply using :meth:`.Output.plot`:

>>> out.plot()

which will give the figure below.

.. figure:: images/symmcav_w0_vs_Rc.png
    :align: center

.. rubric:: Multiple targets with parameter data ranges

The :func:`.calculate` function is flexible in that it allows you to provide parameters as
data ranges even when the ``target`` is set to "all":

>>> out = cc.calculate(L=10, Rc=np.linspace(10, 20, 100))

You can find which targets are 1D array results now with:

>>> out.vector_results(just_param=True)
[<Parameter.GFACTOR_SINGLE: 15>, <Parameter.CAV_GFACTOR: 16>, <Parameter.BEAMSIZE: 1>, <Parameter.WAISTSIZE: 2>, <Parameter.GOUY: 4>, <Parameter.DIVERGENCE: 5>, <Parameter.MODESEP: 10>]

This gives you a list of the :class:`.Parameter` instances corresponding to the targets which are 1D arrays. Note that the
``just_param`` argument here tells :meth:`.Output.vector_results` to return only the parameters instead of the dictionary
containing all of the values.

If you now try to call :meth:`.Output.plot` with no arguments you will see this error:

>>> out.plot()
cavcalc.utilities.misc.CavCalcError: Multiple computed parameters are arrays, yparam must be specified so that Output.plot knows what to plot.

This tells us that we need to specify the parameter we want to plot now that multiple computed results are
arrays. So we could plot, for example, the round-trip Gouy phase of the cavity with:

>>> out.plot(yparam="gouy")

which will give us the figure below.

.. figure:: images/symmcav_gouy_vs_Rc.png
    :align: center

.. rubric:: Grid calculations

All of the above logic also applies to computing parameters over two array-like arguments, where any
result which uses these parameters will then be a "grid result" (you can find these with
:meth:`.Output.grid_results`). Grid results can be plotted using :meth:`.Output.implot`.
