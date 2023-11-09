"""This module contains the dependencies for the FastAPI application."""
from pydantic import BaseModel
from dotenv import load_dotenv

from ai import AIService
from request_repository import RequestRepository

load_dotenv()


class Settings(BaseModel):
    """Settings for the application."""

    topic_id: str
    project_id: str


def get_settings():
    """Returns an instance of the settings."""
    topic_id = os.getenv("TOPIC_ID")
    project_id = os.getenv("PROJECT_ID")
    return {
        "topic_id": topic_id,
        "project_id": project_id,
    }


def get_ai_service():
    """Returns an instance of the AI service."""
    service = AIService()
    print("AI service created")
    return service


def get_request_repository():
    """Returns an instance of the request repository."""
    repository = RequestRepository()
    print("Request repository created")
    return repository
