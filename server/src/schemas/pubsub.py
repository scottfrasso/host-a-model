""" PubSub schemas """
from pydantic import BaseModel

from .ai import PatientModel


class RequestPubSubMessage(BaseModel):
    """
    Schema for a PubSub message.
    """

    id: str
    data: PatientModel
