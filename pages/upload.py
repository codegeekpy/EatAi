import streamlit as st
import time
from components.protected import protected_page
from utils.db import save_recipe, upload_recipe_image, get_supabase
from utils.translation import get_translation
from components.cuisine_selector import cuisine_selector
from utils.error_handling import handle_upload_error

@protected_page
def show():
    """Secure recipe upload page with comprehensive error handling"""
    st.title(get_translation('upload_title'))
    
    with st.form("recipe_form", clear_on_submit=True):
        # Section 1: Recipe Information
        with st.expander("📝 Recipe Details", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                name_en = st.text_input(
                    get_translation('Name_English') + "*",
                    help="Primary name for the recipe"
                )
            with col2:
                name_te = st.text_input(
                    get_translation('Name_Telugu'),
                    help="Optional Telugu name"
                )
            name_hi = st.text_input(
                get_translation('Name_Hindi'),
                help="Optional Hindi name"
            )
            
            cuisine_selector()

        # Section 2: Image Upload
        with st.expander("🖼️ Recipe Image", expanded=True):
            uploaded_file = st.file_uploader(
                get_translation('image_upload_label'),
                type=["jpg", "jpeg", "png"],
                accept_multiple_files=False,
                help="Upload a clear image of your recipe (max 5MB)"
            )
            
            if uploaded_file:
                if uploaded_file.size > 5 * 1024 * 1024:  # 5MB limit
                    st.warning("Image too large! Please upload under 5MB")
                    uploaded_file = None
                else:
                    st.image(uploaded_file, caption="Preview", width=300)

        # Section 3: Recipe Content
        with st.expander("📝 Recipe Content", expanded=True):
            ingredients = st.text_area(
                get_translation('ingredients_label') + "*",
                help="Enter one ingredient per line",
                height=150
            )
            steps = st.text_area(
                get_translation('steps_label') + "*",
                help="Enter one step per line",
                height=200
            )
            tips = st.text_area(
                get_translation('tips_label'),
                help="Optional cooking tips",
                height=100
            )

        # Form submission
        submitted = st.form_submit_button(
            get_translation('submit_button'),
            use_container_width=True
        )
        
        if submitted:
            with st.spinner("Saving your recipe..."):
                try:
                    # Validation
                    if not all([name_en, ingredients, steps]):
                        raise ValueError("Please fill all required fields (*)")
                    
                    # Prepare recipe data
                    recipe_data = {
                        "name": {
                            "en": name_en,
                            "te": name_te or name_en,
                            "hi": name_hi or name_en
                        },
                        "category": st.session_state.cuisine,
                        "ingredients": [i.strip() for i in ingredients.split('\n') if i.strip()],
                        "steps": [s.strip() for s in steps.split('\n') if s.strip()],
                        "tips": [t.strip() for t in tips.split('\n') if t and t.strip()],
                        "author_id": st.session_state.user.id,
                        "author_name": st.session_state.user.email
                    }

                    # Phase 1: Save basic recipe (without image)
                    recipe_id = save_recipe(recipe_data)
                    if not recipe_id:
                        raise RuntimeError("Failed to save recipe to database")

                    # Phase 2: Handle image upload if provided
                    if uploaded_file:
                        try:
                            image_url = upload_recipe_image(uploaded_file, recipe_id)
                            if image_url:
                                # Update recipe with image URL
                                supabase = get_supabase()
                                update_response = supabase.table("recipes").update(
                                    {"image_url": image_url}
                                ).eq("id", recipe_id).execute()
                                
                                if not update_response.data:
                                    st.warning("Recipe saved but image URL couldn't be updated")
                        except Exception as img_error:
                            st.warning(f"Recipe saved but image upload failed: {handle_upload_error(img_error)}")

                    # Success message
                    st.success("Recipe saved successfully!")
                    st.balloons()
                    time.sleep(2)
                    st.rerun()

                except Exception as e:
                    st.error(f"Error: {handle_upload_error(e)}")
                    st.error("Please check your inputs and try again")

if __name__ == "__main__":
    show()