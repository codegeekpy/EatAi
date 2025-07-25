from utils.translation import get_translation
import streamlit as st
from PIL import Image
import io

def recipe_card(recipe):
    """Displays an interactive recipe card with enhanced features.
    
    Args:
        recipe (dict): Recipe dictionary containing:
            - id (str): Unique recipe identifier
            - name (dict): Multilingual name {'en': 'Name', 'te': 'నామం', ...}
            - category (str): Recipe category
            - author (str): Author username
            - image (bytes/str): Image data or path
            - likes (int): Number of likes
            - prep_time (int): Preparation time in minutes
    """
    with st.container():
        # Create columns for layout (image + content)
        img_col, content_col = st.columns([1, 3])
        
        # --- Image Column ---
        with img_col:
            try:
                if isinstance(recipe.get('image'), bytes):
                    # Handle binary image data
                    img = Image.open(io.BytesIO(recipe['image']))
                    st.image(img, width=150, caption=recipe['name'].get('en', ''))
                elif recipe.get('image'):
                    # Handle file path/URL
                    st.image(recipe['image'], width=150, caption=recipe['name'].get('en', ''))
                else:
                    # Fallback placeholder
                    st.image('assets/placeholder.jpg', width=150)
            except Exception as e:
                st.error(f"Error loading image: {str(e)}")
                st.image('assets/error_placeholder.jpg', width=150)
        
        # --- Content Column ---
        with content_col:
            # Display name in current language (with fallback)
            display_name = recipe['name'].get(
                st.session_state.get('lang', 'en'), 
                recipe['name'].get('en', 'Unnamed Recipe')
            )
            st.subheader(display_name)
            
            # Metadata row
            meta_col1, meta_col2, meta_col3 = st.columns([2, 2, 1])
            with meta_col1:
                # Translated category
                category_translation = get_translation(
                    'cuisines', 
                    {}
                ).get(recipe.get('category', ''), recipe.get('category', 'Unknown'))
                st.markdown(f"**{category_translation}**")
                
            with meta_col2:
                # Preparation time
                prep_time = recipe.get('prep_time')
                if prep_time:
                    st.markdown(f"⏱️ {prep_time} min")
                
            with meta_col3:
                # Like button with persistent state
                like_key = f"like_{recipe['id']}"
                if like_key not in st.session_state:
                    st.session_state[like_key] = recipe.get('likes', 0)
                
                if st.button(
                    f"❤️ {st.session_state[like_key]}",
                    key=f"like_btn_{recipe['id']}",
                    help="Like this recipe"
                ):
                    st.session_state[like_key] += 1
                    # Here you would update your database
                    # update_likes_in_db(recipe['id'], st.session_state[like_key])
            
            # Author information
            st.caption(f"👨‍🍳 By {recipe.get('author', 'Anonymous')}")
            
            # View Recipe button
            if st.button(
                "View Details →",
                key=f"view_btn_{recipe['id']}",
                type="primary",
                use_container_width=True
            ):
                st.session_state['selected_recipe'] = recipe
                st.rerun()
        
        st.divider()