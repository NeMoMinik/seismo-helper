import numpy as np
from tensorflow import keras

"""trace - двухмерный массив с тремя каналами сейсмотрассы с одной станции
model_name - путь до модели Keras"""


class Peaker:
    def __init__(self, trace: np.ndarray, model_name: str):
        self.trace = trace
        self.model_name = model_name
        self.peaks = {}

    def predict(self) -> dict:
        model = keras.models.load_model(self.model_name)
        self.trace = self.trace[np.newaxis, :]
        self.trace = np.transpose(self.trace, (0, 2, 1))
        peakS = 0
        peakP = 0
        pred = model.predict(self.trace, verbose=0)
        predt = np.transpose(pred, (0, 2, 1))
        if self.model_name == 'model5.keras':
            peakS = np.where(np.isclose(predt[0][3], np.max(predt[0][3])))[0][0]
            peakP = np.where(np.isclose(predt[0][1], np.max(predt[0][1])))[0][0]
        elif self.model_name == 'model3.keras':
            peakS = np.where(np.isclose(predt[0][1], np.max(predt[0][1])))[0][0]
            peakP = np.where(np.isclose(predt[0][2], np.max(predt[0][2])))[0][0]
        self.peaks = {'Peak P': peakP, 'Peak S': peakS}
        return self.peaks
