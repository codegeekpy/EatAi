import os
from PIL import Image, ImageDraw
import io

AVATAR_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'avatars')

def get_default_avatar(username):
    # Try local file first
    default_path = os.path.join(AVATAR_DIR, 'default.png')
    if os.path.exists(default_path):
        return default_path
    
    # Fallback to generated avatar
    img = Image.new('RGB', (150, 150), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)
    draw.text((75, 75), username[0].upper(), 
             fill=(70, 130, 180),  # Steel blue color
             font_size=72)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()