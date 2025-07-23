from utils.translation import get_translation
from utils.db import get_recipes
from components.recipe_card import recipe_card
import streamlit as st
lang = st.session_state.get('lang', 'en')
translations = st.session_state.get('translations', {})
# Use:
from firebase_init import initialize_firebase
from utils.translation import get_translation
def show():
    lang = st.session_state.lang
    translations = st.session_state.translations
    
    st.header(translations[lang]["welcome"])
    recipes = get_recipes()
    if recipes:
        for recipe in recipes:
            recipe_card(recipe)
    else:
        st.info("No recipes found")