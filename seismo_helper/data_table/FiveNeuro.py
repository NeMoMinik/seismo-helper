import torch
import torch.nn as nn
import numpy as np


class NeuralNetwork(nn.Module):
    def __init__(self):
        """
        Нейронная сеть из 3 сверточных слоев
        На входе 3 канала HHE, HHN, HHZ
        На выходе 5 каналов ДоP, P, МеждуPS, S, ПослеS
        """
        super(NeuralNetwork, self).__init__()

        self.conv_1 = nn.Conv1d(3, 32, kernel_size=65, padding="same")
        self.batchnorm_1 = nn.BatchNorm1d(1500)
        self.activation_1 = nn.ReLU()
        self.dropout_1 = nn.Dropout(0.10)

        self.conv_2 = nn.Conv1d(32, 64, kernel_size=65, padding="same")
        self.batchnorm_2 = nn.BatchNorm1d(1500)
        self.activation_2 = nn.ReLU()
        self.dropout_2 = nn.Dropout(0.10)

        self.conv_3 = nn.Conv1d(64, 5, kernel_size=65, padding="same")
        self.activation_3 = nn.Sigmoid()

    def forward(self, x):
        x = self.conv_1(x)
        x = self.batchnorm_1(x)
        x = self.activation_1(x)
        x = self.dropout_1(x)

        x = self.conv_2(x)
        x = self.batchnorm_2(x)
        x = self.activation_2(x)
        x = self.dropout_2(x)

        x = self.conv_3(x)
        x = self.activation_3(x)

        return x


class NeuralNetworkUse:
    def __init__(self, path: str):
        """
        Класс для использования нейронной сети
        path: путь до модели *.mdl
        """

        self.model = NeuralNetwork()
        self.model.load_state_dict(torch.load(path))

    def find_peaks(self, input_: torch.Tensor) -> tuple:
        """
        Функция поиска пиков
        input_: тензор с входными 3 каналами
        На выходе Пик P и Пик S волн
        """

        input_ = input_ / torch.max(input_) if torch.max(input_) > 1.0 else input_  # Нормализация входных данных
        output = self.model(input_).detach().numpy()

        map_to_zeros = output[0] + output[2] + output[4]  # Сложение ограничителей

        p_samples = (1 - map_to_zeros) * (output[1])  # Получение P
        s_samples = (1 - map_to_zeros) * (output[3])  # Получение S

        return np.argmax(p_samples), np.argmax(s_samples)
