import streamlit as st
import pandas as pd
from utils.translation import get_translation  # Using safe translation utility

def show():
    # Safe language and translations access
    lang = st.session_state.lang
    translations = st.session_state.translations
    
    st.header(translations[lang]["welcome"])
    st.subheader(get_translation('explore_cuisines', lang))
    
    # Main categories with translations
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"{get_translation('andhra_cuisine', lang)} 🍛"):
            st.session_state.selected_category = "Andhra"
    with col2:
        if st.button(f"{get_translation('telangana_cuisine', lang)} 🍲"):
            st.session_state.selected_category = "Telangana"
    
    # Show recipes if category selected
    if 'selected_category' in st.session_state:
        category = st.session_state.selected_category
        st.subheader(f"{category} {get_translation('recipes', lang)}")
        
        # Safe recipes access
        recipes_df = st.session_state.get('recipes', pd.DataFrame())
        
        if not recipes_df.empty and 'category' in recipes_df.columns:
            filtered_recipes = recipes_df[
                recipes_df['category'].str.contains(category, na=False)
            ]
            
            if not filtered_recipes.empty:
                for _, recipe in filtered_recipes.iterrows():
                    with st.expander(f"{recipe.get('english_name', 'Unnamed Recipe')} ({recipe.get('local_name', '')})"):
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            st.image(
                                recipe.get('image', 'https://via.placeholder.com/150'), 
                                width=150
                            )
                        with col2:
                            # Ingredients
                            st.write(f"**{get_translation('ingredients', lang)}:**")
                            for ing in recipe.get('ingredients', []):
                                st.write(f"- {ing}")
                            
                            # Preparation steps
                            st.write(f"\n**{get_translation('preparation', lang)}:**")
                            for i, step in enumerate(recipe.get('steps', []), 1):
                                st.write(f"{i}. {step}")
                            
                            # Tips (optional)
                            if recipe.get('tips'):
                                st.write(f"\n**{get_translation('tips', lang)}:**")
                                for tip in recipe.get('tips', []):
                                    st.write(f"- {tip}")
            else:
                st.info(get_translation('no_recipes_category', lang).format(category=category))
        else:
            st.info(get_translation('no_recipes', lang))