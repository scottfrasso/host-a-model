"""This module contains the dependencies for the FastAPI application."""
import os
from pydantic import BaseModel
from dotenv import load_dotenv

from services.ai import AIService
from services.db import RequestRepository
from services.pubsub import PubSubPublisher

load_dotenv()


class Settings(BaseModel):
    """Settings for the application."""

    ai_predictions_topic: str
    ai_model_location: str
    project_id: str


def get_settings() -> Settings:
    """Returns an instance of the settings."""
    ai_predictions_topic = os.getenv("AI_PREDICTION_TOPIC")
    project_id = os.getenv("PROJECT_ID")
    ai_model_location = os.getenv("MODEL_LOCATION")
    return Settings(
        ai_predictions_topic=ai_predictions_topic,
        project_id=project_id,
        ai_model_location=ai_model_location,
    )


def get_ai_service() -> AIService:
    """Returns an instance of the AI service."""
    settings = get_settings()
    service = AIService(settings.ai_model_location)
    print("AI service created")
    return service


def get_request_repository() -> RequestRepository:
    """Returns an instance of the request repository."""
    repository = RequestRepository()
    print("Request repository created")
    return repository


def get_pubsub_publisher() -> PubSubPublisher:
    """Returns an instance of the pubsub publisher."""
    settings = get_settings()
    publisher = PubSubPublisher(settings.project_id, settings.ai_predictions_topic)
    print("PubSub publisher created")
    return publisher
