import numpy as np

class Data:
    def __init__(self):
        self.wavelength = None
        self.intensity = []
        self.time = []
        self.absTime = []
        self.dark_ref = None
        self.bright_ref = None

class InsplorionFileReader:
    data_template = {
        'wavelength': None,
        'intensity': [],
        'time': [],
        'absTime':[],
        'dark ref': None,
        'bright ref': None
    }

    @staticmethod
    def read_data_from_file(filename_ins, debug):
        data = Data()
        #data = InsplorionFileReader.data_template.copy()
        with open(filename_ins) as insplorion_ins_file:
            for line_nr, line in enumerate(insplorion_ins_file):
                if line_nr == 2:
                    data.wavelength = InsplorionFileReader._read_wavelengths(line)
                elif line_nr == 4:
                    data.dark_ref = InsplorionFileReader._read_reference_intensity(line)
                elif line_nr == 6:
                    data.bright_ref = InsplorionFileReader._read_reference_intensity(line)
                elif line_nr > 7:
                    if debug is True:
                        print(line_nr, line)
                    time, intensity = InsplorionFileReader._read_time_and_intensity(line)
                    data.intensity.append(intensity - data.bright_ref)
                    data.time.append(time)
        return data

    @staticmethod
    def read_corrupted_data_from_file(filename_ins):
        faulty_lines = 0
        correct_lines = 0
        data = Data()
        with open(filename_ins, 'r', errors='replace') as file:
            for count, line in enumerate(file):
                line = line.strip()

                if count == 2:
                    values = line.split('\t')
                    data.wavelength = np.array(list(map(float, values)))
                    needed_length = len(data.wavelength)

                if count == 4:
                    values = line.split('\t')
                    data.dark_ref = np.array(list(map(float, values[1:])))

                if count == 6:
                    values = line.split('\t')
                    data.bright_ref = np.array(list(map(float, values[1:])))

                if count > 7:
                    values = line.split('\t')
                    if needed_length == len(values) - 2:
                        time = float(values[1])
                        values = values[2:]
                        data.intensity.append(np.array(list(map(float, values))) - data.bright_ref)
                        data.time.append(time)
                        correct_lines = correct_lines + 1
                    else:
                        faulty_lines = faulty_lines + 1
        #                 print(count, length, len(values),'!!!!!')

        if faulty_lines > 0:
            print('Corrupted File! {:d} of {:d} time steps are missing'.format(faulty_lines, correct_lines))

        return data

    @staticmethod
    def read_data_from_gridfs(gridfs):
        data = InsplorionFileReader.data_template.copy()
        line = gridfs.readline()
        line_nr = 0
        while line is not b'':
            decoded_line = line.decode("utf-8")
            if line_nr == 2:
                data['wavelength'] = InsplorionFileReader._read_wavelengths(decoded_line)
            elif line_nr == 4:
                data['dark ref'] = InsplorionFileReader._read_reference_intensity(decoded_line)
            elif line_nr == 6:
                data['bright ref'] = InsplorionFileReader._read_reference_intensity(decoded_line)
            elif line_nr > 7:
                time, intensity = InsplorionFileReader._read_time_and_intensity(decoded_line)
                data['intensity'].append(intensity - data['bright ref'])
                data['time'].append(time)
            line = gridfs.readline()
            line_nr += 1
        return data

    @staticmethod
    def _read_reference_intensity(line_with_reference_intensity):
        values = line_with_reference_intensity.split('\t')
        intensities = InsplorionFileReader._convert_to_floats(values[1:])
        return np.array(intensities)

    @staticmethod
    def _read_time_and_intensity(line_with_intensities):
        values = line_with_intensities.split('\t')
        intensities = InsplorionFileReader._convert_to_floats(values[2:])
        time = float(values[1])
        return time, np.array(intensities)

    @staticmethod
    def _read_wavelengths(line_with_wavelengths):
        values = line_with_wavelengths.split('\t')
        wavelengths = InsplorionFileReader._convert_to_floats(values)
        return np.array(wavelengths)

    @staticmethod
    def _convert_to_floats(list_with_strings):
        return list(map(float, list_with_strings))
