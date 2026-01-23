import streamlit as st
from streamlit_cookies_controller import CookieController
import datetime as dt
import json
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import time
import stripe
from utils.subscription import get_profile, has_access

st.set_page_config(page_title="Tablora - Offres", layout="wide", initial_sidebar_state="collapsed", page_icon="https://i.imgur.com/QiTTNUk.png")

controller = CookieController()
if "cookies_ready" not in st.session_state:
    time.sleep(0.2)
    st.session_state.cookies_ready = True
raw = controller.get('username')
user = raw if raw else None
if raw:
    controller.set('username', raw) 
    
from utils.load_css import load_css
load_css("styles/style.css")


load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

trial_used = False
user_id = None
profile = None
user_is_premium = False

if user:
    user_id = user.get("id")
    if user_id:
        # Get profile from Supabase
        try:
            result = supabase.table("profiles").select("*").eq("user_id", user_id).execute()
            if result.data:
                profile = result.data[0]
                # Check if user already has a plan (free or premium)
                if profile.get("plan") in ["free", "premium"]:
                    trial_used = True
        except Exception as e:
            st.error(f"Erreur lors de la récupération du profil: {str(e)}")

if user_id:
    profile = get_profile(user_id)
    user_is_premium = has_access(profile)

if "_upgrade" in st.query_params:
    time.sleep(0.1)
    if user is None:
        st.query_params.clear()
        st.switch_page("pages/1_Login.py")
        st.stop()
    st.query_params.clear()

    if user:
        checkout_session = stripe.checkout.Session.create(
            mode="subscription",  
            line_items=[{
                "price": os.getenv("PRICE_ID"),  # Price ID Stripe
                "quantity": 1,
            }],
            success_url="https://tablora.ch/Offre",
            cancel_url="https://tablora.ch/Offre",
            subscription_data={
                "metadata": {
                    "user_id": user["id"]
                }
            }
        )

        # Redirection immédiate vers Stripe Checkout
        st.markdown(
            f'<meta http-equiv="refresh" content="0; url={checkout_session.url}">',
            unsafe_allow_html=True
        )
        st.stop()
        
if "_go_try" in st.query_params:
    time.sleep(0.1)

    if user is None:
        st.query_params.clear()
        st.switch_page("pages/1_Login.py")
        st.stop()
    
    st.query_params.clear()

    if trial_used:
        st.error("Vous avez déjà activé votre essai gratuit ou avez un abonnement actif.")
        st.stop()

    user_id = user.get("id")
    
    if not user_id:
        st.error("Impossible de récupérer votre identifiant utilisateur.")
        st.stop()

    now = dt.datetime.utcnow().isoformat()

    try:
        if profile is None:
            # Create new profile with free trial
            supabase.table("profiles").insert({
                "user_id": user_id,
                "email": user.get("email"),
                "name": user.get("name"),
                "picture": user.get("picture"),
                "plan": "free",
                "subscription_start": now
            }).execute()
        else:
            # Update existing profile to free trial
            supabase.table("profiles").update({
                "plan": "free",
                "subscription_start": now
            }).eq("user_id", user_id).execute()

        st.success("Votre essai gratuit est activé ! Vous pouvez maintenant créer vos graphiques pendant 7 jours.")
        
        # Wait a bit then redirect
        import time
        time.sleep(0.5)
        st.switch_page("pages/2_Creer.py")
    except Exception as e:
        st.error(f"Erreur lors de l'activation de l'essai: {str(e)}")
        st.stop()

if "_check" in st.query_params:
    st.query_params.clear()
    st.switch_page("pages/1_Login.py")
    st.stop()

if user is None:
    st.markdown("""  
    <div class="topnav">
        <a href="/" target="_self">Accueil</a>
        <a class="active" href="" target="_self">Offre</a>
        <a href="/Creer" target="_self">Créer</a>
        <a href="/Login" target="_self">Login</a>
        
    <div class="logo-image-graph">
        <img src="https://i.imgur.com/6e9Z5aA.png" class="logo-image-img" alt="Tablora Logo" />
    </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""  
    <div class="topnav">
        <a href="/" target="_self">Accueil</a>
        <a class="active" href="" target="_self">Offre</a>
        <a href="/Creer" target="_self">Créer</a>
        <a href="/Login" target="_self">Logout</a>
        
    <div class="logo-image-graph">
        <img src="https://i.imgur.com/6e9Z5aA.png" class="logo-image-img" alt="Tablora Logo" />
    </div>
    </div>
    """, unsafe_allow_html=True)

