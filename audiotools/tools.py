import os
import librosa
import soundfile as sf

class AudioFile:
    """Вспомогательные инструменты для работы с аудиофайлом"""
    def __init__(self, file):
        """Инициализация аудиофайла"""
        self.file = file

    def load(self):
        """Загрузка файла (аудиоряд, частота дискретизации по умолчанию)"""
        y, sr = librosa.load(self.file, sr=None)
        return y, sr

    def save(self, y, sr, outfile):
        """Запись аудиофайла в новый"""
        sf.write(outfile, y, sr)

    def get_file_name(self):
        """Получение имени аудиофайла"""
        return os.path.basename(self.file)
