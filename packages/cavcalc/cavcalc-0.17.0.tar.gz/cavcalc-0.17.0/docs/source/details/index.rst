.. _details:

Mathematical details
====================

For transparency and convenience reasons all of the equations used to compute the
target parameters of `cavcalc` are detailed here. Due to the way `cavcalc` has been
implemented, only a core set of combinations of input parameters mapping to output
targets are included here - e.g. I give the equation for computing the beam radius
on mirrors given the cavity length and stability factors, but *not* the equation
to compute the beam radius on the mirror given the length and mirror curvatures. This
is because `cavcalc` makes use of chained function calls to compute targets given
a set of input parameters if it cannot directly compute the target from these arguments.

The equations for each target are separated into different pages according to the type
of the target, as shown below.

.. toctree::
    :maxdepth: 1

    beamsizes
    stabilities
    resonance
