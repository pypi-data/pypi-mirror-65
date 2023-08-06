import scipy.io
import numpy as np


class FileReader:

    @staticmethod
    def read_data_from_file(file_path):
        matlab_data = scipy.io.loadmat(file_path)['data']
        data = {
            'frames': np.rollaxis(matlab_data['I'][0][0], 2, 0),
            'time': matlab_data['time'][0][0][0]
        }
        measurement_info = {
            'x pixels': matlab_data['imageWidth'][0][0][0][0],
            'y pixels': matlab_data['imageHeight'][0][0][0][0],
            'exposure time': matlab_data['exposureTime'][0][0][0][0],
            'number of accumulations': matlab_data['numberOfAccumulations'][0][0][0][0],
            'vertical binning': matlab_data['Ybinning'][0][0][0][0],
            'horisontal binning': matlab_data['Xbinning'][0][0][0][0],
            'frame rate': matlab_data['frameRate'][0][0][0][0],
            'image left position': matlab_data['imageLeftPosition'][0][0][0][0],
            'image top position': matlab_data['imageTopPosition'][0][0][0][0],
            'pixel size': matlab_data['pixel_size'][0][0][0][0],
            'magnification': matlab_data['magnification'][0][0][0][0]
        }
        return data, measurement_info

    def read_data_from_gridfs(gridfs):
        filename = gridfs.filename
        matlab_data = scipy.io.loadmat(gridfs)['data']
        data = {
            'frames': np.rollaxis(matlab_data['I'][0][0], 2, 0),
            'time': matlab_data['time'][0][0][0]
        }
        measurement_info = {
            'x pixels': matlab_data['imageWidth'][0][0][0][0],
            'y pixels': matlab_data['imageHeight'][0][0][0][0],
            'exposure time': matlab_data['exposureTime'][0][0][0][0],
            'number of accumulations': matlab_data['numberOfAccumulations'][0][0][0][0],
            'vertical binning': matlab_data['Ybinning'][0][0][0][0],
            'horisontal binning': matlab_data['Xbinning'][0][0][0][0],
            'frame rate': matlab_data['frameRate'][0][0][0][0],
            'image left position': matlab_data['imageLeftPosition'][0][0][0][0],
            'image top position': matlab_data['imageTopPosition'][0][0][0][0],
            'pixel size': matlab_data['pixel_size'][0][0][0][0],
            'magnification': matlab_data['magnification'][0][0][0][0]
        }
        return data, measurement_info, filename
