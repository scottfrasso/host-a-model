"""This module contains the dependencies for the FastAPI application."""
import os
from pydantic import BaseModel
from dotenv import load_dotenv

from ai import AIService
from pubsub import PubSubPublisher
from request_repository import RequestRepository

load_dotenv()


class Settings(BaseModel):
    """Settings for the application."""

    topic_id: str
    project_id: str


def get_settings() -> Settings:
    """Returns an instance of the settings."""
    topic_id = os.getenv("TOPIC_ID")
    project_id = os.getenv("PROJECT_ID")
    return Settings(topic_id=topic_id, project_id=project_id)


def get_ai_service() -> AIService:
    """Returns an instance of the AI service."""
    service = AIService()
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
    publisher = PubSubPublisher(settings.project_id, settings.topic_id)
    print("PubSub publisher created")
    return publisher
