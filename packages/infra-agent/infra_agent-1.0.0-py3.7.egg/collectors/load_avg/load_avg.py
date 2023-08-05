import os
import multiprocessing


class LoadAvgMetrics():
    def __init__(self):
        self.metrics = {}

    def retrieve(self):
        load01, load05, load15 = os.getloadavg()
        cpu_count = multiprocessing.cpu_count()

        self.metrics['load_1min'] = load01
        self.metrics['load_5min'] = load05
        self.metrics['load_15min'] = load15
        self.metrics['load_1min_normalized'] = load01 / cpu_count
        self.metrics['load_5min_normalized'] = load05 / cpu_count
        self.metrics['load_15min_normalized'] = load15 / cpu_count

        return self.metrics
