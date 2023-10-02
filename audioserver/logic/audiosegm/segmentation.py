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

        classification = ['S' if ste < e_st else 'UV' if e_st < ste < e_ut else 'V' for ste in pow_frames]

        # где ставить границы
        frame_times = np.arange(num_frames) * overlap / sr
        border_frames = [i + 1 for i in range(num_frames - 1) if classification[i+1] != classification[i]]
        borders_exact = [frame_times[i] for i in border_frames]
        borders_exact = np.array(borders_exact)

        # метки, соответствующие переходу классов
        classification_reduced = [classification[0]]
        classification_reduced.extend([classification[i+1] for i in border_frames])

        # замена функции uniquetol
        filter_threshold = 0.03
        borders_exact = borders_exact[~(np.triu(np.abs(borders_exact[:,None] - borders_exact) <= filter_threshold,1)).any(0)]
        borders_exact = borders_exact.tolist()

        # создание выходной структуры: начало сегмента, конец сегмента, тип сегмента
        borders_and_classes = [(borders_exact[i - 1] if i > 0 else 'Begin', borders_exact[i], classification_reduced[i]) for i in range(len(borders_exact))]
        borders_and_classes.append((borders_exact[-1], 'End', classification_reduced[-1]))

        return borders_and_classes
