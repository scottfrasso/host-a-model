import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred)

db = firestore.client()


def insert_request():
    # doc_ref = db.collection(collection_name).document(document_id)
    # doc_ref.set(data)
    pass
