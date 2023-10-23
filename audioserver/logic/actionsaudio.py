import os
from loguru import logger
from .audiotools.tools import AudioFile
from .audiopreproc.preprocessing import AudioPreprocessor
from .audiometrics.metrics import AudioMetrics
from .audiorecognition.recognition import recognize_vosk, levenstein

# Инициализируем логгер
if os.environ.get('LOG_LEVEL') == 'DEBUG':
    LEVEL = 'DEBUG'
else:
    LEVEL = 'INFO'

def compare_two_sessions_dtw(speech_values_dict):
    """Сравнение двух сеансов по DTW"""
    audio_preprocessor = AudioPreprocessor()
    audio_metrics = AudioMetrics()
    dtw_distances = {}

    for key, speech_values in speech_values_dict.items():
        speech_1_base64, speech_2_base64 = speech_values

        AudioFile.decode_base64(speech_1_base64, f"speech_{key}_1.wav")
        AudioFile.decode_base64(speech_2_base64, f"speech_{key}_2.wav")

    for key in speech_values_dict:
        speech_1_file = AudioFile(f"speech_{key}_1.wav")
        speech_2_file = AudioFile(f"speech_{key}_2.wav")

        y1, sr1 = speech_1_file.load()
        y2, sr2 = speech_2_file.load()

        y1_reduced = audio_preprocessor.reduce_noise(y1, sr1)
        y2_reduced = audio_preprocessor.reduce_noise(y2, sr2)

        speech_1_file.save(y1_reduced, sr1, f"speech_{key}_1_reduced.wav")
        speech_2_file.save(y2_reduced, sr2, f"speech_{key}_2_reduced.wav")

    for key in speech_values_dict:
        speech_1_file = AudioFile(f"speech_{key}_1_reduced.wav")
        speech_2_file = AudioFile(f"speech_{key}_2_reduced.wav")

        y1, sr1 = speech_1_file.load()
        y2, sr2 = speech_2_file.load()
        dtw_distance = audio_metrics.get_audio_dtw(y1, y2)
        dtw_distances[key] = dtw_distance

    for key in speech_values_dict:
        os.remove(f"speech_{key}_1.wav")
        os.remove(f"speech_{key}_2.wav")
        os.remove(f"speech_{key}_1_reduced.wav")
        os.remove(f"speech_{key}_2_reduced.wav")

    return dtw_distances

def compare_three_sessions_dtw(speech_values_dict):
    """Сравнение трех сеансов по DTW"""
    audio_preprocessor = AudioPreprocessor()
    audio_metrics = AudioMetrics()
    dtw_distances = {}

    for key, speech_values in speech_values_dict.items():
        speech_1_base64, speech_2_base64, speech_3_base64 = speech_values

        logger.debug('Декодируем base64 в 3 .wav файла')
        AudioFile.decode_base64(speech_1_base64, f"speech_{key}_1.wav")
        AudioFile.decode_base64(speech_2_base64, f"speech_{key}_2.wav")
        AudioFile.decode_base64(speech_3_base64, f"speech_{key}_3.wav")

    for key in speech_values_dict:
        speech_1_file = AudioFile(f"speech_{key}_1.wav")
        speech_2_file = AudioFile(f"speech_{key}_2.wav")
        speech_3_file = AudioFile(f"speech_{key}_3.wav")

        logger.debug('Загружаем 3 .wav файла в память')
        y1, sr1 = speech_1_file.load()
        y2, sr2 = speech_2_file.load()
        y3, sr3 = speech_3_file.load()

        logger.debug('Снижаем 3 шум в 3 .wav файлах')
        y1_reduced = audio_preprocessor.reduce_noise(y1, sr1)
        y2_reduced = audio_preprocessor.reduce_noise(y2, sr2)
        y3_reduced = audio_preprocessor.reduce_noise(y3, sr3)

        logger.debug('Сохраняем 3 .wav файла со сниженным шумом')
        speech_1_file.save(y1_reduced, sr1, f"speech_{key}_1_reduced.wav")
        speech_2_file.save(y2_reduced, sr2, f"speech_{key}_2_reduced.wav")
        speech_3_file.save(y3_reduced, sr3, f"speech_{key}_3_reduced.wav")

    for key in speech_values_dict:
        speech_1_file = AudioFile(f"speech_{key}_1_reduced.wav")
        speech_2_file = AudioFile(f"speech_{key}_2_reduced.wav")
        speech_3_file = AudioFile(f"speech_{key}_3_reduced.wav")

        logger.debug('Загружаем 3 .wav файла со сниженным шумом в память')
        y1, sr1 = speech_1_file.load()
        y2, sr2 = speech_2_file.load()
        y3, sr3 = speech_3_file.load()

        logger.debug('Получаем расстояния между 3 .wav файлами')
        dtw_distance_12 = audio_metrics.get_audio_dtw(y1, y2)
        dtw_distance_13 = audio_metrics.get_audio_dtw(y1, y3)
        dtw_distance_23 = audio_metrics.get_audio_dtw(y2, y3)

        logger.debug('Рассчитываем оценку речи по формуле (обычная с 2 эталонами)')

        if (dtw_distance_12+dtw_distance_13) == 0:
            logger.debug('Знаменатель в формуле оценки 0, считаем что оценка 0')
            dtw_distances[key] = 0
        else:
            dtw_distances[key] = (2*dtw_distance_23)/(dtw_distance_12+dtw_distance_13)

        if dtw_distances[key] > 1:
            logger.debug('Оценка получилась больше 1, считаем что 1')
            dtw_distances[key] = 1

    for key in speech_values_dict:
        logger.debug('Удаляем файлы .wav')
        os.remove(f"speech_{key}_1.wav")
        os.remove(f"speech_{key}_2.wav")
        os.remove(f"speech_{key}_3.wav")
        os.remove(f"speech_{key}_1_reduced.wav")
        os.remove(f"speech_{key}_2_reduced.wav")
        os.remove(f"speech_{key}_3_reduced.wav")

    return dtw_distances

def compare_phrases_levenstein(real_value, base64):
    """Сравнение фразы с реальным значением и получение расстояния Левенштейна"""

    audio_preprocessor = AudioPreprocessor()
    AudioFile.decode_base64(base64, "phrase.wav")
    phrase_file = AudioFile("phrase.wav")

    # Снижение уровня шума
    y, sr = phrase_file.load_in_16k()
    y_reduced = audio_preprocessor.reduce_noise(y, sr)
    phrase_file.save(y_reduced, sr, "phrase_reduced.wav")

    phrase_file_reduced = AudioFile("phrase_reduced.wav")
    file_path = phrase_file_reduced.get_file_path()
    model_path = os.path.join(os.getcwd(), 'logic', 'audiorecognition', 'vosk-model-ru-0.22')

    # Получение точности распознавания
    recognition_result = recognize_vosk(file_path, model_path)
    original_string = real_value
    _, __, accuracy = levenstein(recognition_result, original_string)

    os.remove("phrase.wav")
    os.remove("phrase_reduced.wav")

    return accuracy
