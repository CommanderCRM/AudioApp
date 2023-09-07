from audiotools.tools import AudioFile
from audiopreproc.preprocessing import AudioPreprocessor
from audiometrics.metrics import AudioMetrics
from audiosegm.segmentation import Segmentation

file = AudioFile('1.wav')
y, sr = file.load()
file.save(y, sr, '2.wav')

audio_preprocessor = AudioPreprocessor()
reduced_audio = audio_preprocessor.reduce_noise(y, sr)
file.save(reduced_audio, sr, "3.wav")

file5 = AudioFile('5.wav')
y5, sr5 = file5.load()

metrics = AudioMetrics()
print('DTW:', metrics.get_audio_dtw(y, y5))
print('ERP:', metrics.get_audio_erp(y, y5))
print('EDR:', metrics.get_audio_edr(y, y5))

file8 = AudioFile('8.wav')
y8, sr8 = file8.load()

segm = Segmentation()
print('Borders:', segm.voiced_unvoiced_silence(y8, sr8))
