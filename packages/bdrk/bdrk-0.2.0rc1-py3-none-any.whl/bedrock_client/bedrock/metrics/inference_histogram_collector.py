from typing import List, Optional


class InferenceHistogramCollector:
    def __init__(self, data, model, categories: Optional[List[str]] = None):
        self.data = data
        self.model = model
        self.categories = categories

    def collect(self):
        for feature in self.data:
            yield self.model.predict(feature)
