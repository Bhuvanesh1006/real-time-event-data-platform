from pydantic import BaseModel
from typing import Dict, Optional


class EventPayload(BaseModel):
    event_id: str
    user_id: str
    event_type: str
    experiment_id: Optional[str]
    variant: Optional[str]
    event_ts: int
    producer_ts: int
    properties: Dict
    sdk_version: str
    source: str
    app_id: str
