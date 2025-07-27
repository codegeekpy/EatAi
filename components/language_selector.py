import streamlit as st
from utils.translation import get_translation

def language_selector():
    """Reusable language selector component"""
    if 'lang' not in st.session_state:
        st.session_state.lang = 'en'
    
    new_lang = st.selectbox(
        label=get_translation('language_selector'),
        options=['en', 'te', 'hi'],
        format_func=lambda x: get_translation(f'lang_{x}'),
        index=['en', 'te', 'hi'].index(st.session_state.lang),
        key='lang_selector'
    )
    
    if new_lang != st.session_state.lang:
        st.session_state.lang = new_lang
        st.rerun()