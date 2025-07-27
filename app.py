import streamlit as st
from streamlit_option_menu import option_menu
from utils.auth import sign_in, get_current_user, sign_out

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = get_current_user()
if 'lang' not in st.session_state:
    st.session_state.lang = 'en'  # Default language
# Add to your session state initialization
if 'cuisine' not in st.session_state:
    st.session_state.cuisine = 'telangana'  # Default cuisine
if 'translations' not in st.session_state:
    from utils.translation import load_translations
    st.session_state.translations = load_translations()
# Custom CSS for better menu styling
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        position: relative;
        height: 100vh;
    }
    .stSidebar > div:first-child {
        position: sticky;
        top: 0;
    }
    .css-1vq4p4l {
        gap: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def show_login_form():
    """Login form component with proper key management"""
    with st.form(key="login_form", clear_on_submit=True):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Login"):
            success, response = sign_in(email, password)
            if success:
                st.session_state.user = response.user
                st.rerun()
            else:
                st.error(f"Login failed: {response}")

def main():
    with st.sidebar:
        if st.session_state.user:
            # Authenticated Menu
            selected = option_menu(
                menu_title="Main Menu",
                options=["Home", "Upload", "Categories", "Profile"],
                icons=["house", "cloud-upload", "book", "person"],
                default_index=0,
                styles={
                    "container": {"padding": "0!important"},
                    "nav-link": {"font-size": "14px", "margin": "5px 0"}
                }
            )
            
            st.write(f"Logged in as: {st.session_state.user.email}")
            if st.button("Logout", key="unique_logout_btn"):
                sign_out()
                st.session_state.user = None
                st.rerun()
        else:
            # Guest Menu (simplified)
            selected = option_menu(
                menu_title="Main Menu",
                options=["Home", "Login"],
                icons=["house", "box-arrow-in-right"],
                default_index=0
            )
    
    # Page routing
    if not st.session_state.user:
        if selected == "Login":
            show_login_form()
        else:
            st.warning("Please login to access the app")
            show_login_form()
    else:
        # Import pages only when needed (prevents circular imports)
        if selected == "Home":
            from pages import home
            home.show()
        elif selected == "Upload":
            from pages import upload
            upload.show()
        elif selected == "Categories":
            from pages import categories
            categories.show()
        elif selected == "Profile":
            from pages import profile
            profile.show()

if __name__ == "__main__":
    main()