import streamlit as st
from utils.translation import get_translation

def cuisine_selector():
    """Reusable cuisine selector component"""
    if 'cuisine' not in st.session_state:
        st.session_state.cuisine = 'andhra'
        
    cuisines = {
        'andhra': get_translation('cuisine_andhra'),
        'telangana': get_translation('cuisine_telangana'),
        'punjabi': get_translation('cuisine_punjabi')
    }
    
    selected = st.selectbox(
        get_translation('cuisine_selector'),
        options=list(cuisines.keys()),
        format_func=lambda x: cuisines[x],
        index=list(cuisines.keys()).index(st.session_state.cuisine)
    )
    
    if selected != st.session_state.cuisine:
        st.session_state.cuisine = selected
        st.rerun()