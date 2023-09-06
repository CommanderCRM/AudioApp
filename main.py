from audiotools.tools import AudioFile
from audiopreproc.preprocessing import AudioPreprocessor
from audiometrics.metrics import AudioMetrics

file = AudioFile('1.wav')
y, sr = file.load()
file.save(y, sr, '2.wav')

audio_preprocessor = AudioPreprocessor()
reduced_audio = audio_preprocessor.reduce_noise(y, sr)
file.save(reduced_audio, sr, "3.wav")

file2 = AudioFile('5.wav')
y2, sr2 = file2.load()
metrics = AudioMetrics()
print(metrics.get_audio_dtw(y, y2))
print(metrics.get_audio_erp(y, y2))
print(metrics.get_audio_edr(y, y2))
