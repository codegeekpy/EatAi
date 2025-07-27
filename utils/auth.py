from utils.supabase_init import get_supabase
import streamlit as st

def sign_in(email: str, password: str):
    """Authenticate user with email/password"""
    supabase = get_supabase()
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return True, response
    except Exception as e:
        return False, str(e)

def get_current_user():
    """Get currently logged in user"""
    supabase = get_supabase()
    try:
        return supabase.auth.get_user()
    except:
        return None

def sign_out():
    """Log out current user"""
    supabase = get_supabase()
    supabase.auth.sign_out()
    st.session_state.user = None