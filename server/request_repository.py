from typing import Optional
from enum import Enum

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.client import Client, CollectionReference
from pydantic import BaseModel

from ai import PatientModel, HeartDiseasResult

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(
    cred,
    {
        "projectId": "host-a-model",  # TODO: Get this from an environment variable
    },
)


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


class RequestRepository:
    """Repository for interacting with the Firestore database to store requests"""

    _db: Client
    _requests_collection: CollectionReference

    def __init__(self) -> None:
        self._db = firestore.client()
        self._requests_collection = self._db.collection("ml-requests")

    def insert_request(self, patient_model: PatientModel) -> RequestResponse:
        """Inserts a new request into the database and returns the document ID."""
        request_ref = self._requests_collection.document()
        request = {
            "state": "NOT_STARTED",
            "data": patient_model.model_dump(),  # Data to be passed to the ML model
            "results": None,  # Empty dict to hold results from the model
        }
        request_ref.set(request)

        return RequestResponse(id=request_ref.id, **request)

    def update_request(
        self, request_id: str, state: RequestState, results=None
    ) -> None:
        """Updates a request in the database with the given state and results."""
        request_ref = self._requests_collection.document(request_id)
        update_data = {"state": state}

        if results is not None:
            update_data["results"] = results

        request_ref.update(update_data)

    def query_request_by_id(self, document_id) -> RequestResponse:
        """Queries the database for requests with the given state."""
        doc_ref = self._requests_collection.document(document_id)
        doc = doc_ref.get()

        if not doc.exists:
            return None

        return RequestResponse(id=doc.id, **doc.to_dict())
