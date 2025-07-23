import streamlit as st
from streamlit_option_menu import option_menu
from utils.auth import authenticator
from utils.translation import get_translation
import json
from firebase_init import initialize_firebase
from session_manager import init_session
init_session() 
# Initialize Firebase
initialize_firebase()

# Initialize all session state variables
def init_session_state():
    """Initialize all required session state variables"""
    defaults = {
        'lang': 'en',
        'user': None,
        'users': {
            'current_user': {
                'username': 'Guest',
                'email': None,
                'favorites': [],
                'uploaded_recipes': []
            }
        }
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Initialize session state
init_session_state()

# Page configuration
st.set_page_config(
    page_title="Indian Recipe Share",
    page_icon="🍛",
    layout="wide"
)

# Sidebar - Authentication and Language
with st.sidebar:
    st.title("🍛 Recipe Share")
    
    # Language Selector
    new_lang = st.selectbox(
        "🌐 Language",
        options=["en", "te", "hi"],
        index=["en", "te", "hi"].index(st.session_state.lang),
        format_func=lambda x: {"en": "English", "te": "తెలుగు", "hi": "हिंदी"}[x]
    )
    
    # Update language if changed
    if new_lang != st.session_state.lang:
        st.session_state.lang = new_lang
        st.rerun()
    
    # Authentication Section
    if st.session_state.user is None:
        st.header("Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            try:
                if authenticator.login(email, password):
                    # Update current user in session state
                    st.session_state.users['current_user'] = {
                        'username': email.split('@')[0],
                        'email': email,
                        'favorites': [],
                        'uploaded_recipes': []
                    }
                    st.session_state.user = email  # Set authenticated user
                    st.rerun()
            except Exception as e:
                st.error(f"Login failed: {str(e)}")
    else:
        user_data = st.session_state.users['current_user']
        st.header(f"Welcome, {user_data['username']}!")
        if st.button("Logout"):
            authenticator.logout()
            st.session_state.user = None
            st.rerun()

# Main App Content
if st.session_state.user is None:
    st.warning("Please login to access the app")
    st.stop()

# Navigation Menu
selected = option_menu(
    menu_title=None,
    options=["Home", "Upload", "AI Chef", "Profile"],
    icons=["house", "cloud-upload", "robot", "person"],
    default_index=0,
    orientation="horizontal"
)

# Page Routing
if selected == "Home":
    from pages import home
    home.show()
elif selected == "Upload":
    from pages import upload
    upload.show()
elif selected == "AI Chef":
    from pages import ai_chef
    ai_chef.show()
elif selected == "Profile":
    from pages import profile
    profile.show()