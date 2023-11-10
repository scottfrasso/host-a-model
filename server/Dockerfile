# Start by pulling the official base image
FROM python:3.11-slim as build
RUN adduser --system --no-create-home nonroot

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the model so we can use it in the container
COPY ./model/heart_disease_random_forest_classifier.joblib /app/heart_disease_random_forest_classifier.joblib
ENV MODEL_LOCATION=/app/heart_disease_random_forest_classifier.joblib

# Copy the content of the local src directory to the working directory
COPY ./src/ /app/

USER nonroot

# Specify the command to run on container start
ENTRYPOINT [ "uvicorn" ]
