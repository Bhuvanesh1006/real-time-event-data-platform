# sdk/event_sdk/validators.py

from .schema import ALLOWED_EVENT_TYPES, ALLOWED_VARIANTS


def validate_event(event):
    if not event.user_id:
        raise ValueError("user_id is required")

    if event.event_type not in ALLOWED_EVENT_TYPES:
        raise ValueError(f"Invalid event_type: {event.event_type}")

    if event.variant and event.variant not in ALLOWED_VARIANTS:
        raise ValueError(f"Invalid variant: {event.variant}")

    if event.experiment_id and not event.variant:
        raise ValueError("variant required if experiment_id is present")
