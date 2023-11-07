import os
from loguru import logger
from .audiotools.tools import AudioFile
from .audiopreproc.preprocessing import AudioPreprocessor
from .signalmetrics.metrics import SignalMetrics
from .signalmetrics.envelopes import SignalEnvelopes
from .audiorecognition.recognition import recognize_vosk, levenstein

# Инициализируем логгер
if os.environ.get('LOG_LEVEL') == 'DEBUG':
    LEVEL = 'DEBUG'
else:
    LEVEL = 'INFO'

def load_and_reduce_noise(audio_file):
    """Загрузка файла в память и снижение шума"""
    audio_preprocessor = AudioPreprocessor()

    y, sr = audio_file.load()
    logger.debug('Аудиофайл загружен, снижаем шум')

    y_reduced = audio_preprocessor.reduce_noise(y, sr)
    logger.debug('Шум снижен')
    return y_reduced, sr

def compare_two_sessions_dtw(speech_values_dict):
    """Сравнение двух сеансов по DTW"""
    audio_metrics = SignalMetrics()
    audio_envelopes = SignalEnvelopes()
    dtw_distances = {}

    for key, speech_values in speech_values_dict.items():
        speech_base64_list = speech_values

        logger.debug('Декодируем base64 в .wav файлы')
        for i, speech_base64 in enumerate(speech_base64_list, 1):
            AudioFile.decode_base64(speech_base64, f"speech_{key}_{i}.wav")

        logger.debug('Снижаем шум в .wav файлах')
        for i in range(1, 3):
            speech_file = AudioFile(f"speech_{key}_{i}.wav")
            y, sr = load_and_reduce_noise(speech_file)
            speech_file.save(y, sr, f"speech_{key}_{i}_reduced.wav")

        logger.debug('Загружаем .wav файлы со сниженным шумом в память')
        y1, _ = AudioFile(f"speech_{key}_1_reduced.wav").load()
        y2, _ = AudioFile(f"speech_{key}_2_reduced.wav").load()

        logger.debug('Рассчитываем огибающую Гильберта на .wav файлы')
        y1_hilbert = audio_envelopes.hilbert_envelope(y1)
        y2_hilbert = audio_envelopes.hilbert_envelope(y2)

        logger.debug('Получаем расстояния между 2 .wav файлами')
        dtw_distance = audio_metrics.get_dtw_unbound(y1_hilbert, y2_hilbert)
        logger.debug(f'DTW между Ei и R1i: {dtw_distance}')

        dtw_distances[key] = dtw_distance

        logger.debug('Удаляем файлы')
        for i in range(1, 3):
            os.remove(f"speech_{key}_{i}.wav")
            os.remove(f"speech_{key}_{i}_reduced.wav")

    return dtw_distances

def compare_three_sessions_dtw(speech_values_dict):
    """Сравнение трех сеансов по DTW"""
    audio_metrics = SignalMetrics()
    audio_envelopes = SignalEnvelopes()
    dtw_distances = {}

    for key, speech_values in speech_values_dict.items():
        speech_base64_list = speech_values

        logger.debug('Декодируем base64 в .wav файлы')
        for i, speech_base64 in enumerate(speech_base64_list, 1):
            AudioFile.decode_base64(speech_base64, f"speech_{key}_{i}.wav")

        logger.debug('Снижаем шум в .wav файлах')
        for i in range(1, 4):
            speech_file = AudioFile(f"speech_{key}_{i}.wav")
            y, sr = load_and_reduce_noise(speech_file)
            speech_file.save(y, sr, f"speech_{key}_{i}_reduced.wav")

        logger.debug('Загружаем .wav файлы со сниженным шумом в память')
        y1, _ = AudioFile(f"speech_{key}_1_reduced.wav").load()
        y2, _ = AudioFile(f"speech_{key}_2_reduced.wav").load()
        y3, _ = AudioFile(f"speech_{key}_3_reduced.wav").load()

        logger.debug('Рассчитываем огибающую Гильберта на .wav файлы')
        y1_hilbert = audio_envelopes.hilbert_envelope(y1)
        y2_hilbert = audio_envelopes.hilbert_envelope(y2)
        y3_hilbert = audio_envelopes.hilbert_envelope(y3)

        logger.debug('Получаем расстояния между 3 .wav файлами')
        dtw_distance_12 = audio_metrics.get_dtw_unbound(y1_hilbert, y2_hilbert)
        logger.debug(f'DTW между Ei и R1i: {dtw_distance_12}')
        dtw_distance_13 = audio_metrics.get_dtw_unbound(y1_hilbert, y3_hilbert)
        logger.debug(f'DTW между Ei и R2i: {dtw_distance_13}')
        dtw_distance_23 = audio_metrics.get_dtw_unbound(y2_hilbert, y3_hilbert)
        logger.debug(f'DTW между R1i и R2i: {dtw_distance_23}')

        logger.debug('Рассчитываем оценку речи по формуле (обычная с 2 эталонами)')

        if (dtw_distance_12+dtw_distance_13) == 0:
            logger.debug('Знаменатель в формуле оценки 0, считаем что оценка 1')
            dtw_distances[key] = 1
        elif (2*dtw_distance_23) == 0:
            logger.debug('Расстояние между 2 эталонами слишком маленькое, считаем что числитель 1')
            dtw_distances[key] = 1/(dtw_distance_12+dtw_distance_13)
            logger.debug(f'Формула: 1 / ({dtw_distance_12} + {dtw_distance_13})')
            logger.debug(f'Оценка: {dtw_distances[key]}')
        else:
            dtw_distances[key] = (2*dtw_distance_23)/(dtw_distance_12+dtw_distance_13)
            logger.debug(f'Формула: 2 * {dtw_distance_23} / ({dtw_distance_12} + {dtw_distance_13})')
            logger.debug(f'Оценка: {dtw_distances[key]}')

        if dtw_distances[key] > 1:
            logger.debug('Оценка получилась больше 1, считаем что 1')
            dtw_distances[key] = 1

        logger.debug('Удаляем файлы')
        for i in range(1, 4):
            os.remove(f"speech_{key}_{i}.wav")
            os.remove(f"speech_{key}_{i}_reduced.wav")

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
