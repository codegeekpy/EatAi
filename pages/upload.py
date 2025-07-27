import streamlit as st
from components.protected import protected_page
from utils.db import save_recipe, upload_recipe_image
from utils.translation import get_translation
from components.cuisine_selector import cuisine_selector
@protected_page
def show():
    """Recipe upload page with image handling"""
    st.title(get_translation('upload_title'))
    with st.form("recipe_upload_form", clear_on_submit=True):
        # Recipe names
        name_en = st.text_input(get_translation('Name_English') + "*")
        name_te = st.text_input(get_translation('Name_Telugu'))
        name_hi = st.text_input(get_translation('Name_Hindi'))
        
        # Recipe details
        category = st.selectbox(
            get_translation('category_label'),
            options=["Andhra", "Telangana"],
            format_func=lambda x: get_translation(f'cuisine_{x.lower()}')
        )
        
        # Image upload
        uploaded_file = st.file_uploader(
            get_translation('image_upload_label'),
            type=["jpg", "jpeg", "png"]
        )
        
        # Recipe content
        ingredients = st.text_area(
            get_translation('ingredients_label') + "*",
            help=get_translation('ingredients_help')
        )
        steps = st.text_area(
            get_translation('steps_label') + "*",
            help=get_translation('steps_help')
        )
        
        submitted = st.form_submit_button(get_translation('submit_button'))
        
        if submitted:
            if not all([name_en, ingredients, steps]):
                st.error(get_translation('error_required_fields'))
                return
            
            try:
                # Process image if uploaded
                image_url = None
                if uploaded_file:
                    image_url = upload_recipe_image(
                        uploaded_file,
                        st.session_state.user.id,
                        uploaded_file.name
                    )
                
                # Prepare recipe data
                recipe_data = {
                    "name": {
                        "en": name_en,
                        "te": name_te or name_en,
                        "hi": name_hi or name_en
                    },
                    "category": category,
                    "ingredients": [i.strip() for i in ingredients.split('\n') if i.strip()],
                    "steps": [s.strip() for s in steps.split('\n') if s.strip()],
                    "author_id": st.session_state.user.id,
                    "author_name": st.session_state.user.email,
                    "image_url": image_url,
                    "likes": 0
                }
                
                # Save to database
                if save_recipe(recipe_data):
                    st.success(get_translation('upload_success'))
                    st.balloons()
                else:
                    st.error(get_translation('upload_error'))
                    
            except Exception as e:
                st.error(f"{get_translation('upload_error')}: {str(e)}")

# For direct testing
if __name__ == "__main__":
    show()