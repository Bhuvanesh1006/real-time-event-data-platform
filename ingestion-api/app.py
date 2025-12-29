from fastapi import FastAPI, HTTPException
from models import EventPayload
from producer import send_to_kafka

app = FastAPI()


@app.post("/events")
def ingest_event(event: EventPayload):
    try:
        send_to_kafka(event.dict())
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
