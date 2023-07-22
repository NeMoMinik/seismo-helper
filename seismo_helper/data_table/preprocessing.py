from scipy import signal


class Preprocessing:
    def __init__(self, data, lowcut, highcut, fs, order=5):
        """data - переменная содержащаая инфу
        \nlowcut - низ для вырезки 5
        \nhighcut - верх для вырезки 50
        \nfs - длина волны (частота) 200
        \norder - порядок default = 5"""
        self.data = data
        self.lowcut = lowcut
        self.highcut = highcut
        self.fs = fs
        self.order = order

    def callc(self):
        bandpassed_data = self.butter_bandpass_filter(self.data, self.lowcut, self.highcut, self.fs, self.order)
        detrended_data = self.detrend(bandpassed_data)
        return detrended_data

    @staticmethod
    def butter_bandpass(lowcut, highcut, fs, order):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        b, a = signal.butter(order, [low, high], btype='band')
        return b, a

    def butter_bandpass_filter(self, data, lowcut, highcut, fs, order):
        b, a = self.butter_bandpass(lowcut, highcut, fs, order)
        y = signal.filtfilt(b, a, data)
        return y

    @staticmethod
    def detrend(data):
        return signal.detrend(data)
