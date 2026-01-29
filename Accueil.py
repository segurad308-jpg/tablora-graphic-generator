import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import streamlit.components.v1 as components
import extra_streamlit_components as stx
from streamlit_cookies_controller import CookieController
import time

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

from utils.load_css import load_css
load_css("styles/style.css")

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

if "_learn_more" in st.query_params:
    st.switch_page("pages/3_Offre.py")

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
        Créer maintenant ⟶
    </a>
</div>
</div>
""", unsafe_allow_html=True)

# ===== HERO SECTION =====
st.markdown("""
<div class="hero-section">
    <div class="hero-left">
        <div class="hero-title">Tablora</div>
        <div class="hero-sub">Facile, Rapide, Magnifique.</div>
        <div class="hero-desc">
            Dévoilez la puissance de vos données grâce à des visualisations  
            créées en quelques clics. <br><br>
            Construisez, personnalisez et donnez vie à vos graphiques sans effort.
        </div>
        <div style="display: flex; gap: 20px; margin-top: 30px;">
            <a href="/Offre" target="_self" class="neumo-btn1">
                Essayer gratuitement
            </a>
            <form action="" method="get">
                <button class="neumo-btn" name="_learn_more" value="1" type="submit">
                    Voir l'offre
                </button>
            </form>
        </div>
    </div>
    <div class="hero-right">
        <img src="https://github.com/segurad308-jpg/images-tablora/blob/main/Tablora%20(1).webp?raw=true" class="hero-img" alt="Hero Image" />
    </div>
</div>
""", unsafe_allow_html=True)



# ===== FEATURE CARD =====
st.markdown("""       
<div class="neumo-card">
    <img src="https://github.com/segurad308-jpg/images-tablora/blob/main/design.webp?raw=true" class="neumo-img" alt="Feature">
    <div style="display: flex; flex-direction: column; width: 50%;">
        <div class="st1">
            Visualisez plus vite et mieux<br> 
            avec 
            <span style="color:#603CC9;">Tablora</span>
        </div>
        <div class="neumo-text">
            Générez des graphiques époustouflants en seulement quelques secondes grâce à notre interface intuitive.
        </div>
        <form action="" method="get">
            <button class="neumo-btn1" name="_learn_more" value="1" type="submit">
                Essayer maintenant
            </button>
        </form>
    </div>
</div>
""", unsafe_allow_html=True)


st.markdown("""
<div class="st2">
    <div style="text-align: center;">
        Tablora explore et visualise vos données<br>
         en un clin d'œil
    </div>
</div>
""", unsafe_allow_html=True)

# ===== FEATURE ROW =====
st.markdown("""
<div class="neumo-row">

<div class="feature-card">
    <img src="https://github.com/segurad308-jpg/images-tablora/blob/main/Design%20sans%20titre.webp?raw=true" class="feature-image" />
    <div class="feature-title">Importez vos données CSV et Excel</div>
    <div class="feature-desc">Importez en un clic vos tableau de données.</div>
</div>

<div class="feature-card">
    <img src="https://github.com/segurad308-jpg/images-tablora/blob/main/his.webp?raw=true" class="feature-image" />
    <div class="feature-title">Créez des graphes personnalisables et rapides</div>
    <div class="feature-desc">Choisissez le graphe qui vous correspond le mieux.</div>
</div>

<div class="feature-card">
    <img src="https://github.com/segurad308-jpg/images-tablora/blob/main/Design%20sans%20titre%20(1).webp?raw=true" class="feature-image" />
    <div class="feature-title">Téléchargement pro</div>
    <div class="feature-desc">Exportez en PNG, PDF, SVG et partagez vos créations partout.</div>
</div>

<div class="feature-card">
    <img src="https://github.com/segurad308-jpg/images-tablora/blob/main/Design%20sans%20titre%20(2).webp?raw=true" class="feature-image" />
    <div class="feature-title">Données sécurisées</div>
    <div class="feature-desc">Vos fichiers ne quittent jamais votre ordinateur et ne sont pas stockés.</div>
</div>

</div>
""", unsafe_allow_html=True)


st.markdown("""
<div class='gradient-section'>
    <div class="bottom-section">
        <div class="bottom-left">
            <div class="st1">Qui sommes-nous ?</div>
            <div class="bottom-desc">
                <span style="color:#603CC9;">Tablora</span> est une entreprise Suisse, ayant conçu un outil de visualisation de données pour les étudiants et les professionnels.
                Notre mission est de rendre la création de graphiques accessible à tous, en simplifiant le processus qui parfois peut sembler complexe.<br><br>
                La conception de graphiques prend souvent du temps et nécessite des compétences techniques et par conséquent,
                nous cherchons à faciliter la tâche aux personnes souhaitant représenter visuellement leurs données.<br>
                Avec <span style="color:#603CC9;">Tablora</span>, ménagez vos efforts et transformez vos données en visualisations percutantes en seulement quelques clics.
            </div>
        </div>
        <div class="bottom-right">
            <img src="https://github.com/segurad308-jpg/images-tablora/blob/main/travail.webp?raw=true" class="bottom-img" alt="Demo" />
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='separator'></div>", unsafe_allow_html=True)

