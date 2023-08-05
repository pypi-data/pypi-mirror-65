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
from unittest.mock import patch
from eadf.importers import fromAngleListData
from eadf.arrays import generateUCA
from eadf.arrays import generateStackedUCA
from eadf.auxiliary import sampleAngles, toGrid
import numpy as np

from . import TestCase


class TestFromAngleListData(TestCase):
    def setUp(self):
        self.array = generateUCA(13, 1.2)
        self.arrCoEleS, self.arrAziS = toGrid(*sampleAngles(20, 40))
        self.arrCoEleI, self.arrAziI = toGrid(*sampleAngles(30, 60))

        # we need the frequency dimension
        self.dataS = self.array.patternNarrowBand(
            self.arrCoEleS, self.arrAziS, self.array.arrFreq[0]
        )[:, np.newaxis, :]

    def test_inputSizeFail1(self):
        with self.assertRaisesWithMessage(
            ValueError,
            (
                "fromAngleListData: Input arrays"
                + " of sizes %d ele, %d azi, %d values dont match"
            )
            % (
                self.arrCoEleS.shape[0],
                self.arrAziS[:-1].shape[0],
                self.dataS.shape[0],
            ),
        ):
            fromAngleListData(
                self.arrCoEleS,
                self.arrAziS[:-1],
                self.dataS,
                self.array.arrFreq,
                self.array.arrPos,
                30,
                60,
            )

    def test_inputSizeFail2(self):
        with self.assertRaisesWithMessage(
            ValueError,
            (
                "fromAngleListData: Input arrays"
                + " of sizes %d ele, %d azi, %d values dont match"
            )
            % (
                self.arrCoEleS[:-1].shape[0],
                self.arrAziS[:-1].shape[0],
                self.dataS.shape[0],
            ),
        ):
            fromAngleListData(
                self.arrCoEleS[:-1],
                self.arrAziS[:-1],
                self.dataS,
                self.array.arrFreq,
                self.array.arrPos,
                30,
                60,
            )

    def test_inputSizeFail3(self):
        with self.assertRaisesWithMessage(
            ValueError,
            (
                "fromAngleListData:"
                + "Number of positions %d does not match provided data %d"
            )
            % (self.array.arrPos.shape[1] - 1, self.dataS.shape[3]),
        ):
            fromAngleListData(
                self.arrCoEleS,
                self.arrAziS,
                self.dataS,
                self.array.arrFreq,
                self.array.arrPos[:, :-1],
                30,
                60,
            )

    def test_inputSizeFail4(self):
        with self.assertRaisesWithMessage(
            ValueError,
            (
                "fromAngleListData:"
                + "Number of freqs %d does not match provided data %d"
            )
            % (self.array.arrFreq.shape[0] - 1, self.dataS.shape[1]),
        ):
            fromAngleListData(
                self.arrCoEleS,
                self.arrAziS,
                self.dataS,
                self.array.arrFreq[:-1],
                self.array.arrPos,
                30,
                60,
            )

    def test_inputSizeFail5(self):
        with self.assertRaisesWithMessage(
            ValueError, "fromAngleListData: numAzi must be larger than 0."
        ):
            fromAngleListData(
                self.arrCoEleS,
                self.arrAziS,
                self.dataS,
                self.array.arrFreq,
                self.array.arrPos,
                30,
                -60,
            )

    def test_inputSizeFail6(self):
        with self.assertRaisesWithMessage(
            ValueError, "fromAngleListData: numCoEle must be larger than 0."
        ):
            fromAngleListData(
                self.arrCoEleS,
                self.arrAziS,
                self.dataS,
                self.array.arrFreq,
                self.array.arrPos,
                -30,
                60,
            )

    def test_hfss_import(self):
        with self.assertRaisesWithMessage(
            ValueError, "fromAngleListData: numCoEle must be larger than 0."
        ):
            fromAngleListData(
                self.arrCoEleS,
                self.arrAziS,
                self.dataS,
                self.array.arrFreq,
                self.array.arrPos,
                -30,
                60,
            )


if __name__ == "__main__":
    unittest.main()
