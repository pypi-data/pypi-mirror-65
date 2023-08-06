from typing import List

from prometheus_client import Metric


class ComputedMetricCollector:
    def __init__(self, metric: List[Metric]):
        """A wrapper for manually computed baseline distribution of features metrics.

        :param metric: A list of Prometheus metrics returned from FrequencyMetric.dump_frequency.
        :type metric: List[Metric]
        """
        self.metric = metric

    def collect(self):
        return self.metric
