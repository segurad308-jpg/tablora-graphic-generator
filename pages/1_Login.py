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
from utils.subscription import cgu_modal, get_profile, has_access, is_unine_email, open_stripe_portal
from datetime import datetime, timedelta, timezone
from utils.cache_function import get_cached_profile, has_access_cached, get_supabase
from utils.cache_function import load_css

st.set_page_config(
    page_title="Tablora - Connexion", 
    layout="centered", 
    initial_sidebar_state="collapsed", 
    page_icon="https://github.com/segurad308-jpg/images-tablora/blob/main/logo.webp?raw=true"
)

# Cookie controller
controller = CookieController()
if "cookies_ready" not in st.session_state:
    time.sleep(0.2)
    st.session_state.cookies_ready = True
raw = controller.get('username')
user = raw if raw else None
if raw:
    controller.set('username', raw)

load_css("styles/style.css")
# Load .env
current_path = Path(__file__).resolve()
project_root = current_path
while project_root.parent != project_root:
    if (project_root / '.env').exists():
        break
    project_root = project_root.parent

env_path = project_root / '.env'
if env_path.exists():
    load_dotenv(env_path)

# Supabase Configuration with SERVICE KEY
supabase: Client = get_supabase()

# OAuth Configuration
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "https://tablora.ch/Login")

AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

user_is_premium = False
trial_used = False
profile = None

if user:
    user_id = user.get("id")
    if user_id:
        profile = get_cached_profile(user_id)
        if profile.get("plan") in ["free", "premium"]:
            trial_used = True
        user_is_premium = has_access_cached(profile)

if "_stripe_return" in st.query_params:
    get_cached_profile.clear()
    has_access_cached.clear()
    st.query_params.clear()

# Initialize session state
if "oauth_state" not in st.session_state:
    st.session_state.oauth_state = None

if "cgu_accepted" not in st.session_state:
    st.session_state.cgu_accepted = False

if "pending_action" not in st.session_state:
    st.session_state.pending_action = None

