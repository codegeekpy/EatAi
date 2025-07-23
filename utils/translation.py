import json
import streamlit as st
from pathlib import Path

# Cache translations for better performance
@st.cache_data
def load_translations():
    """Load translations from JSON file with error handling"""
    try:
        with open(Path(__file__).parent.parent / 'locales.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Translation file not found. Using empty translations.")
        return {}
    except json.JSONDecodeError:
        st.error("Invalid translation file format. Using empty translations.")
        return {}

def get_translation(key, fallback=None, lang=None):
    """
    Safe translation lookup with multiple fallback layers
    Args:
        key: Translation key
        fallback: Custom fallback text (optional)
        lang: Force specific language (optional)
    Returns:
        Translated string or fallback
    """
    translations = load_translations()
    lang = lang or st.session_state.get('lang', 'en')
    
    # Layer 1: Try requested language
    try:
        return translations[key][lang]
    except KeyError:
        pass
    
    # Layer 2: Try English fallback
    if lang != 'en':
        try:
            return translations[key]['en']
        except KeyError:
            pass
    
    # Layer 3: Try key prefixes (e.g., 'home.title' -> 'title')
    if '.' in key:
        prefix, suffix = key.rsplit('.', 1)
        try:
            return translations[prefix][lang][suffix]
        except KeyError:
            try:
                return translations[prefix]['en'][suffix]
            except KeyError:
                pass
    
    # Layer 4: Return fallback or key
    return fallback or key

def get_all_translations(key):
    """Get all language versions of a key"""
    translations = load_translations()
    try:
        return {
            lang: text 
            for lang, text in translations[key].items()
            if isinstance(text, str)
        }
    except KeyError:
        return {}