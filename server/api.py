"""
Starts up a basic server using FastAPI.
"""
import json
from fastapi import Depends

from ai import AIService, PatientModel, HeartDiseasResult
from dependencies import (
    get_ai_service,
    get_pubsub_publisher,
    get_request_repository,
    get_settings,
    Settings,
)
from pubsub import PubSubPublisher
from pubsub_types import RequestPubSubMessage
from request_repository import RequestRepository, RequestResponse

from server import app


# Define a GET route
@app.get("/")
async def read_root():
    """
    Returns a JSON object with a single key-value pair: "message": "Hello World!".
    """
    return {"message": "Hello World!"}


@app.post("/request_prediction")
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
    print(f"Using topic {settings.topic_id} in project {settings.project_id}")

    message = {
        "id": response.id,
        "data": patient_model.model_dump(),
    }
    pubsub_publisher.publish_message(json.dumps(message))
    return response


@app.get("/request_prediction/{request_id}")
async def get_request_prediction(
    request_id: str,
    request_repository: RequestRepository = Depends(get_request_repository),
) -> RequestResponse:
    """
    Gets a request for a heart disease prediction.
    """
    response = request_repository.query_request_by_id(request_id)
    return response


@app.post("/predict")
async def predict(
    patient_model: PatientModel, ai_service: AIService = Depends(get_ai_service)
) -> HeartDiseasResult:
    """
    Retrieve an item by ID.

    Args:
      item_id (int): The ID of the item to retrieve.

    Returns:
      dict: A dictionary containing the item ID and name.
    """
    return ai_service.predict(patient_model)
