from utils.translation import get_translation
from utils.db import save_recipe
import streamlit as st
from PIL import Image
import io

def show():
    st.title(get_translation('upload_title'))
    
    with st.form("recipe_form", clear_on_submit=True):
        # Recipe Names (Multilingual)
        col1, col2 = st.columns(2)
        with col1:
            name_en = st.text_input("Name (English)*", help="Required field")
        with col2:
            name_te = st.text_input("Name (Telugu)", help="Optional")
        
        name_hi = st.text_input("Name (Hindi)", help="Optional")

        # Category Selection
        category = st.selectbox(
            get_translation('category_label'),
            options=["Andhra", "Telangana"],
            format_func=lambda x: get_translation(f'cuisine_{x.lower()}')
        )

        # Image Upload
        uploaded_image = st.file_uploader(
            get_translation('upload_image_label'),
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=False
        )

        # Recipe Content
        ingredients = st.text_area(
            get_translation('ingredients_label') + "*",
            help="Enter one ingredient per line"
        )
        steps = st.text_area(
            get_translation('steps_label') + "*",
            help="Enter one step per line"
        )
        tips = st.text_area(get_translation('tips_label'))

        # Form Submission
        if st.form_submit_button(get_translation('submit_button')):
            if not name_en:
                st.error(get_translation('error_name_required'))
                return

            # Process image if uploaded
            image_data = None
            if uploaded_image is not None:
                try:
                    # Validate and resize image
                    img = Image.open(uploaded_image)
                    img.thumbnail((800, 800))  # Resize while maintaining aspect ratio
                    img_byte_arr = io.BytesIO()
                    img.save(img_byte_arr, format='JPEG')
                    image_data = img_byte_arr.getvalue()
                except Exception as e:
                    st.error(get_translation('error_image_processing'))
                    st.stop()

            # Save recipe data
            recipe_data = {
                'name': {
                    'en': name_en,
                    'te': name_te if name_te else name_en,
                    'hi': name_hi if name_hi else name_en
                },
                'category': category,
                'ingredients': [i.strip() for i in ingredients.split('\n') if i.strip()],
                'steps': [s.strip() for s in steps.split('\n') if s.strip()],
                'tips': [t.strip() for t in tips.split('\n') if t.strip()],
                'author': st.session_state.user,
                'image': image_data,  # Can be None
                'likes': 0,
                'comments': []
            }

            try:
                save_recipe(recipe_data)
                st.success(get_translation('success_recipe_saved'))
            except Exception as e:
                st.error(get_translation('error_saving_recipe') + f": {str(e)}")