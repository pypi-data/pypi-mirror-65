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
from eadf.arrays import generateUCA
from eadf.plot import *
import unittest
from unittest.mock import patch

from . import TestCase


class TestArrayPlotting(TestCase):
    def setUp(self):
        self.array = generateUCA(10, 0.5)

    @patch("matplotlib.pyplot.scatter")
    @patch("matplotlib.pyplot.show")
    def test_visualizeCut_success(self, show, scatter):
        visualizeCut(
            self.array, np.pi / 2, 40, [0], self.array.arrFreq[0], [0]
        )
        self.assertTrue(show.called)

    @patch("matplotlib.pyplot.scatter")
    @patch("matplotlib.pyplot.show")
    def test_visualize2D_success(self, show, scatter):
        visualize2D(self.array, 10, 10, [0], self.array.arrFreq[0], [0])
        self.assertTrue(show.called)

    @patch("matplotlib.pyplot.scatter")
    @patch("matplotlib.pyplot.show")
    def test_plotCut2D(self, show, scatter):
        plotCut2D(
            np.ones((20, 1, 2)),
            np.linspace(0, 2 * np.pi, 20),
            np.random.uniform(0, 1, (3, 2)),
        )
        self.assertTrue(show.called)
        self.assertTrue(scatter.called)

    def test_plotCut2DFail1(self):
        with self.assertRaisesWithMessage(
            ValueError,
            "plotCut2D:arrData.shape[0] %d does not fit arrAzi size %d"
            % (19, 20),
        ):
            plotCut2D(
                np.ones((19, 1, 2)),
                np.linspace(0, 2 * np.pi, 20),
                np.random.uniform(0, 1, (3, 2)),
            )

    def test_plotCut2DFail2(self):
        with self.assertRaisesWithMessage(
            ValueError,
            "plotCut2D:Number of pos %d does not match data dimension %d"
            % (2, 3),
        ):
            plotCut2D(
                np.ones((20, 1, 3)),
                np.linspace(0, 2 * np.pi, 20),
                np.random.uniform(0, 1, (3, 2)),
            )

    def test_plotBeamPattern3DFail1(self):
        with self.assertRaisesWithMessage(
            ValueError,
            "plotBeamPattern3D:Num of CoEle and Azi %d,%d dont fit %d, %d"
            % (4, 4, 20, 1),
        ):
            plotBeamPattern3D(
                np.ones((20, 1)),
                np.linspace(0, np.pi, 20),
                np.linspace(0, 2 * np.pi, 20),
                np.random.uniform(0, 1, (3, 1)),
                4,
                4,
            )

    def test_plotBeamPattern3DFail2(self):
        with self.assertRaisesWithMessage(
            ValueError,
            "plotBeamPattern3D:arrData.shape[0] %d doesnt fit arrAzi %d"
            % (20, 19),
        ):
            plotBeamPattern3D(
                np.ones((20, 1)),
                np.linspace(0, np.pi, 20),
                np.linspace(0, 2 * np.pi, 19),
                np.random.uniform(0, 1, (3, 1)),
                4,
                5,
            )

    def test_plotBeamPattern3DFail3(self):
        with self.assertRaisesWithMessage(
            ValueError,
            "plotBeamPattern3D:arrData.shape[0] %d doesnt fit arrCoEle %d"
            % (20, 19),
        ):
            plotBeamPattern3D(
                np.ones((20, 1)),
                np.linspace(0, np.pi, 19),
                np.linspace(0, 2 * np.pi, 20),
                np.random.uniform(0, 1, (3, 1)),
                4,
                5,
            )

    def test_plotBeamPattern3DFail4(self):
        with self.assertRaisesWithMessage(
            ValueError,
            "plotBeamPattern3D:Number of pos %d doesnt match data dim %d"
            % (2, 1),
        ):
            plotBeamPattern3D(
                np.ones((20, 1)),
                np.linspace(0, np.pi, 20),
                np.linspace(0, 2 * np.pi, 20),
                np.random.uniform(0, 1, (3, 2)),
                4,
                5,
            )

    @patch("matplotlib.pyplot.show")
    def test_plotBeamPattern3D(self, show):
        plotBeamPattern3D(
            np.ones((20, 1)),
            np.linspace(0, np.pi, 20),
            np.linspace(0, 2 * np.pi, 20),
            np.random.uniform(0, 1, (3, 1)),
            4,
            5,
        )
        self.assertTrue(show.called)

    @patch("matplotlib.pyplot.show")
    def test_plotBeamPattern2D(self, show):
        plotBeamPattern2D(
            np.ones((20, 1)),
            np.linspace(0, np.pi, 20),
            np.linspace(0, 2 * np.pi, 20),
            4,
            5,
        )
        self.assertTrue(show.called)

    def test_plotBeamPattern2DFail1(self):
        with self.assertRaisesWithMessage(
            ValueError,
            "plotBeamPattern2D:Num of CoEle and Azi %d,%d dont fit data %d,%d"
            % (4, 4, 20, 1),
        ):
            plotBeamPattern2D(
                np.ones((20, 1)),
                np.linspace(0, np.pi, 20),
                np.linspace(0, 2 * np.pi, 20),
                4,
                4,
            )
