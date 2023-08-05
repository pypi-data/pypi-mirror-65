import sys
import os

sys.path.insert(0, os.path.abspath("."))
from appteka.pyqt import testing
from appteka.pyqtgraph.waveform import Waveform


class TestWaveform(testing.TestDialog):
    """Test suite for Waveform widget."""
    def __init__(self):
        super().__init__()
        self.resize(600, 600)

    def test_xlabel(self):
        w = Waveform(self, "Time [sec]")
        self.set_widget(w)
        self.add_assertion("x label is 'Time [sec]'")

    def test_time_axis_false(self):
        w = Waveform(self, time_axis=False)
        self.set_widget(w)
        w.update_data([0, 1, 2, 3], [1, 2, 1, 2])
        self.add_assertion("x values are usual numbers from 0 to 3")

    def test_time_axis_true(self):
        w = Waveform(self, time_axis=True)
        self.set_widget(w)
        w.update_data([0, 1, 2, 3], [1, 2, 1, 2])
        self.add_assertion("x values are time values")

    def test_scaling(self):
        # Scenario: scaling with keys CONTROL and SHIFT
        w = Waveform(self)
        self.set_widget(w)
        w.update_data([0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                      [1, 2, 0, 3, 1, 2, 3, 4, 1, 3])

        self.add_assertion("both axis scaling with mouse wheel")
        self.add_assertion("x-scaling with CONTROL pressed")
        self.add_assertion("y-scaling with SHIFT pressed")


testing.run(TestWaveform)
