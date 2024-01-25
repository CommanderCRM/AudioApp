import re
import wave
import multiprocessing
import Levenshtein
import vosk

def recognize_vosk(path_to_file, path_to_model, result):
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

    result.update({'value': result_recognition})

def run_recognition(path_to_file, path_to_model):
    """Запуск функции распознавания в отдельном процессе"""
    manager = multiprocessing.Manager()
    result = manager.dict()

    process = multiprocessing.Process(target=recognize_vosk, args=(path_to_file, path_to_model, result))
    process.start()
    process.join()

    return result.get('value')

def levenstein(result, orig_str):
    """Расчет расстояния Левенштейна и точность фразы"""
    # Обращение происходит только к первому эталону
    levenstein_distance = Levenshtein.distance(str(result), orig_str)
    original_length = len(orig_str)
    recognition_error = round((levenstein_distance/original_length)*100, 2)
    recognition_accuracy = round((100 - recognition_error), 2)
    return levenstein_distance, original_length, recognition_accuracy
