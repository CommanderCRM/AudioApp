import os
import numpy as np
from loguru import logger
from scipy.signal import hilbert
from scipy.fft import fft

# Инициализируем логгер
if os.environ.get('LOG_LEVEL') == 'DEBUG':
    LEVEL = 'DEBUG'
else:
    LEVEL = 'INFO'

class SignalEnvelopes:
    """Огибающие сигналов"""

    def absolute_envelope(self, y):
        """Огибающая по модулю значений"""
        return np.abs(y)

    def short_time_energy_envelope(self, y):
        """Огибающая по мгновенной энергии
           Используем окна"""
        logger.debug('Расчет огибающей по STE')
        logger.debug(f'Изначальное кол-во элементов в аудиоряде: {len(y)}')

        window_size = 1024
        logger.debug(f'Размер окна: {window_size}')

        step_size = int(0.5 * window_size)
        logger.debug(f'Размер шага: {step_size}')

        energy_envelope = []
        for i in range(0, len(y) - window_size + 1, step_size):
            window = y[int(i):int(i+window_size)]
            energy = np.sum(window**2) / window_size
            energy_envelope.append(energy)

        logger.debug(f'Кол-во элементов в огибающей: {len(energy_envelope)}')

        return np.array(energy_envelope)

    def hilbert_envelope(self, y):
        """Огибающая Гильберта"""
        logger.debug('Расчет огибающей Гильберта')
        logger.debug(f'Изначальное кол-во элементов в аудиоряде: {len(y)}')

        analytic_signal = hilbert(y)

        hilbert_envelope = np.abs(analytic_signal)
        logger.debug(f'Кол-во элементов в огибающей: {len(hilbert_envelope)}')

        return hilbert_envelope

    def fft_envelope(self, y):
        """Огибающая FFT"""
        logger.debug('Расчет огибающей FFT')
        logger.debug(f'Изначальное кол-во элементов в аудиоряде: {len(y)}')

        fourier_transform = fft(y)
        fourier_envelope = np.abs(fourier_transform)
        logger.debug(f'Кол-во элементов в огибающей: {len(fourier_envelope)}')

        return fourier_envelope
