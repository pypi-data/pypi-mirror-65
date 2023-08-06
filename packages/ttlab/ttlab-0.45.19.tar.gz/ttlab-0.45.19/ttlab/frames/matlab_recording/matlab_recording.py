from .file_reader import FileReader
import matplotlib.pyplot as plt
import ipywidgets as widgets
from ipywidgets import interact
import numpy as np


class MatlabRecording:

    def __init__(self, filename=None, gridfs=None):
        if filename is not None:
            self.filename = filename
            measurement_data, self.measurement_info = FileReader.read_data_from_file(filename)
            self.frames = measurement_data['frames']
            self.time = measurement_data['time']
        elif gridfs is not None:
            measurement_data, self.measurement_info, filename = FileReader.read_data_from_gridfs(gridfs)
            self.frames = measurement_data['frames']
            self.time = measurement_data['time']
            self.filename = filename

    def get_frame_at_time(self, time):
        index = self._find_index_of_nearest(self.time, time)
        return self.frames[index]

    def plot_frame_at_time(self, time, ax=None, **kwargs):
        frame = self.get_frame_at_time(time)
        self._plot_frame(frame, ax=ax, **kwargs)

    def plot_all_frames(self, ax=None, **kwargs):
        if ax is None:
            ax = plt.axes()
        interact(lambda time: self.plot_frame_at_time(ax=ax, time=time, **kwargs), time=widgets.SelectionSlider(
            options=self.time,
            value=self.time[0],
            description='Time:',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True
        ))

    @staticmethod
    def _find_index_of_nearest(array, value):
        return (np.abs(np.array(array) - value)).argmin()

    @staticmethod
    def _plot_frame(frame, ax=None, **kwargs):
        if ax is None:
            ax = plt.axes()
        return ax.imshow(frame, **kwargs)
