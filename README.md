`python -m venv ./venv/`

`source ./venv/bin/activate`

`uvicorn main:app --reload`

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

```bash
gcloud iam service-accounts create setup-svc-acct \
  --description="My service account for model hosting" \
  --display-name="setup-svc-acct"
gcloud projects add-iam-policy-binding host-a-model \
  --member="serviceAccount:setup-svc-acct@host-a-model.iam.gserviceaccount.com" \
  --role="roles/resourcemanager.projectIamAdmin"
```
