import numpy as np
from scipy.fft import fft
from scipy.stats.mstats import gmean

class VoiceActivityDetector():
    """Детектор голосовой активности"""
    def detect_voice_activity(self, y, sr):
        """На основе SF, STE"""
        # Сторонние параметры (значения предложены авторами)
        EPT = 40
        FPT = 0.185 # кГц
        SPT = 5
        FRAME_TIME = 0.01

        # Количество фреймов в аудиоряде
        frame_size = int(sr * FRAME_TIME)
        num_frames = len(y) // frame_size
        frame_size_seconds = frame_size / 1000
        frame_duration = frame_size_seconds / sr

        # Расчет значений параметров E, F, SFM в рамках фрейма
        frame_energy = self.__compute_frame_energy(y, num_frames)
        frame_fft = self.__compute_fft_for_frames(y, num_frames)
        frame_freq_f = self.__compute_max_fft_freq(frame_fft, sr)
        frame_sfm = self.__compute_sfm(frame_fft)

        # Минимальные значения параметров
        min_E = min(frame_energy[0:30])
        min_F = min(frame_freq_f[0:30])
        min_SF = min(frame_sfm[0:30])

        # Пороги
        thr_E = EPT * np.log(min_E)
        thr_F = FPT
        thr_SF = SPT

        # Алгоритм детектирования активности
        silence_count = 0
        silence_local_count = 0
        speech_local_count = 0
        ignore_silence = 10
        ignore_speech = 5
        segments = []
        for i in range(num_frames):
            counter = 0
            if ((frame_energy[i]-min_E)>=thr_E):
                counter += 1
            if ((frame_freq_f[i]-min_F)>=thr_F):
                counter += 1
            if ((frame_sfm[i]-min_SF)>=thr_SF):
                counter += 1
            if counter > 1:
                speech_local_count += 1
                silence_local_count = 0
                if speech_local_count >= ignore_speech:
                    start_time = i * frame_duration
                    end_time = (i + 1) * frame_duration
                    if segments and segments[-1][0] == 'Speech':
                        segments[-1][2] = end_time
                    else:
                        segments.append(['Speech', start_time, end_time])
            else:
                silence_count += 1
                silence_local_count += 1
                speech_local_count = 0
                if silence_local_count >= ignore_silence:
                    min_E = ((silence_count*min_E) + frame_energy[i])/(silence_count+1)
                    thr_E = EPT * np.log(min_E)
                    start_time = i * frame_duration
                    end_time = (i + 1) * frame_duration
                    if segments and segments[-1][0] == 'Silence':
                        segments[-1][2] = end_time
                    else:
                        segments.append(['Silence', start_time, end_time])

        return segments

    def __compute_frame_energy(self, y, num_frames):
        """Расчет значений энергии в каждом фрейме"""
        frame_size = len(y) // num_frames
        frame_energy = []

        for i in range(num_frames):
            start = i * frame_size
            end = start + frame_size
            frame_samples = y[start:end]
            energy = sum(sample ** 2 for sample in frame_samples)
            frame_energy.append(energy)

        return frame_energy

    def __compute_fft_for_frames(self, y, num_frames):
        """Применение FFT в каждом фрейме"""
        frame_size = len(y) // num_frames
        frame_fft = []

        for i in range(num_frames):
            start = i * frame_size
            end = start + frame_size
            frame_samples = y[start:end]
            fft_result = fft(frame_samples)
            frame_fft.append(fft_result)

        return frame_fft

    def __compute_max_fft_freq(self, frame_fft, sr):
        """Расчет доминантных частот F в кГц"""
        frame_size = len(frame_fft[0])
        frame_freq = []

        for fft_result in frame_fft:
            spectrum_magnitudes = np.abs(fft_result)
            max_index = np.argmax(spectrum_magnitudes)
            frequency = max_index * sr / frame_size
            frequency_khz = frequency / 1000
            frame_freq.append(frequency_khz)

        return frame_freq

    def __compute_sfm(self, frame_fft):
        """Расчет SFM"""
        frame_sfm = []

        for fft_result in frame_fft:
            spectrum_magnitudes = np.abs(fft_result)
            G = gmean(spectrum_magnitudes)
            A = np.mean(spectrum_magnitudes)
            SFM = G / A if A != 0 else 0
            frame_sfm.append(SFM)

        return frame_sfm
