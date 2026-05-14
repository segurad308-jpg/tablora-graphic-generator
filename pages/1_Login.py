import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
import os
from urllib.parse import urlencode
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client
from streamlit_cookies_controller import CookieController
import json
import datetime as dt
import time
from datetime import datetime, timedelta, timezone
from utils.cache_function import get_cached_profile, get_supabase
from utils.cache_function import load_css
from utils.cache_footer import cache_footer
st.set_page_config(
    page_title="Tablora - Connexion",
    layout="centered",
    initial_sidebar_state="collapsed",
    page_icon="https://raw.githubusercontent.com/segurad308-jpg/images-tablora/refs/heads/main/logo.webp"
)

controller = CookieController()
if "cookies_ready" not in st.session_state:
    time.sleep(0.2)
    st.session_state.cookies_ready = True
raw = controller.get('username')
user = raw if raw else None
if raw:
    controller.set('username', raw, expires=datetime.now() + timedelta(days=30))

load_css("styles/style.css")

# Walk up from this file until we find a .env, then load it.
current_path = Path(__file__).resolve()
project_root = current_path
while project_root.parent != project_root:
    if (project_root / '.env').exists():
        break
    project_root = project_root.parent

env_path = project_root / '.env'
if env_path.exists():
    load_dotenv(env_path)

supabase: Client = get_supabase()

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "https://tablora.ch/Login")

AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

profile = None

if user:
    user_id = user.get("id")
    if user_id:
        profile = get_cached_profile(user_id)

if "oauth_state" not in st.session_state:
    st.session_state.oauth_state = None

if "cgu_accepted" not in st.session_state:
    st.session_state.cgu_accepted = False

if "pending_action" not in st.session_state:
    st.session_state.pending_action = None

