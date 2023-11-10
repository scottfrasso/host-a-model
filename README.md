`python -m venv ./venv/`

`source ./venv/bin/activate`

`uvicorn api:app --host 0.0.0.0 --port 8080 --reload`

`uvicorn ai_worker_api:app --host 0.0.0.0 --port 8081 --reload`

`gcloud auth application-default login`

Enable the services that pulumi will use

```bash
gcloud services enable cloudresourcemanager.googleapis.com
gcloud services enable iam.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

Create a repo

```bash
gcloud artifacts repositories create host-a-model-repo \
 --repository-format=docker \
 --location=europe-central2 \
 --description="Host a Model Docker Repo"

 gcloud artifacts repositories list
```

Configure Docker to use the gcloud command-line tool as a credential helper

```bash
gcloud auth configure-docker europe-central2-docker.pkg.dev
```


Lock firestore

```
rules_version = '2';

service cloud.firestore {
  match /{document=**} {
   allow read, write: if false;
	}
}
```