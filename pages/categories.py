from components.protected import protected_page
from components.combined_selector import combined_selector
from utils.db import get_recipes_by_cuisine
import streamlit as st
@protected_page
def show():
    st.title("Browse Recipes")
    
    # Add selectors at the top
    combined_selector()
    
    # Get recipes for selected cuisine
    recipes = get_recipes_by_cuisine(st.session_state.cuisine)
    
    if not recipes:
        st.info("No recipes found for this cuisine")
        return
        
    for recipe in recipes:
        # Display recipe cards
        st.write(recipe['name'][st.session_state.lang])