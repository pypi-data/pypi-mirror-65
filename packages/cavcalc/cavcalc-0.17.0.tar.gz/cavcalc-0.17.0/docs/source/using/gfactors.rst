A note on g-factors
===================

Stability (g) factors are split into four different parameters for implementation purposes and to
hopefully make it clearer as to which argument is being used and whether the resulting cavity
computations are for a symmetric or asymmetric cavity. These arguments are detailed here:

* `-gs` --- The symmetric, singular stability factor. This represents the individual g-factors of **both** cavity mirrors. Use this to define a *symmetric* cavity where the overall cavity g-factor is then simply :math:`g = g_s^2`.
* `-g` --- The overall cavity stability factor. This is the product of the individual g-factors of the cavity mirrors. Use this to define a *symmetric* cavity where the individual g-factors of **both** mirrors are then :math:`g_s = \sqrt{g}`.
* `-g1` --- The stability factor of the first cavity mirror. Use this to define an *asymmetric* cavity along with the argument `-g2` such that the overall cavity g-factor is then :math:`g = g_1 * g_2`.
* `-g2` --- The stability factor of the second cavity mirror. Use this to define an *asymmetric* cavity along with the argument `-g1` such that the overall cavity g-factor is then :math:`g = g_1 * g_2`.
