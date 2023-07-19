import numpy as np
from math import sqrt, log10

"""station_coords - двухмерный массив координат станций (x, y, z)
event_coord - координаты события (x, y, z)
traces - трехмерный массив сейсмотрасс события в соответствии со станциями - три канала на станцию"""


class Magnitude:

    def __init__(self, station_coords: np.ndarray, event_coord: list, traces: np.ndarray):
        self.station_coords = station_coords
        self.event_coord = event_coord
        self.traces = traces

    def distance_calc(self) -> list:
        station_coords = self.station_coords
        event_coord = self.event_coord
        distances = []
        for i in range(station_coords.shape[0]):
            distances.append(sqrt((station_coords[i][0]-event_coord[0])**2+(station_coords[i][1]-event_coord[1])**2+(station_coords[i][2]-event_coord[2])**2))
        return distances #список расстояний от станций до события

    def amplitude_calc(self) -> float:
        traces = self.traces
        distances = self.distance_calc()
        amplitudes = []
        for i in range(len(distances)):
            amplitude = traces[i].max()
            amplitudes.append(amplitude*distances[i])
        original_amplitude = sum(amplitudes) / len(amplitudes)
        return original_amplitude #амплитуда события

    def magnitude_calc(self) -> float:
        magnitude = log10(self.amplitude_calc())
        return magnitude

