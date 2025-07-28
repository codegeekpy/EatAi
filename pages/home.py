import streamlit as st
from utils.translation import get_translation
from utils.db import get_recipes
from components.recipe_card import recipe_card
from components.recipe_detail import show_recipe_detail
from components.language_selector import language_selector
from components.cuisine_filter import cuisine_filter
from utils.initialization import initialize_app

def show():
    """Modern home feed with enhanced UI and performance"""
    # Initialize app (session state, translations, etc.)
    initialize_app()
    
    # Show recipe detail if viewing specific recipe
    if 'viewing_recipe' in st.session_state:
        show_recipe_detail()
        return
    
    # Page header with responsive layout
    header_col1, header_col2 = st.columns([3, 1])
    with header_col1:
        st.title(get_translation('welcome'))
    with header_col2:
        language_selector()
    
    # Search and filter section
    with st.expander("🔍 Search & Filter", expanded=True):
        search_query = st.text_input(
            get_translation('search'),
            placeholder=get_translation('search_placeholder'),
            key="home_search"
        )
        selected_cuisine = cuisine_filter()
    
    # Recipe display section
    try:
        recipes = load_filtered_recipes(search_query, selected_cuisine)
        
        if not recipes:
            show_empty_state()
            return
            
        display_recipe_grid(recipes)
        
    except Exception as e:
        show_error_state(e)

def load_filtered_recipes(search_query, selected_cuisine):
    """Load and filter recipes with error handling"""
    recipes = get_recipes()
    
    # Apply search filter
    if search_query:
        search_lower = search_query.lower()
        recipes = [
            r for r in recipes 
            if (search_lower in r.get('name', {}).get('en', '').lower() or
                any(search_lower in name.lower() for name in r.get('name', {}).values()))
        ]
    
    # Apply cuisine filter
    if selected_cuisine != "All":
        recipes = [r for r in recipes if r.get('category') == selected_cuisine]
    
    return recipes

def display_recipe_grid(recipes):
    """Display recipes in responsive grid"""
    cols = st.columns(3)  # 3-column layout
    
    for i, recipe in enumerate(recipes):
        with cols[i % 3]:  # Cycle through columns
            with st.container(border=True):  # Card-like container
                recipe_card(recipe)
                
                # Action buttons
                action_col1, action_col2 = st.columns(2)
                with action_col1:
                    display_like_button(recipe, i)
                with action_col2:
                    display_comment_button(recipe, i)

def display_like_button(recipe, index):
    """Interactive like button with persistence"""
    like_key = f"like_{recipe['id']}"
    if like_key not in st.session_state:
        st.session_state[like_key] = recipe.get('likes', 0)
    
    if st.button(
        f"❤️ {st.session_state[like_key]}",
        key=f"like_{recipe['id']}_{index}",
        help=get_translation('like_help')
    ):
        st.session_state[like_key] += 1
        # update_recipe_likes(recipe['id'], st.session_state[like_key])

def display_comment_button(recipe, index):
    """Comment button with count"""
    comment_count = len(recipe.get('comments', []))
    if st.button(
        f"💬 {comment_count}",
        key=f"comment_{recipe['id']}_{index}",
        help=get_translation('comment_help')
    ):
        st.session_state['viewing_comments'] = recipe['id']
        st.rerun()

def show_empty_state():
    """Display when no recipes found"""
    st.markdown("""
    <div style="text-align:center; padding:40px">
        <h3>🍳 No recipes found</h3>
        <p>Be the first to share your recipe!</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button(get_translation('upload_prompt')):
        st.session_state.page = "Upload"
        st.rerun()

def show_error_state(error):
    """Display error message with recovery options"""
    st.error(f"Error loading recipes: {str(error)}")
    
    recovery_col1, recovery_col2 = st.columns(2)
    with recovery_col1:
        if st.button("🔄 Refresh Page"):
            st.rerun()
    with recovery_col2:
        if st.button("📋 Report Issue"):
            st.session_state.show_feedback = True
    
    if st.session_state.get('show_feedback'):
        with st.form("feedback_form"):
            st.text_area("Describe the issue")
            if st.form_submit_button("Submit"):
                st.success("Thank you for your feedback!")
                st.session_state.show_feedback = False

if __name__ == "__main__":
    show()