st.markdown("""
<div class="st2">
    <div style="justify-content: center;">
        Pourquoi choisir Tablora ?
    </div>
</div> 
""", unsafe_allow_html=True)

st.markdown("""
<div class="neumo-container">
<table class="neumo-table">
<tr>
    <th style="color:#311566;">Avantages</th>
    <th style="text-align:center;color:#603CC9;">Tablora</th>
    <th style="text-align:center;color:#311566;">&copy; Tableau Software</th>
    <th style="text-align:center;color:#311566;">&copy; Excel</th>
</tr>

<tr>
    <td>Rapide et intuitif</td>
    <td class="neumo-check">✔</td>
    <td class="neumo-check">-</td>
    <td class="neumo-check">✔</td>
</tr>

<tr>
    <td>Visualisation puissante</td>
    <td class="neumo-check">✔</td>
    <td class="neumo-check">✔</td>
    <td class="neumo-check">-</td>
</tr>

<tr>
    <td>Personnalisation facile</td>
    <td class="neumo-check">✔</td>
    <td class="neumo-check">✔</td>
    <td class="neumo-check">-</td>
</tr>

<tr>
    <td>Téléchargement haute qualité</td>
    <td class="neumo-check">✔</td>
    <td class="neumo-check">✔</td>
    <td class="neumo-check">-</td>
</tr>

<tr>
    <td>Abordable et accessible</td>
    <td class="neumo-check">✔</td>
    <td class="neumo-check">-</td>
    <td class="neumo-check">✔</td>
</tr>
</table>
</div>
""", unsafe_allow_html=True)

# ===== FAQ SECTION =====
st.markdown("""
<div class="st2">
    <div style="justify-content: center;">
        Questions fréquentes
    </div>
</div> 
""", unsafe_allow_html=True)

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

st.markdown("""
<section class="reviews-section">
    <div class="st4">Avis</div>
    <div class="reviews-grid">
            
<div class="review-card">
    <div class="review-header">
        <div class="review-avatar">Q</div>
        <div class="review-meta">
            <div class="review-name">Quentin S.</div>
            <div class="review-stars">★★★★★</div>
        </div>
    </div>
    <div class="review-text">J'ai été impressionné par la facilité d'utilisation du logiciel. J'ai l'habitude
            de créer des graphiques et par conséquent j'étais sceptique à l'idée d'utiliser Tablora, car c'est en général une tâche
            laborieuse et complexe. J'ai fait mon choix et je ne reviendrai pas en arrière.</div>
</div>

<div class="review-card">
    <div class="review-header">
        <div class="review-avatar">D</div>
        <div class="review-meta">
            <div class="review-name">David L.</div>
            <div class="review-stars">★★★★★</div>
        </div>
    </div>
    <div class="review-text">Tout simplement j'adore ! J'aurais jamais cru que ce serait autant facile de créer des
            graphiques mais avec Tablora j'ai qu'à cliquer sur quelques boutons et le tour est joué !
            Si vous avez besoin de créer des graphiques rapidement, je recommande fortement Tablora.</div>
</div>

<div class="review-card">
    <div class="review-header">
        <div class="review-avatar">C</div>
        <div class="review-meta">
            <div class="review-name">Catherine M.</div>
            <div class="review-stars">★★★★☆</div>
        </div>
    </div>
    <div class="review-text">Cela a toujours été pour moi une tâche compliquée, et donc en trouvant ce logiciel, 
            j'ai pu facilement créer de bons graphiques sans effort. De cette manière, je peux maintenant facilement 
            intégrer des graphiques à mes présentations lors de mes projets d'étude.</div>
</div>

</div>
<div class="review-submit-card">
    <div class="st3">Donner votre avis</div>

<form action="https://formspree.io/f/mkojrbjk" method="POST" class="review-form">

<!-- Ligne du haut -->
<div class="review-top">
<input type="text" name="Nom" placeholder="Votre nom" required>

<div class="star-rating">
<input type="radio" id="star5" name="Note" value="5" required>
<label for="star5">★</label>

<input type="radio" id="star4" name="Note" value="4">
<label for="star4">★</label>

<input type="radio" id="star3" name="Note" value="3">
<label for="star3">★</label>

<input type="radio" id="star2" name="Note" value="2">
<label for="star2">★</label>

<input type="radio" id="star1" name="Note" value="1">
<label for="star1">★</label>
</div>
</div>

<!-- Avis -->
<textarea name="Avis" rows="3" placeholder="Votre avis" required></textarea>

<button type="submit">Publier mon avis</button>
</form>
</div>

</section>
""", unsafe_allow_html=True)

st.markdown("""
<div class="banner">
    <div class="banner-text">
            Commencez gratuitement dès aujourd'hui !
    </div>
</div>
""", unsafe_allow_html=True)
    
st.markdown("""
<div style="display: flex; justify-content: center; gap: 20px; margin-top: 0;">
    <form action="" method="get">
        <button class="neumo-btn2" name="_learn_more" value="1" type="submit">
            Essayer gratuitement
        </button>
    </form>
    <form action="" method="get">
        <button class="neumo-btn3" name="_learn_more" value="1" type="submit">
            Acheter l'offre maintenant
        </button>
    </form>
</div>
""", unsafe_allow_html=True)

# ===== FOOTER =====
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