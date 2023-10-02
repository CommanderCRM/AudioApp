import os
import base64
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

    def load_in_16k(self):
        """Загрузка файла в частоте дискретизации 16кГц"""
        y, sr = librosa.load(self.file, sr=16000)
        return y,sr

    def save(self, y, sr, outfile):
        """Запись аудиофайла в новый"""
        sf.write(outfile, y, sr)

    def get_file_name(self):
        """Получение имени аудиофайла"""
        return os.path.basename(self.file)

    def encode_base64(self):
        """Кодирование аудиофайла в строку base64"""
        with open(self.file, 'rb') as binary_file:
            binary_file_data = binary_file.read()
            return base64.b64encode(binary_file_data).decode('utf-8')

    @staticmethod
    def decode_base64(base64_string, outfile):
        """Декодирование аудиофайла из строки base64"""
        base64_bytes = base64_string.encode('utf-8')
        with open(outfile, 'wb') as file_to_save:
            decoded_data = base64.decodebytes(base64_bytes)
            file_to_save.write(decoded_data)

    @staticmethod
    def compare_files(file1, file2):
        """Побайтовое сравнение двух .wav файлов и вывод уровня различий"""
        with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
            file1_data = f1.read()
            file2_data = f2.read()
            if len(file1_data) != len(file2_data):
                raise ValueError("Файлы различной длины")

            diff_count = sum(b1 != b2 for b1, b2 in zip(file1_data, file2_data))
            return diff_count
