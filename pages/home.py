from utils.translation import get_translation
from utils.db import get_recipes
from components.recipe_card import recipe_card
from components.recipe_detail import show_recipe_detail
import streamlit as st
from firebase_init import initialize_firebase

def show():
    """Display the home feed with recipes, search, and filtering options."""
    try:
        # Initialize Firebase if not already done
        initialize_firebase()
        
        # Check if we're viewing a specific recipe
        if 'viewing_recipe' in st.session_state:
            show_recipe_detail()
            return
            
        # Get language settings
        lang = st.session_state.get('lang', 'en')
        translations = st.session_state.get('translations', {})
        
        # Header with language-specific welcome
        st.header(translations.get(lang, {}).get("welcome", "Welcome to Recipe Share"))
        
        # Search and filter controls
        with st.container():
            search_col, filter_col = st.columns([3, 1])
            
            with search_col:
                search_query = st.text_input(
                    translations.get(lang, {}).get("search", "Search recipes..."),
                    key="home_search"
                )
            
            with filter_col:
                cuisine_options = ["All"] + list(translations.get("cuisines", {}).get("en", {}).keys())
                selected_cuisine = st.selectbox(
                    translations.get(lang, {}).get("filter", "Filter by"),
                    options=cuisine_options,
                    format_func=lambda x: translations.get("cuisines", {}).get(lang, {}).get(x, x),
                    key="cuisine_filter"
                )
        
        # Load recipes with error handling
        try:
            recipes = get_recipes()
            if not recipes:
                st.info(translations.get(lang, {}).get("no_recipes", "No recipes found"))
                return
            
            # Apply filters
            if search_query:
                recipes = [
                    r for r in recipes 
                    if search_query.lower() in r.get('name', {}).get('en', '').lower()
                    or any(search_query.lower() in name.lower() 
                          for name in r.get('name', {}).values())
                ]
            
            if selected_cuisine != "All":
                recipes = [r for r in recipes if r.get('category') == selected_cuisine]
            
            if not recipes:
                st.warning(translations.get(lang, {}).get("no_matches", "No matching recipes found"))
                return
            
            # Display recipes
            for i, recipe in enumerate(recipes):
                with st.container():
                    # Display the recipe card (handles its own view details button)
                    recipe_card(recipe)
                    
                    # Additional interactive elements below card
                    action_col1, action_col2 = st.columns(2)
                    
                    with action_col1:
                        # Like button with persistent count
                        like_key = f"like_{recipe['id']}"
                        if like_key not in st.session_state:
                            st.session_state[like_key] = recipe.get('likes', 0)
                        
                        if st.button(
                            f"❤️ {st.session_state[like_key]}",
                            key=f"like_btn_{recipe['id']}_{i}",
                            help=f"Like {recipe['name'].get('en', 'this recipe')}"
                        ):
                            st.session_state[like_key] += 1
                            # TODO: Update like count in database
                            # update_recipe_likes(recipe['id'], st.session_state[like_key])
                    
                    with action_col2:
                        # Comment button
                        if st.button(
                            f"💬 {len(recipe.get('comments', []))}",
                            key=f"comment_btn_{recipe['id']}_{i}",
                            help=f"View comments for {recipe['name'].get('en', 'this recipe')}"
                        ):
                            st.session_state['viewing_comments'] = recipe['id']
                            st.rerun()
                    
                    st.divider()  # Clean divider between recipes
        
        except Exception as e:
            st.error(f"Error loading recipes: {str(e)}")
            st.error("Please try refreshing the page")
    
    except Exception as e:
        st.error(f"Initialization error: {str(e)}")
        st.error("Please check your internet connection and try again")