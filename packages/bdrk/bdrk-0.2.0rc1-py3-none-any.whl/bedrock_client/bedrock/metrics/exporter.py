from abc import abstractmethod

from .type import PredictionContext


class LogExporter:
    @abstractmethod
    def emit(self, prediction: PredictionContext):
        """
        Saves the full prediction context to an external datastore.

        :param prediction: The completed prediction
        :type prediction: PredictionContext
        """
        raise NotImplementedError
