import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import json
import time
from dotenv import load_dotenv

st.set_page_config(
    page_title="Admin Dashboard",
    layout="wide",
    page_icon="https://i.imgur.com/QiTTNUk.png",
)

ADMIN_EMAIL = "info.tablora@gmail.com"

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
response = (
            supabase.table("profiles")
            .select("*")
            .eq("email", ADMIN_EMAIL)
            .execute()
        )

from streamlit_cookies_controller import CookieController
controller = CookieController()
raw = controller.get('username')
user = raw if raw else None
if raw:
    controller.set('username', raw)


time.sleep(0.2)
if user is None:
    st.error("Accès refusé : aucun utilisateur connecté.")
    st.stop()

if user.get("id") != response.data[0].get("user_id"):
    st.error("Accès refusé : vous n'avez pas les droits administrateur.")
    st.stop()

auth_users = supabase.auth.admin.list_users()
users = [u.__dict__ for u in auth_users]

try:
    visitors = supabase.table("website_stats").select("*").execute().data
except:
    visitors = []

total_users = len(users)
total_visitors = len(visitors)

st.title("Dashboard Administrateur")
st.caption(f"Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

col1, col2 = st.columns(2)
col1.metric("Visiteurs", total_visitors)
col2.metric("Inscrits", total_users)

st.divider()

import plotly.express as px
def fetch_data(table_name, date_key):
    """Fetch all rows from a Supabase table."""
    response = supabase.table("profiles").select("*").execute()
    if response.data:
        return response.data
    return []

users = fetch_data("users", "created_at")
visitors = fetch_data("visitors", "created_at")

def build_cumulative_df(data, date_key):
    dates = []
    for d in data:
        raw_date = d.get(date_key)
        if raw_date:
            try:
                dt = datetime.fromisoformat(raw_date.replace("Z", "+00:00")).date()
                dates.append(dt)
            except:
                pass

    if not dates:
        return pd.DataFrame({"date": [], "count": []})

    df = pd.DataFrame({"date": sorted(dates)})
    df["count"] = range(1, len(df) + 1)
    df = df.groupby("date").max().reset_index()
    return df

def plot_daily(df, title, y_label):
    if df.empty:
        st.info(f"Aucune donnée pour {title}.")
        return
    fig = px.line(
        df, 
        x="date", 
        y="count", 
        title=title,
        labels={"date": "Date", "count": y_label},
        markers=True
    )
    fig.update_layout(
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True),
        title=dict(x=0.5),
        template="plotly_white",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Évolution des inscriptions")
df_users = build_cumulative_df(users, "created_at")
plot_daily(df_users, " ", "Nombre d'inscriptions")

st.subheader("Évolution des visiteurs")
df_visitors = build_cumulative_df(visitors, "created_at")
plot_daily(df_visitors, "Visiteurs quotidiens", "Nombre de visiteurs")

