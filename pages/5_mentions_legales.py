import streamlit as st

st.set_page_config(page_title="Mentions légales", layout="wide", initial_sidebar_state="collapsed", page_icon="https://i.imgur.com/QiTTNUk.png")

st.markdown("""
    <style>
    header {visibility: hidden;}
            
    body, [data-testid="stAppViewContainer"], section.main {
    background-color: #ECF0F3 !important;
    font-family: 'Segoe UI', sans-serif !important;
    color: #000000 !important;
    }
            
    </style>
    <div>
    <head>
        <meta charset="UTF-8">
        <title>Mentions légales - Tablora</title>
    </head>
    <body>

    <h1>Mentions légales</h1>
    
    <p>Dernière mise à jour : <strong>22/01/2026</strong></p>

    <h2>Éditeur du site</h2>
    <p>
        Le site <strong>Tablora</strong> est édité par :
    </p>
    <p>
        <strong>Tablora</strong><br>
        Entreprise individuelle<br>
        Suisse
    </p>
    <p>
        <strong>Email :</strong> info.tablora@gmail.com
    </p>

    <h2>Hébergement</h2>
    <p>
        Le site est hébergé par :
    </p>
    <p>
        <strong>Render<br>
        Serveurs situés en Europe.
    </p>

    <h2>Objet du service</h2>
    <p>
        Tablora est une application en ligne permettant la <strong>création, la visualisation et l’exportation de graphiques à partir de données fournies par l’utilisateur</strong>.
    </p>

    <h2>Accès au service</h2>
    <p>
        Le service est accessible gratuitement à tous les utilisateurs.
    </p>
    <p>
        L’éditeur se réserve le droit de modifier, suspendre ou interrompre tout ou partie du service à tout moment, notamment pour des raisons de maintenance ou d’amélioration.
    </p>

    <h2>Responsabilité</h2>
    <p>
        L’éditeur met tout en œuvre pour fournir un service fiable et fonctionnel, mais ne peut garantir l’absence totale d’erreurs ou d’interruptions.
    </p>
    <p>
        L’utilisateur reste seul responsable de l’usage qu’il fait des graphiques générés et des données importées dans l’application.
    </p>

    <h2>Données personnelles</h2>
    <p>
        Les données importées par l’utilisateur (fichiers CSV, Excel, etc.) <strong>ne sont pas stockées sur les serveurs de Tablora</strong> et sont traitées uniquement dans le cadre de la génération des graphiques.
    </p>
    <p>
        Les données de compte (email, nom, photo de profil) sont utilisées uniquement pour :
    </p>
    <ul>
        <li>l’authentification,</li>
        <li>le bon fonctionnement du service.</li>
    </ul>
    <p>
        Aucune donnée personnelle n’est vendue ou transmise à des tiers.
    </p>

    <h2>Cookies</h2>
    <p>
        Le site utilise des cookies strictement nécessaires au fonctionnement de l’application (authentification, session utilisateur).
        Aucun cookie publicitaire ou de suivi tiers n’est utilisé.
    </p>

    <h2>Propriété intellectuelle</h2>
    <p>
        Tous les éléments présents sur le site (nom, logo, interface, textes, graphismes) sont la propriété exclusive de <strong>Tablora</strong>, sauf mention contraire.
    </p>
    <p>
        Toute reproduction, représentation ou exploitation sans autorisation est interdite.
    </p>

    <h2>Droit applicable</h2>
    <p>
        Les présentes mentions légales sont régies par le <strong>droit suisse</strong>.
        En cas de litige, une solution amiable sera recherchée avant toute action judiciaire.
    </p>

    <h2>Contact</h2>
    <p>
        Pour toute question ou demande d’information :
    </p>
    <p>
        <strong>Email :</strong> info.tablora@gmail.com
    </p>

    </body>
    </div>
""", unsafe_allow_html=True)