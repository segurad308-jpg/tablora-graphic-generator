import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import json
import time
from dotenv import load_dotenv

# ---------- CONFIG ----------
st.set_page_config(
    page_title="Admin Dashboard",
    layout="wide",
    page_icon="https://i.imgur.com/QiTTNUk.png",
)

# ---------- ADMIN ACCESS ----------
ADMIN_EMAIL = "info.tablora@gmail.com"
# ---------- LOAD ENV ----------
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

# ---------- FETCH DATA ----------
# Users (auth system)
auth_users = supabase.auth.admin.list_users()
users = [u.__dict__ for u in auth_users]

# Subscriptions (your table)
try:
    subscriptions = supabase.table("profiles").select("*").eq("plan", "premium").execute().data
except:
    subscriptions = []

# Visitors (your table)
try:
    visitors = supabase.table("website_stats").select("*").execute().data
except:
    visitors = []

# ---------- METRICS ----------
total_users = len(users)
active_subs = len(subscriptions)
total_visitors = len(visitors)

st.title("Dashboard Administrateur")
st.caption(f"Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

col1, col2, col3 = st.columns(3)
col1.metric("Visiteurs", total_visitors)
col2.metric("Inscrits", total_users)
col3.metric("Abonnements actifs", active_subs)

st.divider()

# ---------- CHARTS ----------
import plotly.express as px
def fetch_data(table_name, date_key):
    """Récupère toutes les lignes d'une table Supabase"""
    response = supabase.table("profiles").select("*").execute()
    if response.data:
        return response.data
    return []

# Exemple pour les utilisateurs
users = fetch_data("users", "created_at")
subscriptions = fetch_data("users", "plan")
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

def build_cumulative_df_by_plan(data, date_key, plan_key="plan", target_plan="premium"):
    """
    Transforme une liste de dict en DataFrame cumulative avec deux colonnes :
    - total : nombre total d'utilisateurs
    - target : nombre d'utilisateurs avec plan spécifique (ex: premium)
    """
    # Extraire les dates et les plans
    dates_total = []
    dates_target = []

    for d in data:
        raw_date = d.get(date_key)
        if raw_date:
            try:
                dt = datetime.fromisoformat(raw_date.replace("Z", "+00:00")).date()
                dates_total.append(dt)
                if d.get(plan_key) == target_plan:
                    dates_target.append(dt)
            except:
                pass

    if not dates_total:
        return pd.DataFrame({"date": [], "total": [], target_plan: []})

    # DataFrame total
    df_total = pd.DataFrame({"date": sorted(dates_total)})
    df_total["total"] = range(1, len(df_total) + 1)
    df_total = df_total.groupby("date").max().reset_index()

    # DataFrame target plan
    df_target = pd.DataFrame({"date": sorted(dates_target)})
    df_target[target_plan] = range(1, len(df_target) + 1)
    df_target = df_target.groupby("date").max().reset_index()

    # Merge les deux
    df = pd.merge(df_total, df_target, on="date", how="outer").fillna(method="ffill").fillna(0)
    return df

def plot_comparative(df, title, target_plan="premium"):
    if df.empty:
        st.info(f"Aucune donnée pour {title}.")
        return

    fig = px.line(
        df,
        x="date",
        y=["total", target_plan],
        labels={"value": "Nombre d'utilisateurs", "date": "Date", "variable": "Type"},
        title=title,
        markers=True
    )
    fig.update_layout(
        template="plotly_white",
        hovermode="x unified",
        title=dict(x=0.5)
    )
    st.plotly_chart(fig, use_container_width=True)


# Users chart
st.subheader("Évolution des inscriptions")
df_users = build_cumulative_df(users, "created_at")
plot_daily(df_users, " ", "Nombre d'inscriptions")

# Subscriptions chart
st.subheader("Évolution des utilisateurs et premium")
df_subs = build_cumulative_df_by_plan(subscriptions, "subscription_start", target_plan="premium")
plot_comparative(df_subs, "Utilisateurs inscrits vs Premium", target_plan="premium")

# Visitors chart
st.subheader("Évolution des visiteurs")
df_visitors = build_cumulative_df(visitors, "created_at")
plot_daily(df_visitors, "Visiteurs quotidiens", "Nombre de visiteurs")

