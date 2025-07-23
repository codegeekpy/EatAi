import firebase_admin
from firebase_admin import credentials, firestore
from firebase_init import initialize_firebase
initialize_firebase()
db = firestore.client()

def save_recipe(recipe):
    doc_ref = db.collection('recipes').document()
    recipe['id'] = doc_ref.id
    doc_ref.set(recipe)
    return recipe['id']

def get_recipes():
    return [doc.to_dict() for doc in db.collection('recipes').stream()]

def get_user_recipes(username):
    return [doc.to_dict() for doc in db.collection('recipes').where('author', '==', username).stream()]