from fastapi import FastAPI, Request, status, HTTPException
from pydantic import BaseModel

from pubsub_types import RequestPubSubMessage
from server import app


@app.post("/run_prediction")
async def run_prediction(request: RequestPubSubMessage):
    """
    Recieve a pubsub message and run a prediction.
    """
    print(f"Received request with ID: {request.id}")

    return {"status": "Message received"}
