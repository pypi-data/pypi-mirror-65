import os
from typing import Any, Callable, Iterable, Mapping, Optional, Tuple

from prometheus_client import CollectorRegistry, generate_latest
from prometheus_client.exposition import choose_encoder
from prometheus_client.metrics import MetricWrapperBase
from prometheus_client.multiprocess import MultiProcessCollector


class PrometheusExporter:
    def __init__(self, collectors: Iterable[Any]):
        self._registry = CollectorRegistry()

        # Always use a new registry for writing through to the filesystem under multiprocess mode
        if "prometheus_multiproc_dir" in os.environ:
            MultiProcessCollector(self._registry)
            # Remove metrics that implement MultiprocessValue
            collectors = filter(
                lambda c: not isinstance(c, CollectorRegistry)
                and not isinstance(c, MetricWrapperBase)
                and hasattr(c, "collect"),
                collectors,
            )

        for c in collectors:
            self._registry.register(c)

    def export_text(
        self, names: Optional[Iterable[str]] = None, encoder: Optional[Callable] = None
    ) -> bytes:
        """Exports selected metrics in the registry as bytes string.

        :param names: [description], defaults to None
        :type names: Optional[Set[str]], optional
        :param encoder: [description], defaults to None
        :type encoder: Optional[str], optional
        :return: Serialized metrics
        :rtype: bytes
        """
        encoder = encoder or generate_latest
        registry = self._registry.restricted_registry(names) if names else self._registry
        return encoder(registry)

    def export_http(
        self,
        params: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> Tuple[bytes, str]:
        """Exports all metrics in the registry as a http response.

        Extracts the HTTP accept header and name multidict from query params. Based off
        `prometheus_client.exposition.MetricsHandler`.

        :param params: The request query params, defaults to None
        :type params: Optional[Mapping[str, Any]], optional
        :param headers: The HTTP request headers, defaults to None
        :type headers: Optional[Mapping[str, str]], optional
        :return: A tuple of response body and content type
        :rtype: Tuple[bytes, str]
        """
        params = params or {}
        headers = headers or {}
        encoder, content_type = choose_encoder(headers.get("Accept"))
        body = self.export_text(names=params.get("name[]"), encoder=encoder)
        return body, content_type
