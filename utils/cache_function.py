import streamlit as st
import os
from supabase import create_client, Client
from pathlib import Path
from dotenv import load_dotenv
import datetime

# Load environment variables
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

@st.cache_resource
def get_supabase():
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

supabase: Client = get_supabase()


# Cache functions
@st.cache_data(ttl=60)
def get_cached_profile(user_id):
    try:
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
def has_access_cached(profile):
    if not profile:
        return False

    plan = profile.get("plan")
    is_premium = profile.get("is_premium", False)
    sub_end_str = profile.get("subscription_end")

    # ───────── PREMIUM CHECK ─────────
    if plan == "premium" and is_premium:
        if sub_end_str:
            try:
                sub_end = datetime.datetime.fromisoformat(sub_end_str.replace("Z", "+00:00"))
            except Exception:
                sub_end = datetime.datetime.strptime(sub_end_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                sub_end = sub_end.replace(tzinfo=datetime.timezone.utc)
            now = datetime.datetime.now(datetime.timezone.utc)
            if now <= sub_end:
                return True
            else:
                plan = None
        else:
            return True
    return False

@st.cache_data
def load_css(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)