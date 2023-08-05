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

import numpy as np
import unittest
from unittest.mock import patch

from eadf.eadf import EADF
from eadf.auxiliary import toGrid
from eadf.auxiliary import sampleAngles
from eadf.arrays import generateUniformArbitrary

from . import TestCase


class TestInit(TestCase):
    def setUp(self):
        self.array = generateUniformArbitrary(np.random.randn(3, 11))

        self.data = self.array.patternNarrowBand(
            *toGrid(self.array.arrCoEle, self.array.arrAzi),
            self.array.arrFreq[0]
        ).reshape(
            (
                self.array.arrCoEle.shape[0],
                self.array.arrAzi.shape[0],
                1,
                1,
                11,
            )
        )

    def test_arrAziShape(self):
        with self.assertRaisesWithMessage(
            ValueError,
            "EADF:arrAzi.shape%s != expected shape%s"
            % ((self.array.arrAzi.shape[0],), (self.data.shape[1] - 1,)),
        ):
            EADF(
                self.data[:, :-1],
                self.array.arrCoEle,
                self.array.arrAzi,
                self.array.arrFreq,
                self.array.arrPos,
            )

    def test_arrCoEleShape(self):
        with self.assertRaisesWithMessage(
            ValueError,
            "EADF:arrCoEle.shape%s != expected shape%s"
            % ((self.array.arrCoEle.shape[0],), (self.data.shape[0] - 1,)),
        ):
            EADF(
                self.data[:-1],
                self.array.arrCoEle,
                self.array.arrAzi,
                self.array.arrFreq,
                self.array.arrPos,
            )

    def test_arrFreqShape(self):
        with self.assertRaisesWithMessage(
            ValueError,
            "EADF:arrFreq.shape%s != expected shape%s"
            % ((2,), (self.data.shape[2],)),
        ):
            EADF(
                self.data,
                self.array.arrCoEle,
                self.array.arrAzi,
                np.linspace(1, 2, 2),
                self.array.arrPos,
            )

    def test_arrPos1Shape(self):
        with self.assertRaisesWithMessage(
            ValueError,
            "EADF:arrPos.shape%s != expected shape%s"
            % (
                (self.array.arrPos.shape[0] - 1, self.array.arrPos.shape[1]),
                self.array.arrPos.shape,
            ),
        ):
            EADF(
                self.data,
                self.array.arrCoEle,
                self.array.arrAzi,
                self.array.arrFreq,
                self.array.arrPos[:-1],
            )

    def test_arrPos2Shape(self):
        with self.assertRaisesWithMessage(
            ValueError,
            "EADF:arrPos.shape%s != expected shape%s"
            % (
                (self.array.arrPos.shape[0], self.array.arrPos.shape[1] - 1),
                self.array.arrPos.shape,
            ),
        ):
            EADF(
                self.data,
                self.array.arrCoEle,
                self.array.arrAzi,
                self.array.arrFreq,
                self.array.arrPos[:, :-1],
            )


class TestProperties(TestCase):
    def setUp(self):
        self.array = generateUniformArbitrary(np.random.randn(3, 11))

    def test_arrComFactSuccess(self):
        self.array.compressionFactor = 0.9
        self.assertTrue(self.array.compressionFactor > 0.9)

    def test_arrComFact1(self):
        with self.assertRaisesWithMessage(
            ValueError, "Supplied Value must be in (0, 1]"
        ):
            self.array.compressionFactor = 1.1

    def test_arrComFact2(self):
        with self.assertRaisesWithMessage(
            ValueError, "Supplied Value must be in (0, 1]"
        ):
            self.array.compressionFactor = -1.1

    def test_arrDType(self):
        with self.assertRaisesWithMessage(
            ValueError, "dtype: datatype not implemented."
        ):
            self.array.dtype = "floaty"

    def test_dtypeFloat(self):
        self.array.dtype = "float"
        self.assertTrue(self.array._complexDtype == "complex64")
        self.assertTrue(self.array._realDtype == "float32")
        self.assertTrue(self.array._dtype == "float")

    def test_dtypeFloatDouble(self):
        self.array.dtype = "float"
        self.array.dtype = "double"
        self.assertTrue(self.array._complexDtype == "complex128")
        self.assertTrue(self.array._realDtype == "float64")
        self.assertTrue(self.array._dtype == "double")

    def test_arrDTypeFail(self):
        with self.assertRaisesWithMessage(
            ValueError, "dtype: datatype not implemented."
        ):
            self.array.dtype = "floaty"


class TestPatternNarrowBand(TestCase):
    def setUp(self):
        self.array = generateUniformArbitrary(np.random.randn(3, 11))
        self.arrCoEle, self.arrAzi = toGrid(*sampleAngles(5, 10))

    def test_success_pattern(self):
        self.array.patternNarrowBand(
            self.arrCoEle, self.arrAzi, self.array.arrFreq[0]
        )

    def test_success_gradient(self):
        self.array.gradientNarrowBand(
            self.arrCoEle, self.arrAzi, self.array.arrFreq[0]
        )

    def test_success_hessian(self):
        self.array.hessianNarrowBand(
            self.arrCoEle, self.arrAzi, self.array.arrFreq[0]
        )

    def test_inputSizeFail(self):
        with self.assertRaisesWithMessage(
            ValueError,
            "patternNarrowBand: supplied angle arrays have size %d and %d."
            % (self.arrCoEle[:-1].shape[0], self.arrAzi.shape[0]),
        ):
            self.array.patternNarrowBand(
                self.arrCoEle[:-1], self.arrAzi, self.array.arrFreq[0]
            )

    def test_freqFail(self):
        with self.assertRaisesWithMessage(
            ValueError,
            "Desired freq %s does not match sampled one %s"
            % (str(2 * self.array._arrFreq[0]), str(self.array._arrFreq[0])),
        ):
            self.array.patternNarrowBand(
                self.arrCoEle, self.arrAzi, 2 * self.array.arrFreq[0]
            )


class TestSerialization(unittest.TestCase):
    def setUp(self):
        self.array = generateUniformArbitrary(np.random.randn(3, 11))

    def test_save_success(self):
        self.array.save("test.dat")

    def test_load_success(self):
        self.array.save("test.dat")
        arrayLoad = EADF.load("test.dat")

    @patch("logging.warning")
    def test_load_version_warn(self, mock):
        self.array._version += "bla"
        self.array.save("test.dat")
        arrayLoad = EADF.load("test.dat")
        mock.assert_called_with(
            "eadf.load: loaded object does not match current version."
        )


if __name__ == "__main__":
    unittest.main()
