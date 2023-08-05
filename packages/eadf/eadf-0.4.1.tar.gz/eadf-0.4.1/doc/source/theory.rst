.. toctree::
   :maxdepth: -1
   :hidden:

Theoretical Preliminaries
=========================

The angle and frequency dependent effective aperture of a polarimetric antenna array is usually modeled as a function

.. math::

  a : [0, \pi] \times (-\pi, +\pi] \times [f_1, f_2] \rightarrow \mathbb{C}^{2 \times m}.

The first two arguments represent a point on the 3D unit sphere and the latter describes the excitation frequency of the array. This function is naturally periodic in its second argument, since we hope we are working according to the laws of physics. Moreover, it holds that

.. math::

  a(\alpha, \theta, f) = -a(\alpha - \pi, \theta + \pi),
  \quad \mathrm{for} \quad
  \alpha > \pi.

So we can extend the function according to the equation above such that

.. math::

  a : [0, 2\pi] \times (-\pi, +\pi] \times \mathbb{R}^+ \rightarrow \mathbb{C}^{2 \times m}.

is periodic in its first two arguments.

Narrowband Assumption
---------------------

In cases when we use the function `a` only for a small relative bandwidth, so when

.. math::

  \frac{f_2 - f_1}{f_2} \ll 1

we can assume that `a` is constant along it's third argument, so we have

.. math::

  a_{f_0} : [0, 2\pi] \times (-\pi, +\pi] \rightarrow \mathbb{C}^{2 \times m}.

being a naturally periodic function. As such we can expand it into its Fourier series via

.. math::

  a(\alpha, \theta) = \sum\limits_{\ell_1}^{L_1} \sum\limits_{\ell_2}^{L_2}
  g_{\ell_1, \ell_2}
  \exp(\jmath 2 \pi \ell_1 \alpha)
  \exp(\jmath 2 \pi \ell_2 \theta).

This is very nice, because the Fourier coefficients can be calculated from a regular sampling of `a` in both angular domains via an FFT. This is why the :py:obj:`EADF` object has to be initialized with a regular sampling in co-elevation and azimuth.


Wideband Arrays
---------------

 - not constant along freq anymore
 - spline extrapolation for smooth periodification
 - possibly windowing for trivial periodification


Derivatives
-----------

The cool thing now is that once we have the analytical expression for the beampattern, we can also calculate derivatives of any order. Most commonly one uses first and second derivatives. The gradients read as

.. math::

  \frac{\partial}{\partial \alpha} a(\alpha, \theta, f) =
    \sum\limits_{\ell_1}^{L_1}
    \sum\limits_{\ell_2}^{L_2}
    \sum\limits_{\ell_3}^{L_3}
    \jmath \ell_1 2 \pi  g_{\ell_1, \ell_2, \ell_3}
    \exp(\jmath 2 \pi \ell_1 \alpha)
    \exp(\jmath 2 \pi \ell_2 \theta)
    \exp(\jmath 2 \pi \ell_3 f).

and the other derivatives can be calculated in a similar fashion. For instance

.. math::

  \frac{\partial^2}{\partial^2 f} a(\alpha, \theta, f) =
    \sum\limits_{\ell_1}^{L_1}
    \sum\limits_{\ell_2}^{L_2}
    \sum\limits_{\ell_3}^{L_3}
    - 4 \pi^2 \ell_3^2 g_{\ell_1, \ell_2, \ell_3}
    \exp(\jmath 2 \pi \ell_1 \alpha)
    \exp(\jmath 2 \pi \ell_2 \theta)
    \exp(\jmath 2 \pi \ell_3 f).


Missing / Irregular Data
------------------------

 - spherical harmonics
 - least squares
