# RUNBOOK — Real-Time Event Data Platform

This document describes how to **operate, monitor, and recover** the real-time event data platform.

It is written from the perspective of a **data platform owner**, not a BI user.

---

## Platform Components

- SDK (Application-facing producer contract)
- Ingestion API (FastAPI)
- Kafka (event backbone)
- Spark Structured Streaming (Bronze & Silver)
- AWS S3 (data lake storage)

---

## Service Startup Order

Services must be started in the following order:

1. **Zookeeper**
2. **Kafka Broker**
3. **Ingestion API**
4. **Spark Streaming Jobs**
5. **SDK / Application Producers**

Starting Spark or the API before Kafka will result in failures.

---

## Kafka Operations

### Check Kafka is Running
```bash
jps
Expected:

Kafka
QuorumPeerMain

Restart Kafka
bin/kafka-server-stop.sh
bin/kafka-server-start.sh config/server.properties

Verify Topic
bin/kafka-topics.sh --list --bootstrap-server localhost:9092

Ingestion API Operations
Start API
uvicorn app:app --host 0.0.0.0 --port 8000

Health Check
curl http://<host>:8000/docs


If Swagger UI loads, the service is healthy.

Spark Streaming Operations
Bronze Job
spark-submit spark/streaming/bronze_stream.py

Silver Job
spark-submit spark/streaming/silver_stream.py

Verifying Data Flow
Kafka → Bronze

Check S3 path:

s3://<bucket>/bronze/events/


Check checkpoint:

s3://<bucket>/checkpoints/bronze/

Bronze → Silver

Check S3 path:

s3://<bucket>/silver/events/


Check checkpoint:

s3://<bucket>/checkpoints/silver/


Presence of checkpoints confirms streaming job health.

Failure Scenarios & Recovery
Kafka Broker Crash

Impact: Ingestion API cannot publish events

Recovery:

Restart Kafka

API automatically resumes publishing

No data loss due to Kafka durability

Spark Streaming Job Crash

Impact: Temporary delay in data availability

Recovery:

Restart Spark job

Job resumes from last checkpoint

No duplicate data due to exactly-once semantics

Bad Events / Schema Issues

Impact: Spark job may fail on malformed records

Recovery:

Fix validation logic (SDK / API)

Restart Spark job

Replay data from Bronze if required

Replay & Backfills

To replay historical data:

Stop Silver job

Delete Silver output and checkpoint directories

Restart Silver job reading from Bronze

Bronze data remains immutable and acts as the system of record.

Observability (Current)

Spark UI for job metrics

Kafka logs for producer/consumer errors

Application logs for ingestion failures

Observability (Future Improvements)

Structured logging

Metrics (ingestion rate, lag, failures)

Alerts on stalled streams

Dead-letter queues for invalid events

Cost & Resource Considerations

Single-node Kafka for development

Spark jobs tuned for small EC2 instances

S3 used for low-cost, durable storage

Architecture designed to scale horizontally in production

Operational Ownership Notes

Bronze layer is immutable

Silver can always be rebuilt

Kafka decouples producers and consumers

Platform favors correctness over immediate availability

Summary

This runbook ensures:

Predictable operations

Safe recovery from failures

Clear ownership boundaries

Replayable and auditable data pipelines