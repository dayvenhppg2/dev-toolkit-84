import time

class CryptoAnalyzer:
    def __init__(self, data):
        self.data = data

    def calculate_moving_average(self, period):
        if period <= 0:
            raise ValueError('Period must be positive')
        return [sum(self.data[i:i + period]) / period for i in range(len(self.data) - period + 1)]

    def optimized_calculate_moving_average(self, period):
        if period <= 0:
            raise ValueError('Period must be positive')
        moving_avg = []
        window_sum = sum(self.data[:period])
        moving_avg.append(window_sum / period)
        for i in range(period, len(self.data)):
            window_sum += self.data[i] - self.data[i - period]
            moving_avg.append(window_sum / period)
        return moving_avg

    def analyze_data(self):
        start_time = time.time()
        ma = self.optimized_calculate_moving_average(5)
        elapsed_time = time.time() - start_time
        return ma, elapsed_time

data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

analyzer = CryptoAnalyzer(data)
print(analyzer.analyze_data())