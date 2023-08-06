import unittest
from ttlab.frames import Frames
import numpy as np


class FrameAnalyserTestCases(unittest.TestCase):
    class DataExampleWithTime:
        filename = 'tests/mock_data/frame_analyser_example_with_time.txt'
        info = {
            'x pixels': 30,
            'y pixels': 2160,
            'exposure time': 0.020003,
            'number of accumulations': 10,
            'vertical binning': 1,
            'horisontal binning': 1,
            'pixel readout rate': '280 MHz',
            'overlap readout': True,
            'spurious noise filter': True,
            'cycle mode': 'Continuous',
            'trigger mode': 'Internal',
            'simple pre amp gain control': '16-bit (low noise & high well capacity)',
            'pixel encoding': 'Mono32',
            'fan speed': 'Off',
            'electronic shuttering mode': 'Rolling',
            'fast AOI frame rate enabled': True,
            'frame rate': None
        }
        frames = np.array([
            [[1, 0], [0, 0]],
            [[0, 1], [0, 0]],
            [[0, 0], [1, 0]],
            [[0, 0], [0, 1]]
        ], dtype=np.int64)
        times = np.array([0.0, 0.1, 0.2, 0.3], dtype=np.float64)

    class DataExampleWithoutTime:
        filename = 'tests/mock_data/frame_analyser_example_without_time.txt'
        info = {
            'x pixels': 30,
            'y pixels': 2160,
            'exposure time': 0.020003,
            'number of accumulations': 10,
            'vertical binning': 1,
            'horisontal binning': 1,
            'pixel readout rate': '280 MHz',
            'overlap readout': True,
            'spurious noise filter': True,
            'cycle mode': 'Continuous',
            'trigger mode': 'Internal',
            'simple pre amp gain control': '16-bit (low noise & high well capacity)',
            'pixel encoding': 'Mono32',
            'fan speed': 'Off',
            'electronic shuttering mode': 'Rolling',
            'fast AOI frame rate enabled': True,
            'frame rate': 250.0
        }
        frames = np.array([
            [[1, 0], [0, 0], [0, 0]],
            [[0, 1], [0, 0], [0, 0]],
            [[0, 0], [1, 0], [0, 0]],
            [[0, 0], [0, 1], [0, 0]],
            [[0, 0], [0, 0], [1, 0]],
            [[0, 0], [0, 0], [0, 1]]
        ], dtype=np.int64)

        frames_flipped_dimension = np.array([
            [[1, 0, 0], [0, 0, 0]],
            [[0, 1, 0], [0, 0, 0]],
            [[0, 0, 1], [0, 0, 0]],
            [[0, 0, 0], [1, 0, 0]],
            [[0, 0, 0], [0, 1, 0]],
            [[0, 0, 0], [0, 0, 1]]
        ], dtype=np.int64)

        times = np.array([0, 0.004, 0.008, 0.012, 0.016, 0.020], dtype=np.float64)

    def test_read_data_with_time(self):
        frame_analyser = Frames(filename=self.DataExampleWithTime.filename)
        self.assertEqual(frame_analyser.measurement_info.keys(), self.DataExampleWithTime.info.keys())
        np.testing.assert_array_equal(self.DataExampleWithTime.frames, frame_analyser.frames)
        np.testing.assert_array_equal(self.DataExampleWithTime.times, frame_analyser.time)

    def test_read_data_without_time(self):
        frame_analyser = Frames(filename=self.DataExampleWithoutTime.filename)
        self.assertEqual(frame_analyser.measurement_info.keys(), self.DataExampleWithoutTime.info.keys())
        np.testing.assert_array_equal(self.DataExampleWithoutTime.frames, frame_analyser.frames)
        np.testing.assert_array_equal(self.DataExampleWithoutTime.times, frame_analyser.time)

    def test_read_data_flip_dimensions(self):
        frame_analyser = Frames(filename=self.DataExampleWithoutTime.filename, flip_dimensions=True)
        np.testing.assert_array_equal(self.DataExampleWithoutTime.frames_flipped_dimension, frame_analyser.frames)

