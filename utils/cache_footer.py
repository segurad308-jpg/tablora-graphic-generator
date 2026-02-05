import streamlit as st

@st.cache_data
def cache_footer():
    return """
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
        © 2026 Tablora — Tous droits réservés
    </div>
    </div>
    """