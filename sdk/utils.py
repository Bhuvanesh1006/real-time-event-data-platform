# sdk/event_sdk/utils.py

SDK_VERSION = "1.0.0"
SOURCE = "python-sdk"


def build_payload(event, app_id):
    return {
        "event_id": event.event_id,
        "user_id": event.user_id,
        "event_type": event.event_type,
        "experiment_id": event.experiment_id,
        "variant": event.variant,
        "event_ts": event.event_ts,
        "producer_ts": event.producer_ts,
        "properties": event.properties,
        "sdk_version": SDK_VERSION,
        "source": SOURCE,
        "app_id": app_id
    }
