# Ingestion API

The Ingestion API is the **controlled entry point** into the real-time data platform.

Applications never publish events directly to Kafka.  
All events flow through this service to ensure **validation, safety, and decoupling**.

---

## Why an Ingestion API?

Direct Kafka access from application services creates several problems:

- Tight coupling between applications and Kafka internals
- No centralized validation or schema enforcement
- Difficult auth, rate-limiting, and observability
- Unsafe producer behavior affecting cluster stability

This service solves those issues by acting as a **platform-owned ingestion boundary**.

---

## Responsibilities

- Accept events from applications via HTTP
- Validate incoming payloads
- Enrich or normalize events if required
- Publish events asynchronously to Kafka
- Shield applications from Kafka configuration and failures

---

## High-Level Flow

Application / SDK
↓
Ingestion API (FastAPI)
↓
Kafka topic (product_events)


---

## API Design

### Endpoint



POST /events


### Expected Payload

```json
{
  "event_id": "uuid",
  "user_id": "user_123",
  "event_type": "page_view",
  "event_time": 1710000000000,
  "experiment_id": "exp_42",
  "variant": "A",
  "properties": {
    "page": "checkout"
  }
}

Kafka Integration

Produces events to a dedicated Kafka topic

Uses asynchronous, non-blocking producers

Kafka acts as the durable event backbone

The API does not perform retries or buffering logic that belongs to Kafka itself.

Failure Handling

Invalid events are rejected at the API layer

Kafka publish failures are surfaced clearly

Application failures do not impact downstream consumers

This design ensures failures are isolated and observable.

Why FastAPI?

Lightweight and fast

Strong request validation

Easy extensibility for auth, rate-limiting, and metrics

Production-proven for ingestion services

Production Considerations (Future)

In a real production environment, this service would add:

Authentication (API keys / OAuth)

Rate limiting and throttling

Request-level metrics and logging

Dead-letter queues for invalid events

Horizontal scaling behind a load balancer

Role in the Platform

The Ingestion API allows the platform team to evolve Kafka, schemas, and downstream processing without requiring application changes.

It is a critical component for maintaining long-term platform stability.


---

