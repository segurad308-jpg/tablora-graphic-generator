import streamlit as st
import os
from supabase import create_client, Client
from pathlib import Path
from dotenv import load_dotenv

# Walk up the directory tree to find .env, no matter how deeply nested the caller is.
current_path = Path(__file__).resolve()
project_root = current_path
while project_root.parent != project_root:
    if (project_root / '.env').exists():
        break
    project_root = project_root.parent
env_path = project_root / '.env'
if env_path.exists():
    load_dotenv(env_path)


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

def get_supabase_anon():
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

@st.cache_data(ttl=60)
def get_cached_profile(user_id):
    try:
        supabase = get_supabase()

        response = (
            supabase.table("profiles")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )

        if not response or not hasattr(response, "data"):
            return None

        if len(response.data) == 0:
            return None

        return response.data[0]
    except Exception as e:
        st.error(f"Erreur lors de la récupération du profil: {str(e)}")
        return None

@st.cache_data
def load_css(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)