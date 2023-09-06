from audiotools.tools import AudioFile
from audiopreproc.preprocessing import AudioPreprocessor

file = AudioFile('1.wav')
y, sr = file.load()
file.save(y, sr, '2.wav')

audio_preprocessor = AudioPreprocessor()
reduced_audio = audio_preprocessor.reduce_noise(y, sr)
file.save(reduced_audio, sr, "3.wav")
