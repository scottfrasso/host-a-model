from pydantic import BaseModel

from .ai import PatientModel


class RequestPubSubMessage(BaseModel):
    id: str
    data: PatientModel
