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
Internal Properties
^^^^^^^^^^^^^^^^^^^

- _arrIndAziCompress: subselection index array in azimuth frequency used during
  compression of the beampattern
- _arrIndCoEleCompress: subselection index array in elevation frequency used
  during compression of the beampattern
- _arrAzi: -> :py:obj:`EADF.arrAzi`
- _arrCoEle: -> :py:obj:`EADF.arrCoEle`
- _arrFreq: -> :py:obj:`EADF.arrFreq`
- _numElements: -> :py:obj:`EADF.numElements`
- _arrFourierData: Fourier data generated upon initialisation
- _arrPos: -> :py:obj:`EADF.arrPos`
- _arrRawData: -> :py:obj:`EADF.arrRawData`
- _dtype -> :py:obj:`EADF.dtype`
- _complexDtype: data type used for complex numbers based on
  :py:obj:`EADF.dtype`
- _realDtype: data type used for real numbers based on :py:obj:`EADF.dtype`
- _compressionFactor: -> :py:obj:`EADF.compressionFactor`
- _arrDataCalc: data used for actually calculating the beam pattern
- _muAziCalc: data used for actually calculating the beam pattern
- _muCoEleCalc: data used for actually calculating the beam pattern
- _arrFreqCalc: data used for actually calculating the beam pattern
- _isNarrowBand -> :py:obj:`EADF.isNarrowBand`
- _version -> :py:obj:`EADF.version`
- _blockSize -> :py:obj:`EADF.blockSize`
- _numFreqPadding: how many samples we add in direction of frequency
- _lowMemory -> :py:obj:`EADF.lowMemory`


EADF Object
^^^^^^^^^^^

