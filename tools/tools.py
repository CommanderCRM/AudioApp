import librosa
import soundfile as sf

class AudioFile:
    """Вспомогательные инструменты для работы с аудиофайлом"""
    def __init__(self, file):
        """Инициализация аудиофайла"""
        self.file = file

    def load(self):
        """Загрузка информации о файле (аудиоряд, частота дискретизации)"""
        y, sr = librosa.load(self.file, sr=None)
        return y, sr

    def save(self, y, sr, outfile):
        """Запись аудиофайла в новый"""
        sf.write(outfile, y, sr)
