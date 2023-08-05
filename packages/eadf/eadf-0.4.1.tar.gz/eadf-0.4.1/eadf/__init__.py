# -*- coding: UTF8 -*-
# Copyright 2020 S. Pawar, S. Semper
#     https://www.tu-ilmenau.de/it-ems/
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

r"""
Modelling Antenna Arrays with the EADF
======================================

Motivation
----------

Geometry-based MIMO channel modelling and a high-resolution parameter
estimation are applications in which a precise description of the radiation
pattern of the antenna arrays is required. In this package we implement an
efficient representation of the polarimetric antenna response, which we refer
to as the Effective Aperture Distribution Function (EADF). High-resolution
parameter estimation are applications in which this reduced description permits
us to efficiently interpolate the beam pattern to gather the antenna response
for an arbitrary direction in azimuth and elevation. Moreover, the EADF
provides a continuous description of the array manifold and its derivatives
with respect to azimuth and elevation. The latter is valuable for the
performance evaluation of an antenna array as well as for gradient-based
parameter estimation techniques.

Features
--------

This package allows to import measurement data that represents beam
patterns of antenna arrays, you can export these to a more convenient
format. It handles interpolation along the frequencies the antenna array
was excited with and can also deal with irregularly sampled beampatterns,
so it can interpolate along azimuth and co-elevation. Moreover one can
compress beampatterns by truncating their representation in the spatial
Fourier domain.

Performance
-----------

Since this package is mainly for academic purposes, we do not aim at the
highest level of optimization. Instead we try to provide clean, readable and
nicely structured code. Algorithmic optimizations are always welcome, if
they are sufficiently motivated and documented in the implementation or
some publication.

Intel Python
^^^^^^^^^^^^

Moreover we have found out that for most purposes it is sufficient to just use
the `Intel Python Distribution
<https://software.intel.com/en-us/distribution-for-python>`_,
which can be installed and used alongside any conventional CPython
distribution. It is automatically optimized for modern CPU instruction sets.
For instance Numpy operations are implemented using SIMD and SMP,
which would require a huge manual effort to replicate.
For example putting the following into a file

>>> import eadf
>>> A = eadf.generateStackedUCA(11, 3, 1.5, 0.5)
>>> arrEle, arrAzi = eadf.toGrid(
>>>     *eadf.sampleAngles(120, 240)
>>> )
>>> A.patternNarrowBand(arrEle, arrAzi, 1)

and changing nothing but the Python executable, yields the following:

>>> [user@pc EADF]$ time python/intelpython3 profiler.py
>>> real	0m51,424s/0m6,250s
>>> user	0m49,874s/0m8,469s
>>> sys	    0m0,485s/0m2,842s

Note that in this example we evaluate the beampattern at 28800 distinct
angular locations. (YMMV)

CuPy
^^^^

Cupy is a very nice reimplementation of the numpy API but for CUDA enabled
graphics chips. So it works as a drop-in replacement for numpy in our core
routines as soon as you enable it. So, install cupy for your currently
installed CUDA version and easily get going with your graphics chip. Again,
as above, your mileage may vary. One simply has to use the EADF_BACKEND
environment variable and set it to either "numpy" or "cupy".

References
----------

*Full 3D Antenna Pattern Interpolation Using Fourier Transform
Based Wavefield Modelling*; S. Haefner, R. Mueller, R. S. Thomae;
WSA 2016; 20th International ITG Workshop on Smart Antennas;
Munich, Germany; pp. 1-8

*Impact of Incomplete and Inaccurate Data Models on High Resolution Parameter
Estimation in Multidimensional Channel Sounding*, M. Landmann, M. Käske
and R.S. Thomä; IEEE Trans. on Antennas and Propagation, vol. 60, no 2,
February 2012, pp. 557-573

*Efficient antenna description for MIMO channel modelling and estimation*,
M. Landmann, G. Del Galdo; 7th European Conference on Wireless Technology;
Amsterdam; 2004; `IEEE Link <https://ieeexplore.ieee.org/document/1394809>`_

*Geometry-based Channel Modeling for Multi-User MIMO Systems and
Applications*, G. Del Galdo; Dissertation, Research Reports from the
Communications Research Laboratory at TU Ilmenau; Ilmenau; 2007
`Download1 <https://www.db-thueringen.de/servlets/MCRFileNodeServlet/
dbt_derivate_00014957/ilm1-2007000136.pdf>`_

*Limitations of Experimental Channel Characterisation*, M. Landmann;
Dissertation; Ilmenau; 2008 `Download2 <https://www.db-thueringen.de/servlets
/MCRFileNodeServlet/dbt_derivate_00015967/ilm1-2008000090.pdf>`_

*cupy* `Cupy Documentation
<https://docs-cupy.chainer.org/en/stable/>`_

*Intel Python* `Intelpython Documentation
<https://software.intel.com/en-us/distribution-for-python>`_
"""


__version__ = "0.4.1"


from .arrays import generateURA, generateULA, generateUCA, generateStackedUCA
from .arrays import generateUniformArbitrary

from .auxiliary import cartesianToSpherical, toGrid
from .auxiliary import columnwiseKron, sampleAngles

from .backend import asNumpy

from .core import evaluatePattern
from .core import evaluateGradient
from .core import evaluateHessian
from .core import evaluatePatternNarrowBand
from .core import evaluateGradientNarrowBand
from .core import evaluateHessianNarrowBand
from .core import fourierToSampled
from .core import regularSamplingToGrid
from .core import sampledToFourier
from .core import symmetrizeData

from .eadf import EADF

from .importers import fromAngleListData, fromArraydefData
from .importers import fromWidebandAngData, fromNarrowBandAngData
from .importers import fromHFSS

from .plot import plotBeamPattern2D, plotBeamPattern3D, plotCut2D

from .preprocess import interpolateDataSphere

__all__ = [
    "generateURA",
    "generateULA",
    "generateUCA",
    "generateStackedUCA",
    "generateUniformArbitrary",
    "toGrid",
    "columnwiseKron",
    "sampleAngles",
    "evaluatePattern",
    "evaluateGradient",
    "evaluateHessian",
    "evaluatePatternNarrowBand",
    "evaluateGradientNarrowBand",
    "evaluateHessianNarrowBand",
    "fourierToSampled",
    "regularSamplingToGrid",
    "sampledToFourier",
    "symmetrizeData",
    "EADF",
    "fromAngleListData",
    "fromArraydefData",
    "plotBeamPattern2D",
    "plotBeamPattern3D",
    "plotCut2D",
    "interpolateDataSphere",
    "fromNarrowBandAngData",
    "fromWidebandAngData",
]
