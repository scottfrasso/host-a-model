"""This module defines the FastAPI application."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


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


# @app.middleware("http")
# async def log_requests(request: Request, call_next):
#     body = await request.body()
#     print(f"Request body: {body.decode()}")
#     response: Response = await call_next(request)
#     return response
