import os
import streamlit as st
from PIL import Image
import requests
from io import BytesIO

def load_image(image_path=None):
    """
    Safely loads an image with multiple fallbacks:
    1. Try the provided path (URL or local)
    2. Try local placeholder
    3. Try remote placeholder
    4. Fallback to generated blank image
    """
    try:
        # Use default if no path provided
        if not image_path:
            return Image.open('assets/placeholder.jpg')
        
        # Handle URL case
        if image_path.startswith(('http://', 'https://')):
            response = requests.get(image_path, timeout=5)
            return Image.open(BytesIO(response.content))
        
        # Handle local file case
        if os.path.exists(image_path):
            return Image.open(image_path)
            
    except Exception:
        pass
    
    # Final fallbacks
    try:
        return Image.open('assets/error_placeholder.jpg')
    except:
        # Ultimate fallback - generate blank image
        return Image.new('RGB', (800, 600), color='gray')