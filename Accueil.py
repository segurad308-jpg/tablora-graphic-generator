import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import streamlit.components.v1 as components
import extra_streamlit_components as stx
from streamlit_cookies_controller import CookieController
import time
from utils.cache_footer import cache_footer
from utils.cache_function import load_css
from utils.html_home import render_static_home, render_static_home2

# THIS MUST BE THE ABSOLUTE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="Tablora - Accueil", layout="wide", initial_sidebar_state="collapsed", page_icon="https://github.com/segurad308-jpg/images-tablora/blob/main/logo.webp?raw=true")
 
controller = CookieController()
if "cookies_ready" not in st.session_state:
    time.sleep(0.2)
    st.session_state.cookies_ready = True
raw = controller.get('username')
user = raw if raw else None
if raw:
    controller.set('username', raw) 

load_css("styles/style.css")

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
<a href="/Login" target="_self">{login_status}</a>
<div class="cta-wrapper">
    <a href="/Offre" target="_self" class="CTA-nav-btn">
        Créer maintenant  🡪
    </a>
</div>
</div>
""", unsafe_allow_html=True)

# ===== HERO SECTION =====
st.markdown(render_static_home(), unsafe_allow_html=True)

# ===== FAQ SECTION =====
with st.expander("Comment ça marche ?"):
    st.markdown(
        """
        <p>
            1. Importez votre fichier de données (CSV ou Excel).<br><br>
            <img src="https://github.com/segurad308-jpg/images-tablora/blob/main/faq.webp?raw=true" class="faq-image">
        </p>

        <p>
            2. Sélectionnez vos préférences.<br><br>
            <img src="https://github.com/segurad308-jpg/images-tablora/blob/main/faq%202.webp?raw=true" class="faq-image">
        </p>

        <p>
            3. Générez et téléchargez votre graphique.<br><br>
            <img src="https://github.com/segurad308-jpg/images-tablora/blob/main/faq%203.webp?raw=true" class="faq-image">
        </p>
        """,
        unsafe_allow_html=True) 
    
with st.expander("Comment choisir mon graphique ?"):
    st.markdown(
        """
        <p>
            1. Vous voulez montrer une évolution ou une tendance dans le temps ? Utilisez un <strong>graphique en ligne</strong>.<br>
        </p>
        <p>
            2. Vous souhaitez comparer des catégories entre elles ? Choisissez un <strong>graphique en barres</strong>.<br>
        </p>
        <p>
            3. Vous cherchez à analyser la relation entre deux variables ? Le <strong>nuage de points</strong> est le plus adapté.<br>
        </p>
        <p>
            4. Vous voulez visualiser la répartition d’un ensemble en pourcentages ? Utilisez un <strong>graphique circulaire</strong>.<br>
        </p>
        """,
        unsafe_allow_html=True)

with st.expander("Mes données sont-elles stockées ?"):
    st.markdown("""
        <strong>Non</strong>, toutes les données que vous importez restent sur votre ordinateur.
        """, unsafe_allow_html=True)

with st.expander("Puis-je exporter mes résultats ?"):
    st.markdown("""
        <strong>Oui</strong>, nous avons plusieurs formats disponibles ; <strong>PNG, PDF, SVG</strong>.
        """, unsafe_allow_html=True)

st.markdown(render_static_home2(), unsafe_allow_html=True)

# ===== FOOTER =====
st.markdown(cache_footer(), unsafe_allow_html=True)