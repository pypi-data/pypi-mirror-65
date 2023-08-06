from typing import Optional

from prometheus_client.parser import text_fd_to_metric_families


class BaselineMetricCollector:

    DEFAULT_HISTOGRAM_PATH = "/artefact/histogram.prom"

    def __init__(self, path: Optional[str] = None):
        """Parses baseline metrics from a local file.

        :param path: Path to Prometheus file, defaults to `DEFAULT_HISTOGRAM_PATH`
        :type path: Optional[str], optional
        """
        self.path = path or self.DEFAULT_HISTOGRAM_PATH

    def collect(self):
        with open(self.path, "r") as f:
            for metric in text_fd_to_metric_families(f):
                # Ignore non-baseline metrics
                if not metric.name.endswith("_baseline"):
                    continue
                yield metric
