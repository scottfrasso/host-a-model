"""
Starts up a basic server using FastAPI.
"""
from fastapi import FastAPI, Depends

from ai_service import AIService, PatientModel
from dependencies import get_ai_service

# Create an instance of the FastAPI class
app = FastAPI()


# Define a GET route
@app.get("/")
async def read_root():
    """
    Returns a JSON object with a single key-value pair: "message": "Hello World!".
    """
    return {"message": "Hello World!"}


@app.post("/predict")
async def predict(
    patient_model: PatientModel, ai_service: AIService = Depends(get_ai_service)
):
    """
    Retrieve an item by ID.

    Args:
      item_id (int): The ID of the item to retrieve.

    Returns:
      dict: A dictionary containing the item ID and name.
    """
    return ai_service.predict(patient_model)
