import numpy as np

class Segmentation:
    """Сегментация аудиофайла"""
    def voiced_unvoiced_silence(self, y, sr):
        """Сегментация на вокализованные, невокализованные участки и тишину"""
        data = y

        # в индексы замены buffer принимаются только целочисленные значения
        frame_size = int(0.02 * sr)
        overlap = int(0.01 * sr)

        # оптимальные параметры получены на НИР
        alpha = 0.0017
        beta = 0.8482

        # замена функции buffer
        frames = [data[i:i + frame_size] for i in range(0, len(data), overlap)]

        # расчет энергии и порогов
        num_frames = len(frames)
        pow_frames = [np.sum(np.power(frame, 2)) for frame in frames]
        ste_sum = np.sum(pow_frames)
        e_avg = (1/num_frames)*ste_sum
        e_st = alpha * e_avg
        e_ut = beta * e_avg

        classification = [1 if ste < e_st else 2 if e_st < ste < e_ut else 3 for ste in pow_frames]

        # где ставить границы
        frame_times = np.arange(num_frames) * overlap / sr
        border_frames = [i + 1 for i in range(num_frames - 1) if classification[i+1] != classification[i]]
        borders_exact = [frame_times[i] for i in border_frames]
        borders_exact = np.array(borders_exact)

        # замена функции uniquetol
        filter_threshold = 0.03
        borders_exact = borders_exact[~(np.triu(np.abs(borders_exact[:,None] - borders_exact) <= filter_threshold,1)).any(0)]

        borders_exact = borders_exact.tolist()
        return borders_exact
