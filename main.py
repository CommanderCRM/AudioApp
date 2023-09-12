from audiotools.tools import AudioFile
from audiopreproc.preprocessing import AudioPreprocessor
from audiopreproc.voiceactivity import VoiceActivityDetector
from audiometrics.metrics import AudioMetrics
from audiosegm.segmentation import Segmentation

file = AudioFile('1.wav')
y, sr = file.load()
file_name = file.get_file_name()
file.save(y, sr, '2.wav')

audio_preprocessor = AudioPreprocessor()
reduced_audio = audio_preprocessor.reduce_noise(y, sr)
file.save(reduced_audio, sr, "3.wav")

file5 = AudioFile('5.wav')
file5_name = file5.get_file_name()
y5, sr5 = file5.load()

metrics = AudioMetrics()
print(f'DTW between {file_name} and {file5_name}:', metrics.get_audio_dtw(y, y5))
print(f'ERP between {file_name} and {file5_name}:', metrics.get_audio_erp(y, y5))
print(f'EDR between {file_name} and {file5_name}:', metrics.get_audio_edr(y, y5))

file8 = AudioFile('8.wav')
file8_name = file8.get_file_name()
y8, sr8 = file8.load()

segm = Segmentation()
print(f'Segments of {file8_name}:', segm.voiced_unvoiced_silence(y8, sr8))

VAD = VoiceActivityDetector()
print(f'Voice activity detection in {file8_name}:', VAD.detect_voice_activity(y8, sr8))

file8_base64_string = file8.encode_base64()
AudioFile.decode_base64(file8_base64_string, '888.wav')
print(f'Difference between {file8_name} and its decoded base64 version:', AudioFile.compare_files('8.wav', '888.wav'))
