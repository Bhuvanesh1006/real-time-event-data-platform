# Event SDK

The SDK provides a simple, strongly-typed interface for applications to emit events into the data platform.

Applications interact only with the SDK — never directly with Kafka or Spark.

---

## Responsibilities

- Enforce event schema at the edge
- Validate event types and required fields
- Abstract ingestion endpoint details
- Provide a stable producer contract

---

## Example Usage

```python
from sdk import EventClient, Event

client = EventClient(
    endpoint="http://<ingestion-api-host>/events"
)

event = Event.create(
    user_id="user_123",
    event_type="page_view",
    experiment_id="exp_42",
    variant="A",
    properties={"page": "checkout"}
)

client.track(event)
