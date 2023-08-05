.. _beam_sizes:

Equations for beam radii
========================

Symmetric cavities
------------------

.. rubric:: Radius of the beam impinging on the cavity mirrors...

As a function of cavity length (:math:`L`) and mirror stability (:math:`g_s`),

.. math::
    w\left(L, \lambda, g_s\right) = \sqrt{
        \frac{L \lambda}{\pi} \sqrt{\frac{1}{1 - g_s^2}}
    }.

As a function of cavity length (:math:`L`) and cavity stability (:math:`g`),

.. math::
    w\left(L, \lambda, g\right) = \sqrt{
        \frac{L \lambda}{\pi} \sqrt{\frac{1}{1 - g}}
    }.

As a function of cavity length (:math:`L`) and round-trip Gouy phase (:math:`\psi`),

.. math::
    w\left(L, \lambda, \psi\right) = \sqrt{
        \frac{L \lambda}{\pi \sin{\left(\frac{\psi}{2}\right)}}
    }.

As a function of cavity length (:math:`L`) and divergence angle (:math:`\Theta`),

.. math::
    w\left(L, \lambda, \Theta\right) = \sqrt{ \frac{L\lambda}{\pi}
        \sqrt{\frac{1}{1-
        \left( \frac{1- \left(
            \frac{L\pi}{2\lambda}\right)^2 \tan^4{\Theta} }{
                1 + \left(
                    \frac{L\pi}{2\lambda}\right)^2 \tan^4{\Theta}
        } \right)^2
        }} }.

.. rubric:: Radius of the beam at the waist...

As a function of cavity length (:math:`L`) and mirror stability (:math:`g_s`),

.. math::
    w_0\left(L, \lambda, g_s\right) = \sqrt{
        \frac{L \lambda}{2\pi} \sqrt{\frac{1 + g_s}{1 - g_s}}
    }.

As a function of cavity length (:math:`L`) and round-trip Gouy phase (:math:`\psi`),

.. math::
    w_0\left(L, \lambda, \psi\right) = \sqrt{
        \frac{L \lambda}{2\pi} \sqrt{
            \frac{1 + \cos{\left(\frac{\psi}{2}\right)}}{1 - \cos{\left(\frac{\psi}{2}\right)}}
        }
    }.


Asymmetric cavities
-------------------

.. rubric:: Radius of the beam impinging on the cavity mirrors...

As a function of cavity length (:math:`L`) and mirror stabilities (:math:`g_1`, :math:`g_2`),

.. math::
    w_1\left(L, \lambda, g_1, g_2\right) = \sqrt{
        \frac{L \lambda}{\pi} \sqrt{\frac{g_2}{g_1(1 - g_2)}}
    }.

.. math::
    w_2\left(L, \lambda, g_1, g_2\right) = \sqrt{
        \frac{L \lambda}{\pi} \sqrt{\frac{g_1}{g_2(1 - g_2)}}
    }.

.. rubric:: Radius of the beam at the waist...

As a function of cavity length (:math:`L`) and mirror stabilities (:math:`g_1`, :math:`g_2`),

.. math::
    w_0\left(L, \lambda, g_1, g_2\right) = \sqrt{
        \frac{L \lambda}{2\pi} \sqrt{
            \frac{g_1 g_2 (1 - g_1g_2)}{(g_1 + g_2 - 2g_1g_2)^2}
        }
    }.
