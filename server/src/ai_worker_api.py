""" FastAPI server for the AI worker. """
from fastapi import Depends

from services.ai import AIService
from services.db import RequestRepository
from dependencies import get_ai_service, get_request_repository
from schemas import RequestPubSubMessage, RequestState
from app_server import app


@app.post("/queued_prediction")
async def run_prediction(
    request: RequestPubSubMessage,
    request_repository: RequestRepository = Depends(get_request_repository),
    ai_service: AIService = Depends(get_ai_service),
):
    """
    Recieve a pubsub message and run a prediction.
    """
    print(f"Received request with ID: {request.id}")

    request_repository.update_request(
        request.id,
        RequestState.IN_PROGRESS,
    )

    results = ai_service.predict(request.data)

    request_repository.update_request(
        request.id,
        RequestState.COMPLETED,
        results.model_dump(),
    )

    print(f"Completed request with ID: {request.id}")

    return {
        "id": request.id,
    }


@app.post("/delete_expired_requests")
async def delete_expired_requests(
    request_repository: RequestRepository = Depends(get_request_repository),
) -> None:
    """
    Delete old requests from the database.
    """
    print("Deleting old requests")
    request_repository.delete_expired_requests()
    print("Old requests deleted")

    return {
        "message": "Old requests deleted",
    }
