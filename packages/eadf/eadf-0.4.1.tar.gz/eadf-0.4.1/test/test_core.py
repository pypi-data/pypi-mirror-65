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


import unittest
import numpy as np
from eadf.core import fourierToSampled, sampledToFourier, symmetrizeData
from eadf.core import _inversePatternTransformNarrowBand
from eadf.core import _inversePatternTransformNarrowBandLowMem
from eadf.core import _inversePatternTransform
from eadf.core import _inversePatternTransformLowMem
from eadf.core import calcBlockSizeNarrowBand
from eadf.core import calcBlockSize
from eadf.core import regularSamplingToGrid
from eadf.backend import xp

from . import TestCase


class TestFourierToSampled(TestCase):
    def setUp(self):
        self.data = np.random.randn(14, 28, 2, 2, 5) + 1j

    def test_success2D(self):
        fourierToSampled(self.data, (0, 1))

    def test_success3D(self):
        fourierToSampled(self.data, (0, 1, 2))

    def test_shapeFail1(self):
        with self.assertRaisesWithMessage(
            ValueError,
            "fourierToSampled: arrData has wrong number of dimensions",
        ):
            fourierToSampled(self.data[0], (0, 1, 2))

    def test_shapeFail2(self):
        with self.assertRaisesWithMessage(
            ValueError,
            "fourierToSampled: There must be at most 2 polarisations",
        ):
            fourierToSampled(np.random.randn(14, 28, 2, 3, 5) + 1j, (0, 1, 2))


class TestSampledToFourier(TestCase):
    def setUp(self):
        self.data = np.random.randn(14, 28, 2, 2, 5) + 1j

    def test_success2D(self):
        sampledToFourier(self.data, (0, 1))

    def test_success3D(self):
        sampledToFourier(self.data, (0, 1, 2))

    def test_shapeFail1(self):
        with self.assertRaisesWithMessage(
            ValueError,
            "sampledToFourier: 1st dim of arrData must have even size.",
        ):
            sampledToFourier(self.data[:3], (0, 1, 2))

    def test_shapeFail2(self):
        with self.assertRaisesWithMessage(
            ValueError,
            "sampledToFourier: arrData has wrong number of dimensions",
        ):
            sampledToFourier(self.data[0], (0, 1, 2))

    def test_shapeFail3(self):
        with self.assertRaisesWithMessage(
            ValueError,
            "sampledToFourier: There must be at most 2 polarisations",
        ):
            sampledToFourier(np.random.randn(14, 28, 2, 3, 5) + 1j, (0, 1, 2))


class TestBlockSizeCalculation(TestCase):
    def test_success(self):
        calcBlockSize(
            xp.random.randn(5),
            xp.random.randn(6),
            xp.random.randn(7),
            xp.random.randn(5, 6, 7, 2, 5) + 1j,
        )


class TestBlockSizeNarrowBandCalculation(TestCase):
    def test_success(self):
        calcBlockSizeNarrowBand(
            xp.random.randn(5),
            xp.random.randn(6),
            xp.random.randn(5, 6, 2, 5) + 1j,
        )


class TestPatternTransform(TestCase):
    def test_inversePatternTransformNarrowBand_success(self):
        _inversePatternTransformNarrowBand(
            xp.random.randn(6, 20) + 1j,
            xp.random.randn(5, 20) + 1j,
            xp.random.randn(6, 5, 2, 5) + 1j,
            7,
        )

    def test_inversePatternTransform_success(self):
        _inversePatternTransform(
            xp.random.randn(6, 20) + 1j,
            xp.random.randn(5, 20) + 1j,
            xp.random.randn(7, 20) + 1j,
            xp.random.randn(6, 5, 7, 2, 5) + 1j,
            7,
        )

    def test_inversePatternTransformNarrowBandLowMem_success(self):
        def funCoEle(arrcoEle):
            return 1j * xp.outer(xp.random.randn(6), arrcoEle)

        def funAzi(arrAzi):
            return 1j * xp.outer(xp.random.randn(5), arrAzi)

        _inversePatternTransformNarrowBandLowMem(
            xp.random.randn(20) + 1j,
            xp.random.randn(20) + 1j,
            funCoEle,
            funAzi,
            xp.random.randn(6, 5, 2, 5) + 1j,
            7,
        )

    def test_inversePatternTransformLowMem_success(self):
        def funCoEle(arrCoEle):
            return 1j * xp.outer(xp.random.randn(6), arrCoEle)

        def funAzi(arrAzi):
            return 1j * xp.outer(xp.random.randn(5), arrAzi)

        def funFreq(arrFreq):
            return 1j * xp.outer(xp.random.randn(7), arrFreq)

        _inversePatternTransformLowMem(
            xp.random.randn(20) + 1j,
            xp.random.randn(20) + 1j,
            xp.random.randn(20) + 1j,
            funCoEle,
            funAzi,
            funFreq,
            xp.random.randn(6, 5, 7, 2, 5) + 1j,
            7,
        )


class TestSymmetrizeData(TestCase):
    def setUp(self):
        self.data = np.random.randn(14, 28, 2, 3, 5)

    def test_success(self):
        symmetrizeData(self.data)

    def test_shapeFail(self):
        with self.assertRaisesWithMessage(
            ValueError, "symmetrizeData: got %d dimensions instead of 5" % (4)
        ):
            symmetrizeData(self.data[0])


class TestRegularSamplingToGrid(TestCase):
    def setUp(self):
        self.data = np.random.randn(14 * 13, 2, 3, 5)

    def test_success(self):
        regularSamplingToGrid(self.data, 13, 14)

    def test_shapeFail1(self):
        with self.assertRaisesWithMessage(
            ValueError,
            (
                "regularSamplingToGrid:"
                + "Input arrA has %d dimensions instead of 4"
            )
            % (len(self.data[:, :, :, 0].shape)),
        ):
            regularSamplingToGrid(self.data[:, :, :, 0], 13, 14)

    def test_shapeFail2(self):
        with self.assertRaisesWithMessage(
            ValueError,
            (
                "regularSamplingToGrid:"
                + "numCoEle %d, numAzi %d and arrA.shape[0] %d dont match"
            )
            % (14, 13, self.data[:13].shape[0]),
        ):
            regularSamplingToGrid(self.data[:13], 13, 14)


if __name__ == "__main__":
    unittest.main()
