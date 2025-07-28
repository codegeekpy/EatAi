import streamlit as st
from utils.translation import get_translation

def cuisine_filter():
    """Reusable cuisine filter component"""
    cuisines = {
        'all': get_translation('filter_all'),
        'andhra': get_translation('cuisine_andhra'),
        'telangana': get_translation('cuisine_telangana')
    }
    
    return st.selectbox(
        get_translation('filter_label'),
        options=list(cuisines.keys()),
        format_func=lambda x: cuisines[x],
        key='cuisine_filter'
    )