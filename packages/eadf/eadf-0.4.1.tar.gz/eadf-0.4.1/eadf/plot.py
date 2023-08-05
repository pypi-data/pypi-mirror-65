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
Plotting Routines
-----------------

These routines are called using an EADF object to aid visualization.
They should not be used directly from outside the package,
but rather developers should implement new plotting functions here
and expose them via appropraite EADF methods.
"""

import numpy as np
from .backend import asNumpy
from .auxiliary import toGrid, sampleAngles
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d


def visualizeCut(
    array,
    numCoEle: float,
    numAzi: int,
    numPol: list,
    numFreq: float,
    arrIndElem: list,
    fun=None,
) -> None:
    """Visualize the Beampattern Along a Certain Angle of Co-Elevation

    This plots several beam patterns along one co-elevation level.
    It also positions the elements in the correct 2D-position from top
    down.

    Example
    -------
    >>> import eadf
    >>> A = eadf.generateStackedUCA(11, 3, 1.5, 0.5)
    >>> visualizeCut(
    >>>     A, 1.67, 60, [0], A.arrFreq[0], list(range(11))
    >>> )

    Parameters
    ----------
    numCoEle : float
        Co-Elevation angle to make the cut at in radians
    numAzi : int
        Number of regularly spaced azimuth grid points
    numPol : list
        Can be either [0], [1] or [0,1]. Selects the polarizations
    numFreq : float
        Freqency to plot
    arrIndElem : list
        Antenna elements to plot
    fun : method
        function to apply to the elements values
        right before plotting. popular choices are np.real or np.imag
        if not specified we use np.abs( . )

    """

    # sample the angles on a regular grid
    arrCoEle, arrAzi = sampleAngles(1, numAzi, lstEndPoints=[True, False])

    # set the elevation angle array to the specified elevation
    # angle
    arrCoEle[:] = numCoEle

    # now generate the grid
    grdCoEle, grdAzi = toGrid(arrCoEle, arrAzi)

    # now sample the array values on the grid
    arrPlotData = array.patternNarrowBand(grdCoEle, grdAzi, numFreq)

    arrPlotData = asNumpy(arrPlotData)

    plotCut2D(
        # now subselect the samples values to the specified
        # polarisation, elements and frequency (the 0)
        arrPlotData[:, numPol, arrIndElem].reshape((-1, 1, len(arrIndElem))),
        grdAzi,
        array._arrPos[:, arrIndElem],
        fun,
    )


def visualize2D(
    array,
    numCoEle: int,
    numAzi: int,
    numPol: int,
    numFreq: float,
    arrIndElem: list,
    fun=None,
) -> None:
    """Plot an Image of several Elements' Beampatterns

    Example
    -------

    >>> import eadf
    >>> A = eadf.generateStackedUCA(11, 3, 1.5, 0.5)
    >>> visualize2D(A, 20, 40, 0, A.arrFreq[0], [0])

    Parameters
    ----------
    numCoEle : int
        number of samples in co-elevation direction
    numAzi : int
        number of samples in azimuth direction
    numPol : int
        polarisation 0, or 1?
    numFreq : float
        Frequency to plot at
    arrIndElem : list
        Index of element to visualize
    fun : method
        function to apply to the elements values
        right before plotting. popular choices are np.real or np.imag
        if not specified we use np.abs( . )
    """

    arrCoEle, arrAzi = sampleAngles(
        numCoEle, numAzi, lstEndPoints=[True, True]
    )
    grdCoEle, grdAzi = toGrid(arrCoEle, arrAzi)
    arrPlotData = array.patternNarrowBand(grdCoEle, grdAzi, numFreq)

    arrPlotData = asNumpy(arrPlotData)

    plotBeamPattern2D(
        arrPlotData[:, numPol, arrIndElem], grdCoEle, grdAzi, numCoEle, numAzi,
    )


def visualize3D(
    array,
    numCoEle: int,
    numAzi: int,
    numPol: int,
    numFreq: float,
    arrIndElem: list,
    fun=None,
) -> None:
    """Plot the Array with 3D Beampatterns

    We first sample the array for on a regular grid in co-elevation
    and azimuth and then we put deformed spheres at the elements
    positions to represent the array elements. for this a fixed
    polarization and a fixed wave-frequency have to be selected.

    Example
    -------

    >>> import eadf
    >>> A = eadf.generateStackedUCA(11, 3, 1.5, 0.5)
    >>> visualize3D(A, 20, 40, 0, 1, [0])

    Parameters
    ----------
    numCoEle : int
        number of samples in co-elevation direction
    numAzi : int
        number of samples in azimuth direction
    numPol : int
        polarisation 0, or 1?
    numFreq : float
        Frequency to sample at
    arrIndElem : list
        Element index to visualize
    fun : method
        function to apply to the elements values
        right before plotting. popular choices are np.real or np.imag
        if not specified we use np.abs( . )
    """

    arrCoEle, arrAzi = sampleAngles(
        numCoEle, numAzi, lstEndPoints=[True, True]
    )
    grdCoEle, grdAzi = toGrid(arrCoEle, arrAzi)
    arrPlotData = array.patternNarrowBand(grdCoEle, grdAzi, numFreq)

    # copy back to host to plot it
    arrPlotData = asNumpy(arrPlotData)

    plotBeamPattern3D(
        arrPlotData[:, numPol, arrIndElem],
        grdCoEle,
        grdAzi,
        array._arrPos[:, arrIndElem],
        numCoEle,
        numAzi,
        fun=(lambda c: np.abs(c) ** 2),
    )


def __defaultFun(x: np.ndarray) -> np.ndarray:
    """Default Function to apply before plotting

    Parameters
    ----------
    x : np.ndarray
        Input

    Returns
    -------
    np.ndarray
        np.abs(Input)

    """
    return np.log(np.abs(x) ** 2)


def plotBeamPattern2D(
    arrData: np.ndarray,
    arrCoEle: np.ndarray,
    arrAzi: np.ndarray,
    numCoEle: int,
    numAzi: int,
    fun=None,
) -> None:
    """Plot several 2D beampatterns

    This routine plots the beam pattern for a single
    frequency of at most 9 Elements
    since we are using subplots.

    Parameters
    ----------
    arrData : np.ndarray
        Input Data in Angle x Elem
    arrCoEle : np.ndarray
        Co-Elevation Angles we sampled at in radians
    arrAzi : np.ndarray
        Azimuth Angles we sampled at in radians
    numCoEle : int
        Number of Samples in CoElevation direction
    numAzi : int
        Number of Samples in Azimuth direction
    fun : method
        function to apply to the elements values
    """
    if (numCoEle * numAzi) != arrData.shape[0]:
        raise ValueError(
            "plotBeamPattern2D:Num of CoEle and Azi %d,%d dont fit data %d,%d"
            % (numCoEle, numAzi, arrData.shape[0], arrData.shape[1])
        )
    if fun is None:
        fun = __defaultFun

    numPlots = min(arrData.shape[-1], 9)

    for ii in range(numPlots):
        plt.subplot(str(100 * (numPlots) + 10 + (ii + 1)))
        # we just take the squared absolute values
        arrR = fun(arrData[..., ii])

        plt.imshow(arrR.reshape((numCoEle, numAzi)))
        plt.colorbar()
    plt.show()


def plotBeamPattern3D(
    arrData: np.ndarray,
    arrCoEle: np.ndarray,
    arrAzi: np.ndarray,
    arrPos: np.ndarray,
    numCoEle: int,
    numAzi: int,
    fun=None,
) -> None:
    """Plot Beampatterns as spherical Gain Plots

    Each array element gets a ball around its position to display the
    respective gain for a single frequency.

    Parameters
    ----------
    arrData : np.ndarray
        Input Data in Angle X Elem
    arrCoEle : np.ndarray
        Co-Elevation Angles we sampled at in radians
    arrAzi : np.ndarray
        Azimuth Angles we sampled at in radians
    arrPos : np.ndarray,
        Positions of the array elements
    numCoEle : int
        Number of Samples in CoElevation direction
    numAzi : int
        Number of Samples in Azimuth direction
    fun : method
        function to apply to the elements values
    """
    if (numCoEle * numAzi) != arrData.shape[0]:
        raise ValueError(
            "plotBeamPattern3D:Num of CoEle and Azi %d,%d dont fit %d, %d"
            % (numCoEle, numAzi, arrData.shape[0], arrData.shape[1])
        )
    if arrData.shape[0] != arrCoEle.shape[0]:
        raise ValueError(
            "plotBeamPattern3D:arrData.shape[0] %d doesnt fit arrCoEle %d"
            % (arrData.shape[0], arrCoEle.shape[0])
        )
    if arrData.shape[0] != arrAzi.shape[0]:
        raise ValueError(
            "plotBeamPattern3D:arrData.shape[0] %d doesnt fit arrAzi %d"
            % (arrData.shape[0], arrAzi.shape[0])
        )
    if arrPos.shape[1] != arrData.shape[-1]:
        raise ValueError(
            "plotBeamPattern3D:Number of pos %d doesnt match data dim %d"
            % (arrPos.shape[1], arrData.shape[-1])
        )

    if fun is None:
        fun = __defaultFun

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection="3d")

    for ii in range(arrData.shape[-1]):
        # we just take the real part
        arrR = fun(arrData[..., ii])

        # transform everything into cartesian coordinates
        # obey the array element positions
        arrX = arrR * np.sin(arrCoEle) * np.sin(arrAzi) + arrPos[0, ii]
        arrY = arrR * np.sin(arrCoEle) * np.cos(arrAzi) + arrPos[1, ii]
        arrZ = arrR * np.cos(arrCoEle) + arrPos[2, ii]

        ax.plot_surface(
            (arrX).reshape((numCoEle, numAzi)),
            (arrY).reshape((numCoEle, numAzi)),
            (arrZ).reshape((numCoEle, numAzi)),
            rstride=2,
            cstride=2,
            linewidth=0,
            antialiased=True,
            alpha=1,
        )
    plt.show()


def plotCut2D(
    arrData: np.ndarray, arrAzi: np.ndarray, arrPos: np.ndarray, fun=None
) -> None:
    """Plot the beam Pattern for a fixed Co-Elevation

    Parameters
    ----------
    arrData : np.ndarray
        Input Data in Angle x Elem
    arrAzi : np.ndarray
        Azimuth Angles we sampled at in radians
    arrPos : np.ndarray
        Positions of the array elements
    fun : method
        function to apply to the elements values
    """
    if arrData.shape[0] != arrAzi.shape[0]:
        raise ValueError(
            "plotCut2D:arrData.shape[0] %d does not fit arrAzi size %d"
            % (arrData.shape[0], arrAzi.shape[0])
        )
    if arrPos.shape[1] != arrData.shape[-1]:
        raise ValueError(
            "plotCut2D:Number of pos %d does not match data dimension %d"
            % (arrPos.shape[1], arrData.shape[-1])
        )

    if fun is None:
        fun = __defaultFun

    # iterate through the elements for one fixed polarization (the 0)
    for jj in range(arrData.shape[-1]):
        arrR = fun(arrData[:, 0, jj])
        arrXPos = arrPos[0, jj] + np.cos(arrAzi) * arrR
        arrYPos = arrPos[1, jj] + np.sin(arrAzi) * arrR
        plt.plot(arrXPos, arrYPos)
        plt.scatter(arrPos[0, jj], arrPos[1, jj])

    plt.show()
