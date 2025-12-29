from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

producer.send("product_events", {"source": "laptop-test", "msg": "hello kafka"})
producer.flush()

print("Message sent")
