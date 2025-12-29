# sdk/event_sdk/schema.py

from typing import Dict, Optional
from dataclasses import dataclass, field
import time
import uuid

ALLOWED_EVENT_TYPES = {
    "page_view",
    "feature_exposed",
    "conversion"
}

ALLOWED_VARIANTS = {"A", "B"}


@dataclass
class Event:
    user_id: str
    event_type: str
    experiment_id: Optional[str]
    variant: Optional[str]
    properties: Dict

    # Auto-filled
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_ts: int = field(default_factory=lambda: int(time.time() * 1000))
    producer_ts: int = field(default_factory=lambda: int(time.time() * 1000))
