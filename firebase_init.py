import firebase_admin
from firebase_admin import credentials

# Singleton Firebase initialization
_initialized = False

def initialize_firebase():
    global _initialized
    if not _initialized:
        cred = credentials.Certificate("firebase-key.json")
        firebase_admin.initialize_app(cred)
        _initialized = True