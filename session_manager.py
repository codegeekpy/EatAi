# session_manager.py
import streamlit as st
from config import DEFAULT_LANGUAGE, TRANSLATIONS

def init_session():
    if 'lang' not in st.session_state:
        st.session_state.lang = DEFAULT_LANGUAGE
    if 'translations' not in st.session_state:
        st.session_state.translations = TRANSLATIONS

def get_current_language():
    return st.session_state.get('lang', DEFAULT_LANGUAGE)

def get_translations():
    return st.session_state.get('translations', {})