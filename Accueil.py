import streamlit as st
from streamlit_cookies_controller import CookieController
import time
from datetime import datetime, timedelta
from utils.cache_footer import cache_footer
from utils.html_home import render_static_home, render_static_home2

# set_page_config must be the first Streamlit call on the page.
st.set_page_config(page_title="Tablora - Accueil", layout="wide", initial_sidebar_state="collapsed", page_icon="https://raw.githubusercontent.com/segurad308-jpg/images-tablora/refs/heads/main/logo.webp")
 

controller = CookieController()
if "cookies_ready" not in st.session_state:
    time.sleep(0.2)
    st.session_state.cookies_ready = True
raw = controller.get('username')
user = raw if raw else None
if raw:
    controller.set('username', raw, expires=datetime.now() + timedelta(days=30)) 


from utils.load_css import load_css
load_css("styles/style.css")

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
    <a href="/Login" target="_self">{login_status}</a>
    <a href="/Creer" target="_self" class="CTA-nav-btn">
        Créer maintenant  🡪
    </a>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown(render_static_home(), unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1.7])

with col_left:
    st.markdown("""
    <div class="st2">
        Frequently Asked ‎<span style="color:#a47cff;"><i>Questions</i></span>
    </div>
    <a href="/Creer" target="_self" class="neumo-btn1" style="margin-top: 0;">
                Essayer gratuitement
    </a>
    """, unsafe_allow_html=True)

with col_right:
    with st.expander("Comment ça marche ?"):
        st.markdown(
            """
            <p>
                1. Importez votre fichier de données (CSV ou Excel).<br><br>
                <img src="https://raw.githubusercontent.com/segurad308-jpg/images-tablora/refs/heads/main/faq.webp" class="faq-image">
            </p>

            <p>
                2. Sélectionnez vos préférences.<br><br>
                <img src="https://raw.githubusercontent.com/segurad308-jpg/images-tablora/refs/heads/main/faq%202.webp" class="faq-image">
            </p>

            <p>
                3. Générez et téléchargez votre graphique.<br><br>
                <img src="https://raw.githubusercontent.com/segurad308-jpg/images-tablora/refs/heads/main/faq%203.webp" class="faq-image">
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

st.markdown(cache_footer(), unsafe_allow_html=True)