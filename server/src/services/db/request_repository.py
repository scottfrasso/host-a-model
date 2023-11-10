from datetime import datetime, timedelta

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.client import Client, CollectionReference

from schemas import PatientModel, HeartDiseasResult, RequestState, RequestResponse

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(
    cred,
    {
        "projectId": "host-a-model",  # TODO: Get this from an environment variable
    },
)


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
        ttl_hours = 1
        expiration_time = datetime.utcnow() + timedelta(hours=ttl_hours)
        request = {
            "state": "NOT_STARTED",
            "data": patient_model.model_dump(),  # Data to be passed to the ML model
            "results": None,
            "expiration_time": expiration_time,
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

    def delete_expired_requests(self) -> None:
        """Deletes all requests that have expired."""
        now = datetime.utcnow()
        expired_requests = self._requests_collection.where(
            "expiration_time", "<", now
        ).stream()

        for request in expired_requests:
            print(f"Deleting doc {request.id} because it has expired")
            request.reference.delete()

        # Query for documents that don't have an 'expiration_time' field
        no_expiry_docs_query = self._requests_collection.where(
            "expiration_time", "==", None
        )
        no_expiry_docs = no_expiry_docs_query.stream()

        # Delete documents without an 'expiration_time' field
        for doc in no_expiry_docs:
            print(f"Deleting doc {doc.id} because it does not have an expiration time")
            doc.reference.delete()
