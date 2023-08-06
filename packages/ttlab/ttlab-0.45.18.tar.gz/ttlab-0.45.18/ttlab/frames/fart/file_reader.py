from .info_reader import InfoReader
import numpy as np


class FileReader:

    def __init__(self, filename=None, gridfs=None, flip_dimensions=False):
        self._flip_dimensions = flip_dimensions
        self.time = np.empty((0,), dtype=np.float64)
        self.frames = []
        self.measurement_info = None
        self.x_pixels = None
        self.y_pixels = None
        if filename:
            self._read_data_from_file(filename)
        elif gridfs:
            self._read_data_from_gridfs(gridfs)
        if self.time[-1] == 0:
            self._calculate_times_from_frame_rate()

    def get_frame_at_time(self, time):
        index = self._find_index_of_nearest(self.time, time)
        return self.frames[index]

    @staticmethod
    def _find_index_of_nearest(array, value):
        return (np.abs(np.array(array) - value)).argmin()

    def _read_data_from_file(self, filename):
        self.measurement_info = InfoReader.read_info_from_file(filename)
        if not self._flip_dimensions:
            self.x_pixels = self.measurement_info['x pixels']
            self.y_pixels = self.measurement_info['y pixels']
        else:
            self.x_pixels = self.measurement_info['y pixels']
            self.y_pixels = self.measurement_info['x pixels']

        end_of_header_string = 'Time, Intensity:'
        is_in_header = True
        with open(filename) as file_stream:
            for line_nr, line in enumerate(file_stream):
                if is_in_header and end_of_header_string in line:
                    is_in_header = False
                elif not is_in_header:
                    self._read_time_and_intensity_in_line(line)
        self.frames = np.array(self.frames, dtype=np.int64)

    def _read_data_from_gridfs(self, gridfs):
        self.measurement_info = InfoReader.read_info_from_gridfs(gridfs)
        gridfs.seek(0)
        if not self._flip_dimensions:
            self.x_pixels = self.measurement_info['x pixels']
            self.y_pixels = self.measurement_info['y pixels']
        else:
            self.x_pixels = self.measurement_info['y pixels']
            self.y_pixels = self.measurement_info['x pixels']
        end_of_header_string = 'Time, Intensity:'
        is_in_header = True
        line_nr = 0
        line = gridfs.readline()
        while line is not b'':
            decoded_line = line.decode("utf-8")
            if is_in_header and end_of_header_string in decoded_line:
                is_in_header = False
            elif not is_in_header:
                self._read_time_and_intensity_in_line(decoded_line)
            line = gridfs.readline()
            line_nr += 1
        self.frames = np.array(self.frames, dtype=np.int64)

    def _read_time_and_intensity_in_line(self, line):
        self.time = np.append(self.time, self._extract_time_from_line(line))
        intensity = self._extract_intensity_from_line(line)
        frame = self._reshape_into_frame(intensity)
        self.frames.append(frame)

    @staticmethod
    def _extract_time_from_line(line):
        return float(line.split(',')[0])

    @staticmethod
    def _extract_intensity_from_line(line):
        intensity_string = line.split(',')[1].split(';')[:-1]
        return np.array([float(i) for i in intensity_string], dtype=np.int64)

    def _reshape_into_frame(self, intensity):
        return np.reshape(intensity, (self.x_pixels, self.y_pixels))

    def _calculate_times_from_frame_rate(self):
        time_step = 1 / self.measurement_info['frame rate']
        self.time = np.arange(0, self.frames.shape[0] * time_step, time_step)
