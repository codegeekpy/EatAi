import os
from supabase import create_client
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@st.cache_resource
def init_supabase():
    """Initialize and cache Supabase client"""
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    if not url or not key:
        raise ValueError("""
        Missing Supabase credentials. Please:
        1. Create a .env file
        2. Add SUPABASE_URL and SUPABASE_KEY
        3. Get credentials from Supabase Dashboard → Project Settings → API
        """)
    
    return create_client(url, key)

def get_supabase():
    """Get cached Supabase client"""
    if 'supabase' not in st.session_state:
        try:
            st.session_state.supabase = init_supabase()
        except Exception as e:
            st.error(f"Supabase initialization failed: {str(e)}")
            st.stop()
    return st.session_state.supabase