if trial_used:
    st.markdown("""
    <style>
    .pricing-card-free {
        opacity: 0.5;
        pointer-events: none;
        position: relative;
    }
    .pricing-card-free::after {
        content: "Déjà utilisé";
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(96, 60, 201, 0.9);
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    time.sleep(0.2)
    if profile and profile.get("plan") == "free":
        # Get the start string and make it ISO-compliant (+00:00)
        start_str = profile["subscription_start"].replace("Z", "+00:00")
        
        # 1. Parse start time as Timezone-Aware (it detects the +00:00)
        start = dt.datetime.fromisoformat(start_str)

        # 2. Get the current time as Timezone-Aware UTC
        now = dt.datetime.now(dt.timezone.utc)

        # 3. Perform subtraction (Aware - Aware)
        # The start time is already in UTC due to the +00:00
        days_elapsed = (now - start).days
        days_remaining = max(0, 7 - days_elapsed)
        if days_remaining > 0:
            st.info(f"Votre essai gratuit est actif ! Il vous reste {days_remaining} jour{'s' if days_remaining > 1 else ''} pour profiter de toutes les fonctionnalités.")
        else:
            st.warning("Votre essai gratuit a expiré. Passez à Premium pour continuer à créer des graphiques !")
    elif user_is_premium:
        st.success("Vous êtes Premium ! Profitez de toutes les fonctionnalités sans limite.")

if not user_is_premium:
    st.markdown("""
    <div class="pricing-wrapper">
        <div class="pricing-header">
            <div class="pricing-main-title">Choisissez votre plan</div>
            <p class="pricing-subtitle">
                Commencez gratuitement ou passez à la version Premium pour accéder à toutes les fonctionnalités
            </p>
        </div>
        
    <div class="pricing-cards-container">
    <!-- Free Plan -->
    <div class="pricing-card pricing-card-free">
        <div class="pricing-card-badge">Essai gratuit</div>
        <div class="pricing-card-plan-name">Gratuit</div>
        <p class="pricing-card-description">
            Découvrez Tablora et créez vos premiers graphiques
        </p>
        
    <div class="pricing-card-price-section">
        <span class="pricing-card-price">0 CHF</span>
        <span class="pricing-card-period">pendant 1 semaine</span>
        <form action="" method="get">
            <button class="pricing-cta-button" name="_go_try" value="1" type="submit">
                Commencer gratuitement
            </button>
        </form>
    </div>


    <div class="pricing-features-list">
        <div class="pricing-feature-item">
            <span class="pricing-feature-icon">✓</span>
            <span>Période d'essai</span>
        </div>
        <div class="pricing-feature-item">
            <span class="pricing-feature-icon">✓</span>
            <span>Types de base (ligne, barre)</span>
        </div>
        <div class="pricing-feature-item">
            <span class="pricing-feature-icon">✓</span>
            <span>Thème de base</span>
        </div>
        <div class="pricing-feature-item">
            <span class="pricing-feature-icon">✓</span>
            <span>Export PNG uniquement</span>
        </div>
        <div class="pricing-feature-item">
            <span class="pricing-feature-icon">✓</span>
            <span>Support communautaire</span>
        </div>
    </div>
    </div>

    <!-- Premium Plan -->
    <div class="pricing-card pricing-card-premium">
        <div class="pricing-card-badge">Le plus populaire</div>
        <div class="pricing-card-plan-name">Premium</div>
        <p class="pricing-card-description">
            Visualisez, créez et analysez au meilleur niveau
        </p>
        
    <div class="pricing-card-price-section">
        <span class="pricing-card-price">7 CHF</span>
        <span class="pricing-card-period">/ mois</span>
        <form action="" method="get">
            <button class="pricing-cta-button" name="_upgrade" value="1" type="submit">
                Passer à Premium
            </button>
        </form>
    </div>

    <div class="pricing-features-list">
        <div class="pricing-feature-item">
            <span class="pricing-feature-icon">✓</span>
            <span>Graphiques illimités</span>
        </div>
        <div class="pricing-feature-item">
            <span class="pricing-feature-icon">✓</span>
            <span>Tous les types de graphiques</span>
        </div>
        <div class="pricing-feature-item">
            <span class="pricing-feature-icon">✓</span>
            <span>Export PNG, PDF, SVG</span>
        </div>
        <div class="pricing-feature-item">
            <span class="pricing-feature-icon">✓</span>
            <span>Personnalisation avancée</span>
        </div>
        <div class="pricing-feature-item">
            <span class="pricing-feature-icon">✓</span>
            <span>Sauvegarde des graphiques</span>
        </div>
        <div class="pricing-feature-item">
            <span class="pricing-feature-icon">✓</span>
            <span>Support prioritaire</span>
        </div>
    </div>

    </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

if user_is_premium:
    st.markdown("""
    <div class="pricing-wrapper">
        <div class="pricing-header">
            <div class="pricing-main-title">Choisissez votre plan</div>
            <p class="pricing-subtitle">
                Commencez gratuitement ou passez à la version Premium pour accéder à toutes les fonctionnalités
            </p>
        </div>
        
    <div class="pricing-cards-container">
    <!-- Free Plan -->
    <div class="pricing-card pricing-card-free">
        <div class="pricing-card-badge">Essai gratuit</div>
        <div class="pricing-card-plan-name">Gratuit</div>
        <p class="pricing-card-description">
            Découvrez Tablora et créez vos premiers graphiques
        </p>
        
    <div class="pricing-card-price-section">
        <span class="pricing-card-price">0 CHF</span>
        <span class="pricing-card-period">pendant 1 semaine</span>
        <form action="" method="get">
            <button class="pricing-cta-button" name="_go_try" value="1" type="submit">
                Commencer gratuitement
            </button>
        </form>
    </div>


    <div class="pricing-features-list">
        <div class="pricing-feature-item">
            <span class="pricing-feature-icon">✓</span>
            <span>Période d'essai</span>
        </div>
        <div class="pricing-feature-item">
            <span class="pricing-feature-icon">✓</span>
            <span>Types de base (ligne, barre)</span>
        </div>
        <div class="pricing-feature-item">
            <span class="pricing-feature-icon">✓</span>
            <span>Thème de base</span>
        </div>
        <div class="pricing-feature-item">
            <span class="pricing-feature-icon">✓</span>
            <span>Export PNG uniquement</span>
        </div>
        <div class="pricing-feature-item">
            <span class="pricing-feature-icon">✓</span>
            <span>Support communautaire</span>
        </div>
    </div>
    </div>

    <!-- Premium Plan -->
    <div class="pricing-card pricing-card-premium">
        <div class="pricing-card-badge">Le plus populaire</div>
        <div class="pricing-card-plan-name">Premium</div>
        <p class="pricing-card-description">
            Visualisez, créez et analysez au meilleur niveau
        </p>
        
    <div class="pricing-card-price-section">
        <span class="pricing-card-price">7 CHF</span>
        <span class="pricing-card-period">/ mois</span>
        <form action="" method="get">
            <button class="pricing-cta-button" name="_check" value="1" type="submit">
                Voir mon abonnement
            </button>
        </form>
    </div>

    <div class="pricing-features-list">
        <div class="pricing-feature-item">
            <span class="pricing-feature-icon">✓</span>
            <span>Graphiques illimités</span>
        </div>
        <div class="pricing-feature-item">
            <span class="pricing-feature-icon">✓</span>
            <span>Tous les types de graphiques</span>
        </div>
        <div class="pricing-feature-item">
            <span class="pricing-feature-icon">✓</span>
            <span>Export PNG, PDF, SVG</span>
        </div>
        <div class="pricing-feature-item">
            <span class="pricing-feature-icon">✓</span>
            <span>Personnalisation avancée</span>
        </div>
        <div class="pricing-feature-item">
            <span class="pricing-feature-icon">✓</span>
            <span>Sauvegarde des graphiques</span>
        </div>
        <div class="pricing-feature-item">
            <span class="pricing-feature-icon">✓</span>
            <span>Support prioritaire</span>
        </div>
    </div>

    </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

# Footer CTA
if not trial_used or not user_is_premium:
    st.markdown("""
    <div style="text-align: center; margin: 70px auto 50px auto;">
        <h2 style="font-size: 28px; color: #603CC9; margin-bottom: 16px; text-shadow: 1px 1px 2px #EEE;">
            Prêt à créer des graphiques professionnels ?
        </h2>
        <p style="font-size: 16px; color: #595959; margin-bottom: 25px;">
            Commencez gratuitement, aucune carte de crédit requise
        </p>
    <form action="" method="get" style="text-align: center;">
        <button class="neumo-btn2" name="_go_try" value="1" type="submit" style="display: inline-block;">
            Essayer gratuitement
        </button>
    </form>
    </div>
    """, unsafe_allow_html=True)
elif not user_is_premium:
    st.markdown("""
    <div style="text-align: center; margin: 70px auto 50px auto;">
        <h2 style="font-size: 28px; color: #603CC9; margin-bottom: 16px; text-shadow: 1px 1px 2px #EEE;">
            Prêt à créer des graphiques professionnels ?
        </h2>
        <p style="font-size: 16px; color: #595959; margin-bottom: 25px;">
            Passez dès maintenant à la version premium pour profiter de toutes les fonctionnalités
        </p>
    <form action="" method="get" style="text-align: center;">
        <button class="neumo-btn2" name="_upgrade" value="1" type="submit" style="display: inline-block;">
            Passer à Premium
        </button>
    </form>
    </div>
    """, unsafe_allow_html=True)

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