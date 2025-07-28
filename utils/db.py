from utils.supabase_init import get_supabase
import streamlit as st
def save_recipe(recipe_data):
    supabase = get_supabase()
    response = supabase.table('recipes').insert(recipe_data).execute()
    return response.data[0]['id'] if response.data else None

def get_recipes():
    supabase = get_supabase()
    response = supabase.table('recipes').select("*").execute()
    return response.data

def get_recipe_by_id(recipe_id):
    supabase = get_supabase()
    response = supabase.table('recipes').select("*").eq('id', recipe_id).execute()
    return response.data[0] if response.data else None

def update_recipe_likes(recipe_id, likes):
    supabase = get_supabase()
    supabase.table('recipes').update({'likes': likes}).eq('id', recipe_id).execute()

def upload_recipe_image(file, recipe_id=None):
    """Robust image upload handler with proper error checking"""
    supabase = get_supabase()
    
    try:
        # 1. Verify file exists and is valid
        if not file or not hasattr(file, 'read'):
            raise ValueError("Invalid file object provided")
        
        # 2. Prepare upload path
        user_id = st.session_state.user.id
        file_ext = file.name.split('.')[-1].lower()
        valid_extensions = ['jpg', 'jpeg', 'png']
        
        if file_ext not in valid_extensions:
            raise ValueError(f"Invalid file type. Only {', '.join(valid_extensions)} allowed")
        
        # 3. Create unique filename
        timestamp = int(time.time())
        filename = f"{timestamp}_{file.name}"
        file_path = f"user_{user_id}/{filename}" if not recipe_id else f"recipes/{recipe_id}/{filename}"
        
        # 4. Read file content
        file_content = file.read()
        
        # 5. Upload with proper headers
        headers = {
            "Authorization": f"Bearer {supabase.auth.get_session().access_token}",
            "Content-Type": f"image/{file_ext}"
        }
        
        response = supabase.storage.from_("recipe-images").upload(
            path=file_path,
            file=file_content,
            file_options=headers
        )
        
        # 6. Verify upload success
        if not response or 'Key' not in response:
            raise ValueError("Upload failed - no response key received")
        
        # 7. Get public URL
        return supabase.storage.from_("recipe-images").get_public_url(file_path)
        
    except Exception as e:
        st.error(f"Image upload failed: {str(e)}")
        return None
    

def get_recipes_by_cuisine(cuisine):
    supabase = get_supabase()
    response = supabase.table('recipes') \
                     .select('*') \
                     .eq('category', cuisine) \
                     .execute()
    return response.data


def save_recipe(recipe_data):
    """Save recipe with proper authentication"""
    supabase = get_supabase()
    try:
        # Ensure user is authenticated
        if not st.session_state.user:
            raise Exception("User not authenticated")
        
        # Add author information
        recipe_data.update({
            "author_id": st.session_state.user.id,
            "author_name": st.session_state.user.email
        })
        
        # Insert with auth headers
        response = supabase.table("recipes").insert(recipe_data).execute()
        
        if not response.data:
            raise Exception("No data returned from insert")
            
        return response.data[0]['id']
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        return None