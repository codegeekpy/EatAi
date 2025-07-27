import streamlit as st
from utils.auth import get_current_user

def protected_page(func):
    """Decorator to protect pages requiring authentication"""
    def wrapper(*args, **kwargs):
        if 'user' not in st.session_state:
            st.session_state.user = get_current_user()
        
        if st.session_state.user:
            return func(*args, **kwargs)
        else:
            st.warning("🔒 Please login to access this page")
            from pages import login
            login.show()
            return None
    return wrapper