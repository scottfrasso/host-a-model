"""
Starts up a basic server using FastAPI.
"""
import json
from fastapi import Depends

from schemas import (
    PatientModel,
    HeartDiseasResult,
    RequestPubSubMessage,
    RequestResponse,
)
from services.pubsub import PubSubPublisher
from services.db import RequestRepository
from dependencies import (
    get_ai_service,
    get_pubsub_publisher,
    get_request_repository,
    get_settings,
    Settings,
)

from app_server import app


@app.post("/prediction")
async def request_prediction(
    patient_model: PatientModel,
    settings: Settings = Depends(get_settings),
    request_repository: RequestRepository = Depends(get_request_repository),
    pubsub_publisher: PubSubPublisher = Depends(get_pubsub_publisher),
) -> RequestResponse:
    """
    Creates a new request for a heart disease prediction.
    """
    response = request_repository.insert_request(patient_model)
    print(
        f"Using topic {settings.ai_predictions_topic} in project {settings.project_id}"
    )

    message = {
        "id": response.id,
        "data": patient_model.model_dump(),
    }
    pubsub_publisher.publish_message(json.dumps(message))
    return response


@app.get("/prediction/{request_id}")
async def get_request_prediction(
    request_id: str,
    request_repository: RequestRepository = Depends(get_request_repository),
) -> RequestResponse:
    """
    Gets a request for a heart disease prediction.
    """
    response = request_repository.query_request_by_id(request_id)
    return response
