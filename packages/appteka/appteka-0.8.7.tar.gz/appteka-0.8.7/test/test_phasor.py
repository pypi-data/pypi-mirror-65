import os
import sys

from PyQt5 import QtCore

sys.path.insert(0, os.path.abspath("."))
from appteka.pyqt import testing
from appteka.pyqtgraph import phasor


class TestPhasor(testing.TestDialog):
    def test_just_visible(self):
        self.set_widget(phasor.PhasorDiagram())
        self.add_assertion("Widget seems to be OK")

    def test_radius_labels(self):
        d = phasor.PhasorDiagram()
        self.set_widget(d)
        self.add_assertion("Widget seems to be OK")

    def test_range_is_two(self):
        d = phasor.PhasorDiagram()
        self.set_widget(d)
        d.set_range(2)
        self.add_assertion("Grid is OK")
        self.add_assertion("The max circle in grid has radius of 2")

    def test_change_range(self):
        d = phasor.PhasorDiagram()
        self.set_widget(d)
        d.set_range(2)
        d.set_range(4)
        self.add_assertion("Grid is OK")
        self.add_assertion("The max circle in grid has radius of 4")

    def test_add_phasor(self):
        d = phasor.PhasorDiagram()
        self.set_widget(d)
        d.set_range(100)
        d.add_phasor('ph-1', 80, 1)
        self.add_assertion("There is a phasor in first quadrant")
        self.add_assertion("The color of phasor is white")

    def test_update_phasor(self):
        d = phasor.PhasorDiagram()
        self.set_widget(d)
        d.set_range(100)
        d.add_phasor('ph-1', 80, 1)
        d.update_phasor('ph-1', 80, 2)
        self.add_assertion("There is a phasor in second quadrant")
        self.add_assertion("Phasor in single")

    def test_phasor_color(self):
        d = phasor.PhasorDiagram()
        self.set_widget(d)
        d.set_range(100)
        d.add_phasor('ph-1', 80, 1, (255, 0, 0))
        self.add_assertion("There is a red phasor in first quadrant")

    def test_three_phasors(self):
        d = phasor.PhasorDiagram()
        self.set_widget(d)
        d.set_range(100)
        d.add_phasor('ph-1', 80, 0, (255, 0, 0))
        d.add_phasor('ph-2', 80, 2 * 3.1415 / 3, (0, 255, 0))
        d.add_phasor('ph-3', 80, -2 * 3.1415 / 3, (0, 0, 255))

        self.add_assertion("There are 3 phasors: red, green and blue")
        self.add_assertion("About 120 degrees between every two phasors")

    def test_three_phasors_rotated(self):
        d = phasor.PhasorDiagram()
        self.set_widget(d)
        d.set_range(100)
        d.add_phasor('ph-1', 80, 0, (255, 0, 0))
        d.add_phasor('ph-2', 80, 2 * 3.1415 / 3, (0, 255, 0))
        d.add_phasor('ph-3', 80, -2 * 3.1415 / 3, (0, 0, 255))
        d.update_phasor('ph-1', 80, 1)
        d.update_phasor('ph-2', 80, 1 + 2 * 3.1415 / 3)
        d.update_phasor('ph-3', 80, 1 - 2 * 3.1415 / 3)

        self.add_assertion("There are 3 phasors: red, green and blue")
        self.add_assertion("About 120 degrees between every two phasors")
        self.add_assertion("Red phasor has angle about 1 radian")

    def test_range_to_phasor(self):
        d = phasor.PhasorDiagram()
        self.set_widget(d)
        d.add_phasor('ph-1', color=(255, 255, 0))
        d.update_phasor('ph-1', 1, 1)
        d.update_phasor('ph-1', 100, 1)
        d.set_range(100)
        self.add_assertion("Grid corresponds to phasor")

    def test_legend(self):
        d = phasor.PhasorDiagram()
        self.set_widget(d)
        d.add_phasor('ph-1', 80, 0, (255, 0, 0))
        d.add_phasor('ph-2', 80, 2 * 3.1415 / 3, (0, 255, 0))
        d.add_phasor('ph-3', 80, -2 * 3.1415 / 3, (0, 0, 255))
        d.show_legend()
        d.set_range(80)
        self.add_assertion("Legend is correct")

    def test_three_phasors_animation(self):
        d = phasor.PhasorDiagram()
        self.set_widget(d)
        d.add_phasor('ph-1', color=(255, 0, 0))
        d.add_phasor('ph-2', color=(0, 255, 0))
        d.add_phasor('ph-3', color=(0, 0, 255))
        d.show_legend()

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(10)

        self.step = 0

        def rotate():
            a = 2 * 3.1415 / 3
            sh = self.step / 200
            ash = self.step / 10
            d.update_phasor('ph-1', ash + 10, sh)
            d.update_phasor('ph-2', 10, sh + a)
            d.update_phasor('ph-3', 10, sh - a)
            d.set_range(ash + 10)

            self.step += 1
            if self.step > 100:
                self.timer.stop()
                self.enable_buttons()

        self.timer.timeout.connect(rotate)
        self.timer.start()
        self.disable_buttons()

        self.add_assertion("Phasors smoothly rotating")
        self.add_assertion("Amplitude of red phasor grows")

    def test_width_of_phasors(self):
        # Given phasor diagram
        d = phasor.PhasorDiagram()
        self.set_widget(d)

        # When add two phasors
        # And widths of phasors are set to be significantly differ
        d.add_phasor('ph-1', color=(255, 255, 255), width=1)
        d.add_phasor('ph-2', color=(255, 255, 255), width=4)
        d.update_phasor('ph-1', 100, 1)
        d.update_phasor('ph-2', 100, 2)
        d.set_range(100)

        # Then widths of phasors are differ
        self.add_assertion("widths of phasors are differ")


testing.run(TestPhasor)
