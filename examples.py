import pathlib
import os
from multiprocessing import Process
from audioserver.logic.audiotools.tools import AudioFile
from audioserver.logic.audiopreproc.preprocessing import AudioPreprocessor
from audioserver.logic.audiopreproc.voiceactivity import VoiceActivityDetector
from audioserver.logic.audiometrics.metrics import AudioMetrics
from audioserver.logic.audiosegm.segmentation import Segmentation
from audioserver.logic.audiorecognition.recognition import recognize_vosk, levenstein
from audioserver.logic.secactions import hash_gost_3411
from audioserver.logic.audiometrics.envelopes import AudioEnvelopes


# Пример загрузки и сохранения файла
file = AudioFile('1.wav')
y, sr = file.load()
file_name = file.get_file_name()
file.save(y, sr, '2.wav')

# Пример снижения шума
audio_preprocessor = AudioPreprocessor()
reduced_audio = audio_preprocessor.reduce_noise(y, sr)
file.save(reduced_audio, sr, "3.wav")

# Пример расчета метрик
file8 = AudioFile('8.wav')
file15 = AudioFile('15.wav')

y8, sr8 = AudioFile('8.wav').load()
y15, sr15 = AudioFile('15.wav').load()

file8_name = file8.get_file_name()
file15_name = file15.get_file_name()

metrics = AudioMetrics()

# собственная имплементация, > 5 мин на каждую
def print_dtw():
    '''Расчет DTW с прогрессом в отдельном процессе'''
    print(f'DTW between {file8_name} and {file15_name}:', metrics.get_dtw_native(y8, y15))

def print_erp():
    '''Расчет ERP с прогрессом в отдельном процессе'''
    print(f'ERP between {file8_name} and {file15_name}:', metrics.get_erp_native(y8, y15))

def print_edr():
    '''Расчет EDR с прогрессом в отдельном процессе'''
    print(f'EDR between {file8_name} and {file15_name}:', metrics.get_edr_native(y8, y15))

def print_msm():
    '''Расчет MSM с прогрессом в отдельном процессе'''
    print(f'MSM between {file8_name} and {file15_name}:', metrics.get_msm_native(y8, y15))

functions = [print_dtw, print_erp, print_edr, print_msm]

processes = [Process(target=func) for func in functions]

for process in processes:
    process.start()

for process in processes:
    process.join()

# sktime/scipy, быстрый расчет
print(f'ERP between {file8_name} and {file15_name}:', metrics.get_erp(y8, y15))
print(f'EDR between {file8_name} and {file15_name}:', metrics.get_edr(y8, y15))
print(f'MSM between {file8_name} and {file15_name}:', metrics.get_msm(y8, y15))
print(f'Minkowski between {file8_name} and {file15_name}:', metrics.get_minkowski(y8, y15))
print(f'Pearson between {file8_name} and {file15_name} (coef, pval):', metrics.get_pearson(y8, y15))

dtw_dist = metrics.get_dtw_unbound(y8, y15)
mink_dist = metrics.get_minkowski(y8, y15)
coef, _ = metrics.get_pearson(y8, y15)

values = [dtw_dist, mink_dist, coef]
coeffs = [0.3, 0.4, 0.3]

print('Linear convolution between DTW, Minkowski, PCorr:', metrics.get_linconv(values, coeffs))

# Пример сегментации, детектора голосовой активности, кодирования/декодирования base64
file8 = AudioFile('8.wav')
file8_name = file8.get_file_name()
y8, sr8 = file8.load()

segm = Segmentation()
print(f'Segments of {file8_name}:', segm.voiced_unvoiced_silence(y8, sr8))

VAD = VoiceActivityDetector()
print(f'Voice activity detection in {file8_name}:', VAD.detect_voice_activity(y8, sr8))

file8_base64_string = file8.encode_base64()
AudioFile.decode_base64(file8_base64_string, '888.wav')
print(f'Difference between {file8_name} and its decoded base64 version:',
      AudioFile.compare_files('8.wav', '888.wav'))

# Пример распознавания речи и расчета расстояния Левенштейна
file = AudioFile('3.wav')
y, sr = file.load_in_16k()
file.save(y, sr, '3_16k.wav')
current_path = pathlib.Path(__file__).parent.resolve()
file_path = current_path.joinpath('3_16k.wav')
model_path = os.path.join(os.getcwd(), 'audiorecognition', 'vosk-model-ru-0.22')

