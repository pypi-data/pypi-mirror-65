import unittest
from ttlab.frames import Frames
import numpy as np


class MatlabRecordingReaderTester(unittest.TestCase):
    class MatlabRecordingDataExample:
        filename = 'tests/mock_data/21-11-19_19-14-04.mat'
        info = {
            'x pixels': 3,
            'y pixels': 2,
            'exposure time': 9.239436619718310e-06,
            'number of accumulations': 30,
            'vertical binning': 1,
            'horisontal binning': 1,
            'frame rate': 6.012872628726288e+03,
            'image left position': 1066,
            'image top position': 1000,
            'pixel size': 6.5,
            'magnification': 220
        }
        time = np.array([1, 2, 3, 4], dtype=np.float32)
        frames = np.array([[[1, 3, 5],
                            [2, 4, 6]],
                           [[7, 9, 11],
                            [8, 10, 12]],
                           [[13, 15, 17],
                            [14, 16, 18]],
                           [[19, 21, 23],
                            [20, 22, 24]]],
                          )

    def test_read_info(self):
        result = Frames(filename=self.MatlabRecordingDataExample.filename, recording_software='matlab').measurement_info
        self.assertEqual(self.MatlabRecordingDataExample.info['x pixels'], result['x pixels'])
        self.assertEqual(self.MatlabRecordingDataExample.info['y pixels'], result['y pixels'])
        self.assertEqual(self.MatlabRecordingDataExample.info['exposure time'], result['exposure time'])
        self.assertEqual(self.MatlabRecordingDataExample.info['number of accumulations'], result['number of accumulations'])
        self.assertEqual(self.MatlabRecordingDataExample.info['vertical binning'], result['vertical binning'])
        self.assertEqual(self.MatlabRecordingDataExample.info['horisontal binning'], result['horisontal binning'])
        self.assertEqual(self.MatlabRecordingDataExample.info['frame rate'], result['frame rate'])
        self.assertEqual(self.MatlabRecordingDataExample.info['image left position'], result['image left position'])
        self.assertEqual(self.MatlabRecordingDataExample.info['image top position'], result['image top position'])
        self.assertEqual(self.MatlabRecordingDataExample.info['pixel size'], result['pixel size'])
        self.assertEqual(self.MatlabRecordingDataExample.info['magnification'], result['magnification'])

    def test_read_intensity_and_time(self):
        frames = Frames(filename=self.MatlabRecordingDataExample.filename, recording_software='matlab')
        result_time = frames.time
        result_frames = frames.frames
        np.testing.assert_almost_equal(result_time, self.MatlabRecordingDataExample.time)
        np.testing.assert_array_equal(result_frames, self.MatlabRecordingDataExample.frames)