The EADF object can be used to represent wideband or narrowband antenna
beampatterns.
"""

from . import __version__
import numpy as np
import logging
import pickle
from .core import evaluatePattern
from .core import evaluatePatternNarrowBand
from .core import evaluateGradient
from .core import evaluateGradientNarrowBand
from .core import evaluateHessian
from .core import evaluateHessianNarrowBand
from .core import calcBlockSize
from .core import calcBlockSizeNarrowBand
from .core import ureg
from .preprocess import periodifyFreq
from .core import sampledToFourier
from .core import symmetrizeData
from .preprocess import setCompressionFactor

from .backend import xp
from .backend import lowMemory
from .backend import dtype


def _checkInputData(
    arrData: np.ndarray,
    arrCoEle: np.ndarray,
    arrAzi: np.ndarray,
    arrFreq: np.ndarray,
    arrPos: np.ndarray,
    **options
) -> None:
    def check_support(
        arrSupport,
        strName,
        targetUnit,
        expectedShape,
        cast_shape=np.atleast_1d,
    ):
        # Cast support array to default unit, if not already a quantity
        if not isinstance(arrSupport, ureg.Quantity):
            arrSupport = arrSupport * ureg.Quantity(targetUnit).u

        # Make any ndarray, with only one axis of size > 1, a vector
        arrSupport = cast_shape(
            np.squeeze(arrSupport.to(targetUnit).m)
        ) * ureg.Quantity(targetUnit)

        # check if sizes match
        if arrSupport.shape != expectedShape:
            raise ValueError(
                "EADF:%s.shape%s != expected shape%s"
                % (strName, repr(arrSupport.shape), repr(expectedShape))
            )

        return arrSupport

    # check for correct shapes and support and introduce default units
    arrCoEle = check_support(
        arrCoEle, "arrCoEle", "radian", (arrData.shape[0],)
    )
    arrAzi = check_support(arrAzi, "arrAzi", "radian", (arrData.shape[1],))
    arrFreq = check_support(arrFreq, "arrFreq", "hertz", (arrData.shape[2],))
    arrPos = check_support(
        arrPos,
        "arrPos",
        "meter",
        (3, arrData.shape[4]),
        cast_shape=lambda arr: (
            arr.reshape((-1, 1)) if arr.ndim == 1 else arr
        ),
    )
    if not isinstance(arrData, ureg.Quantity):
        arrData = arrData * ureg.Quantity("1").u

    # Now we want to allow for some preparations or modifications of the
    # data given with the input arguments, prior to asserting correctness
    # or alignment of the grids.

    def preprocess_support_axis(arrSupport, nameOption):
        func = options.get(nameOption, None)
        return arrSupport if func is None else func(arrSupport)

    def rearrange_axis(arrSupport, arrData, numAxis, arrIndex):
        index = arrData.ndim * [slice(None)]
        index[numAxis] = arrIndex
        return arrSupport[arrIndex], arrData[tuple(index)]

    # Preprocessing: Apply lambda function to axis support
    arrCoEle = preprocess_support_axis(arrCoEle, "modify_support_CoEle")
    arrAzi = preprocess_support_axis(arrAzi, "modify_support_Azi")
    arrFreq = preprocess_support_axis(arrFreq, "modify_support_Freq")

    # Preprocessing: sort tensor align the support axes
    if options.get("sort_support", False):
        arrCoEle, arrData = rearrange_axis(
            arrCoEle, arrData, 0, np.argsort(arrCoEle)
        )
        arrAzi, arrData = rearrange_axis(
            arrAzi, arrData, 1, np.argsort(arrAzi)
        )
        arrFreq, arrData = rearrange_axis(
            arrFreq, arrData, 2, np.argsort(arrFreq)
        )

    # Preprocessing: truncate along data axis based on support
    def truncate_axis(arrSupport, arrData, numAxis, nameOption):
        limits = options.get(nameOption, None)
        if limits is None:
            return arrSupport, arrData

        if len(limits) != 2 or limits[0] > limits[1]:
            raise ValueError("EADF:Truncation range must be an interval")

        return rearrange_axis(
            arrSupport,
            arrData,
            numAxis,
            np.logical_and(arrSupport >= limits[0], arrSupport <= limits[1]),
        )

    arrCoEle, arrData = truncate_axis(arrCoEle, arrData, 0, "truncate_CoEle")
    arrAzi, arrData = truncate_axis(arrAzi, arrData, 1, "truncate_Azi")
    arrFreq, arrData = truncate_axis(arrFreq, arrData, 2, "truncate_Freq")

    # check if angular and frequency grids are sampled regularly
    # and the are also sorted in ascending order
    def check_grid(**support):
        for name, arrSupport in support.items():
            arrDiff = np.diff(arrSupport.m)
            if not np.isclose(arrDiff.max(), arrDiff.min()):
                raise ValueError(
                    "EADF:%s grid is not sampled evenly" % (name,)
                )

            if np.any(arrDiff <= 0):
                raise ValueError("EADF:%s grid must be sorted." % (name,))

    check_grid(azimuth=arrAzi, coelevation=arrCoEle)
    if arrFreq.size > 1:
        check_grid(frequency=arrFreq)

    # in elevation we check if we sampled from north to south pole
    if not np.allclose(arrCoEle.m[0], 0):
        raise ValueError("EADF:you must sample at the north pole.")

    if not np.allclose(arrCoEle.m[-1], np.pi):
        raise ValueError("EADF:you must sample at the south pole.")

    return (arrData, arrCoEle, arrAzi, arrFreq, arrPos)


class EADF(object):
    @property
    def arrIndAziCompress(self) -> np.ndarray:
        """Subselection indices for the compressed array in azimuth (ro)

        Returns
        -------
        np.ndarray
            Subselection in spatial Fourier domain in azimuth

        """
        return self._arrIndAziCompress

    @property
    def arrIndCoEleCompress(self) -> np.ndarray:
        """Subselection indices for the compressed array in elevation (ro)

        Returns
        -------
        np.ndarray
            Subselection in spatial Fourier domain in elevation

        """
        return self._arrIndCoEleCompress

    @property
    def arrIndFreqCompress(self) -> np.ndarray:
        """Subselection indices for the compressed array in ex. freq. (ro)

        Returns
        -------
        np.ndarray
            Subselection in spatial Fourier domain in excitation frequency

        """
        return self._arrIndFreqCompress

    @property
    def arrAzi(self) -> np.ndarray:
        """Return Array Containing the sampled Azimuth Angles

        Returns
        -------
        np.ndarray
            Sampled Azimuth Angles in radians

        """
        return self._arrAzi

    @property
    def arrCoEle(self) -> np.ndarray:
        """Return Array Containing the sampled Co-Elevation Angles

        Returns
        -------
        np.ndarray
            Sampled Co-Elevation Angles in radians

        """
        return self._arrCoEle

    @property
    def arrFreq(self) -> np.ndarray:
        """Return Array Containing the Sampled Frequencies

        Returns
        -------
        np.ndarray
            Sampled Frequencies in Hertz

        """
        return self._arrFreq

    @property
    def numElements(self) -> int:
        """Number of Array Elements (read only)

        Returns
        -------
        int
            Number of Antenna Elements / Ports

        """
        return self._numElements

    @property
    def arrFourierData(self) -> np.ndarray:
        """Return the Fourier Data used to represent the antenna. (read only)

        This is the data after compression with the original data type

        Returns
        -------
        np.ndarray
            2D/3D Fourier Data (compressed)
        """

        return self._arrFourierData[:, self.arrIndAziCompress][
            self.arrIndCoEleCompress
        ][:, :, self.arrIndFreqCompress]

    @property
    def arrRawFourierData(self) -> np.ndarray:
        """Return the Fourier Data used to represent the antenna. (read only)

        This is the data before compression with the original data type

        Returns
        -------
        np.ndarray
            2D Fourier Data (uncompressed)
        """

        return self._arrFourierData

    @property
    def arrPos(self) -> np.ndarray:
        """Positions of the Elements as 3 x numElements

        Returns
        -------
        np.ndarray
            Positions of the Elements as 3 x numElements

        """

        return self._arrPos

    @property
    def arrRawData(self) -> np.ndarray:
        """Return the Raw Data used during construction. (read only)

        Returns
        -------
        np.ndarray
            Raw Data in 2 * Co-Ele x Azi x Freq x Pol x Element
        """

        return self._arrRawData

    @property
    def lowMemory(self) -> bool:
        return self._lowMemory

    @lowMemory.setter
    def lowMemory(self, flag) -> None:
        self._lowMemory = flag

    @property
    def dtype(self) -> str:
        """Data Type to use during calculations

        Returns
        -------
        str
            either 'float' for single precision or 'double' for
            double precision
        """

        return self._dtype

    @dtype.setter
    def dtype(self, dtype: str) -> None:
        """Set the Data Type

        Parameters
        ----------
        dtype : str
            either 'float' for single precision or 'double' for
            double precision
        """

        if dtype == "float":
            self._complexDtype = "complex64"
            self._realDtype = "float32"
            self._dtype = "float"
        elif dtype == "double":
            self._complexDtype = "complex128"
            self._realDtype = "float64"
            self._dtype = "double"
        else:
            raise ValueError("dtype: datatype not implemented.")

        # recache the calculation data we use during the beam pattern
        # transform
        self._cacheCalculationData()

    @property
    def isNarrowBand(self) -> None:
        """Return if the current EADF object represents a narrowband Array
        """
        return self._isNarrowBand

    @property
    def version(self) -> None:
        """Return the version of the EADF package used to create the object

        This is important, if we pickle an EADF object and recreate it from
        disk with a possible API break between two versions of the package.
        Right now we only use the property to issue a warning to the user
        when the versions dont match when reading an object from disk.
        """
        return self._version

    @property
    def compressionFactor(self) -> float:
        """Compression Factor

        See also :py:obj:`EADF.setCompressionFactor`.

        Returns
        -------
        float
            Compression factor in (0,1]

        """
        return self._compressionFactor

    @property
    def blockSize(self) -> float:
        """Block Size for Transform

        See optimizeBlockSize().

        Returns
        -------
        int
            block size

        """
        return self._blockSize

    @compressionFactor.setter
    def compressionFactor(self, numValue: float) -> None:
        """Set the Compression Factor

        The EADF allows to reduce the number of parameters of a given
        beampattern by reducing the number of Fourier coefficients.
        This should be done carefully, since one should not throw away
        necessary information. So, we define a compression factor 'p', which
        determines how much 'energy' the remaining Fourier coefficients
        contain.
        So we have the equation: E_c = p * E, where 'E' is the energy of the
        uncompressed array. See also :py:obj:`setCompressionFactor`.

        Parameters
        ----------
        numValue : float
            Factor to be set. Must be in (0,1]. The actual subselection
            is done such that the remaining energy is always greater or
            equal than the specified value, which minimizes the expected
            computation time.

        """
        if (numValue <= 0.0) or (numValue > 1.0):
            raise ValueError("Supplied Value must be in (0, 1]")
        else:
            tplRes = setCompressionFactor(
                self._arrFourierData,
                self._numCoEleInit,
                self._numAziInit,
                self._numFreqInit,
                self._isNarrowBand,
                numValue,
            )

            if self._isNarrowBand:
                # in the narrowband case, we do not subselect in frequency
                # domain, so we append an array that selects all
                # excitation
                tplRes = tplRes + (np.arange(self._arrFreq.shape[0]),)

            (
                self._compressionFactor,
                self._arrIndCoEleCompress,
                self._arrIndAziCompress,
                self._arrIndFreqCompress,
            ) = tplRes

            # recache the calculation data we use during the beam pattern
            # transform
            self._cacheCalculationData()

    def _cacheCalculationData(self) -> None:
        """Cache the actually used calculation data

        This method is the central hub, to keep calculation data
        in the correct data format and in the correct memory (device/host).
        So it should be extended for any new functionality of the class
        that depends on possibly changing data or that introduces parameters
        that influence the calculation.
        """

        self._arrDataCalc = xp.asarray(
            self.arrFourierData.astype(self._complexDtype)
        )
        self._muCoEleCalc = xp.asarray(
            self._muCoEle[self._arrIndCoEleCompress].astype(self._realDtype)
        )
        self._muAziCalc = xp.asarray(
            self._muAzi[self._arrIndAziCompress].astype(self._realDtype)
        )

        if not self._isNarrowBand:
            self._muFreqCalc = xp.asarray(
                self._muFreq[self._arrIndFreqCompress].astype(self._realDtype)
            )

    def optimizeBlockSize(self) -> None:
        """Optimize the Blocksize during the Calculation

        Instead of processing all angles and (possibly) frequencies all at
        once, we process them in blocks. This can produce a decent speedup
        and makes the transform scale nicer with increasing number of angles.

        Simply call this function, which might take some time to determine the
        best block size.
        """

        if self._isNarrowBand:
            self._blockSize = calcBlockSizeNarrowBand(
                self._muCoEleCalc,
                self._muAziCalc,
                self._arrDataCalc[:, :, 0, :, :],
            )
        else:
            self._blockSize = calcBlockSize(
                self._muCoEleCalc,
                self._muAziCalc,
                self._muFreqCalc,
                self._arrDataCalc,
            )

    def _eval(
        self,
        arrCoEle: np.ndarray,
        arrAzi: np.ndarray,
        arrFreq: np.ndarray,
        funCall,
    ) -> np.ndarray:
        """Unified Evaluation Function

        This function allows to calculate the Hessian, gradient
        and the values themselves with respect to the parameters
        angle and frequency.

        Parameters
        ----------
        arrCoEle : np.ndarray
            Sample at these elevations in radians
        arrAzi : np.ndarray
            Sample at these azimuths in radians
        arrFreq : np.ndarray
            Sample at these frequencies in Hertz
        funCall : function
            evaluatePattern, evaluateGradient, evaluateHessian

        Returns
        -------
        np.ndarray
            pattern, gradient or Hessian array
        """

        if self.isNarrowBand:
            raise ValueError(
                "This array is narrowband. Cannot use this function"
            )

        # convert the given inputs to the current datatype
        # nothing is copied, if everything is already on the host / the
        # GPU respectively
        arrCoEle = xp.asarray(arrCoEle.astype(self._realDtype))
        arrAzi = xp.asarray(arrAzi.astype(self._realDtype))
        arrFreq = xp.array(arrFreq.astype(self._realDtype))

        # normalize the physical frequency values to the virtual
        # values between 0 and 2pi * NF / (NF + P)
        arrFreq -= self._arrFreq[0]
        arrFreq /= self._arrFreq[-1] - self._arrFreq[0]
        arrFreq *= (
            2
            * np.pi
            * (self._arrFreq.shape[0] - 1)
            / (self._arrFreq.shape[0] + self._numFreqPadding)
        )
        # calls either pattern, gradient or hessian
        return funCall(
            arrCoEle,
            arrAzi,
            arrFreq,
            self._muCoEleCalc,
            self._muAziCalc,
            self._muFreqCalc,
            self._arrDataCalc,
            self._blockSize,
            self._lowMemory,
        )

    def _evalNarrowBand(
        self, arrCoEle: np.ndarray, arrAzi: np.ndarray, numFreq: float, funCall
    ) -> np.ndarray:
        """Unified Narrowband Evaluation Function

        This function allows to calculate the Hessian, gradient
        and the values themselves with respect to the parameters
        angle for a single frequency.

        Parameters
        ----------
        arrCoEle : np.ndarray
            Sample at these elevations in radians
        arrAzi : np.ndarray
            Sample at these azimuths in radians
        numFreq : np.ndarray
            Sample at this frequency in Hertz
        funCall : function
            evaluatePatternNarrowBand,
            evaluateGradientNarrowBand,
            evaluateHessianNarrowBand

        Returns
        -------
        np.ndarray
            pattern/gradient/hessian
        """

        if arrAzi.shape[0] != arrCoEle.shape[0]:
            raise ValueError(
                "patternNarrowBand: supplied angle arrays have size %d and %d."
                % (arrCoEle.shape[0], arrAzi.shape[0])
            )

        if self._isSingleFreq:
            if numFreq != self._arrFreq[0]:
                raise ValueError(
                    "Desired freq %s does not match sampled one %s"
                    % (str(numFreq), str(self._arrFreq[0]))
                )
            arrData = self._arrDataCalc[:, :, 0, :, :]
        else:
            # check if the supplied frequency is in the range we used during
            # the construction
            if (numFreq < np.min(self._arrFreq)) or (
                numFreq > np.max(self._arrFreq)
            ):
                raise ValueError("Desired freq must be in excitation range.")

            # if the required frequency is among the excitation
            # frequencies, we dont need to interpolate
            if numFreq in self._arrFreq:

                # we simply pick the index in the data array that matches
                # the desired frequency
                numInd = np.arange(self._arrFreq.shape[0])[
                    self._arrFreq == numFreq
                ][0]

                arrData = self._arrDataCalc[:, :, numInd, :, :]
            else:
                # highest index, such that the excitation frequencies
                # are lower than the requested one.
                numInd = np.arange(self._arrFreq.shape[0])[
                    self._arrFreq <= numFreq
                ][-1]

                # calculate the weighting coefficients of the patterns for
                # neighbouring frequency bins
                a1 = (self._arrFreq[numInd + 1] - numFreq) / (
                    self._arrFreq[numInd + 1] - self._arrFreq[numInd]
                )
                a2 = (numFreq - self._arrFreq[numInd]) / (
                    self._arrFreq[numInd + 1] - self._arrFreq[numInd]
                )

                # here we supply the linearly interpolated data directly
                # thus reducing the EADF computation again to 1 call.
                arrData = (
                    a1 * self._arrDataCalc[:, :, numInd, :, :]
                    + a2 * self._arrDataCalc[:, :, numInd + 1, :, :]
                )

        # copy everything to device/host ram
        arrCoEle = xp.asarray((arrCoEle).astype(self._realDtype))
        arrAzi = xp.asarray(arrAzi.astype(self._realDtype))

        # calls either pattern, gradient or hessian
        return funCall(
            arrCoEle,
            arrAzi,
            self._muCoEleCalc,
            self._muAziCalc,
            arrData,
            self._blockSize,
            self._lowMemory,
        )

    def patternNarrowBand(
        self, arrCoEle: np.ndarray, arrAzi: np.ndarray, numFreq: float
    ) -> np.ndarray:
        """Sample the Beampattern at Angles and a single Frequency

        The supplied arrays need to have the same length. The returned
        array has again the same length. This method samples the EADF object
        for given angles and excitation frequencies
        for all polarizations and array elements.
        So it yields a (Ang,Freq) x Pol x Element ndarray.

        Since we have no crystalline sphere to guess, we cannot do
        extrapolation, so the requested frequency has to be between the
        minimum and maximum frequency the array was excited with.

        .. note::
          If the GPU is used for calculation a cupy.ndarray is returned,
          so for further processing on the host, you need to copy ot yourself.
          otherwise you can simply continue on the GPU device. Moreover,
          if you supply cupy.ndarrays with the right data types,
          this also speeds up the computation, since no copying or
          conversion have to be done.

        Parameters
        ----------
        arrCoEle : np.ndarray
            Sample at these elevations in radians
        arrAzi : np.ndarray
            Sample at these azimuths in radians
        numFreq : np.ndarray
            Sample at this frequency in Hertz

        Returns
        -------
        np.ndarray
            (Ang x Pol x Elem)
        """
        return self._evalNarrowBand(
            arrCoEle, arrAzi, numFreq, evaluatePatternNarrowBand
        )

    def gradientNarrowBand(
        self, arrCoEle: np.ndarray, arrAzi: np.ndarray, numFreq: float
    ) -> np.ndarray:
        """Sample the Beampattern Gradient at Angles and a single Frequency

        The supplied arrays need to have the same length. The returned
        array has again the same length. This method samples the EADF object
        for given angles and excitation frequencies
        for all polarizations and array elements.
        So it yields a (Ang,Freq) x Pol x Element ndarray.

        Since we have no crystalline sphere to guess, we cannot do
        extrapolation, so the requested frequency has to be between the
        minimum and maximum frequency the array was excited with.

        .. note::
          If the GPU is used for calculation a cupy.ndarray is returned,
          so for further processing on the host, you need to copy ot yourself.
          otherwise you can simply continue on the GPU device. Moreover,
          if you supply cupy.ndarrays with the right data types,
          this also speeds up the computation, since no copying or
          conversion have to be done.

        Parameters
        ----------
        arrCoEle : np.ndarray
            Sample at these elevations in radians
        arrAzi : np.ndarray
            Sample at these azimuths in radians
        numFreq : np.ndarray
            Sample at this frequency in Hertz

        Returns
        -------
        np.ndarray
            (Ang x Pol x Elem x (derivAzi, derivEle))
        """
        return self._evalNarrowBand(
            arrCoEle, arrAzi, numFreq, evaluateGradientNarrowBand
        )

    def hessianNarrowBand(
        self, arrCoEle: np.ndarray, arrAzi: np.ndarray, numFreq: float
    ) -> np.ndarray:
        """Sample the Beampattern Hessian at Angles and a single Frequency

        The supplied arrays need to have the same length. The returned
        array has again the same length. This method samples the EADF object
        for given angles and excitation frequencies
        for all polarizations and array elements.
        So it yields a (Ang,Freq) x Pol x Element ndarray.

        Since we have no crystalline sphere to guess, we cannot do
        extrapolation, so the requested frequency has to be between the
        minimum and maximum frequency the array was excited with.

        .. note::
          If the GPU is used for calculation a cupy.ndarray is returned,
          so for further processing on the host, you need to copy ot yourself.
          otherwise you can simply continue on the GPU device. Moreover,
          if you supply cupy.ndarrays with the right data types,
          this also speeds up the computation, since no copying or
          conversion have to be done.

        Parameters
        ----------
        arrCoEle : np.ndarray
            Sample at these elevations in radians
        arrAzi : np.ndarray
            Sample at these azimuths in radians
        numFreq : np.ndarray
            Sample at this frequency in Hertz

        Returns
        -------
        np.ndarray
            (Ang x Pol x Elem x x Pol x Elem x (
            (derivEle, derivAzi) x (derivEle, derivAzi)
            )))
        """
        return self._evalNarrowBand(
            arrCoEle, arrAzi, numFreq, evaluateHessianNarrowBand
        )

    def pattern(
        self, arrCoEle: np.ndarray, arrAzi: np.ndarray, arrFreq: np.ndarray
    ) -> np.ndarray:
        """Sample the Beampattern at Angles and Frequencies

        The supplied arrays need to have the same length. The returned
        array has again the same length. This method samples the EADF object
        for given angles and excitation frequencies
        for all polarizations and array elements.
        So it yields a (Ang,Freq) x Pol x Element ndarray.

        Since we have no crystalline sphere to guess, we cannot do
        extrapolation, so the requested frequencies have to be between the
        minimum and maximum frequency the array was excited with.

        .. note::
          If the GPU is used for calculation a cupy.ndarray is returned,
          so for further processing on the host, you need to copy ot yourself.
          otherwise you can simply continue on the GPU device. Moreover,
          if you supply cupy.ndarrays with the right data types,
          this also speeds up the computation, since no copying or
          conversion have to be done.

        Parameters
        ----------
        arrCoEle : np.ndarray
            Sample at these elevations in radians
        arrAzi : np.ndarray
            Sample at these azimuths in radians
        arrFreq : np.ndarray
            Sample at these frequencies in Hertz

        Returns
        -------
        np.ndarray
            Beampattern values at the requested angles
            ((Ang, Freq) x Pol x Elem)
        """

        return self._eval(arrCoEle, arrAzi, arrFreq, evaluatePattern)

    def gradient(
        self, arrCoEle: np.ndarray, arrAzi: np.ndarray, arrFreq: np.ndarray
    ) -> np.ndarray:
        """Sample the Beampattern Gradient at Angles and Frequencies

        The supplied arrays need to have the same length. The returned
        array has again the same length. This method samples the EADF object
        for given angles and excitation frequencies
        for all polarizations and array elements.
        So it yields a (Ang,Freq) x Pol x Element ndarray.

        Since we have no crystalline sphere to guess, we cannot do
        extrapolation, so the requested frequencies have to be between the
        minimum and maximum frequency the array was excited with.

        .. note::
          If the GPU is used for calculation a cupy.ndarray is returned,
          so for further processing on the host, you need to copy ot yourself.
          otherwise you can simply continue on the GPU device. Moreover,
          if you supply cupy.ndarrays with the right data types,
          this also speeds up the computation, since no copying or
          conversion have to be done.

        Parameters
        ----------
        arrCoEle : np.ndarray
            Sample at these elevations in radians
        arrAzi : np.ndarray
            Sample at these azimuths in radians
        arrFreq : np.ndarray
            Sample at these frequencies in Hertz

        Returns
        -------
        np.ndarray
            Beampattern gradient values at the requested angles
            ((Ang, Freq) x Pol x Elem x (derivEle, derivAzi, derivFreq))
        """

        return self._eval(arrCoEle, arrAzi, arrFreq, evaluateGradient)

    def hessian(
        self, arrCoEle: np.ndarray, arrAzi: np.ndarray, arrFreq: np.ndarray
    ) -> np.ndarray:
        """Sample the Beampattern Hessian at Angles and Frequencies

        The supplied arrays need to have the same length. The returned
        array has again the same length. This method samples the EADF object
        for given angles and excitation frequencies
        for all polarizations and array elements.
        So it yields a (Ang,Freq) x Pol x Element ndarray.

        Since we have no crystalline sphere to guess, we cannot do
        extrapolation, so the requested frequencies have to be between the
        minimum and maximum frequency the array was excited with.

        .. note::
          If the GPU is used for calculation a cupy.ndarray is returned,
          so for further processing on the host, you need to copy ot yourself.
          otherwise you can simply continue on the GPU device. Moreover,
          if you supply cupy.ndarrays with the right data types,
          this also speeds up the computation, since no copying or
          conversion have to be done.

        Parameters
        ----------
        arrCoEle : np.ndarray
            Sample at these elevations in radians
        arrAzi : np.ndarray
            Sample at these azimuths in radians
        arrFreq : np.ndarray
            Sample at these frequencies in Hertz

        Returns
        -------
        np.ndarray
            Beampattern gradient values at the requested angles
            ((Ang, Freq) x Pol x Elem x (
            (derivEle, derivAzi, derivFreq)
            x (derivEle, derivAzi, derivFreq)))
        """

        return self._eval(arrCoEle, arrAzi, arrFreq, evaluateHessian)

    def __getstate__(self):
        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        # Restore instance attributes
        self.__dict__.update(state)

        # reimport the backend appropriately
        # by trying to recover the old state
        # this might result in a different backend as before
        # depending on availability of hardware and cupy
        self._cacheCalculationData()

    def save(self, path: str) -> None:
        """Save the object to disk in a serialized way

        .. note::
            This is not safe! Make sure the requirements for pickling are met.
            Among these are different CPU architectures, Python versions,
            Numpy versions and so forth.

            However we at least check the eadf package version when reading
            back from disk.

        Parameters
        ----------
        path : str
            Path to write to
        """
        with open(path, "wb") as file:
            pickle.dump(self, file)

    @classmethod
    def load(cls, path: str) -> object:
        """Load the Class from Serialized Data

        .. note::
            This is not safe! Make sure the requirements for pickling are met.
            Among these are different CPU architectures, Python versions,
            Numpy versions and so forth.

            However we at least check the eadf package version when reading
            back from disk and issue a warning if the versions don't match.
            then you are on your own!

        Parameters
        ----------
        path : str
            Path to load from

        Returns
        -------
        object
            The EADF object
        """
        with open(path, "rb") as file:
            res = pickle.load(file)

        from . import __version__

        if res.version != __version__:
            logging.warning(
                "eadf.load: loaded object does not match current version."
            )
        return res

    def __init__(
        self,
        arrData: np.ndarray,
        arrCoEle: np.ndarray,
        arrAzi: np.ndarray,
        arrFreq: np.ndarray,
        arrPos: np.ndarray,
        **options
    ) -> None:
        """Initialize an EADF Object

        Here we assume that the input data is given in the internal data
        format already. If you have antenna data, which is not in the
        internat data format, we advice you to use one of the importers,
        or implement your own.

        In direction of co-elevation, we assume that both the north and the
        south pole were sampled, where the first sample represents the north
        pole and the last one the south pole. So arrCoEle must run from 0 to
        pi. In azimuth direction, we truncate the last
        sample, if we detect in arrAzi that both the first and last sample
        match. Both arrays have to contain values that are evenly spaced and
        ascending in value.

        In frequency we assume a regular grid with ascending values.

        Parameters
        ----------
        arrData : np.ndarray
            Co-Ele x Azi x Freq x Pol x Element
        arrCoEle : np.ndarray
            Co-elevation sampling positions in radians.
            both poles should be sampled.
        arrAzi : np.ndarray
            Azimuth sampling positions in radians.
        arrFreq : np.ndarray
            Frequencies sampled at.
        arrPos : np.ndarray
            (3 x numElements) Positions of the single antenna elements.
            this is just for vizualisation purposes.
        keepNarrowBand: bool, optional
            this enforces the array to be treated as a
            collection of narrowband array. So no interpolation along
            frequency is done during preprocessing and one can only
            call the *NarrowBand methods of the instance. Can only be
            used if you are supplying data with arrData.shape[2] > 1.

            Defaults to (arrData.shape[2] == 1)
        numFreqPadding: int, optional
            number of samples to use to periodify in frequency direction.

            Defaults to 10.

        """
        # Chek the input arguments and allow for readjustments of them
        arrData, arrCoEle, arrAzi, arrFreq, arrPos = _checkInputData(
            arrData, arrCoEle, arrAzi, arrFreq, arrPos, **options
        )

        # store the unit of the original data array
        arrData, self.unitRawData = arrData.m, arrData.u
        arrCoEle, self.unitCoEle = arrCoEle.m, arrCoEle.u
        arrAzi, self.unitAzi = arrAzi.m, arrAzi.u
        arrFreq, self.unitFreq = arrFreq.m, arrFreq.u
        arrPos, self.unitPos = arrPos.m, arrPos.u

        # if the measurements only have one frequency bin,
        # the data is inherently narrowband
        self._isSingleFreq = arrData.shape[2] == 1

        # if we might be tempted to treat the array was wideband data,
        # the user might have set the flag to not do so.
        self._isNarrowBand = options.get("keepNarrowBand", self._isSingleFreq)
        self._numFreqPadding = options.get("numFreqPadding", 10)

        # truncate the beampattern data correctly
        # in azimuth we make sure that we did not sample the same angle twice
        if np.allclose(
            np.mod(arrAzi[0] + 2 * np.pi, 2 * np.pi),
            np.mod(arrAzi[-1], 2 * np.pi),
        ):
            arrAziTrunc = np.arange(arrAzi.shape[0] - 1)
        else:
            arrAziTrunc = np.arange(arrAzi.shape[0])

        # if we are not narrowband we apply spline extrapolation
        # to make the data in frequency periodic

        if not self._isNarrowBand:
            self._arrRawData = periodifyFreq(
                arrData[:, arrAziTrunc], self._numFreqPadding
            )
        else:
            # make a copy of the supplied data
            self._arrRawData = np.copy(arrData)

        # do the flipping and shifting in elevation and azimuth
        self._arrRawData = symmetrizeData(self._arrRawData[:, arrAziTrunc])

        # extract some meta data from the input
        self._arrPos = np.copy(arrPos)
        self._numElements = self._arrPos.shape[1]
        self._numCoEleInit = 2 * arrCoEle.shape[0] - 2
        self._numAziInit = arrAziTrunc.shape[0]
        self._arrCoEle = np.copy(arrCoEle.flatten())
        self._arrAzi = np.copy(arrAzi.flatten()[arrAziTrunc])
        self._arrFreq = np.copy(arrFreq.flatten())
        self._lowMemory = lowMemory

        # now we know how many samples exactly we have in frequency
        # direction
        self._numFreqInit = self._arrRawData.shape[2]

        # generate the Fourier representation and the according
        # frequency bins
        if self._isNarrowBand:
            (
                self._arrFourierData,
                self._muCoEle,
                self._muAzi,
            ) = sampledToFourier(self._arrRawData[:, arrAziTrunc], (0, 1))
        else:
            (
                self._arrFourierData,
                self._muCoEle,
                self._muAzi,
                self._muFreq,
            ) = sampledToFourier(self._arrRawData[:, arrAziTrunc], (0, 1, 2))

        # initialize some properties with defaults values
        self._complexDtype = "complex128"
        self._realDtype = "float64"
        self._dtype = "double"
        self._blockSize = 128

        # initially we don't do any compression
        # but this already truncates any zeros in the spectrum
        self.compressionFactor = 1.0
        self.dtype = dtype

        # so we can start off quickly!
        self._cacheCalculationData()

        # set the version
        self._version = __version__
