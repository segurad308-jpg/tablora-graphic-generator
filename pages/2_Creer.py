from graph_generator import generate_graph, load_data
import streamlit as st
from streamlit_cookies_controller import CookieController
from supabase import create_client, Client
import os
from dotenv import load_dotenv
from utils.cache_function import get_cached_profile, get_supabase
import json
import time
import io
import base64
from datetime import datetime, timedelta

st.set_page_config(page_title="Tablora - Créer un graphique", layout="centered", page_icon="https://raw.githubusercontent.com/segurad308-jpg/images-tablora/refs/heads/main/logo.webp")

controller = CookieController()
if "cookies_ready" not in st.session_state:
    time.sleep(0.2)
    st.session_state.cookies_ready = True

raw = controller.get('username')
user = raw if raw else None
if raw:
    controller.set('username', raw, expires=datetime.now() + timedelta(days=30))

load_dotenv()

supabase = get_supabase()

try:
    user_id = user.get("id")
    if not user_id:
        st.error("Erreur: Impossible de récupérer votre identifiant.")
        st.stop()
except AttributeError:
    st.switch_page("pages/1_Login.py")

profile = get_cached_profile(user_id)

st.markdown("""
<style>
header {visibility: hidden;}

[data-testid="stAppViewContainer"] {
    position: relative;
    z-index: 1;
    background-color: transparent !important;
    padding-top: 0 !important;
}

#neumo-bg {
    position: fixed;
    inset: 0;
    width: 100%;
    height: 100%;
    z-index: 0;
    overflow: hidden;
    pointer-events: none;
}
.shape {
    position: absolute;
    border-radius: 50%;
    background: #ECF0F3;
    box-shadow: 12px 12px 20px #D1D9E6, -12px -12px 20px #FFFFFF;
    opacity: 0.8;
    animation: floaty 12s ease-in-out infinite;
}
.shape:nth-child(1) { width: 180px; height: 180px; top: 10%; left: 8%; animation-delay: 0s; }
.shape:nth-child(2) { width: 260px; height: 260px; bottom: 12%; right: 10%; animation-delay: 3s; }
.shape:nth-child(3) { width: 140px; height: 140px; top: 55%; left: 20%; animation-delay: 5s; }
.shape:nth-child(4) { width: 220px; height: 220px; top: 25%; right: 25%; animation-delay: 1s; }

@keyframes floaty {
    0%, 100% { transform: translateY(0px) scale(1); opacity: 0.8; }
    50% { transform: translateY(-25px) scale(1.05); opacity: 1; }
}

body, section.main, [data-testid="stAppViewContainer"] {
    background-color: #ECF0F3 !important;
}

html, body, [class*="css"] {
    color: #7B4EBF !important;
    font-family: 'Segoe UI', sans-serif !important;
}

h1, h2, h3 {
    color: #373736 !important;
    text-align: center;
    text-shadow: 1px 1px 2px #FFF;
}

div[data-testid="stFileUploader"] {
    background: #ECF0F3 !important;
    border-radius: 15px;
    box-shadow: 18px 18px 30px #D1D9E6, -18px -18px 30px #FFFFFF;
    padding: 20px;
    margin-bottom: 20px;
}
div[data-testid="stFileUploader"] label { color: #666 !important; }

div.stButton > button {
    background: linear-gradient(135deg, #b26bff, #db66ff) !important;
    color: #fff !important;
    font-weight: 500 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 20px !important;
    font-size: 16px !important;
    box-shadow: 6px 6px 12px rgba(0,0,0,0.15), -6px -6px 12px rgba(255,255,255,0.2) !important;
    transition: all 0.25s ease-in-out !important;
}
div.stButton > button:hover, 
div.stButton > button:active {
    color: #fff !important;
    background: linear-gradient(135deg, #db66ff, #caa8ff) !important;
    transform: translateY(-2px);
    box-shadow: 3px 3px 6px rgba(0,0,0,0.2), -3px -3px 6px rgba(255,255,255,0.3) !important;
}


div[data-baseweb="select"], input[type="text"], textarea {
    background: #ECF0F3 !important;
    color: #555 !important;
    border: none !important;
    border-radius: 12px !important;
    box-shadow: inset 18px 18px 30px #D1D9E6, inset -18px -18px 30px #FFFFFF !important;
    padding: 8px 15px !important;
    transition: all 0.25s ease-in-out;
}
div[data-baseweb="select"]:hover, input[type="text"]:hover, textarea:hover {
    box-shadow: inset 15px 15px 25px #D1D9E6, inset -15px -15px 25px #FFFFFF !important;
}

label, p { color: #373736 !important; font-weight: 500 !important; }

[data-testid="stDataFrame"] {
    background: #ECF0F3 !important;
    border-radius: 15px;
    box-shadow: inset 18px 18px 30px #D1D9E6, inset -18px -18px 30px #FFFFFF;
    padding: 15px;
}

section[data-testid="stSidebar"] {
    background-color: #ECF0F3 !important;
    box-shadow: 18px 0px 30px #D1D9E6;
}
section[data-testid="stSidebar"] * { color: #555 !important; }

[data-testid="stDecoration"] { display: none; }

.logo-image {
    width: 100%;
    margin-top: 0px;
    margin-bottom: 0px;
}
.logo-image-graph {
    display: block;
}
.logo-image-img {
    width: 150px;
    height: auto;
    display: block;
    margin-left: auto;
    margin-right: auto;
    transition: all 0.3s ease;
}

.topnav {
    display: flex;
    align-items: center;
    position: relative;
    z-index: 10;
    overflow: hidden;
    background: #f0f0f0;
    padding: 8px 0;
    border-radius: 10px;
    height: 60px;
    box-shadow:
        3px 3px 6px #c8c8c8,
        -3px -3px 6px #ffffff;
}

.topnav a:not(.CTA-nav-btn):not(.logo-image-graph) {
    color: #555;
    padding: 12px 16px;
    margin: 0 6px;
    text-decoration: none;
    font-size: 17px;
    font-weight: 450;
    border-radius: 25px;

    height: 40px;
    background: #f0f0f0;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transform: translateY(8px);
    transition: all 0.3s ease !important;
}

.topnav a.logo-link {
    padding: 7px 10px;
    margin: 0;
    background: none;
    box-shadow: none;
    transform: translateY(0);
}

.topnav a.logo-link:hover {
    box-shadow: none;
}

.topnav a:hover:not(.CTA-nav-btn):not(.logo-image-graph) {
    background-color: #e7e7e7;
    color: #222;
}

.topnav a.active {
    background: #a47cff !important;
    color: white !important;
    box-shadow:
        inset 2px 2px 4px #8c6de0,
        inset -2px -2px 4px #c7aaff !important;
}   
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
[data-baseweb="tag"] {
    background: #ecf0f3 !important;
    color: #7B4EBF !important;
    font-weight: 500 !important;
    border: none !important;
    border-radius: 9px !important;
    box-shadow: 2px 2px 8px #9c94a1, -2px -2px 8px #9c94a1 !important;
    padding: 6px 15px !important;
    margin: 4px 3px 2px 0 !important;
    transition: box-shadow 0.2s, color 0.2s, background 0.2s;
}

[data-baseweb="tag"]:hover {
    background: #e7eaf3 !important;
    color: #5d3cae !important;
    box-shadow: 4px 4px 14px #c4becf, -2px -2px 8px #c4becf !important;
}

[data-baseweb="tag"] span {
    color: #7B4EBF !important;
    font-weight: 500 !important;
    letter-spacing: 0.01em !important;
}

[data-baseweb="tag"] svg {
    color: #b8b3d1 !important;
}

[data-baseweb="tag"]:focus {
    outline: none !important;
    border: none !important;
}

.neumo-btn2 {
    display: flex;
    background: #603CC9;
    color: #fff;
    font-family: 'Segoe UI', sans-serif !important;
    font-weight: 600;
    font-size: 16px;
    padding: 10px 14px;
    border-radius: 10px;
    text-decoration: none;
    margin: 0px auto 0px auto;
    box-shadow: 6px 6px 14px #D1D9E6, -6px -6px 14px #FFFFFF;
    transition: all 0.25s ease-in-out;
    width: fit-content;
    white-space: nowrap;
    border: 2px solid #603CC9;
}
.neumo-btn2:hover {
    box-shadow: inset 6px 6px 14px #3d277c, inset -6px -6px 14px #3d277c;
    color: #f1e8ff;
    border-color: #3d277c;
    transform: translateY(-1px);
} 
.nav-right {
    margin-left: auto;
    margin-right: 6px;
    display: flex;
    align-items: center;
    gap: 10px;
    transform: translateY(-8px);
}
.nav-right a {
    transform: translateY(8px);
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
.stFileUploaderFileName {
    color: #555 !important;
}

.st-emotion-cache-1fi65ho {
    color: #555 !important;
}

.st-emotion-cache-c8ta4l {
    color: #777 !important;
}
</style>
""", unsafe_allow_html=True)

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
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div id="neumo-bg">
    <div class="shape"></div>
    <div class="shape"></div>
    <div class="shape"></div>
    <div class="shape"></div>
