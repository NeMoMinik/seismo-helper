import obspy
import numpy as np
from datetime import datetime
from data_table.detect import Detect
import requests as rq
from seismo_helper.settings import ALLOWED_HOSTS, DATABASE_API

#  Функция, обрабатывающая загруженные miniseed-файлы и вызывающая детектор


def upload_miniseed(paths, location, token):
    Files = []
    Times = []

    stations_requsted = rq.get(DATABASE_API + 'stations/', headers=token).json()['results']
    stations_dict = {}
    for station in stations_requsted:
        stations_dict[station['name']] = station['id']

    for i in paths:
        tarce = str(obspy.read(i)[0])
        if not tarce.split('.')[1] in stations_dict:
            data = {
                "name": tarce.split('.')[1],
                "x": None,
                "y": None,
                "z": None,
                "location": location,
            }
            r = rq.post(DATABASE_API + 'stations/', data=data, headers=token)
        
        date = datetime.strptime(tarce[tarce.find('| ')+2:tarce.find(' - ')-8], '%Y-%m-%dT%H:%M:%S')
        Files.append([date, i])
        Times.append(date)
    
    sorted_files = []
    Times = list(set(Times))

    for i in Times:
        A = []
        for j in Files:
            if j[0] == i:
                A.append(j[1])
        sorted_files.append(A)
    
    for list_names in sorted_files:
        detect_obj = Detect(list_names, str(location))
        events_list = detect_obj.detection()
        if events_list:
            for event in events_list:
                path, paths, stations = event.save()
                event_r = rq.post(DATABASE_API + 'events/', data={
                    'name': 'event',
                    'start': event.start_time,
                    'end': event.end_time,
                    'location': location
                },
                                  headers=token).json()

                stations_requsted = rq.get(DATABASE_API + 'stations/', headers=token).json()['results']
                stations_dict = {}
                for station in stations_requsted:
                    stations_dict[station['name']] = station['id']
                for traces_files_index in range(len(paths)):
                    r = rq.post(f'{DATABASE_API}traces/',
                                json={
                                    "path": path,
                                    "station": stations_dict[stations[traces_files_index]],  # Нужно добавить станции
                                    "channels": [{"path": paths[traces_files_index][0]},
                                                 {"path": paths[traces_files_index][1]},
                                                 {"path": paths[traces_files_index][2]}],
                                    "event": event_r['id']
                                },
                                headers=token
                    )
    print("FINISHED UPLOADING")
    return "Загружено успешно"
