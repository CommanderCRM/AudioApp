import re
import wave
import Levenshtein
import vosk

# Список эталонных фраз
dict_for_levenstein = ['белый пар расстилается над лужами']

def recognize_vosk(path_to_file, path_to_model):
    """Распознавание речи"""
    # Загрузка модели локально, модель инициализируется при каждом запуске цикла, ускоряет работу
    model_path = path_to_model
    model = vosk.Model(model_path)
    recognizer = vosk.KaldiRecognizer(model, 16000)

    # Распознавание
    wf = wave.open(fr"{path_to_file}", "rb")
    data = wf.readframes(240000)

    while data:
        recognizer.AcceptWaveform(data)
        data = wf.readframes(240000)

    result_recognition = recognizer.FinalResult()
    result_recognition = result_recognition.replace('\\n', ' ')
    result_recognition = re.sub("[^А-Яа-я]", " ", result_recognition)
    result_recognition = ' '.join(result_recognition.split())

    return result_recognition


def levenstein(result):
    """Расчет расстояния Левенштейна и точность фразы"""
    # Обращение происходит только к первому эталону
    levenstein_distance = Levenshtein.distance(str(result), dict_for_levenstein[0])
    original_length = len(dict_for_levenstein[0])
    recognition_error = round((levenstein_distance/original_length)*100, 2)
    recognition_accuracy = round((100 - recognition_error), 2)
    return levenstein_distance, original_length, recognition_accuracy
