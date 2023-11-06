"""
Starts up a basic server using FastAPI.
"""
from fastapi import FastAPI

# Create an instance of the FastAPI class
app = FastAPI()


# Define a GET route
@app.get("/")
async def read_root():
    """
    Returns a JSON object with a single key-value pair: "message": "Hello World!".
    """
    return {"message": "Hello World!"}


# Define another route that takes a path parameter
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    """
    Retrieve an item by ID.

    Args:
      item_id (int): The ID of the item to retrieve.

    Returns:
      dict: A dictionary containing the item ID and name.
    """
    return {"item_id": item_id, "name": "The name of the item"}
