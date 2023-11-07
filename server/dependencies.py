"""This module contains the dependencies for the FastAPI application."""
from ai_service import AIService


def get_ai_service():
    """Returns an instance of the AI service."""
    service = AIService()
    print("AI service created")
    return service
