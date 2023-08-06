from typing import Iterable, List, Mapping, Tuple, Type

import numpy as np

from .frequency import ContinuousVariable, DiscreteVariable, FrequencyMetric


class FeatureHistogramCollector:
    """Collects metrics related to feature distribution from in-memory dataset.

    The collector caps the sample size to a configurable `max_samples` to reduce time needed to
    calculate histogram. It also uses heuristics of the data to decide whether a feature column is
    discrete or continuous. Users may override this behaviour using the `ComputedMetricsCollector`.
    """

    SUPPORTED: Mapping[str, Type[FrequencyMetric]] = {
        "histogram": ContinuousVariable,
        "counter": DiscreteVariable,
    }

    def __init__(self, data: Iterable[Tuple[str, List[float]]], max_samples: int = 100000):
        """
        :param data: Data to build histogram for
        :type data: Iterable[Tuple[str, List[float]]]
        :param max_samples: max number of samples used to calculate histogram, default 100000
        :type max_xamples: int
        """
        self.data: Iterable[Tuple[str, List[float]]] = data
        self.max_samples: int = max_samples

    def _is_discrete(self, val: List[float]) -> bool:
        """Litmus test to determine if val is discrete.

        :param val: Array of positive values
        :type val: List[float]
        :return: Whether input array only contains discrete values
        :rtype: bool
        """
        # Sample size too big, use 1% of max_samples to cap computation at 1ms
        size = len(val)
        if size > 1000:
            size = min(len(val), self.max_samples // 100)
            val = np.random.choice(val, size, replace=False)
        bins = np.unique(val)
        # Caps number of bins to 50
        return len(bins) < 3 or len(bins) * 20 < size

    def _get_bins(self, val: List[float]) -> List[float]:
        """Calculates the optimal bins for prometheus histogram.

        :param val: Array of positive values.
        :type val: List[float]
        :return: Upper bound of each bin (at least 2 bins)
        :rtype: List[float]
        """
        r_min = np.min(val)
        r_max = np.max(val)
        min_bins = 2
        max_bins = 50
        # Calculate bin width using either Freedman-Diaconis or Sturges estimator
        bin_edges = np.histogram_bin_edges(val, bins="auto")
        if len(bin_edges) < min_bins:
            return list(np.linspace(start=r_min, stop=r_max, num=min_bins))
        elif len(bin_edges) <= max_bins:
            return list(bin_edges)
        # Clamp to max_bins by estimating a good bin range to be more robust to outliers
        q75, q25 = np.percentile(val, [75, 25])
        iqr = q75 - q25
        width = 2 * iqr / max_bins
        start = max((q75 + q25) / 2 - iqr, r_min)
        stop = min(start + max_bins * width, r_max)
        # Take the minimum of range and 2x IQR to account for outliers
        edges = list(np.linspace(start=start, stop=stop, num=max_bins))
        prefix = [r_min] if start > r_min else []
        suffix = [r_max] if stop < r_max else []
        return prefix + edges + suffix

    def collect(self):
        """Calculates histogram bins using numpy and converts to Prometheus metric.

        :yield: The converted histogram metric for each feature.
        :rtype: HistogramMetricFamily
        """
        for i, col in enumerate(self.data):
            name, val = col
            # Assuming data is float. Categorical data should have been one-hot encoded
            # dtype=float will convert None values to np.nan as well
            val = np.asarray(val, dtype=float)
            size = len(val)
            # Sample without replacement to cap computation to about 3 seconds for 25 features
            if size > self.max_samples:
                size = self.max_samples
                val = np.random.choice(val, size=self.max_samples, replace=False)

            if self._is_discrete(val):
                bins, counts = np.unique(val, return_counts=True)
                bin_to_count = {str(bins[i]): counts[i] for i in range(len(bins))}
                yield DiscreteVariable.dump_frequency(
                    index=i, name=name, bin_to_count=bin_to_count
                )
                continue

            val = val[~np.isnan(val)]
            val = val[~np.isinf(val)]
            size_inf = size - len(val)

            # Allows negative values as bin edge
            sum_value = np.sum(val)
            if len(val) == 0:
                bin_to_count = {"0.0": 0}
            else:
                bins = self._get_bins(val)
                # Take the negative of all values to use "le" as the bin upper bound
                counts, _ = np.histogram(-val, bins=-np.flip([bins[0]] + bins))
                counts = np.flip(counts)
                bin_to_count = {str(bins[i]): counts[i] for i in range(len(bins))}

            bin_to_count["+Inf"] = size_inf
            yield ContinuousVariable.dump_frequency(
                index=i, name=name, bin_to_count=bin_to_count, sum_value=sum_value
            )
