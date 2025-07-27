from utils.supabase_init import get_supabase

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

def upload_recipe_image(file, recipe_id):
    supabase = get_supabase()
    file_path = f"{recipe_id}/{file.name}"
    res = supabase.storage.from_("recipe-images").upload(file_path, file)
    return supabase.storage.from_("recipe-images").get_public_url(file_path)

def get_recipes_by_cuisine(cuisine):
    supabase = get_supabase()
    response = supabase.table('recipes') \
                     .select('*') \
                     .eq('category', cuisine) \
                     .execute()
    return response.data