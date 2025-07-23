import firebase_admin
from firebase_admin import auth, credentials
import streamlit as st
import json
from firebase_init import initialize_firebase
from firebase_admin import auth

initialize_firebase()  # Safe to call multiple times

class FirebaseAuthenticator:
    # Rest of your auth class remains the same
    def __init__(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate("firebase-key.json")
            firebase_admin.initialize_app(cred)
        
    def login(self, email, password):
        try:
            # Get the user by email to verify existence
            user = auth.get_user_by_email(email)
            
            # In a real app, you should verify password client-side
            # This is just for demonstration
            st.session_state.user = {
                'uid': user.uid,
                'email': user.email,
                'name': user.display_name or email.split('@')[0],
                'is_authenticated': True
            }
            return True
            
        except auth.UserNotFoundError:
            st.error("User not found. Please register first.")
        except exceptions.FirebaseError as e:
            st.error(f"Authentication error: {str(e)}")
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
        return False

authenticator = FirebaseAuthenticator()