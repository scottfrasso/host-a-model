# Hosting a Machine Learning model in GCP

## Introduction

This Python service is designed to leverage Google Cloud Run for scalable, serverless execution. The service architecture involves an API instance that interacts with Google Cloud Pub/Sub and Firestore. It also includes an API worker that processes requests and stores results.

# Architecture

![Architecture diagram](docs/images/Host-a-model-arch.drawio.svg)

# Running the Service

## Environment Setup

Open this project in VS Code which shoudl open it in a dev container with Python.

Setup the Python virtual environment:

```bash
python -m venv ./server/venv/
source ./server/venv/bin/activate
python -m pip install --upgrade pip
```

## Authenticate with Google Cloud

Authenticate to interact with Google Cloud services:

```bash 
gcloud auth application-default login
```

## Start the APIs

Run the main and worker APIs:

```bash
uvicorn main_api:app --host 0.0.0.0 --port 8080 --reload
uvicorn ai_worker_api:app --host 0.0.0.0 --port 8081 --reload
```

# Infrastructure Setup

## Enable required Services

Before deploying, ensure the following Google Cloud services are enabled:

```bash
gcloud services enable cloudresourcemanager.googleapis.com
gcloud services enable iam.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

## Create a Docker Repository

```bash
gcloud artifacts repositories create host-a-model-repo \
 --repository-format=docker \
 --location=europe-central2 \
 --description="Host a Model Docker Repo"

 gcloud artifacts repositories list
```

## Configure Docker

```bash
gcloud auth configure-docker europe-central2-docker.pkg.dev
```

## Pulumi Stack Setup and Deployment

### Prerequisites

Ensure you have Pulumi installed. If not, install it from [Pulumi's official docs](https://www.pulumi.com/docs/get-started/install/)

## Initialize Pulumi Stack

Navigate to the Infrastructure Directory:

```bash
cd /infrastructure
```

Create a New Stack:

```bash
pulumi stack init your-stack-name
```

Set the Configuration

```bash
pulumi config set gcp:project your_project_name
pulumi config set gcp:region your_region
```

Deploy the Stack

```bash
pulumi up
```

## Service Configuration

### Firestore

Setup a Firestore database with a collection called `ml-requests`.

Lock Firestore to restrict access only to the Cloud Run services:

```
rules_version = '2';

service cloud.firestore {
  match /{document=**} {
    allow read, write: if false;
  }
}
```
