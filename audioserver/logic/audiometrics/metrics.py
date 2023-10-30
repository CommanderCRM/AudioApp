import math
import numpy as np
import time
from dtw import dtw
from tqdm import tqdm
from sktime.distances import msm_distance, edr_distance, erp_distance
from scipy.spatial.distance import minkowski
from scipy.stats import pearsonr
from loguru import logger

class AudioMetrics:
    """Расчет расстояний между аудиофайлами"""
    def dtw_native(self, s1,s2):
        """Расстояние DTW"""
        n = len(s1)
        m = len(s2)
        dp = np.zeros((n + 1, m + 1))

        for i in range(1, n + 1):
            dp[i][0] = math.inf
        for i in range(1, m + 1):
            dp[0][i] = math.inf
        dp[0][0] = 0
        for i in tqdm(range(1, n + 1), position=0, desc="Расчет DTW"):
            for j in range(1, m + 1):
                cost = abs(s1[i - 1] - s2[j - 1])
                dp[i][j] = cost + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
        return dp[n][m]


    def edr_native(self, s, t, k):
        """
        Расстояние EDR
        k - чувствительность
        """
        n = len(s)
        m = len(t)
        dp = [[0 for j in range(m+1)] for i in range(n+1)]

        for i in tqdm(range(n+1), position=1, desc="Расчет EDR"):
            for j in range(m+1):
                if i == 0:
                    dp[i][j] = j
                elif j == 0:
                    dp[i][j] = i
                else:
                    if abs(s[i-1] - t[j-1]) <= k:
                        dp[i][j] = dp[i-1][j-1]
                    else:
                        dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])

        return dp[n][m]

    def erp_native(self, s, t, k, g):
        """
        Расстояние ERP
        k - чувствительность
        g - стоимость замены
        """
        n = len(s)
        m = len(t)
        dp = [[float('inf') for j in range(m+1)] for i in range(n+1)]
        dp[0][0] = 0

        for i in tqdm(range(1, n+1), position=2, desc="Расчет ERP"):
            for j in range(1, m+1):
                if abs(s[i-1] - t[j-1]) <= k:
                    dp[i][j] = min(dp[i][j], dp[i-1][j-1])
                else:
                    dp[i][j] = min(dp[i][j], g + dp[i-1][j-1])
                dp[i][j] = min(dp[i][j], 1 + dp[i-1][j], 1 + dp[i][j-1])

        return dp[n][m]

    def msm_native(self, s1, s2, c):
        """Расстояние MSM
           c - стоимость слияния"""
        # Инициализация графа трансформации
        graph = np.zeros((len(s1)+1, len(s2)+1))

        # Заполнение графа трансформации
        for i in tqdm(range(1, len(s1)+1), position=3, desc="Расчет MSM"):
            for j in range(1, len(s2)+1):
                if s1[i-1] == s2[j-1]:
                    graph[i][j] = graph[i-1][j-1]
                else:
                    graph[i][j] = min(graph[i-1][j-1], graph[i-1][j], graph[i][j-1]) + c

        # Расчет расстояния
        msm = graph[-1][-1]

        return msm

    def get_dtw_transformed_sequences(self, y1, y2):
        """Получение трансформированных DTW рядов по изначальным"""
        start = time.process_time()

        dtw_class = dtw(y1, y2)

        dtw_indices1 = dtw_class.index1
        dtw_indices2 = dtw_class.index2

        y1_transformed = [y1[i] for i in dtw_indices1]
        y2_transformed = [y2[i] for i in dtw_indices2]

        stop = time.process_time() - start
        logger.debug(f'Время на получение трансформированных рядов DTW: {stop}')

        return y1_transformed, y2_transformed

    def get_dtw_native(self, y1, y2):
        """Получение DTW между двумя аудиофайлами (собственная имплементация)"""
        y1_transformed, y2_transformed = self.get_dtw_transformed_sequences(y1, y2)
        distance = self.dtw_native(y1_transformed, y2_transformed)
        return distance

    def get_erp_native(self, y1, y2):
        """Получение ERP между двумя аудиофайлами (собственная имплементация)"""
        y1_transformed, y2_transformed = self.get_dtw_transformed_sequences(y1, y2)
        distance = self.erp_native(y1_transformed, y2_transformed, 0.001, 1)
        return distance

    def get_edr_native(self, y1, y2):
        """Получение EDR между двумя аудиофайлами (собственная имплементация)"""
        y1_transformed, y2_transformed = self.get_dtw_transformed_sequences(y1, y2)
        distance = self.edr_native(y1_transformed, y2_transformed, 0.001)
        return distance

    def get_msm_native(self, y1, y2):
        """Получение MSM между двумя аудиофайлами (собственная имплементация)"""
        y1_transformed, y2_transformed = self.get_dtw_transformed_sequences(y1, y2)
        distance = self.msm_native(y1_transformed, y2_transformed, 1)
        return distance

    def get_dtw_with_indices(self, y1, y2):
        """Получение DTW между двумя аудиофайлами (вся длина),
           также рядов с индексами изначальных рядов"""
        dtw_class = dtw(y1, y2)

        dtw_distance = dtw_class.distance
        dtw_indices1 = dtw_class.index1
        dtw_indices2 = dtw_class.index2

        return dtw_distance, dtw_indices1, dtw_indices2

    def get_dtw_unbound(self, y1, y2):
        """Получение DTW расстояния между двумя аудиофайлами (вся длина)"""
        dtw_class = dtw(y1, y2)

        start = time.process_time()
        dtw_distance = dtw_class.distance
        stop = time.process_time() - start

        logger.debug(f'Время на получение DTW: {stop}')

        return dtw_distance

    def get_erp(self, y1, y2):
        """Метрика ERP (быстрая)"""
        y1_transformed, y2_transformed = self.get_dtw_transformed_sequences(y1, y2)
        y1_np, y2_np = np.array(y1_transformed), np.array(y2_transformed)

        start = time.process_time()
        distance = erp_distance(y1_np, y2_np)

        stop = time.process_time() - start
        logger.debug(f'Время на получение ERP: {stop}')

        return distance

    def get_edr(self, y1, y2):
        """Метрика EDR (быстрая)"""
        y1_transformed, y2_transformed = self.get_dtw_transformed_sequences(y1, y2)
        y1_np, y2_np = np.array(y1_transformed), np.array(y2_transformed)

        start = time.process_time()
        distance = edr_distance(y1_np, y2_np) * 100 # выравниваем с остальными метриками

        stop = time.process_time() - start
        logger.debug(f'Время на получение EDR: {stop}')

        return distance

    def get_msm(self, y1, y2):
        """Метрика MSM (быстрая)"""
        y1_transformed, y2_transformed = self.get_dtw_transformed_sequences(y1, y2)
        y1_np, y2_np = np.array(y1_transformed), np.array(y2_transformed)

        start = time.process_time()
        distance = msm_distance(y1_np, y2_np)

        stop = time.process_time() - start
        logger.debug(f'Время на получение MSM: {stop}')

        return distance

    def get_minkowski(self, y1, y2):
        """Расстояние Минковского"""
        y1_transformed, y2_transformed = self.get_dtw_transformed_sequences(y1, y2)
        y1_np, y2_np = np.array(y1_transformed), np.array(y2_transformed)

        start = time.process_time()
        distance = minkowski(y1_np, y2_np)

        stop = time.process_time() - start
        logger.debug(f'Время на получение Minkowski: {stop}')

        return distance

    def get_pearson(self, y1, y2):
        """Коррелляция Пирсона"""
        y1_transformed, y2_transformed = self.get_dtw_transformed_sequences(y1, y2)
        y1_np, y2_np = np.array(y1_transformed), np.array(y2_transformed)

        start = time.process_time()
        coef, pval = pearsonr(y1_np, y2_np)

        stop = time.process_time() - start
        logger.debug(f'Время на получение Pearson: {stop}')

        return coef, pval

    def get_linconv(self, values, coeffs):
        """Линейная свертка для 3 элементов"""
        return sum(v*c for v, c in zip(values, coeffs))
