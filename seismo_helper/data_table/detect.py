import json
import os
from datetime import timedelta

import numpy as np
import obspy

from data_table.preprocessing import Preprocessing


class Detect:
    """Класс для детекции активностей
Параметры
----------
path : list
    Список с путями к файлам miniseed от одного часа
seismic_traces : array
    Двумерный массив numpy размером 3xN
n_sta : int
    Количество элементов в одном интервале sta
n_lta : int
    Количество элементов в одном интервале lta
threshold : float
    Пороговое значение sta/lta, число больше которого считается активностью
    """

    def __init__(self, paths: list, location: str, n_sta: int = 500, n_lta: int = 10000, threshold: float = 5, eps: int = 1000):
        self.paths = paths
        self.location = location
        self.n_sta = n_sta
        self.n_lta = n_lta
        self.threshold = threshold
        self.eps = eps
        self.start_end_time = dict()
        self.stations = []
        self.station_name = []
        self.channel = []

    def detection(self) -> list:
        sta_lta = []
        seismic_stations= self.reading_miniseeds(self.paths)
        filtered_stations = self.using_preprocessing(seismic_stations)
        for filtered_traces in filtered_stations:
            if len(filtered_traces) != 3:
                continue
            sta_lta.append(self.calculation_sta_lta(filtered_traces))
        detect_sta_lta = self.detection_on_sta_lta(sta_lta)
        event = self.event_aggregation(detect_sta_lta)
        event_st = self.event_on_seismic_traces(event)
        event_sample = self.event_on_samples(event_st)
        event_time = self.event_on_time(event_st, seismic_stations)
        detect_event = self.detection_on_seismic_traces(event_sample, filtered_stations)
        return detect_event

    def reading_miniseeds(self, paths: list) -> list:
        """Принимает список с путями к файлам miniseed, читает их и записывает в список"""
        seismic_stations = []
        for path in paths:
            trace = []
            channel = []
            data = obspy.read(path)
            self.station_name.append(data[0].stats.station)
            for sign in data:
                trace.append(sign)
                channel = sign.stats.channel
            self.channel.append(channel)
            seismic_stations.append(trace.copy())
        return seismic_stations

    def using_preprocessing(self, seismic_stations: list) -> list:
        """Использование фильтрации"""
        filtered_station = []
        for station in seismic_stations:
            sign = []
            for canal in station:
                sign.append(Preprocessing(canal.data, 10, 30, 200, 5).callc())
            filtered_station.append(sign)
        return filtered_station

    def calculation_sta_lta(self, seismic_traces: list) -> list:
        """Вычисление sta/lta на одной станции"""
        sta_lta = np.zeros(len(seismic_traces[0]) - self.n_lta)
        m_sta, m_lta = self.n_sta // 2, self.n_lta // 2
        for seismic_trace in seismic_traces:
            if np.shape(seismic_trace) != (720000,):
                return []
            sta, lta = [], []
            lta_i = np.sum(seismic_trace[0: 2 * m_lta] ** 2)
            sta_i = np.sum(seismic_trace[0: 2 * m_sta] ** 2)
            lta.append((lta_i / self.n_lta) ** (1 / 2))
            sta.append((sta_i / self.n_sta) ** (1 / 2))
            for i in range(m_lta + 1, len(seismic_trace) - m_lta):
                lta_i = lta_i - seismic_trace[i - m_lta] ** 2 + seismic_trace[i + m_lta] ** 2
                lta.append((lta_i / self.n_lta) ** (1 / 2))
                sta_i = sta_i - seismic_trace[i - m_sta] ** 2 + seismic_trace[i + m_sta] ** 2
                sta.append((sta_i / self.n_sta) ** (1 / 2))
            sta, lta = np.nan_to_num(np.array(sta), nan=1), np.nan_to_num(np.array(lta), nan=1)
            sta_lta = sta_lta + (sta / lta)
        return sta_lta

    def detection_on_sta_lta(self, all_sta_lta: list) -> dict:
        """Детектирование событий на sta/lta со всех станций"""
        presence_of_activity = False
        detect = dict()

        for ind_station, sta_lta in enumerate(all_sta_lta):
            detect[ind_station] = []
            for detect_ind, value in enumerate(sta_lta):
                if value < self.threshold:
                    presence_of_activity = False
                if value >= self.threshold and not presence_of_activity:
                    presence_of_activity = True
                    detect[ind_station].append(detect_ind)
        return detect  # dict[index_station: index_detected]

    def event_aggregation(self, detect: dict) -> list:
        """Объединение событий и выделение среднего семпла начала"""
        detect_event = {0: {'station': [], 'value': []}}
        for station_id, values in zip(detect.keys(), detect.values()):
            for value in values:
                if np.isnan(value):
                    continue
                for event_id in detect_event.keys():
                    if not detect_event[event_id]:
                        mean_ind = value
                    else:
                        mean_ind = np.nanmean(np.array(detect_event[event_id]['value']))
                    if abs(mean_ind - value) <= self.eps and (station_id not in detect_event[event_id]['station']):
                        detect_event[event_id]['station'].append(station_id)
                        detect_event[event_id]['value'].append(value)
                        break
                else:
                    detect_event[len(detect_event.keys())] = {'station': [station_id], 'value': [value]}
        event = []
        for ev in detect_event.values():
            if len(ev['station']) >= 3:
                self.stations.append(ev['station'])  # list[list[indexes_station]]
                event.append(int(np.min(np.array(ev['value']))))
        return event  # list[mean_value_event]

    def event_on_seismic_traces(self, event: list) -> list:
        """Перевод в значения на трассе"""
        event_st = np.array(event) + self.n_lta // 2
        return event_st  # np.array[list[index_event_on_trace]]

    def event_on_samples(self, event_st: list) -> list[list[int, list, int, int]]:
        """Перевод значений появления событий в индекс на трассе"""
        start_end_sample = [[i, self.stations[i], event_st[i], event_st[i] + 1500] for i in range(len(event_st))]
        return start_end_sample  # list[list[name_event, indexes_station, start_on_samples, end_on_samples]

    def event_on_time(self, event_st: list, seismic_stations: list) -> dict:
        """Перевод значений появления событий в абсолютное время"""
        start = seismic_stations[0][0].stats.starttime
        for i in range(len(event_st)):
            detect_time = timedelta(seconds=event_st[i] * 0.005)
            step = timedelta(seconds=1500 * 0.005)
            self.start_end_time[i] = [start + detect_time,
                                      start + detect_time + step]
        return self.start_end_time  # dict[name_event:[start_on_time, end_on_time]]

    def detection_on_seismic_traces(self, start_end_sample: list[list[int, list, int, int]],
                                    seismic_traces: list) -> list:
        """Детектирование событий на сейсмотрассе"""
        detect_traces = []
        detect_trace = {}
        for ind_event, indexes_st, start, end in start_end_sample:
            for ind_st, traces in enumerate(seismic_traces):
                if ind_st in indexes_st:
                    detect_trace[self.station_name[ind_st]] = []
                    for ind_tr, trace in enumerate(traces):
                        detect_trace[self.station_name[ind_st]].append([self.channel[ind_tr], trace[start:end]])
            detect_traces.append(
                Event(
                    ind_event, self.location,
                    self.start_end_time[ind_event][0],
                    self.start_end_time[ind_event][1],
                    detect_trace,
                    self.n_sta, self.n_lta))
        return detect_traces  # list[Event.object]


