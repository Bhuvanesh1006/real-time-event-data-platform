# sdk/event_sdk/client.py

import requests
from .schema import Event
from .validation import validate_event
from .utils import build_payload
from .exceptions import SDKValidationError, DeliveryError


class EventClient:
    def __init__(self, app_id: str, endpoint: str, timeout=4):
        self.app_id = app_id
        self.endpoint = endpoint
        self.timeout = timeout

    def track(
        self,
        user_id: str,
        event_type: str,
        experiment_id=None,
        variant=None,
        properties=None
    ):
        try:
            event = Event(
                user_id=user_id,
                event_type=event_type,
                experiment_id=experiment_id,
                variant=variant,
                properties=properties or {}
            )

            validate_event(event)
            payload = build_payload(event, self.app_id)

            response = requests.post(
                self.endpoint,
                json=payload,
                timeout=self.timeout
            )

            if response.status_code != 200:
                raise DeliveryError(
                    f"Failed to deliver event: {response.text}"
                )

        except Exception as e:
            raise SDKValidationError(str(e))