# Navbar
login_status = "Logout" if user else "Login"
st.markdown(f"""  
<div class="topnav">
<a href="/" target="_self" class="logo-image-graph logo-link">
    <img src="https://github.com/segurad308-jpg/images-tablora/blob/main/Tablora.webp?raw=true"
        class="logo-image-img"
        alt="Tablora Logo" />
</a>
            
<a href="/Offre" target="_self">Offre</a>
<a href="/Creer" target="_self">Créer</a>
<a class="active" href="/Login" target="_self">{login_status}</a>
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

modal_box = st.empty()

if st.session_state.get("pending_action") in ("signup", "google") and not st.session_state.get("cgu_accepted", False):
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
    """Crée ou met à jour le profil utilisateur dans Supabase en utilisant upsert (clé de service)."""    
    # Prépare l'objet de données
    data_payload = {
        "user_id": user_id,
        "email": email,
        "name": name,
        "picture": picture,
        "updated_at": dt.datetime.utcnow().isoformat()
    }
    
    if is_unine_email(email):
        data_payload.update({
            "plan": "premium",
            "is_premium": True,
            "subscription_start": dt.datetime.utcnow().isoformat(),
            "subscription_end": (dt.datetime.utcnow() + dt.timedelta(days=14)).isoformat(),
        })
    else:
        data_payload.update({
            "is_premium": False,
            "subscription_start": dt.datetime.utcnow().isoformat(),
            "subscription_end": dt.datetime.utcnow().isoformat(),
        })

    try:
        # Utilise upsert en ciblant la colonne UNIQUE: 'user_id'
        res = supabase.table("profiles").upsert(
            data_payload, 
            on_conflict="user_id",
        ).execute()

        # --- 1. VÉRIFICATION DE L'ABSENCE DE RÉPONSE ---
        if not res: 
            return False
            
        # --- 2. VÉRIFICATION DE L'ERREUR (Méthode robuste) ---
        # On vérifie explicitement si l'attribut 'error' existe et s'il a une valeur
        if hasattr(res, 'error') and res.error:
            return False
        
        # --- 3. CONFIRMATION DU SUCCÈS ---
        if hasattr(res, 'data') and res.data and len(res.data) > 0:
            st.success("Profil utilisateur mis à jour/créé avec succès.")
        else:
            st.success("Profil utilisateur créé, mais la réponse API est vide (succès confirmé en base).")
            
        return True
    
    except Exception as e:
        # Cette erreur attrape d'autres exceptions non liées à l'API Supabase
        st.error(f"Erreur inattendue dans la gestion du profil (UPSERT): {str(e)}")
        return False

def signup_user(email, password, name):
    """Create new user with Supabase Auth"""
    try:
        # Sign up user
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
        if is_unine_email(email):
            return True, "Compte créé avec succès! Vérifiez votre email pour confirmer votre compte. L'email peut mettre quelques minutes à arriver."
        else:
            return True, "Compte créé avec succès! Vérifiez votre email pour confirmer votre compte."
            
    except Exception as e:
        error_message = str(e)
        if "User already registered" in error_message:
            return False, "Un compte existe déjà avec cet email"
        return False, f"Erreur: {error_message}"

def login_user(email, password):
    """Login user with Supabase Auth and store in cookie"""
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
            
            # Create/update profile in Supabase
            create_or_update_profile(
                user_info["id"],
                user_info["email"],
                user_info["name"],
                user_info["picture"]
            )
            
            # Store in session
            st.session_state.user = user_info
            st.session_state.token = response.session.access_token
            
            # Store in cookie
            controller.set('username', st.session_state.user)
            
            return True, "Connexion réussie!"
        return False, "Email ou mot de passe incorrect"
        
    except Exception as e:
        error_message = str(e)
        if "Invalid login credentials" in error_message:
            return False, "Email ou mot de passe incorrect"
        return False, f"Erreur: {error_message}"

def create_login_form():
    """Display email login/signup form"""
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
            elif not st.session_state.cgu_accepted:
                st.session_state.pending_action = "signup"
            else:
                success, message = signup_user(email, password, name)
                if success:
                    message_box.success(message)
                    st.session_state.cgu_accepted = False
                    st.session_state.pending_action = None
                else:
                    message_box.error(message)

            
        st.markdown("""
        <div style="text-align: center; margin: 0 0;">
            <span style="color: #666;">ou</span>
        </div>
        """, unsafe_allow_html=True)

def create_google_button():
    """Generate Google OAuth login button"""
    oauth = OAuth2Session(CLIENT_ID, scope="openid email profile", redirect_uri=REDIRECT_URI)
    uri, state = oauth.create_authorization_url(AUTH_URL, access_type="offline", prompt="select_account")
    st.session_state.oauth_state = state
    st.session_state.google_oauth_url = uri

    st.markdown("""
    <form method="get">
        <button class="login-google-btn" name="google_login" value="1">
            <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg">
            Continuer avec Google
        </button>
    </form>
    """, unsafe_allow_html=True)

if st.query_params.get("google_login") == "1":
    st.query_params.clear()

    if not st.session_state.get("cgu_accepted", False):
        st.session_state.pending_action = "google"
        st.rerun()
    else:
        uri = st.session_state.get("google_oauth_url")
        if uri:
            st.markdown(
                f"<meta http-equiv='refresh' content='0; url={uri}'>",
                unsafe_allow_html=True
            )

def fetch_token():
    """Exchange Google OAuth code for token and create Supabase Auth user + profile"""
    import secrets
    from urllib.parse import urlencode
    from authlib.integrations.requests_client import OAuth2Session

    params = dict(st.query_params)
    if "code" not in params:
        return

    auth_response = f"{REDIRECT_URI}?{urlencode(params)}"
    oauth = OAuth2Session(CLIENT_ID, scope="openid email profile", redirect_uri=REDIRECT_URI,
                          state=st.session_state.get("oauth_state"))

    try:
        # 1) Token + User Google
        token = oauth.fetch_token(TOKEN_URL, authorization_response=auth_response, client_secret=CLIENT_SECRET)
        resp = oauth.get(USERINFO_URL)
        resp.raise_for_status()
        google_user = resp.json()

        email = google_user["email"]
        name = google_user.get("name", email.split("@")[0])
        picture = google_user.get("picture", "")

        # 2) CHECK USER IN SUPABASE AUTH (Admin API)
        users = supabase.auth.admin.list_users()

        existing_user = next(
            (u for u in users if u.email.lower() == email.lower()),
            None
        )

        if existing_user:
            user_id = existing_user.id
        else:
            # User does NOT exist → create it
            random_password = secrets.token_urlsafe(32)
            signup = supabase.auth.sign_up({
                "email": email,
                "password": random_password,
                "options": {"data": {"name": name, "picture": picture}}
            })
            user_id = signup.user.id

        # 3) CREATE OR UPDATE PROFILE
        create_or_update_profile(user_id, email, name, picture)

        # 4) SAVE TO SESSION + COOKIE
        user_info = {
            "id": user_id,
            "email": email,
            "name": name,
            "picture": picture,
        }
        st.session_state.user = user_info

        controller.set("username", st.session_state.user)

        st.query_params.clear()
        st.rerun()

    except Exception as e:
        st.error(f"Erreur Google OAuth: {str(e)}")



def logout():
    """Logout and clear session"""
    try:
        supabase.auth.sign_out()
    except:
        pass
    
    st.session_state.user = None
    st.session_state.token = None
    controller.remove('username')
    
    st.session_state.logged_out_success = True
    st.rerun()

# Show logout success message
if st.session_state.get("logged_out_success"):
    st.success("Vous avez été déconnecté avec succès.")
    del st.session_state.logged_out_success

# Check OAuth callback
if "code" in st.query_params and st.session_state.get("user") is None:
    with st.spinner("Connexion en cours..."):
        fetch_token()

# Get current user
user_session = st.session_state.get("user", None)
current_user = user_session or user
plan_info = None
sub_end = None
subscription_status = None

if profile is not None:
    if user_is_premium:
        plan_info = "Premium"
    elif profile and profile.get("plan") == "free":
        plan_info = "Gratuit"
    else:
        plan_info = "Aucun" 
    
    if user_is_premium:
        sub_end = datetime.fromisoformat(profile.get("subscription_end")).strftime("%d/%m/%Y")
    elif datetime.now(timezone.utc) <= datetime.fromisoformat(profile.get("subscription_end")) and profile.get("plan") == "premium":
        sub_end = datetime.fromisoformat(profile.get("subscription_end")).strftime("%d/%m/%Y")
    elif profile and profile.get("plan") == "free":
        sub_end = (datetime.fromisoformat(profile.get("subscription_start")) + timedelta(days=7)).strftime("%d/%m/%Y")
    else:
        sub_end = "Aucun"

    if profile.get("subscription_status") == True:
        subscription_status = "Actif"
    else:
        subscription_status = "Inactif"

if current_user:
    col_profile, col_sub = st.columns(2)

    with col_profile:
        st.markdown(f"""
        <div class="login-user-card">
            <img src="{current_user.get('picture', '')}"
                 class="login-user-avatar"
                 onerror="this.style.display='none'">
            <div class="login-user-name">{current_user.get('name', 'Utilisateur')}</div>
            <div class="login-user-email">{current_user.get('email', '')}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_sub:
        st.markdown(f"""
        <div class="login-user-card">
            <div class="st3">Abonnement</div>
            <div><span style="color:#666;"><strong>Plan :</strong> {plan_info}</span></div>
            <div><span style="color:#666;"><strong>Fin :</strong> {sub_end}</span></div>
            <div><span style="color:#666;"><strong>Renouvellement :</strong> {subscription_status}</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.space(2)

    btn_left, btn_center, btn_right = st.columns([1, 2, 1])

    with btn_center:
        if st.button("Accéder à l'application", use_container_width=True, type="primary"):
            st.switch_page("pages/2_Creer.py")
            
        if user_is_premium:
            if st.button("Gérer mon abonnement", use_container_width=True):
                portal_url = open_stripe_portal(profile.get("user_id"))
                if portal_url:
                    st.markdown(
                        f"<meta http-equiv='refresh' content='0; url={portal_url}'>",
                        unsafe_allow_html=True
                    )

        if st.button("Se déconnecter", use_container_width=True):
            logout()

else:
    create_login_form()
    create_google_button()

st.markdown("""
<div class="footer">
<div class="footer-container">
<div class="footer-block">
    <div class="footer-title">Tablora</div>
    <div>The future of data visualization</div>
</div>

<div class="footer-block">
    <div class="footer-title">Légal</div>
    <div><a href="/mentions_legales" target="_blank">Mentions légales</a></div>
    <div><a href="/CGU" target="_blank">Conditions générales d’utilisation</a></div>
    <div><a href="/CGV" target="_blank">Conditions générales de vente</a></div>
    <div><a href="/LPD" target="_blank">Politique de confidentialité</a></div>
</div>

<div class="footer-block">
    <div class="footer-title">Contact</div>
    <div>
        <a href="mailto:info.tablora@gmail.com">
            info.tablora@gmail.com
        </a>
    </div>
</div>
</div>

<div class="footer-bottom">
    © 2025 Tablora — Tous droits réservés
</div>
</div>
""", unsafe_allow_html=True)
