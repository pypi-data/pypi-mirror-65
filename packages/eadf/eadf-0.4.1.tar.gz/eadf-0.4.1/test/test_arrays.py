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

from eadf.arrays import generateURA
from eadf.arrays import generateULA
from eadf.arrays import generateUCA
from eadf.arrays import generateStackedUCA
from eadf.arrays import generateUniformArbitrary
import unittest
import numpy as np

from . import TestCase


class TestURA(TestCase):
    def setUp(self):
        self.array = generateURA(5, 6, 0.5, 0.75)

    def test_numElements(self):
        self.assertEqual(self.array.numElements, 5 * 6)

    def test_arrPosSize(self):
        self.assertEqual(self.array.arrPos.shape, (3, 5 * 6))

    def test_numElementsXFail(self):
        with self.assertRaisesWithMessage(
            ValueError, "generateULA: numElementsX <= 0 is not allowed."
        ):
            # must not be negative
            self.array = generateURA(-5, 6, 0.5, 0.5)

    def test_numSpacingXFail(self):
        with self.assertRaisesWithMessage(
            ValueError, "generateULA: numSpacingX <= 0 is not allowed."
        ):
            self.array = generateURA(5, 6, -0.5, 0.5)

    def test_numElementsYFail(self):
        with self.assertRaisesWithMessage(
            ValueError, "generateULA: numElementsY <= 0 is not allowed."
        ):
            self.array = generateURA(5, -6, 0.5, 0.5)

    def test_numSpacingYFail(self):
        with self.assertRaisesWithMessage(
            ValueError, "generateULA: numSpacingY <= 0 is not allowed."
        ):
            self.array = generateURA(5, 6, 0.5, -0.5)


class TestULA(TestCase):
    def setUp(self):
        self.array = generateULA(11, 0.5)

    def test_numElements(self):
        self.assertEqual(self.array.numElements, 11)

    def test_arrPosSize(self):
        self.assertEqual(self.array.arrPos.shape, (3, 11))

    def test_numElementsFail(self):
        with self.assertRaisesWithMessage(
            ValueError, "generateULA: numElements <= 0 is not allowed."
        ):
            self.array = generateULA(-11, 0.5)

    def test_numSpacingFail(self):
        with self.assertRaisesWithMessage(
            ValueError, "generateULA: numSpacing <= 0 is not allowed."
        ):
            self.array = generateULA(11, -0.5)


class TestUCA(TestCase):
    def setUp(self):
        self.array = generateUCA(11, 0.5)

    def test_numElements(self):
        self.assertEqual(self.array.numElements, 11)

    def test_arrPosSize(self):
        self.assertEqual(self.array.arrPos.shape, (3, 11))

    def test_numElementsFail(self):
        with self.assertRaisesWithMessage(
            ValueError, "generateUCA: numElements <= 0 is not allowed."
        ):
            self.array = generateUCA(-11, 0.5)

    def test_numRadiusFail(self):
        with self.assertRaisesWithMessage(
            ValueError, "generateUCA: numRadius <= 0 is not allowed."
        ):
            self.array = generateUCA(11, -0.5)


class TestStackedUCA(TestCase):
    def setUp(self):
        self.array = generateStackedUCA(11, 3, 0.5, 0.5)

    def test_numElements(self):
        self.assertEqual(self.array.numElements, 11 * 3)

    def test_arrPosSize(self):
        self.assertEqual(self.array.arrPos.shape, (3, 11 * 3))

    def test_numElementsFail(self):
        with self.assertRaisesWithMessage(
            ValueError, "generateStackedUCA: numElements <= 0 is not allowed."
        ):
            self.array = generateStackedUCA(-11, 3, 0.5, 0.5)

    def test_numStacksFail(self):
        with self.assertRaisesWithMessage(
            ValueError, "generateStackedUCA: numStacks <= 0 is not allowed."
        ):
            self.array = generateStackedUCA(11, -3, 0.5, 0.5)

    def test_numRadiusFail(self):
        with self.assertRaisesWithMessage(
            ValueError, "generateStackedUCA: numRadius <= 0 is not allowed."
        ):
            self.array = generateStackedUCA(11, 3, -0.5, 0.5)

    def test_numHeightFail(self):
        with self.assertRaisesWithMessage(
            ValueError, "generateStackedUCA: numHeight <= 0 is not allowed."
        ):
            self.array = generateStackedUCA(11, 3, 0.5, -0.5)


class TestUniformArbitrary(TestCase):
    def setUp(self):
        self.array = generateUniformArbitrary(np.random.randn(3, 10))

    def test_numElements(self):
        self.assertEqual(self.array.numElements, 10)

    def test_arrPosSize(self):
        self.assertEqual(self.array.arrPos.shape, (3, 10))

    def test_arrPosFail(self):
        with self.assertRaisesWithMessage(
            ValueError,
            "generateUniformArbitrary: arrPos must have exactly 3 rows",
        ):
            generateUniformArbitrary(np.random.randn(2, 10))


if __name__ == "__main__":
    unittest.main()
