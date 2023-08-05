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
The Backend
-----------

Computation Backend
^^^^^^^^^^^^^^^^^^^

If you have an NVIDIA GPU you might install Cuda and cupy in order to do all
the heavy calculations on the GPU. The package parses the EADF_BACKEND
environment variable for the values "cupy" or "numpy" and then tries to import
cupy. If that succeeds, you are good to go.

However the pattern interpolation functions
return cupy.ndarrays, which must be converted to a numpy.ndarray. To this end
we provide the function :py:obj:`.asNumpy`:

>>> aGPU = array.pattern(...)
>>> # now convert to numpy
>>> aCPU = eadf.asNumpy(aGPU)

As a developer contributing to the EADF package you can simply import

>>> from .backend import xp

and then use xp to call array calculation functions as long as they are both
covered by cupy and numpy.

Memory Management
^^^^^^^^^^^^^^^^^

For some calculations it might be a smart idea to process the requested angles
in chunks of a certain size. First, because it might result in fewer cache
misses and second one might be running out of RAM to run the calculations. To
this end, you might set the EADF_LOWMEM environment variable and use it
together with the :py:obj:`.blockSize` property and the
:py:obj:`.optimizeBlockSize` function.

Datatypes
^^^^^^^^^

We support single and double precision calculations. This can be set with the
EADF_DTYPE environment variable. Most of the time single precision allows
approximately twice the computation speed. This is reflected in the
:py:obj:`.dtype` environment variable.

Environment Variables
^^^^^^^^^^^^^^^^^^^^^

A list of all available shell environment variables.

 - EADF_BACKEND: numpy or cupy?
 - EADF_LOWMEM: yay or nay?
 - EADF_DTYPE: float or double?
"""

import logging
import numpy as np
import os

_BACKEND = os.environ.get("EADF_BACKEND", "numpy")
_LOWMEM = os.environ.get("EADF_LOWMEM", 0)
_DTYPE = os.environ.get("EADF_DTYPE", "double")

einsumArgs = {"optimize": "optimal"}
asNumpy = np.array
xp = np

if _BACKEND == "cupy":
    try:
        import cupy as xp

        asNumpy = xp.asnumpy
        einsumArgs = {}
    except ImportError:
        logging.warning("cupy not importable. using numpy.")

elif _BACKEND == "numpy":
    pass
else:
    logging.warning("unknown backend. using numpy.")

if _LOWMEM:
    lowMemory = True
else:
    lowMemory = False

if _DTYPE == "double":
    dtype = "double"
elif _DTYPE == "float":
    dtype = "float"
else:
    dtype = "double"
    logging.warning("Datatype not implemented. using double.")
