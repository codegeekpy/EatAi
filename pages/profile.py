import streamlit as st
from PIL import Image, ImageDraw
import io
import os

def create_default_avatar(username):
    """Generate a simple avatar with user's initial"""
    img = Image.new('RGB', (150, 150), color=(220, 220, 220))
    draw = ImageDraw.Draw(img)
    draw.text(
        (75, 75), 
        username[0].upper() if username else '?', 
        fill=(70, 130, 180),  # Nice blue color
        anchor="mm"  # Center the text
    )
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

def show():
    # Safe access with multiple fallbacks
    current_user = st.session_state.get('users', {}).get('current_user', {})
    username = current_user.get('username', 'Guest')
    
    st.title(f"👤 {username}'s Profile")
    
    with st.container():
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Avatar with multiple fallback options
            avatar = current_user.get('avatar')
            if not avatar:
                try:
                    # Try local file first
                    default_path = os.path.join('assets', 'default_avatar.png')
                    if os.path.exists(default_path):
                        avatar = default_path
                    else:
                        # Generate dynamic avatar as final fallback
                        avatar = create_default_avatar(username)
                except Exception as e:
                    st.error(f"Couldn't load avatar: {str(e)}")
                    avatar = create_default_avatar(username)
            
            st.image(avatar, width=150)
        
        with col2:
            # Safe statistics display
            uploaded_recipes = current_user.get('uploaded_recipes', [])
            st.write(f"**Recipes Uploaded:** {len(uploaded_recipes)}")
            st.write(f"**Total Likes:** {sum(r.get('likes', 0) for r in uploaded_recipes)}")
    
    # Recipe display section
    if uploaded_recipes:
        st.subheader("Your Recipes")
        for recipe in uploaded_recipes:
            with st.expander(recipe.get('title', 'Untitled Recipe')):
                st.write(f"**Likes:** {recipe.get('likes', 0)}")
                st.write(f"**Posted:** {recipe.get('timestamp', 'Unknown')}")
    else:
        st.info("You haven't uploaded any recipes yet.")