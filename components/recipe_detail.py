import streamlit as st
from utils.translation import get_translation

def show_recipe_detail():
    if 'viewing_recipe' not in st.session_state:
        st.warning("No recipe selected")
        return
    
    recipe = st.session_state['viewing_recipe']
    
    # Back button
    if st.button("← Back to Feed"):
        del st.session_state['viewing_recipe']
        st.rerun()
    
    # Recipe header
    st.title(recipe['name'].get(st.session_state.lang, recipe['name']['en']))
    
    # Two-column layout
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Image display
        if recipe.get('image'):
            st.image(recipe['image'], use_column_width=True)
        else:
            st.image("assets/placeholder.jpg", use_column_width=True)
        
        # Metadata
        st.markdown(f"**Category:** {recipe.get('category', 'Unknown')}")
        st.markdown(f"**Prep Time:** {recipe.get('prep_time', 'N/A')} minutes")
        st.markdown(f"**Author:** {recipe.get('author', 'Anonymous')}")
    
    with col2:
        # Ingredients
        st.subheader("Ingredients")
        if isinstance(recipe.get('ingredients'), list):
            for ing in recipe['ingredients']:
                st.markdown(f"- {ing}")
        else:
            st.warning("No ingredients listed")
        
        # Preparation
        st.subheader("Preparation")
        if isinstance(recipe.get('steps'), list):
            for i, step in enumerate(recipe['steps'], 1):
                st.markdown(f"{i}. {step}")
        else:
            st.warning("No preparation steps available")
        
        # Tips (optional)
        if recipe.get('tips'):
            st.subheader("Tips")
            for tip in recipe['tips']:
                st.markdown(f"- {tip}")