RESULT = recognize_vosk(file_path, model_path)
print('Recognition result: ', RESULT)
ORIG_STR = 'белый пар расстилается над лужами'
levenstein_distance, original_length, recognition_accuracy = levenstein(RESULT, ORIG_STR)
print('Levenstein distance: ', levenstein_distance)
print('Original phrase length: ', original_length)
print('Recognition accuracy: ', recognition_accuracy)

# Пример хэширования пароля по ГОСТ 34.11-2012 "Стрибог"
example_str = "boralekkrutoi123!"
another_example_str = "boralekochenkrutoi345!!"
more_example_str = "boralekcooper567!!"

example_hash = hash_gost_3411(example_str)
another_example_hash = hash_gost_3411(another_example_str)
more_example_hash = hash_gost_3411(more_example_str)

print('Пример хэша: ', example_hash)
print('Еще пример хэша: ', another_example_hash)
print('Еще один пример хэша: ', more_example_hash)

# Пример использования огибающих
file = AudioFile('8.wav')
y, sr = file.load()
print('Значения ориг. аудиоряда: ', y)

AE = AudioEnvelopes()
abs_envelope = AE.absolute_envelope(y)
print('Огибающая по абсолютным значениям : ', abs_envelope)

ste_envelope = AE.short_time_energy_envelope(y)
print('Огибающая по мгновенной энергии: ', ste_envelope)

hilbert_envelope = AE.hilbert_envelope(y)
print('Огибающая Гильберта: ', hilbert_envelope)

fft_envelope = AE.fft_envelope(y)
print('Огибающая FFT: ', fft_envelope)

# Пример использования DTW: получение расстояния и трансформированных последовательностей (одинаковая длина)
y8, sr8 = AudioFile('8.wav').load()
y9, sr9 = AudioFile('9.wav').load()

AM = AudioMetrics()
distance, indices1, indices2 = AM.get_dtw_with_indices(y8, y9)

print('Расстояние DTW: ', distance)
print('y1: ', y8)
print('y2: ', y9)
print('Сопоставляемый ряд y1: ', indices1)
print('Сопоставляемый ряд y2: ', indices2)
print('Длина y1: ', len(y8))
print('Длина y2: ', len(y9))
print('Длина сопост. y1: ', len(indices1))
print('Длина сопост. y2: ', len(indices2))

# Пример использования DTW: получение расстояния и индексов трансформированных последовательностей (разная длина)
y8, sr8 = AudioFile('8.wav').load()
y9, sr9 = AudioFile('15.wav').load()

AM = AudioMetrics()
distance, indices1, indices2 = AM.get_dtw_with_indices(y8, y9)

print('Расстояние DTW: ', distance)
print('y1: ', y8)
print('y2: ', y9)
print('Сопоставляемый ряд y1: ', indices1)
print('Сопоставляемый ряд y2: ', indices2)
print('Длина y1: ', len(y8))
print('Длина y2: ', len(y9))
print('Длина сопост. y1: ', len(indices1))
print('Длина сопост. y2: ', len(indices2))

# Пример получения расстояния DTW по всей длине последовательности с последовательностями разной длины
y8, sr8 = AudioFile('8.wav').load()
y15, sr15 = AudioFile('15.wav').load()

AM = AudioMetrics()
distance = AM.get_dtw_unbound(y8, y15)

print('Расстояние DTW: ', distance)
print('Длина y1: ', len(y8))
print('Длина y2: ', len(y15))

# Пример получения трансформированных DTW последовательностей
# Тут лучше запускать скрипт через python3 main.py > main.txt (с перенаправлением)
# т.к. трансформированные ряды не усекаются
y8, sr8 = AudioFile('8.wav').load()
y15, sr15 = AudioFile('15.wav').load()

AM = AudioMetrics()
y1_transformed, y2_transformed = AM.get_dtw_transformed_sequences(y8, y15)

print('Исходный ряд y1: ', y8)
print('Исходный ряд y2: ', y15)
print('Трансформированный ряд y1: ', y1_transformed)
print('Трансформированный ряд y2: ', y2_transformed)
print('Длины рядов y1, y2: ', len(y8), len(y15))
print('Длины трансформированных y1, y2: ', len(y1_transformed), len(y2_transformed))
