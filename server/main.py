"""
Starts up a basic server using FastAPI.
"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from ai_service import AIService, PatientModel
from dependencies import get_ai_service

# Create an instance of the FastAPI class
app = FastAPI()

# Set up CORS middleware options
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


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
