from SDK.client import EventClient

client = EventClient(
    app_id="checkout-service",
    endpoint="http://13.62.230.183:8000/events"
)

client.track(
    user_id="u123",
    event_type="feature_exposed",
    experiment_id="exp_42",
    variant="B",
    properties={"page": "checkout"}
)

print("✅ SDK event sent")
