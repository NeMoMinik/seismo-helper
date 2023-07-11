import obspy
import numpy as np
from datetime import datetime
from data_table.detect import Detect
import requests as rq
from seismo_helper.settings import ALLOWED_HOSTS
DATABASE_API = f'http://{ALLOWED_HOSTS[0]}:8000/api/'


def upload_miniseed(paths, location):
    Files = []
    Times = []
    for i in paths:
        tarce1 = str(obspy.read(i)[0])
        date = datetime.strptime(tarce1[tarce1.find('| ')+2:tarce1.find(' - ')-8], '%Y-%m-%dT%H:%M:%S')
        Files.append([date,i])
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
        print('list_names', list_names)
        detect_obj = Detect(list_names, str(location))
        events_list = detect_obj.detection()
        if events_list:
            for event in events_list:
                event.save()
                r = rq.post(DATABASE_API+'events/', data={
                    'name': 'event',
                    'start': event.start_time,
                    'end': event.end_time,
                    'location': location
                })