login_status = "Profil" if user else "Login"
st.markdown(f"""
<div class="topnav">
<a href="/" target="_self" class="logo-image-graph logo-link">
    <img src="https://raw.githubusercontent.com/segurad308-jpg/images-tablora/refs/heads/main/Tablora.webp"
        class="logo-image-img"
        alt="Tablora Logo" />
</a>

<div class="nav-right">
    <a href="/Creer" target="_self">Créer</a>
    <a class="active" href="/Login" target="_self">{login_status}</a>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.stTextInput > div > div > input,
textarea,
div[data-baseweb="select"] {
    background: #ECF0F3 !important;
    color: #555 !important;
    border: none !important;
    border-radius: 12px !important;
    box-shadow: inset 18px 18px 30px #D1D9E6, inset -18px -18px 30px #FFFFFF !important;
    padding: 8px 15px !important;
    transition: all 0.25s ease-in-out !important;
    font-size: 14px !important;
}

.stTextInput > div > div > input::placeholder,
textarea::placeholder {
    color: #888 !important;
    opacity: 1 !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: #ECF0F3 !important;
    border-radius: 16px !important;
    padding: 6px !important;
    gap: 8px !important;
    box-shadow: 8px 8px 16px #D1D9E6, -8px -8px 16px #FFFFFF !important;
    margin-bottom: 25px !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 12px !important;
    padding: 10px 22px !important;
    font-weight: 600 !important;
    color: #666 !important;
    transition: all 0.25s ease !important;
}

.stTabs [aria-selected="true"] {
    background: #ECF0F3 !important;
    color: #603CC9 !important;
    box-shadow: 6px 6px 12px #D1D9E6, -6px -6px 12px #FFFFFF !important;
}

div.stButton > button {
    background: #ECF0F3 !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 12px 24px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    color: #555 !important;
    box-shadow: 8px 8px 16px #D1D9E6, -8px -8px 16px #FFFFFF !important;
    transition: all 0.25s ease !important;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 4px 4px 8px #D1D9E6, -4px -4px 8px #FFFFFF !important;
}

div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #603CC9, #8A63DF) !important;
    color: #fff !important;
    border: none !important;
    box-shadow: 8px 8px 16px rgba(96, 60, 201, 0.35), -8px -8px 16px rgba(255, 255, 255, 0.7) !important;
}

div.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px);
    box-shadow: 4px 4px 10px rgba(96, 60, 201, 0.45), -4px -4px 10px rgba(255, 255, 255, 0.8) !important;
}

.stAlert {
    background: #ECF0F3 !important;
    border-radius: 12px !important;
    box-shadow: 6px 6px 12px #D1D9E6, -6px -6px 12px #FFFFFF !important;
    font-size: 13px !important;
    padding: 10px 15px !important;
}

.block-container {
    padding-top: 80px !important;
}

.stSpinner > div {
    color: black !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

def cgu_modal(modal_box):
    with modal_box.container():
        st.markdown("""
        <style>
        .cgu-container {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 32px;
            max-width: 550px;
            margin: 40px auto;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        .cgu-title {
            color: #1f2937;
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 24px;
            text-align: center;
            letter-spacing: -0.3px;
        }
        .cgu-content {
            color: #374151;
            font-size: 15px;
            line-height: 1.6;
            margin-bottom: 20px;
        }
        .cgu-content a {
            color: #4b5563;
            text-decoration: none;
            font-weight: 500;
            border-bottom: 1px solid #d1d5db;
            transition: all 0.2s;
        }
        .cgu-content a:hover {
            color: #1f2937;
            border-bottom-color: #1f2937;
        }
        .cgu-list {
            list-style: none;
            padding: 0;
            margin: 16px 0;
        }
        .cgu-list li {
            padding: 10px 0;
            padding-left: 24px;
            position: relative;
            color: #374151;
        }
        .cgu-list li:before {
            content: "•";
            position: absolute;
            left: 0;
            color: #6b7280;
            font-size: 20px;
        }
        div[data-testid="stCheckbox"] label p {
            color: #1f2937 !important;
            font-size: 14px;
        }
        </style>

        <div class="cgu-container">
        <div class="cgu-title">Conditions d'utilisation</div>

        <div class="cgu-content">
            Pour continuer, vous devez accepter les documents suivants :
            <ul class="cgu-list">
                <li><a href="/CGU" target="_blank">Conditions Générales d'Utilisation</a></li>
                <li><a href="/LPD" target="_blank">Politique de confidentialité</a></li>
            </ul>
        </div>
        </div>
        """, unsafe_allow_html=True)

        accept = st.checkbox("J'ai lu et j'accepte les CGU et la politique de confidentialité")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Annuler", use_container_width=True):
                st.session_state.pending_action = None
                modal_box.empty()
                st.rerun()
        with col2:
            if st.button("Continuer", use_container_width=True, disabled=not accept, type="primary"):
                st.session_state.cgu_accepted = True
                modal_box.empty()
                st.rerun()

modal_box = st.empty()

if st.session_state.get("pending_action") == "google" and not st.session_state.get("cgu_accepted", False):
    cgu_modal(modal_box)

if st.session_state.get("cgu_accepted") and st.session_state.get("pending_action") == "google":
    st.session_state.pending_action = None
    uri = st.session_state.get("google_oauth_url")
    if uri:
        st.markdown(
            f"<meta http-equiv='refresh' content='0; url={uri}'>",
            unsafe_allow_html=True
        )

def create_or_update_profile(user_id, email, name, picture):
    """Insert or update the user profile in Supabase (upsert via the service key)."""
    data_payload = {
        "user_id": user_id,
        "email": email,
        "name": name,
        "picture": picture,
        "updated_at": dt.datetime.utcnow().isoformat()
    }

    try:
        res = supabase.table("profiles").upsert(
            data_payload,
            on_conflict="user_id",
        ).execute()

        if not res:
            return False

        if hasattr(res, 'error') and res.error:
            return False

        if hasattr(res, 'data') and res.data and len(res.data) > 0:
            st.success("Profil utilisateur mis à jour/créé avec succès.")
        else:
            st.success("Profil utilisateur créé, mais la réponse API est vide (succès confirmé en base).")

        return True

    except Exception as e:
        st.error(f"Erreur inattendue dans la gestion du profil (UPSERT): {str(e)}")
        return False

def signup_user(email, password, name):
    """Create a new user via Supabase Auth."""
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "name": name,
                    "picture": f"https://ui-avatars.com/api/?name={name.replace(' ', '+')}&background=603CC9&color=fff"
                }
            }
        })
        return True, "Compte créé avec succès! Vérifiez votre email pour confirmer votre compte."

    except Exception as e:
        error_message = str(e)
        if "User already registered" in error_message:
            return False, "Un compte existe déjà avec cet email"
        return False, f"Erreur: {error_message}"

def login_user(email, password):
    """Authenticate the user via Supabase Auth and persist the session in a cookie."""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if response.user and response.session:
            user_data = response.user.user_metadata or {}
            user_info = {
                "email": response.user.email,
                "name": user_data.get("name", response.user.email.split("@")[0]),
                "picture": user_data.get("picture", f"https://ui-avatars.com/api/?name={response.user.email.split('@')[0]}&background=603CC9&color=fff"),
                "id": response.user.id
            }

            create_or_update_profile(
                user_info["id"],
                user_info["email"],
                user_info["name"],
                user_info["picture"]
            )

            st.session_state.user = user_info
            st.session_state.token = response.session.access_token

            controller.set('username', st.session_state.user, expires=datetime.now() + timedelta(days=30))

            return True, "Connexion réussie!"
        return False, "Email ou mot de passe incorrect"

    except Exception as e:
        error_message = str(e)
        if "Invalid login credentials" in error_message:
            return False, "Email ou mot de passe incorrect"
        return False, f"Erreur: {error_message}"

def create_login_form():
    """Render the email-based sign-in and sign-up forms."""
    tab1, tab2 = st.tabs(["Se connecter", "Créer un compte"])

    with tab1:
        with st.form("login_form"):
            st.markdown("""
            <div class="login-box-title">Connexion</div>
            <p class="login-box-subtitle">Accédez à votre espace en toute sécurité</p>
            """, unsafe_allow_html=True)

            email = st.text_input("Email", placeholder="votre@email.com", label_visibility="collapsed")
            password = st.text_input("Mot de passe", type="password", placeholder="Mot de passe", label_visibility="collapsed")

            submit = st.form_submit_button("Se connecter", use_container_width=True, type="primary")

            if submit:
                if not email or not password:
                    st.error("Veuillez remplir tous les champs")
                else:
                    success, message = login_user(email, password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)

            st.markdown("""
            <div style="text-align: center; margin: 0 0;">
                <span style="color: #666;">ou</span>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        with st.form("signup_form"):
            message_box = st.empty()
            st.markdown("""
            <div class="login-box-title">Créer un compte</div>
            <p class="login-box-subtitle">Rejoignez-nous dès maintenant</p>
            """, unsafe_allow_html=True)

            name = st.text_input("Nom complet", placeholder="Nom complet", label_visibility="collapsed")
            email = st.text_input("Email", placeholder="votre@email.com", key="signup_email", label_visibility="collapsed")
            password = st.text_input("Mot de passe", type="password", placeholder="Mot de passe", key="signup_password", label_visibility="collapsed")
            password_confirm = st.text_input("Confirmer le mot de passe", type="password", placeholder="Confirmer le mot de passe", label_visibility="collapsed")
            cgu_ok = st.checkbox("J'accepte les [CGU](/CGU) et la [politique de confidentialité](/LPD).")

            submit = st.form_submit_button("Créer un compte", use_container_width=True, type="primary")

        if submit:
            if not all([name, email, password, password_confirm]):
                st.error("Veuillez remplir tous les champs")
            elif "@" not in email:
                st.error("Format de l'adresse email invalide")
            elif password != password_confirm:
                st.error("Les mots de passe ne correspondent pas")
            elif len(password) < 6:
                st.error("Le mot de passe doit contenir au moins 6 caractères")
            elif not cgu_ok:
                st.error("Vous devez accepter les CGU pour créer un compte")
            else:
                success, message = signup_user(email, password, name)
                if success:
                    message_box.success(message)
                else:
                    message_box.error(message)


        st.markdown("""
        <div style="text-align: center; margin: 0 0;">
            <span style="color: #666;">ou</span>
        </div>
        """, unsafe_allow_html=True)

def create_google_button():
    """Render the Google OAuth sign-in button."""
    oauth = OAuth2Session(CLIENT_ID, scope="openid email profile", redirect_uri=REDIRECT_URI)
    uri, state = oauth.create_authorization_url(AUTH_URL, access_type="offline", prompt="select_account")
    st.session_state.oauth_state = state
    st.session_state.google_oauth_url = uri

    st.markdown(
        f"""
    <form method="get">
        <button class="login-google-btn" name="google_login" value="1">
            <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg">
            Continuer avec Google
        </button>
    </form>
    """,
        unsafe_allow_html=True,
    )

if st.query_params.get("google_login") == "1":
    st.query_params.clear()
    if not st.session_state.get("cgu_accepted", False):
        st.session_state.pending_action = "google"
        st.rerun()
    else:
        st.session_state.pending_action = None
        uri = st.session_state.get("google_oauth_url")
        if uri:
            st.markdown(
                f"<meta http-equiv='refresh' content='0; url={uri}'>",
                unsafe_allow_html=True
            )

def fetch_token():
    """Exchange the Google OAuth code for a token, then create/update the Supabase user and their profile."""
    import secrets
    from urllib.parse import urlencode
    from authlib.integrations.requests_client import OAuth2Session

    params = dict(st.query_params)
    if "code" not in params:
        return

    if st.session_state.get("token_exchanged"):
        st.query_params.clear()
        return

    code = params["code"]
    state_from_url = params.get("state")

    st.query_params.clear()
    st.session_state.token_exchanged = True

    auth_response = f"{REDIRECT_URI}?{urlencode(params)}"
    oauth = OAuth2Session(CLIENT_ID, scope="openid email profile", redirect_uri=REDIRECT_URI,
                          state=st.session_state.get("oauth_state"))

    try:
        token = oauth.fetch_token(
            TOKEN_URL,
            code=code,
            client_secret=CLIENT_SECRET,
            include_client_id=True
        )
        resp = oauth.get(USERINFO_URL)
        resp.raise_for_status()
        google_user = resp.json()

        email = google_user["email"]
        name = google_user.get("name", email.split("@")[0])
        picture = google_user.get("picture", "")

        users = supabase.auth.admin.list_users()

        existing_user = next(
            (u for u in users if u.email.lower() == email.lower()),
            None
        )

        if existing_user:
            user_id = existing_user.id
        else:
            # First Google sign-in: provision a Supabase account with a random password.
            random_password = secrets.token_urlsafe(32)
            signup = supabase.auth.sign_up({
                "email": email,
                "password": random_password,
                "options": {"data": {"name": name, "picture": picture}}
            })
            user_id = signup.user.id

        create_or_update_profile(user_id, email, name, picture)

        user_info = {
            "id": user_id,
            "email": email,
            "name": name,
            "picture": picture,
        }
        st.session_state.user = user_info

        controller.set("username", st.session_state.user, expires=datetime.now() + timedelta(days=30))

        st.query_params.clear()
        st.session_state.token_exchanged = False
        st.rerun()

    except Exception as e:
        st.session_state.token_exchanged = False
        st.error(f"Erreur Google OAuth: {str(e)}")



def logout():
    """Sign the user out and clear both the session and the cookie."""
    try:
        supabase.auth.sign_out()
    except:
        pass

    st.session_state.user = None
    st.session_state.token = None
    st.session_state.token_exchanged = False
    st.session_state.oauth_state = None
    st.session_state.clear()
    controller.remove("username")

    st.session_state.logged_out_success = True
    time.sleep(0.2)
    st.rerun()

if st.session_state.get("logged_out_success"):
    st.success("Vous avez été déconnecté avec succès.")
    del st.session_state.logged_out_success

if "code" in st.query_params and st.session_state.get("user") is None:
    with st.spinner("Connexion en cours..."):
        fetch_token()

user_session = st.session_state.get("user", None)
current_user = user_session or user

if current_user:
    st.markdown(f"""
    <div class="login-user-card">
        <img src="{current_user.get('picture', '')}"
             class="login-user-avatar"
             onerror="this.style.display='none'">
        <div class="login-user-name">{current_user.get('name', 'Utilisateur')}</div>
        <div class="login-user-email">{current_user.get('email', '')}</div>
    </div>
    """, unsafe_allow_html=True)

    btn_left, btn_center, btn_right = st.columns([1, 2, 1])

    with btn_center:
        if st.button("Accéder à l'application", use_container_width=True, type="primary"):
            st.switch_page("pages/2_Creer.py")

        if st.button("Se déconnecter", use_container_width=True):
            logout()

else:
    create_login_form()
    create_google_button()

st.markdown(cache_footer(), unsafe_allow_html=True)
