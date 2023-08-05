.. _resonance:

Cavity resonance properties
===========================

.. rubric:: Free Spectral Range (FSR)

As a function of the cavity length (:math:`L`),

.. math::
    \nu(L) = \frac{c}{2L},

where :math:`c` is the speed of light.

.. rubric:: Finesse

As a function of the reflectivities of the mirrors (:math:`R_1`, :math:`R_2`),

.. math::
    \mathcal{F}(R_1, R_2) = \frac{\pi}{2 \arcsin{\left(\frac{1 - \sqrt{R_1 R_2}}{2\left(R_1 R_2\right)^{1/4}}\right)}}.

.. rubric:: Full-Width at Half-Maximum (FWHM)

As a function of the cavity length (:math:`L`) and reflectivities of the mirrors (:math:`R_1`, :math:`R_2`),

.. math::
    \mathrm{FWHM}(L, R_1, R_2)  = \frac{\nu(L)}{\mathcal{F}(R_1, R_2)}.

.. rubric:: Pole frequency

As a function of the cavity length (:math:`L`) and reflectivities of the mirrors (:math:`R_1`, :math:`R_2`),

.. math::
    p(L, R_1, R_2)  = \frac{\mathrm{FWHM}(L, R_1, R_2)}{2}.
