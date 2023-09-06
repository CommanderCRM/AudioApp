import math
import numpy as np

class AudioMetrics:
    """Расчет расстояний между аудиофайлами"""
    def dtw(self, s1,s2):
        """Расстояние DTW"""
        n = len(s1)
        m = len(s2)
        dp = np.zeros((n + 1, m + 1))

        for i in range(1, n + 1):
            dp[i][0] = math.inf
        for i in range(1, m + 1):
            dp[0][i] = math.inf
        dp[0][0] = 0
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                cost = abs(s1[i - 1] - s2[j - 1])
                dp[i][j] = cost + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
        return dp[n][m]


    def edr(self, s, t, k):
        """Расстояние EDR"""
        n = len(s)
        m = len(t)
        dp = [[0 for j in range(m+1)] for i in range(n+1)]

        for i in range(n+1):
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


    def erp(self, s, t, k, g):
        """Расстояние ERP"""
        n = len(s)
        m = len(t)
        dp = [[float('inf') for j in range(m+1)] for i in range(n+1)]
        dp[0][0] = 0

        for i in range(1, n+1):
            for j in range(1, m+1):
                if abs(s[i-1] - t[j-1]) <= k:
                    dp[i][j] = min(dp[i][j], dp[i-1][j-1])
                else:
                    dp[i][j] = min(dp[i][j], g + dp[i-1][j-1])
                dp[i][j] = min(dp[i][j], 1 + dp[i-1][j], 1 + dp[i][j-1])

        return dp[n][m]

    def get_audio_dtw(self, y1, y2):
        """Получение DTW между двумя аудиофайлами"""
        distance = self.dtw(y1[1:1000], y2[1:1000])
        return distance

    def get_audio_erp(self, y1, y2):
        """Получение ERP между двумя аудиофайлами"""
        distance = self.erp(y1[1:1000], y2[1:1000],1,1)
        return distance

    def get_audio_edr(self, y1, y2):
        """Получение EDR между двумя аудиофайлами"""
        distance = self.edr(y1[1:1000], y2[1:1000],1)
        return distance
