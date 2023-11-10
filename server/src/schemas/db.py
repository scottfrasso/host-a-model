"""Database schemas."""
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from .ai import PatientModel, HeartDiseasResult


class RequestState(str, Enum):
    """Enum for the state of a request."""

    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"


class RequestResponse(BaseModel):
    """Response model for a request."""

    id: str
    state: RequestState
    data: PatientModel
    results: Optional[HeartDiseasResult]
