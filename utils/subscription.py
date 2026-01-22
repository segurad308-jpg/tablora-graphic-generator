import datetime
import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import dateutil.parser
import stripe
from fastapi import FastAPI, Query
from streamlit_cookies_controller import CookieController
import streamlit.components.v1 as components
import supabase

# Load environment variables
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
app = FastAPI()
price_id = os.getenv("PRICE_ID")
# Create Supabase client instance
supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

controller = CookieController()
# Initialize user session from cookie
raw = controller.get('username')
user = raw if raw else None
if raw:
    controller.set('username', raw) 
user_id = user.get("id") if user else None

def get_profile(user_id):
    """Return the user profile row from Supabase."""
    try:
        response = (
            supabase_client.table("profiles")
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
            color: #1f2937 !important; /* gris très foncé */
            font-size: 14px;
        }
        </style>
        
        <div class="cgu-container">
        <div class="cgu-title">Conditions d'utilisation</div>

        <div class="cgu-content">
            Pour continuer, vous devez accepter les documents suivants :
            <ul class="cgu-list">
                <li><a href="/CGU" target="_blank">Conditions Générales d'Utilisation</a></li>
                <li><a href="/CGV" target="_blank">Conditions Générales de Vente</a></li>
                <li><a href="/LPD" target="_blank">Politique de confidentialité</a></li>
            </ul>
        </div>
        </div>
        """, unsafe_allow_html=True)

        accept = st.checkbox("J'ai lu et j'accepte les CGU, CGV et la politique de confidentialité")

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

def is_free_expired(profile):
    """Return True if free trial > 7 days."""
    if not profile or profile.get("plan") != "free":
        return False

    start_str = profile.get("subscription_start")
    if not start_str:
        return False
    try:
        start = datetime.datetime.fromisoformat(start_str.replace("Z", "+00:00"))
    except ValueError:
        try:
             start = dateutil.parser.isoparse(start_str)
        except Exception:
             start = datetime.datetime.strptime(start_str, "%Y-%m-%dT%H:%M:%S.%fZ") # Adjust format if needed
             start = start.replace(tzinfo=datetime.timezone.utc)
    start_utc = start.astimezone(datetime.timezone.utc)
    
    now = datetime.datetime.now(datetime.timezone.utc)

    days_elapsed = (now - start_utc).days
    return days_elapsed > 7


def has_access(profile: dict) -> bool:
    """Return True if user has access to a feature."""
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


@app.post("/create-checkout-session")
def create_checkout_session(user_id: str = Query(...)):
    session = stripe.checkout.sessions.create(
        mode="subscription",  # ou "subscription" plus tard
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        success_url="https://tablora.ch/Offre",
        cancel_url="https://tablora.ch/Offre",
        metadata={
            "user_id": user_id  # lien CRUCIAL
        }
    )

    return {"checkout_url": session.url}

def is_unine_email(email: str) -> bool:
    return email.lower().endswith("@unine.ch")

def open_stripe_portal(user_id):
    profile = (
        supabase_client
        .table("profiles")
        .select("stripe_customer_id")
        .eq("user_id", user_id)
        .single()
        .execute()
    )

    customer_id = profile.data.get("stripe_customer_id")

    if not customer_id:
        st.error("Client Stripe introuvable")
        return

    session = stripe.billing_portal.Session.create(
        customer=customer_id,
        return_url="https://tablora.ch/Login"
    )

    return session.url
