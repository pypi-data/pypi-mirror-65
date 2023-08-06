
@dataclass(frozen=True)
class FeatureMetric:
    index: int
    description: str

    @property
    def name(self):
        return "feature_{0}_value_baseline".format(self.index)

    @property
    def documentation(self):
        return "Baseline values for feature: {0}".format(self.description)


@dataclass(frozen=True)
class InferenceMetric:
    labels: Mapping[str, str] = field(default_factory=dict)

    @property
    def name(self):
        return "inference_value_baseline"

    @property
    def documentation(self):
        return "Inference values for labels: {0}".format(self.labels)


class HistogramMetricFamily:
    pass


class DisVar:
    def __init__(self, name, documentation, labels):
        self.name = name
        self.documentation = documentation
        self.labels = labels

    def dump_frequency(self, bin_to_count):
        buckets = []
        sum_value = 0
        return HistogramMetricFamily(
            name=self.name,
            documentation=self.documentation,
            buckets=buckets,
            sum_value=sum_value
            or sum(float(k) * v for k, v in bin_to_count.items() if k != "+Inf"),
        )

    def load_frequency(self, metric):
        pass

    def observe(self):
        pass



class BaselineMetricExporter:
    DEFAULT_HISTOGRAM_PATH = "/artefact/histogram.prom"
