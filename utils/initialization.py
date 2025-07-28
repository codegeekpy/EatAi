import streamlit as st
from utils.translation import load_translations

def initialize_app():
    """Initialize all app requirements"""
    if not st.session_state.get('initialized'):
        # Session state setup
        st.session_state.update({
            'lang': 'en',
            'translations': load_translations(),
            'initialized': True
        })
        
        # Page config
        st.set_page_config(
            page_title="Recipe Share",
            page_icon="🍳",
            layout="wide"
        )