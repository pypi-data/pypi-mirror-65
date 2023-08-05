.. _command_line:

Using via the command line
==========================

Invoking cavcalc via the command line is the recommended way to use cavcalc due to its convenience
and simplicity. For details on all the available options run ``cavcalc -h`` or just ``cavcalc``.

Computing single parameters
---------------------------

You can ask for, e.g., the beam size on the mirrors of a symmetric cavity given its length and stability factor (g) with::

    cavcalc w -L 4000 -g 0.83

This would result in an output of::

    Given [SYMMETRIC CAVITY]:
        Cavity length = 4000.0 m
        Wavelength of beam = 1064 nm
        Stability g-factor of cavity = 0.83

    Computed:
        Radius of beam at mirrors = 5.732098477230927 cm

Units for both inputs and outputs can also be specified::

    cavcalc w -u mm -L 10km -gouy 145deg

This requests the beam radius (in mm) on the mirrors of a symmetric cavity of length 10km given that the
round-trip Gouy phase is 145 degrees; resulting in the following output::

    Given [SYMMETRIC CAVITY]:
        Cavity length = 10.0 km
        Wavelength of beam = 1064 nm
        Round-trip Gouy phase = 145.0 deg

    Computed:
        Radius of beam at mirrors = 59.59174828941794 mm

Computing all available parameters
----------------------------------

A compute target of `all` is the default choice which is used to calculate all parameters which can be determined
from the arguments specified. For example, using aLIGO parameters::

    cavcalc -L 4km -Rc1 1934 -Rc2 2245 -T1 0.014 -L1 37.5e-6 -T2 5e-6 -L2 37.5e-6

gives the following output::

    Given [ASYMMETRIC CAVITY]:
        Cavity length = 4.0 km
        Wavelength of beam = 1064 nm
        Reflectivity of ITM = 0.9859625
        Reflectivity of ETM = 0.9999574999999999
        Radius of curvature of ITM = 1934.0 m
        Radius of curvature of ETM = 2245.0 m

    Computed:
        FSR = 37474.05725 Hz
        Finesse = 443.11699254426594
        FWHM = 84.56921734107604 Hz
        Pole frequency = 42.28460867053802 Hz
        Eigenmode = (-1837.2153886417173+421.68018375440016j)
        Radius of beam at ITM = 5.342106643304925 cm
        Radius of beam at ETM = 6.244807988323089 cm
        Radius of beam at waist = 1.1950538458990878 cm
        Position of beam waist (from first cavity mirror) = 1837.2153886417168 m
        Round-trip Gouy phase = 312.0813565565169 degrees
        Stability g-factor of ITM = -1.0682523267838677
        Stability g-factor of ETM = -0.7817371937639199
        Stability g-factor of cavity = 0.8350925761717987
        Mode separation frequency = 4988.072188176179 Hz

Units of output
----------------

The default behaviour for the output parameter units is to grab the relevant parameter type option under the `[units]` header
of the ``cavcalc.ini`` configuration file. When installing `cavcalc`, this file is written to a new ``cavcalc/`` directory within
your config directory (i.e. ``~/.config/cavcalc/cavcalc.ini`` under Unix systems). See the comments in this file for details on the options
available for the output units of each parameter type.

`cavcalc` attempts to read a `cavcalc.ini` config file from several locations in this fixed order:

- Firstly from the current working directory, if that fails then
- next it tries to read from ``$XDG_CONFIG_HOME/.cavcalc/`` (or ``%APPDATA%/cavcalc/`` on Windows), if that also fails then
- the final read attempt is from the within the source of the package directory itself.

If a successful read occurs at any of these steps then `cavcalc` will use the configuration defined by that file
for the rest of the session - it will *not* try to read from any of the subsequent locations as well.

Note that if you specify a ``-u`` argument when running `cavcalc` then this takes priority over the options in the config file (as we saw in
the above example).

Evaluating parameters over data ranges
--------------------------------------

Parameters can be computed over ranges of data using:

* the data range syntax:
    * ``-<param_name> "linspace(start, stop, num) [<units>]"``,
    * ``-<param_name> "range(start, stop, stepsize) [<units>]"``,
    * ``-<param_name> "start stop num [<units>]"`` (a shorthand version of the linspace command),
* or data from an input file with ``-<param_name> file.dat``.

An example of using a range could be::

    cavcalc w -L "1 10 100 km" -g 0.9 --plot

This results in a plot (see below) showing how the beam radius at the mirrors of a symmetric cavity varies from
a cavity length of 1km to 10km with 100 data points, with a fixed cavity stability factor g = 0.9.

.. figure:: images/symmcav_ws_vs_lengths.png
    :align: center

Alternatively one could use a file of data, e.g::

    cavcalc gouy -L 10km -w beam_radii.txt --plot --saveplot symmcav_gouy_vs_ws.png

This then computes the round-trip Gouy phase (in degrees) of a symmetric cavity of length 10km
using beam radii data stored in a file ``beam_radii.txt``, and plots the results (see below). Note also that
you can save the resulting figure using the ``--saveplot <filename>`` syntax as seen in the above command.

.. figure:: images/symmcav_gouy_vs_ws.png
    :align: center


.. rubric:: Image/density plots

Two arguments can be specified as data ranges (or files of data) in order to produce
density plots of the target parameter. For example::

    cavcalc w -L "1 10 100 km" -gouy "20 120 100 deg" --plot

computes the radius of the beam on the mirrors of a symmetric cavity, against both the cavity length and
round-trip Gouy phase. This results in the plot shown below.

.. figure:: images/symmcav_w_vs_L_gouy.png
    :align: center

A matplotlib compliant colour-map can be specified when making an image plot using the ``--cmap <name>`` option. For example,
the following command gives the plot shown below::

    cavcalc w0 -L 10km -g1 "-2 2 200" -g2 "-2 2 200" --plot --cmap nipy_spectral

.. figure:: images/asymmcav_w0_vs_g1g2.png
    :align: center


.. rubric::  Finding conditions in a data range

Using the ``--find <condition>`` argument one can prompt cavcalc to spit out the value(s) at which the given
condition is satisfied when doing a data range computation. Taking an example above, we can find the closest value
of the Round-trip Gouy phase when the radius of the beam is 11 cm. The result is printed to the terminal and
given on the plot (see below). The command to perform such a computation is::

    cavcalc gouy -L 10km -w "5.8 15 1000 cm" --plot --find "x=11"

.. figure:: images/symmcav_gouy_vs_ws_find_11cm.png
    :align: center