</div>
""", unsafe_allow_html=True)

st.title("Créer un graphique")


@st.cache_data(show_spinner=False)
def cached_load_data(file_bytes, file_name):
    """Memoize file parsing by content: load_data relies on ``buf.name`` to detect csv vs xlsx."""
    import io
    buf = io.BytesIO(file_bytes)
    buf.name = file_name
    return load_data(buf)


file_path = st.file_uploader("Importer un fichier CSV ou Excel", type=["csv", "xlsx"])

if file_path is not None:
    try:
        file_bytes = file_path.read()
        df = cached_load_data(file_bytes, file_path.name)

        st.write("Données chargées avec succès !")
        st.dataframe(df.head())

        # Streamlit fragment: interactions only re-run this block, not the whole page.
        @st.fragment
        def graph_controls_and_output(df):
            plot_type_label = st.selectbox(
                "Type de graphique",
                ["ligne", "barre", "nuage de points", "circulaire"],
                key="plot_type_select"
            )

            label_to_type = {
                "ligne": "line",
                "barre": "bar",
                "nuage de points": "scatter",
                "circulaire": "pie",
            }
            plot_type = label_to_type.get(plot_type_label, "line")

            x_column = st.selectbox(
                "Colonne pour l'axe X",
                options=df.columns.tolist(),
                index=0,
                key="x_column_select"
            )
            available_y_columns = [col for col in df.columns if col != x_column]

            if plot_type == "pie":
                y_columns = [st.selectbox(
                    "Colonne de valeurs",
                    options=available_y_columns,
                    key="y_pie_select"
                )]
            else:
                y_columns = st.multiselect(
                    "Colonnes de valeurs",
                    options=available_y_columns,
                    default=available_y_columns,
                    key="y_columns_multiselect"
                )

            show_regression = False
            if plot_type == "scatter":
                show_regression = st.checkbox(
                    "Afficher la régression linéaire",
                    key="show_regression_cb"
                )

            fond_choice = st.selectbox(
                "Thème",
                ["Blanc pur", "Clair doux", "Sombre"],
                key="fond_select"
            )

            title_choice = st.text_input("Titre du graphique", key="title_input")
            if plot_type != "pie":
                x_label = st.text_input("Nom de l'axe X", key="x_label_input")
                y_label = st.text_input("Nom de l'axe Y", key="y_label_input")
            else:
                x_label = ""
                y_label = ""

            if st.button("Générer le graphique", key="generate_btn"):
                if y_columns:
                    with st.spinner("Génération du graphique..."):
                        selected_cols = [x_column] + y_columns
                        df_filtered = df[selected_cols].copy()
                        fig = generate_graph(
                            df_filtered, plot_type, fond_choice,
                            title_choice, x_label, y_label, show_regression
                        )
                        # Serialize to bytes immediately so we only keep bytes in session state
                        # (otherwise matplotlib holds the figure in memory).
                        buf = io.BytesIO()
                        buf_pdf = io.BytesIO()
                        buf_svg = io.BytesIO()
                        fig.savefig(buf, format="png", bbox_inches='tight', dpi=300)
                        try:
                            fig.savefig(buf_pdf, format="pdf", bbox_inches='tight', dpi=300)
                        except Exception:
                            buf_pdf = None
                        try:
                            fig.savefig(buf_svg, format="svg", bbox_inches='tight')
                        except Exception:
                            buf_svg = None

                        import matplotlib.pyplot as plt
                        plt.close(fig)

                        st.session_state['last_fig_png'] = buf.getvalue()
                        st.session_state['last_fig_pdf'] = buf_pdf.getvalue() if buf_pdf else None
                        st.session_state['last_fig_svg'] = buf_svg.getvalue() if buf_svg else None
                        st.session_state['last_title'] = title_choice

            if 'last_fig_png' in st.session_state:
                st.image(st.session_state['last_fig_png'], use_container_width=True)

                st.markdown("""
                    <style>
                    .small-select [data-baseweb="select"] {
                        width: 130px !important;
                        min-width: 130px !important;
                        max-width: 130px !important;
                    }
                    .small-select [data-testid="stSelectboxLabel"] p {
                        font-size: 14px !important;
                    }
                    div[data-testid="stDownloadButton"] button {
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        gap: 6px;
                        font-size: 16px;
                    }
                    div[data-testid="stDownloadButton"] svg {
                        margin-bottom: -2px;
                    }
                    </style>
                """, unsafe_allow_html=True)

                st.markdown('<div class="small-select">', unsafe_allow_html=True)
                file_ext = st.selectbox(
                    "Format",
                    ["png", "pdf", "svg"],
                    index=0,
                    key="format_select"
                )
                st.markdown('</div>', unsafe_allow_html=True)

                format_map = {
                    "png": st.session_state.get('last_fig_png'),
                    "pdf": st.session_state.get('last_fig_pdf'),
                    "svg": st.session_state.get('last_fig_svg'),
                }
                raw_bytes = format_map.get(file_ext)

                # PNG is always available: fall back to it if the PDF/SVG export failed.
                if raw_bytes is None:
                    raw_bytes = st.session_state['last_fig_png']
                    file_ext = "png"

                data_b64 = base64.b64encode(raw_bytes).decode('utf-8')
                fname = f"graphe.{file_ext}"
                mime_map = {'png': 'image/png', 'svg': 'image/svg+xml', 'pdf': 'application/pdf'}
                mime = mime_map.get(file_ext, 'application/octet-stream')

                svg_icon = """
                <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" viewBox="0 0 24 24" fill="none" stroke="#666"
                stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:block; margin:auto;">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="7 10 12 15 17 10"/>
                <line x1="12" y1="15" x2="12" y2="3"/>
                </svg>
                """

                st.markdown(f"""
                <style>
                .download-btn {{
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    background: #ECF0F3;
                    color: #666;
                    border: none;
                    border-radius: 15px;
                    padding: 5px 11px;
                    box-shadow: 18px 18px 30px #D1D9E6, -18px -18px 30px #FFFFFF;
                    transition: all 0.25s ease-in-out;
                    text-decoration: none;
                }}
                .download-btn:hover {{
                    box-shadow: inset 18px 18px 30px #D1D9E6, inset -18px -18px 30px #FFFFFF;
                }}
                .download-btn svg {{
                    width: 25px;
                    height: 25px;
                    display: block;
                    margin: auto;
                    transform: translateY(5px);
                }}
                </style>

                <a href="data:{mime};base64,{data_b64}" download="{fname}" class="download-btn">
                {svg_icon}
                </a>
                """, unsafe_allow_html=True)

        graph_controls_and_output(df)

    except Exception as e:
        st.error(f"Erreur : {e}")

st.markdown("""
<style>
.footer {
    margin-top: 80px;
    padding: 30px 10%;
    background: transparent;
    color: #9aa0a6;
    font-size: 15px;
}

.footer-container {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 30px;
}

.footer-block {
    min-width: 220px;
}

.footer-title {
    font-weight: 600;
    color: #6b7280;
    margin-bottom: 10px;
}

.footer a {
    color: #9aa0a6;
    text-decoration: none;
}

.footer a:hover {
    text-decoration: underline;
}

.footer-bottom {
    margin-top: 30px;
    text-align: center;
    font-size: 14px;
    color: #b0b5bd;
}
</style>
            
<div class="footer">
<div class="footer-container">
<div class="footer-block">
    <div class="footer-title">Tablora</div>
    <div>The future of data visualization</div>
</div>

<div class="footer-block">
    <div class="footer-title">Légal</div>
    <div><a href="/mentions_legales" target="_blank">Mentions légales</a></div>
    <div><a href="/CGU" target="_blank">Conditions générales d'utilisation</a></div>
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
