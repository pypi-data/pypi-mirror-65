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
Mathematical Core Routines
--------------------------

In this submodule we place all the mathematical and general core routines
which are used throughout the package. These are not intended for
direct use, but are still documented in order to allow new developers who
are unfamiliar with the code base to get used to the internal structure.
"""

import numpy as np
import pint
from .backend import xp
from .backend import einsumArgs

ureg = pint.UnitRegistry()


def fourierToSampled(arrData: np.ndarray, axes: tuple) -> tuple:
    """Transform the Regularly Sampled Fourier Data in Spatial Domain

    We assume that the provided data was discretely Fourier transformed in both
    angular directions, so we have Fourier samples on a regular 2D grid.
    Moreover in this format all spatial freqencies are obtained for all
    the same wave-freqency samples. This routines then gives back the
    beampattern on a regular angular grid together with the right
    angular frequency bins.

    Parameters
    ----------
    arrData : np.ndarray
        Fourier data in the form
        2 * co-ele x azi x freq x pol x elem

    Returns
    -------
    tuple
        Inverse Fourier Transform and the respective sample frequencies

    """
    if len(arrData.shape) != 5:
        raise ValueError(
            "fourierToSampled: arrData has wrong number of dimensions"
        )
    if arrData.shape[3] > 2:
        raise ValueError(
            "fourierToSampled: There must be at most 2 polarisations"
        )

    freqs = tuple(
        (arrData.shape[ii] * np.fft.fftfreq(arrData.shape[ii])) for ii in axes
    )

    scaling = 1.0
    for aa in axes:
        scaling *= arrData.shape[aa]

    # the frequencies are generated according to (5) in the EADF paper
    res = np.fft.ifftn(arrData, axes=axes) * scaling

    return (res, *freqs)


def sampledToFourier(arrData: np.ndarray, axes: tuple) -> tuple:
    """Transform the regularly sampled data in frequency domain

    Here we assume that the data is already flipped along co-elevation,
    rotated along azimuth as described in the EADF paper and in the wideband
    case it is also preiodified in excitation frequency direction such that we
    can just calculate the respective 2D/3D FFT from this along the first two
    /three axes.

    Parameters
    ----------
    data : np.ndarray
        Raw sampled and preprocessed data in the form
        2 * co-ele x azi x freq x pol x elem

    Returns
    -------
    (np.ndarray, np.ndarray, np.ndarray)
        Fourier Transform and the respective sample frequencies

    """
    if (arrData.shape[0] % 2) != 0:
        raise ValueError(
            "sampledToFourier: 1st dim of arrData must have even size."
        )
    if len(arrData.shape) != 5:
        raise ValueError(
            "sampledToFourier: arrData has wrong number of dimensions"
        )
    if arrData.shape[3] > 2:
        raise ValueError(
            "sampledToFourier: There must be at most 2 polarisations"
        )

    freqs = tuple(
        (arrData.shape[ii] * np.fft.fftfreq(arrData.shape[ii])) for ii in axes
    )

    scaling = 1.0
    for aa in axes:
        scaling *= arrData.shape[aa]

    # the frequencies are generated according to (5) in the EADF paper
    res = np.fft.fftn(arrData, axes=axes) / scaling

    return (res, *freqs)


def calcBlockSizeNarrowBand(
    muCoEle: xp.ndarray, muAzi: xp.ndarray, arrData: xp.ndarray
) -> int:
    """Calculate an optimized block size in the narrowband case

    This function steadily increases the blockSize during the pattern
    transform in order to optimze it for execution time. We only use a very
    crude metric and a very naive measurement for execution time. However,
    it is a starting point.

    Parameters
    ----------
    muCoEle : xp.ndarray
        co-elevation FFT frequencies
    muAzi : xp.ndarray
        azimuth FFT frequencies
    arrData : xp.ndarray
        Fourier coefficients of the array

    Returns
    -------
    int
        block size

    """
    import timeit

    # this also the initial block size
    # we also increase it by this value as long as it decreases
    stepSize = 128
    t1 = 2
    t2 = 1
    s1 = 0

    # iterate until the computation time increases
    while t1 >= t2:
        s2 = s1 + stepSize
        n = np.max(s1 + s2)
        azi = xp.exp(1j * xp.outer(muAzi, xp.random.randn(n)))
        ele = xp.exp(1j * xp.outer(muCoEle, xp.random.randn(n)))

        def A2():
            _inversePatternTransformNarrowBand(ele, azi, arrData, s2)

        t2 = np.mean(timeit.repeat(A2, repeat=5, number=10)) / n

        # if the computation time increased for the first time, we
        # stop the iteration and return the previous s1
        if t2 > t1:
            break
        else:
            t1 = t2
            s1 = s2
    return s1


def calcBlockSize(
    muCoEle: xp.ndarray,
    muAzi: xp.ndarray,
    muFreq: xp.ndarray,
    arrData: xp.ndarray,
) -> int:
    """Calculate an optimized block size

    This function steadily increases the blockSize during the pattern
    transform in order to optimze it for execution time. We only use a very
    crude metric and a very naive measurement for execution time. However,
    it is a starting point.

    Parameters
    ----------
    muCoEle : xp.ndarray
        co-elevation FFT frequencies
    muAzi : xp.ndarray
        azimuth FFT frequencies
    muFreq : xp.ndarray
        frequency FFT frequencies
    arrData : xp.ndarray
        Fourier coefficients of the array

    Returns
    -------
    int
        block size

    """
    import timeit

    # this also the initial block size
    # we also increase it by this value as long as it decreases
    stepSize = 128
    t1 = 2
    t2 = 1
    s1 = 0

    # iterate until the computation time increases
    while t1 >= t2:
        s2 = s1 + stepSize
        n = np.max(s1 + s2)
        ele = xp.exp(1j * xp.outer(muCoEle, np.random.randn(n)))
        azi = xp.exp(1j * xp.outer(muAzi, np.random.randn(n)))
        freq = xp.exp(1j * xp.outer(muFreq, np.random.randn(n)))

        def A2():
            _inversePatternTransform(ele, azi, freq, arrData, s2)

        t2 = np.mean(timeit.repeat(A2, repeat=5, number=10)) / n

        # if the computation time increased for the first time, we
        # stop the iteration and return the previous s1
        if t2 > t1:
            break
        else:
            t1 = t2
            s1 = s2
    return s1


def _inversePatternTransformNarrowBand(
    arrCoEle: xp.ndarray,
    arrAzi: xp.ndarray,
    arrData: xp.ndarray,
    blockSize: int,
) -> xp.ndarray:
    """Samples the Pattern by using the Fourier Coefficients

    This function does the heavy lifting in the EADF evaluation process.
    It is used to sample the beampattern and the derivative itself, by
    evaluating d_phi * Gamma * d_theta^t as stated in (6) in the EADF
    paper by Landmann and delGaldo. It broadcasts this product over
    the last three coordinates of the fourier data, so across all
    polarisations, wave frequency bins and array elements.

    By changing d_theta(arrCoEle) and d_phi (arrAzi) acordingly in the
    arguments one can calculate either the derivative or the pattern itself.

    Parameters
    ----------
    arrCoEle : xp.ndarray
        array of fourier kernels in co-elevation direction
    arrAzi : xp.ndarray
        array of fourier kernels in azimuth direction
    arrData : xp.ndarray
        the Fourier coefficients to use
    blockSize : int
        number of angles to process at once

    Returns
    -------
    xp.ndarray
        beam pattern values at arrCoEle, arrAzi
    """
    # equation (6) in EADF paper by landmann and del galdo
    # xp.einsum(
    #    "ij...,ik,jk->k...", arrData, arrCoEle, arrAzi, **einsumArgs
    # )
    arrRes = xp.empty(
        (arrCoEle.shape[1], *arrData.shape[2:]), dtype=arrData.dtype
    )
    numBlocks = int(arrCoEle.shape[1] / blockSize)

    # iterate over the blocks
    for bb in range(numBlocks):
        # only create the views once.
        ae = arrCoEle[:, bb * blockSize : (bb + 1) * blockSize]
        aa = arrAzi[:, bb * blockSize : (bb + 1) * blockSize]
        for jj in range(arrData.shape[2]):
            for kk in range(arrData.shape[3]):
                arrRes[bb * blockSize : (bb + 1) * blockSize, jj, kk] = np.sum(
                    ae * arrData[:, :, jj, kk].dot(aa), axis=0
                )

    # iterate over the rest
    for jj in range(arrData.shape[2]):
        for kk in range(arrData.shape[3]):
            arrRes[numBlocks * blockSize :, jj, kk] = np.sum(
                arrCoEle[:, numBlocks * blockSize :]
                * arrData[:, :, jj, kk].dot(
                    arrAzi[:, numBlocks * blockSize :]
                ),
                axis=0,
            )
    return arrRes


def _inversePatternTransformNarrowBandLowMem(
    arrCoEle: xp.ndarray,
    arrAzi: xp.ndarray,
    funCoEle,
    funAzi,
    arrData: xp.ndarray,
    blockSize: int,
) -> xp.ndarray:
    """Samples the Pattern by using the Fourier Coefficients

    This function does the heavy lifting in the :py:obj:`EADF` evaluation
    process. It is used to sample the beampattern and the derivative itself, by
    evaluating d_phi * Gamma * d_theta^t as stated in (6) in the EADF
    paper by Landmann and delGaldo. It broadcasts this product over
    the last three coordinates of the fourier data, so across all
    polarisations, wave frequency bins and array elements.

    By changing d_theta(arrCoEle) and d_phi (arrAzi) acordingly in the
    arguments one can calculate either the derivative or the pattern itself.

    Parameters
    ----------
    arrCoEle : xp.ndarray
        array of fourier kernels in co-elevation direction
    arrAzi : xp.ndarray
        array of fourier kernels in azimuth direction
    funAzi : method
        function that generates transform matrix in azimuth direction
    funCoEle : method
        function that generates transform matrix in frequency direction
    arrData : xp.ndarray
        the Fourier coefficients to use
    blockSize : int
        number of blocks to transform at once

    Returns
    -------
    xp.ndarray
        beam pattern values at arrCoEle, arrAzi
    """
    # equation (6) in EADF paper by landmann and del galdo
    # xp.einsum(
    #    "ij...,ik,jk->k...", arrData, arrCoEle, arrAzi, **einsumArgs
    # )
    res = xp.empty(
        (arrCoEle.shape[0], *arrData.shape[2:]), dtype=arrData.dtype
    )
    numBlocks = int(arrCoEle.shape[0] / blockSize)

    # iterate over the blocks
    for bb in range(numBlocks):
        # only create the views once.
        ae = funCoEle(arrCoEle[bb * blockSize : (bb + 1) * blockSize])
        aa = funAzi(arrAzi[bb * blockSize : (bb + 1) * blockSize])
        for jj in range(arrData.shape[2]):
            for kk in range(arrData.shape[3]):
                res[bb * blockSize : (bb + 1) * blockSize, jj, kk] = np.sum(
                    ae * arrData[:, :, jj, kk].dot(aa), axis=0
                )

    # iterate over the rest
    ae = funCoEle(arrCoEle[numBlocks * blockSize :])
    aa = funAzi(arrAzi[numBlocks * blockSize :])

    for jj in range(arrData.shape[2]):
        for kk in range(arrData.shape[3]):
            res[numBlocks * blockSize :, jj, kk] = np.sum(
                ae * arrData[:, :, jj, kk].dot(aa), axis=0
            )
    return res


def _inversePatternTransform(
    arrCoEle: xp.ndarray,
    arrAzi: xp.ndarray,
    arrFreq: xp.ndarray,
    arrData: xp.ndarray,
    blockSize: int,
) -> xp.ndarray:
    """Samples the Pattern by using the Fourier Coefficients

    This function does the heavy lifting in the EADF evaluation process.
    It is used to sample the beampattern and the derivative itself, by
    evaluating d_phi * Gamma * d_theta^t as stated in (6) in the EADF
    paper by Landmann and delGaldo. It broadcasts this product over
    the last three coordinates of the fourier data, so across all
    polarisations, wave frequency bins and array elements.

    By changing d_theta(arrCoEle) and d_phi (arrAzi) accordingly in the
    arguments one can calculate either the derivative or the pattern itself.

    Parameters
    ----------
    arrCoEle : xp.ndarray
        array of fourier kernels in co-elevation direction
    arrAzi : xp.ndarray
        array of fourier kernels in azimuth direction
    arrFreq : xp.ndarray
        array of fourier kernels along  wave frequency
    arrData : xp.ndarray
        the Fourier coefficients to use
    blockSize : int
        number of blocks to transform at once

    Returns
    -------
    xp.ndarray
        beam pattern values at arrCoEle, arrAzi
    """

    # equation (6) in EADF paper by landmann and del galdo
    # extended to another frequency dimension
    arrRes = xp.empty(
        (arrCoEle.shape[-1], *arrData.shape[3:]), dtype=arrData.dtype
    )

    numBlocks = int(arrCoEle.shape[1] / blockSize)
    # iterate over the blocks
    for bb in range(numBlocks):

        arrRes[bb * blockSize : (bb + 1) * blockSize] = xp.einsum(
            "ijl...,ik,jk,lk->k...",
            arrData,
            arrCoEle[:, bb * blockSize : (bb + 1) * blockSize],
            arrAzi[:, bb * blockSize : (bb + 1) * blockSize],
            arrFreq[:, bb * blockSize : (bb + 1) * blockSize],
            **einsumArgs
        )

    # process the rest
    arrRes[numBlocks * blockSize :] = xp.einsum(
        "ijl...,ik,jk,lk->k...",
        arrData,
        arrCoEle[:, numBlocks * blockSize :],
        arrAzi[:, numBlocks * blockSize :],
        arrFreq[:, numBlocks * blockSize :],
        **einsumArgs
    )
    return arrRes


def _inversePatternTransformLowMem(
    arrCoEle: xp.ndarray,
    arrAzi: xp.ndarray,
    arrFreq: xp.ndarray,
    funCoEle,
    funAzi,
    funFreq,
    arrData: xp.ndarray,
    blockSize: int,
) -> xp.ndarray:
    """Samples the Pattern by using the Fourier Coefficients

    This function does the heavy lifting in the :py:obj:`EADF` evaluation
    process. It is used to sample the beampattern and the derivative itself, by
    evaluating d_phi * Gamma * d_theta^t as stated in (6) in the EADF
    paper by Landmann and delGaldo. It broadcasts this product over
    the last three coordinates of the fourier data, so across all
    polarisations, wave frequency bins and array elements.

    By changing d_theta(arrCoEle) and d_phi (arrAzi) accordingly in the
    arguments one can calculate either the derivative or the pattern itself.

    Parameters
    ----------
    arrCoEle : xp.ndarray
        array of fourier kernels in co-elevation direction
    arrAzi : xp.ndarray
        array of fourier kernels in azimuth direction
    arrFreq : xp.ndarray
        array of fourier kernels in co-elevation direction
    funCoEle : method
        Function the generates the transform matrix for Co-Elevation
    funAzi : method
        Function the generates the transform matrix for azimuth
    funFreq : method
        Function the generates the transform matrix for frequency
    arrData : xp.ndarray
        the Fourier coefficients to use
    blockSize : int
        number of blocks to transform at once

    Returns
    -------
    xp.ndarray
        beam pattern values at arrCoEle, arrAzi
    """

    # equation (6) in EADF paper by landmann and del galdo
    # extended to another frequency dimension
    arrRes = xp.empty(
        (arrCoEle.shape[-1], *arrData.shape[3:]), dtype=arrData.dtype
    )
    numBlocks = int(arrCoEle.shape[-1] / blockSize)

    # iterate over the blocks
    for bb in range(numBlocks):
        arrRes[bb * blockSize : (bb + 1) * blockSize] = xp.einsum(
            "ijl...,ik,jk,lk->k...",
            arrData,
            funCoEle(arrCoEle[bb * blockSize : (bb + 1) * blockSize]),
            funAzi(arrAzi[bb * blockSize : (bb + 1) * blockSize]),
            funFreq(arrFreq[bb * blockSize : (bb + 1) * blockSize]),
            **einsumArgs
        )

    # process the rest
    arrRes[numBlocks * blockSize :] = xp.einsum(
        "ijl...,ik,jk,lk->k...",
        arrData,
        funCoEle(arrCoEle[numBlocks * blockSize :]),
        funAzi(arrAzi[numBlocks * blockSize :]),
        funFreq(arrFreq[numBlocks * blockSize :]),
        **einsumArgs
    )
    return arrRes


def evaluatePatternNarrowBand(
    arrCoEle: xp.ndarray,
    arrAzi: xp.ndarray,
    muCoEle: xp.ndarray,
    muAzi: xp.ndarray,
    arrData: xp.ndarray,
    blockSize: int,
    lowMem: bool,
) -> xp.ndarray:
    """Sample the Beampattern at Dedicated Angles

    Parameters
    ----------
    arrCoEle : xp.ndarray
        co-elevation angles to sample at in radians
    arrAzi : xp.ndarray
        azimuth angles to sample at in radians
    muCoEle : xp.ndarray
        spatial frequency bins in co-elevation direction
    muAzi : xp.ndarray
        spatial frequency bins in azimuth direction
    arrData : xp.ndarray
        fourier coefficients
    blockSize : int
        number of angles / frequencies to process at once
    lowMem : bool
        should we save memory?

    Returns
    -------
    xp.ndarray
        sampled values
    """
    if lowMem:

        def funCoEle(arrCoEle):
            # equation (7) in the EADF Paper
            return xp.exp(1j * xp.outer(muCoEle, arrCoEle))

        def funAzi(arrAzi):
            # equation (7) in the EADF Paper
            return xp.exp(1j * xp.outer(muAzi, arrAzi))

        return _inversePatternTransformNarrowBandLowMem(
            arrCoEle, arrAzi, funCoEle, funAzi, arrData, blockSize
        )
    else:
        # equation (7) in the EADF Paper
        arrMultAzi = xp.exp(1j * xp.outer(muAzi, arrAzi))
        arrMultCoEle = xp.exp(1j * xp.outer(muCoEle, arrCoEle))

        return _inversePatternTransformNarrowBand(
            arrMultCoEle, arrMultAzi, arrData, blockSize
        )


def evaluatePattern(
    arrCoEle: xp.ndarray,
    arrAzi: xp.ndarray,
    arrFreq: xp.ndarray,
    muCoEle: xp.ndarray,
    muAzi: xp.ndarray,
    muFreq: xp.ndarray,
    arrData: xp.ndarray,
    blockSize: int,
    lowMem: bool,
) -> xp.ndarray:
    """Sample the Beampattern at Dedicated Angles

    Parameters
    ----------
    arrCoEle : xp.ndarray
        co-elevation angles to sample at in radians
    arrAzi : xp.ndarray
        azimuth angles to sample at in radians
    arrFreq : xp.ndarray
        frequencies to sample at in Hertz
    muCoEle : xp.ndarray
        spatial frequency bins in co-elevation direction
    muAzi : xp.ndarray
        spatial frequency bins in azimuth direction
    muFreq : xp.ndarray
        spatial frequency bins in excitation frequency direction
    arrData : xp.ndarray
        fourier coefficients

    Returns
    -------
    xp.ndarray
        sampled values
    """
    if lowMem:

        def funCoEle(arrCoEle):
            return xp.exp(1j * xp.outer(muCoEle, arrCoEle))

        def funAzi(arrAzi):
            return xp.exp(1j * xp.outer(muAzi, arrAzi))

        def funFreq(arrFreq):
            return xp.exp(1j * xp.outer(muFreq, arrFreq))

        return _inversePatternTransformLowMem(
            arrCoEle,
            arrAzi,
            arrFreq,
            funCoEle,
            funAzi,
            funFreq,
            arrData,
            blockSize,
        )
    else:
        # equation (7) in the EADF Paper
        arrMultCoEle = xp.exp(1j * xp.outer(muCoEle, arrCoEle))
        arrMultAzi = xp.exp(1j * xp.outer(muAzi, arrAzi))

        # extension in frequency domain
        arrMultFreq = xp.exp(1j * xp.outer(muFreq, arrFreq))

        return _inversePatternTransform(
            arrMultCoEle, arrMultAzi, arrMultFreq, arrData, blockSize
        )


def evaluateGradientNarrowBand(
    arrCoEle: xp.ndarray,
    arrAzi: xp.ndarray,
    muCoEle: xp.ndarray,
    muAzi: xp.ndarray,
    arrData: xp.ndarray,
    blockSize: int,
    lowMem: bool,
) -> xp.ndarray:
    """Sample the Beampattern Gradients at Dedicated Angles

    Parameters
    ----------
    arrCoEle : xp.ndarray
        co-elevation angles to sample at in radians
    arrAzi : xp.ndarray
        azimuth angles to sample at in radians
    muCoEle : xp.ndarray
        spatial frequency bins in co-elevation direction
    muAzi : xp.ndarray
        spatial frequency bins in azimuth direction
    arrData : xp.ndarray
        fourier coefficients
    blockSize : int
        number of angles / frequencies to process at once
    lowMem : bool
        should we save memory?

    Returns
    -------
        xp.ndarray
    """
    if lowMem:

        def funCoEle(arrCoEle):
            # equation (7) in the EADF Paper
            return xp.exp(1j * xp.outer(muCoEle, arrCoEle))

        def funAzi(arrAzi):
            # equation (7) in the EADF Paper
            return xp.exp(1j * xp.outer(muAzi, arrAzi))

        def funDerivCoEle(arrCoEle):
            # equation (8) in the EADF Paper
            return xp.multiply(
                xp.pi * 1j * muCoEle,
                xp.exp(1j * xp.outer(muCoEle, arrCoEle)).T,
            ).T

        def funDerivAzi(arrAzi):
            # equation (8) in the EADF Paper
            return xp.multiply(
                xp.pi * 1j * muAzi, xp.exp(1j * xp.outer(muAzi, arrAzi)).T
            ).T

        return xp.stack(
            (
                _inversePatternTransformNarrowBandLowMem(
                    arrCoEle,
                    arrCoEle,
                    funDerivCoEle,
                    funAzi,
                    arrData,
                    blockSize,
                ),
                _inversePatternTransformNarrowBandLowMem(
                    arrCoEle, arrAzi, funCoEle, funDerivAzi, arrData, blockSize
                ),
            ),
            axis=-1,
        )
    else:
        # equation (7) in the EADF Paper
        arrMultCoEle = xp.exp(1j * xp.outer(muCoEle, arrCoEle))
        arrMultAzi = xp.exp(1j * xp.outer(muAzi, arrAzi))

        # equation (8) in the EADF Paper
        arrMultCoEleDeriv = xp.multiply(xp.pi * 1j * muCoEle, arrMultCoEle.T).T
        arrMultAziDeriv = xp.multiply(xp.pi * 1j * muAzi, arrMultAzi.T).T

        # build up array of gradient by calling the pattern transform
        # twice and then stacking them along a new last dimension
        return xp.stack(
            (
                _inversePatternTransformNarrowBand(
                    arrMultCoEleDeriv, arrMultAzi, arrData, blockSize
                ),
                _inversePatternTransformNarrowBand(
                    arrMultCoEle, arrMultAziDeriv, arrData, blockSize
                ),
            ),
            axis=-1,
        )


def evaluateGradient(
    arrCoEle: xp.ndarray,
    arrAzi: xp.ndarray,
    arrFreq: xp.ndarray,
    muCoEle: xp.ndarray,
    muAzi: xp.ndarray,
    muFreq: xp.ndarray,
    arrData: xp.ndarray,
    blockSize: int,
    lowMem: bool,
) -> xp.ndarray:
    """Sample the Beampattern Gradients at Dedicated Angles

    Parameters
    ----------
    arrCoEle : xp.ndarray
        co-elevation angles to sample at in radians
    arrAzi : xp.ndarray
        azimuth angles to sample at in radians
    arrFreq : xp.ndarray
        frequencies to sample at in Hertz
    muCoEle : xp.ndarray
        spatial frequency bins in co-elevation direction
    muAzi : xp.ndarray
        spatial frequency bins in azimuth direction
    muFreq : xp.ndarray
        spatial frequency bins in excitation frequency direction
    arrData : xp.ndarray
        fourier coefficients
    blockSize : int
        number of angles / frequencies to process at once
    lowMem : bool
        should we save memory?

    Returns
    -------
        xp.ndarray
    """
    if lowMem:

        def funCoEle(arrCoEle):
            return xp.exp(1j * xp.outer(muCoEle, arrCoEle))

        def funAzi(arrAzi):
            return xp.exp(1j * xp.outer(muAzi, arrAzi))

        def funFreq(arrFreq):
            return xp.exp(1j * xp.outer(muFreq, arrFreq))

        def funDerivCoEle(arrCoEle):
            return xp.multiply(
                xp.pi * 1j * muCoEle, xp.exp(1j * xp.outer(muCoEle, arrCoEle))
            )

        def funDerivAzi(arrAzi):
            return xp.multiply(
                xp.pi * 1j * muAzi, xp.exp(1j * xp.outer(muAzi, arrAzi))
            )

        def funDerivFreq(arrFreq):
            return xp.multiply(
                xp.pi * 1j * muFreq, xp.exp(1j * xp.outer(muFreq, arrFreq))
            )

        derivCoEle = _inversePatternTransformLowMem(
            arrCoEle,
            arrAzi,
            arrFreq,
            funDerivCoEle,
            funAzi,
            funFreq,
            arrData,
            blockSize,
        )
        derivAzi = _inversePatternTransformLowMem(
            arrCoEle,
            arrAzi,
            arrFreq,
            funCoEle,
            funDerivAzi,
            funFreq,
            arrData,
            blockSize,
        )
        derivFreq = _inversePatternTransformLowMem(
            arrCoEle,
            arrAzi,
            arrFreq,
            funCoEle,
            funAzi,
            funDerivFreq,
            arrData,
            blockSize,
        )
    else:
        # equation (7) in the EADF Paper
        arrMultCoEle = xp.exp(1j * xp.outer(muCoEle, arrCoEle))
        arrMultAzi = xp.exp(1j * xp.outer(muAzi, arrAzi))

        # extension in frequency domain
        arrMultFreq = xp.exp(1j * xp.outer(muFreq, arrFreq))

        # equation (8) in the EADF Paper
        arrMultCoEleDeriv = xp.multiply(xp.pi * 1j * muCoEle, arrMultCoEle.T).T
        arrMultAziDeriv = xp.multiply(xp.pi * 1j * muAzi, arrMultAzi.T).T

        # extension in frequency domain
        arrMultFreqDeriv = xp.multiply(xp.pi * 1j * muFreq, arrMultFreq.T).T

        derivCoEle = _inversePatternTransform(
            arrMultCoEleDeriv, arrMultAzi, arrMultFreq, arrData, blockSize
        )
        derivAzi = _inversePatternTransform(
            arrMultCoEle, arrMultAziDeriv, arrMultFreq, arrData, blockSize
        )
        derivFreq = _inversePatternTransform(
            arrMultCoEleDeriv, arrMultAzi, arrMultFreqDeriv, arrData, blockSize
        )

        # build up array of gradient by calling the pattern transform
        # twice and then stacking them along a new last dimension
    return xp.stack((derivCoEle, derivAzi, derivFreq), axis=-1)


def evaluateHessianNarrowBand(
    arrCoEle: xp.ndarray,
    arrAzi: xp.ndarray,
    muCoEle: xp.ndarray,
    muAzi: xp.ndarray,
    arrData: xp.ndarray,
    blockSize: int,
    lowMem: bool,
) -> xp.ndarray:
    """Sample the Beampattern Gradients at Dedicated Angles

    Parameters
    ----------
    arrCoEle : xp.ndarray
        co-elevation angles to sample at in radians
    arrAzi : xp.ndarray
        azimuth angles to sample at in radians
    muCoEle : xp.ndarray
        spatial frequency bins in co-elevation direction
    muAzi : xp.ndarray
        spatial frequency bins in azimuth direction
    arrData : xp.ndarray
        fourier coefficients
    blockSize : int
        number of angles to process at once
    lowMem : bool
        should we save memory?

    Returns
    -------
        xp.ndarray
    """
    if lowMem:

        def funCoEle(arrCoEle):
            # equation (7) in the EADF Paper
            return xp.exp(1j * xp.outer(muCoEle, arrCoEle))

        def funAzi(arrAzi):
            # equation (7) in the EADF Paper
            return xp.exp(1j * xp.outer(muAzi, arrAzi))

        def funDerivCoEle(arrCoEle):
            # equation (8) in the EADF Paper
            return xp.multiply(
                xp.pi * 1j * muCoEle,
                xp.exp(1j * xp.outer(muCoEle, arrCoEle)).T,
            ).T

        def funDerivAzi(arrAzi):
            # equation (8) in the EADF Paper
            return xp.multiply(
                xp.pi * 1j * muAzi, xp.exp(1j * xp.outer(muAzi, arrAzi)).T
            ).T

        def funDerivDerivCoEle(arrCoEle):
            # another derivative taken in (8) in the EADF paper
            return xp.multiply(
                -(muCoEle ** 2), xp.exp(1j * xp.outer(muCoEle, arrCoEle)).T
            ).T

        def funDerivDerivAzi(arrAzi):
            # another derivative taken in (8) in the EADF paper
            return xp.multiply(
                -(muAzi ** 2), xp.exp(1j * xp.outer(muAzi, arrAzi)).T
            ).T

        d11 = _inversePatternTransformNarrowBandLowMem(
            arrCoEle, arrCoEle, funDerivDerivCoEle, funAzi, arrData, blockSize
        )
        d22 = _inversePatternTransformNarrowBandLowMem(
            arrCoEle, arrAzi, funCoEle, funDerivDerivAzi, arrData, blockSize
        )
        d12 = _inversePatternTransformNarrowBandLowMem(
            arrCoEle, arrAzi, funDerivCoEle, funDerivAzi, arrData, blockSize
        )

    else:
        # equation (7) in the EADF Paper
        arrMultCoEle = xp.exp(1j * xp.outer(muCoEle, arrCoEle))
        arrMultAzi = xp.exp(1j * xp.outer(muAzi, arrAzi))

        # equation (8) in the EADF Paper
        arrMultCoEleDeriv = xp.multiply(1j * muCoEle, arrMultCoEle.T).T
        arrMultAziDeriv = xp.multiply(1j * muAzi, arrMultAzi.T).T

        # another derivative taken in (8) in the EADF paper
        arrMultCoEleDerivDeriv = xp.multiply(-(muCoEle ** 2), arrMultCoEle.T).T
        arrMultAziDerivDeriv = xp.multiply(-(muAzi ** 2), arrMultAzi.T).T

        # build up array of gradient by calling the pattern transform
        # twice and then stacking them along a new last dimension
        d11 = _inversePatternTransformNarrowBand(
            arrMultCoEleDerivDeriv, arrMultAzi, arrData, blockSize
        )
        d22 = _inversePatternTransformNarrowBand(
            arrMultCoEle, arrMultAziDerivDeriv, arrData, blockSize
        )
        d12 = _inversePatternTransformNarrowBand(
            arrMultCoEleDeriv, arrMultAziDeriv, arrData, blockSize
        )

    # this should return
    #     |d11|d12|
    # H = |---|---|
    #     |d12|d22|
    return xp.stack(
        (xp.stack((d11, d12.conj()), axis=-1), xp.stack((d12, d22), axis=-1)),
        axis=-1,
    )


def evaluateHessian(
    arrCoEle: xp.ndarray,
    arrAzi: xp.ndarray,
    arrFreq: xp.ndarray,
    muCoEle: xp.ndarray,
    muAzi: xp.ndarray,
    muFreq: xp.ndarray,
    arrData: xp.ndarray,
    blockSize: int,
    lowMem: bool,
) -> xp.ndarray:
    """Sample the Beampattern Gradients at Dedicated Angles

    Parameters
    ----------
    arrCoEle : xp.ndarray
        co-elevation angles to sample at in radians
    arrAzi : xp.ndarray
        azimuth angles to sample at in radians
    arrFreq : xp.ndarray
        frequencies to sample at in Hertz
    muCoEle : xp.ndarray
        spatial frequency bins in co-elevation direction
    muAzi : xp.ndarray
        spatial frequency bins in azimuth direction
    muFreq : xp.ndarray
        spatial frequency bins in excitation frequency direction
    arrData : xp.ndarray
        fourier coefficients
    blockSize : int
        number of angles / frequencies to process at once
    lowMem : bool
        should we save memory?

    Returns
    -------
        xp.ndarray
    """
    if lowMem:

        def funCoEle(arrCoEle):
            return xp.exp(1j * xp.outer(muCoEle, arrCoEle))

        def funAzi(arrAzi):
            return xp.exp(1j * xp.outer(muAzi, arrAzi))

        def funFreq(arrFreq):
            return xp.exp(1j * xp.outer(muFreq, arrFreq))

        def funDerivCoEle(arrCoEle):
            return xp.multiply(
                1j * muCoEle, xp.exp(1j * xp.outer(muCoEle, arrCoEle))
            )

        def funDerivAzi(arrAzi):
            return xp.multiply(
                1j * muAzi, xp.exp(1j * xp.outer(muAzi, arrAzi))
            )

        def funDerivFreq(arrFreq):
            return xp.multiply(
                1j * muFreq, xp.exp(1j * xp.outer(muFreq, arrFreq))
            )

        def funDerivDerivCoEle(arrCoEle):
            return xp.multiply(
                -(muCoEle ** 2), xp.exp(1j * xp.outer(muCoEle, arrCoEle))
            )

        def funDerivDerivAzi(arrAzi):
            return xp.multiply(
                -(muAzi ** 2), xp.exp(1j * xp.outer(muAzi, arrAzi))
            )

        def funDerivDerivFreq(arrFreq):
            return xp.multiply(
                -(muFreq ** 2), xp.exp(1j * xp.outer(muFreq, arrFreq))
            )

        d11 = _inversePatternTransformLowMem(
            arrCoEle,
            arrAzi,
            arrFreq,
            funDerivDerivCoEle,
            funAzi,
            funFreq,
            arrData,
            blockSize,
        )
        d22 = _inversePatternTransformLowMem(
            arrCoEle,
            arrAzi,
            arrFreq,
            funCoEle,
            funDerivDerivAzi,
            funFreq,
            arrData,
            blockSize,
        )
        d33 = _inversePatternTransformLowMem(
            arrCoEle,
            arrAzi,
            arrFreq,
            funCoEle,
            funAzi,
            funDerivDerivFreq,
            arrData,
            blockSize,
        )
        d12 = _inversePatternTransformLowMem(
            arrCoEle,
            arrAzi,
            arrFreq,
            funDerivCoEle,
            funDerivAzi,
            funFreq,
            arrData,
            blockSize,
        )
        d13 = _inversePatternTransformLowMem(
            arrCoEle,
            arrAzi,
            arrFreq,
            funCoEle,
            funDerivAzi,
            funDerivFreq,
            arrData,
            blockSize,
        )
        d23 = _inversePatternTransformLowMem(
            arrCoEle,
            arrAzi,
            arrFreq,
            funDerivCoEle,
            funAzi,
            funDerivFreq,
            arrData,
            blockSize,
        )
    else:
        # equation (7) in the EADF Paper
        arrMultCoEle = xp.exp(1j * xp.outer(muCoEle, arrCoEle))
        arrMultAzi = xp.exp(1j * xp.outer(muAzi, arrAzi))
        arrMultFreq = xp.exp(1j * xp.outer(muFreq, arrFreq))

        # equation (8) in the EADF Paper
        arrMultCoEleDeriv = xp.multiply(1j * muCoEle, arrMultCoEle.T).T
        arrMultAziDeriv = xp.multiply(1j * muAzi, arrMultAzi.T).T
        arrMultFreqDeriv = xp.multiply(1j * muFreq, arrMultFreq.T).T

        # another derivative taken in (8) in the EADF paper
        arrMultCoEleDerivDeriv = xp.multiply(-(muCoEle ** 2), arrMultCoEle.T).T
        arrMultAziDerivDeriv = xp.multiply(-(muAzi ** 2), arrMultAzi.T).T
        arrMultFreqDerivDeriv = xp.multiply(-(muFreq ** 2), arrMultFreq.T).T

        # build up array of gradient by calling the pattern transform
        # twice and then stacking them along a new last dimension
        d11 = _inversePatternTransform(
            arrMultCoEleDerivDeriv, arrMultAzi, arrMultFreq, arrData, blockSize
        )
        d22 = _inversePatternTransform(
            arrMultCoEle, arrMultAziDerivDeriv, arrMultFreq, arrData, blockSize
        )
        d12 = _inversePatternTransform(
            arrMultCoEleDeriv, arrMultAziDeriv, arrMultFreq, arrData, blockSize
        )
        d13 = _inversePatternTransform(
            arrMultCoEle, arrMultAziDeriv, arrMultFreqDeriv, arrData, blockSize
        )
        d23 = _inversePatternTransform(
            arrMultCoEleDeriv, arrMultAzi, arrMultFreqDeriv, arrData, blockSize
        )
        d33 = _inversePatternTransform(
            arrMultCoEle, arrMultAzi, arrMultFreqDerivDeriv, arrData, blockSize
        )

    # this should return
    #     |d11|d12|d13|
    #     |---|---|---|
    # H = |d12|d22|d23|
    #     |---|---|---|
    #     |d13|d23|d33|
    return xp.stack(
        (
            xp.stack((d11, d12, d13), axis=-1),
            xp.stack((d12.conj(), d22, d23), axis=-1),
            xp.stack((d13.conj(), d23.conj(), d33), axis=-1),
        ),
        axis=-1,
    )


def symmetrizeData(arrA: np.ndarray) -> np.ndarray:
    """Generate a symmetrized version of a regularly sampled array data

    This function assumes that we are given the beam pattern sampled in
    co-elevation and azimuth on a regular grid, as well as for at most 2
    polarizations and all the same wave-frequency bins. Then this function
    applies (2) in the original EADF paper. So the resulting array has
    the same dimensions but 2*n-1 the size in co-elevation direction, if
    n was the original co-elevation size.

    Parameters
    ----------
    arrA : np.ndarray
        Input data (co-elevation x azimuth x pol x freq x elem).

    Returns
    -------
    np.ndarray
        Output data (2*co-elevation - 2 x azimuth x pol x freq x elem).

    """
    if len(arrA.shape) != 5:
        raise ValueError(
            "symmetrizeData: got %d dimensions instead of 5"
            % (len(arrA.shape))
        )

    # allocate memory
    arrRes = np.tile(arrA, (2, 1, 1, 1, 1))[:-2]

    # Equation (2) in EADF Paper by Landmann and DGO
    # or more correctly the equations (3.13) - (3.17) in the
    # dissertation of Landmann
    arrRes[arrA.shape[0] :] = -np.roll(
        np.flip(arrA[1:-1], axis=0),
        shift=int((arrA.shape[1] - (arrA.shape[1] % 2)) / 2),
        axis=1,
    )

    return np.fft.fftshift(arrRes, axes=(0, 1))


def regularSamplingToGrid(
    arrA: np.ndarray, numCoEle: int, numAzi: int
) -> np.ndarray:
    """Reshape an array sampled on a 2D grid to actual 2D data

    Parameters
    ----------
    arrA : np.ndarray
        Input data `arrA` (2D angle x pol x freq x elem).
    numCoEle : int
        Number of samples in co-elevation direction.
    numAzi : int
        Number of samples in azimuth direction.

    Returns
    -------
    np.ndarray
        Output data (co-elevation x azimuth x freq x pol x elem).

    """
    if arrA.shape[0] != (numAzi * numCoEle):
        raise ValueError(
            (
                "regularSamplingToGrid:"
                + "numCoEle %d, numAzi %d and arrA.shape[0] %d dont match"
            )
            % (numAzi, numCoEle, arrA.shape[0])
        )
    if len(arrA.shape) != 4:
        raise ValueError(
            (
                "regularSamplingToGrid:"
                + "Input arrA has %d dimensions instead of 4"
            )
            % (len(arrA.shape))
        )

    return arrA.reshape((numCoEle, numAzi, *arrA.shape[1:]))
