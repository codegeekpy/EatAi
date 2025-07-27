from utils.db import get_supabase
from firebase_init import initialize_firebase
from firebase_admin import firestore

# Initialize both DBs
initialize_firebase()
supabase = get_supabase()
firestore_db = firestore.client()

recipes = firestore_db.collection('recipes').stream()

for recipe in recipes:
    recipe_data = recipe.to_dict()
    supabase.table('recipes').insert(recipe_data).execute()