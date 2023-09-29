import noisereduce as nr

class AudioPreprocessor:
    """Предобработка аудио"""
    def reduce_noise(self, y, sr):
        """Удаление шума"""
        reduced_noise = nr.reduce_noise(y=y, sr=sr)
        return reduced_noise
