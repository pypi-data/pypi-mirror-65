from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import UUID


@dataclass(frozen=True)
class PredictionContext:
    entity_id: UUID
    features: List[float]
    request_body: str
    server_id: str
    output: float
    created_at: datetime
