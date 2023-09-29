import os
from .audiotools.tools import AudioFile
from .audiopreproc.preprocessing import AudioPreprocessor
from .audiometrics.metrics import AudioMetrics

def compare_sessions_dtw(speech_values_dict):
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
