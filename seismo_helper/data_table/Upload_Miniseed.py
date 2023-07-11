import obspy
import numpy as np
from datetime import datetime

def upload_miniseed(paths):
    Files = []
    Times = []
    for i in paths:
        tarce1 = str(obspy.read(i)[0])
        date = datetime.strptime(tarce1[tarce1.find('| ')+2:tarce1.find(' - ')-8], '%Y-%m-%dT%H:%M:%S')
        Files.append([date,i])
        Times.append(date)
    sorted_files = []
    for i in Times:
        A = []
        for j in Files:
            if j[0] == i:
                A.append(j[1])
        sorted_files.append(A)
    