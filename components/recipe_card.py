from utils.translation import get_translation
import streamlit as st

def recipe_card(recipe):
    with st.container():
        cols = st.columns([1, 3])
        with cols[0]:
            st.image(recipe.get('image', 'placeholder.jpg'), width=150)
        with cols[1]:
            st.subheader(f"{recipe['name'].get(st.session_state.lang, recipe['name']['en'])}")
            st.caption(f"{get_translation('cuisines')[recipe['category']]} • By {recipe['author']}")
            
            if st.button("View Recipe"):
                st.session_state.view_recipe = recipe
                st.rerun()