class Event:
    """Класс с информацией о событии
Параметры
----------
name : int
    Название события
start_time : obspy.core.utcdatetime.UTCDateTime
    Абсолютное время начала
end_time : obspy.core.utcdatetime.UTCDateTime
    Абсолютное время конца
traces : dict
    Словарь dict[{индекс станции: обрезанная трасса по всем каналам}
    """

    def __init__(self, name: int, location: str, start_time: obspy.core.utcdatetime.UTCDateTime,
                 end_time: obspy.core.utcdatetime.UTCDateTime, traces: dict,
                 sta: int, lta: int):
        self.name = name
        self.location = location
        self.start_time = start_time
        self.end_time = end_time
        self.traces = traces
        self.sta = sta
        self.lta = lta

    def __str__(self):
        return f'Name:{self.name}, start: {self.start_time}, end: {self.end_time}'

    def save(self):
        start_time = self.start_time.strftime("%Y-%m-%d %H-%M-%S")
        end_time = self.end_time.strftime("%Y-%m-%d %H-%M-%S")
        js = {'name_event': self.name, 'start_time': start_time, 'end_time': end_time}
        path = fr"media/events/{self.location}/{start_time}/"
        paths = []  # C'est le pathes Das ist Paths This is paths Это пути Ci sono gli pathi
        if not os.path.exists(path):
            os.makedirs(path)
        for name, trace in self.traces.items():
            if not os.path.exists(f'{path}'):
                os.makedirs(f'{path}')
            names = []
            for channel in trace:
                np.save(f'{path}/{name}_{channel[0]}', channel[1])
                names.append(f'{name}_{channel[0]}.npy')
            paths.append(names)
        with open(path + f'/info.json', 'w') as outfile:
            json.dump(js, outfile)
        return path, paths
