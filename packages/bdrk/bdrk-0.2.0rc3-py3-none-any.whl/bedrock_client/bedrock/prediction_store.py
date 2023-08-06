import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import List
from uuid import UUID, uuid4

from fluent.asyncsender import FluentSender
from spanlib.infrastructure.kubernetes.env_var import (
    BEDROCK_ENDPOINT_ID,
    BEDROCK_FLUENTD_ADDR,
    BEDROCK_FLUENTD_PREFIX,
    BEDROCK_SERVER_ID,
    POD_NAME,
)


@dataclass(frozen=True)
class Prediction:
    entity_id: UUID
    features: List[float]
    request_body: str
    server_id: str
    output: float
    created_at: datetime


class PredictionStore:
    def __init__(self):
        # Environment variables will be injected by model server chart
        pod_name = os.environ.get(POD_NAME, "unknown-pod")
        endpoint_id = os.environ.get(BEDROCK_ENDPOINT_ID, "unknown-endpoint")
        fluentd_prefix = os.environ.get(BEDROCK_FLUENTD_PREFIX, "models.predictions")
        fluentd_server = os.environ.get(
            BEDROCK_FLUENTD_ADDR, "fluentd-logging.core.svc.cluster.local"
        )
        self._sender: FluentSender = FluentSender(
            tag=f"{fluentd_prefix}.{endpoint_id}.{pod_name}",
            host=fluentd_server,
            queue_circular=True,
        )

    def _save(self, prediction: Prediction):
        """
        Stores the prediction asynchronously to fluentd.

        :param prediction: The completed prediction
        :type prediction: Prediction
        """
        data = asdict(prediction)
        data["entity_id"] = str(prediction.entity_id)
        # fluentd's msgpack version does not yet support serializing datetime
        data["created_at"] = int(prediction.created_at.timestamp())
        # TODO: Supports bytes type which is not json serializable
        self._sender.emit_with_time(label=None, timestamp=data["created_at"], data=data)

    def log_prediction(self, request_body: str, features: List[float], output: float):
        """
        Stores predictions asynchronously in the background.

        :param request_body: The body of this prediction request
        :type request_body: str
        :param features: The transformed feature vector
        :type features: List[float]
        :param output: The model output
        :type output: float
        """
        self._save(
            Prediction(
                request_body=request_body,
                features=features,
                output=output,
                entity_id=uuid4(),
                server_id=os.environ.get(BEDROCK_SERVER_ID, "unknown-server"),
                created_at=datetime.now(tz=timezone.utc),
            )
        )
