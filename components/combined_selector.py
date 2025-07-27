import streamlit as st
from .language_selector import language_selector
from .cuisine_selector import cuisine_selector

def combined_selector():
    """Displays both language and cuisine selectors in a compact layout"""
    col1, col2 = st.columns(2)
    with col1:
        language_selector()
    with col2:
        cuisine_selector()