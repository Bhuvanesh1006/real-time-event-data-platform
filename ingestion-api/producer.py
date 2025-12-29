from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    key_serializer=lambda k: k.encode("utf-8"),
    acks="all",
    retries=5
)


def send_to_kafka(event: dict):
    producer.send(
        topic="product_events",
        key=event["user_id"],
        value=event
    )
