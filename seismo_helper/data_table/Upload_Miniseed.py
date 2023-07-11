import obspy
import numpy as np


def upload_miniseed(path):
    file = obspy.read(path)
    pass