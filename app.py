import streamlit as st
import pandas as pd
from datetime import datetime, time

# Configuration
st.set_page_config(page_title="Suivi Heures 2026+", layout="wide")

st.title("🕒 Mon Suivi de Travail 2026+")

# Barre latérale pour les réglages du mois
with st.sidebar:
    st.header("Paramètres")
    mois = st.selectbox("Mois", ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"])
    annee = st.number_input("Année", min_value=2026, max_value=2035, value=2026)
    heures_dispo = st.number_input("Heures disponibles (Objectif mois)", value=160.0)

# Zone de saisie
st.subheader(f"Saisie pour le jour : {datetime.now().strftime('%d/%m/%Y')}")
c1, c2, c3, c4 = st.columns(4)
with c1: m_deb = st.time_input("Matin de", time(8, 0))
with c2: m_fin = st.time_input("à", time(12, 0))
with c3: a_deb = st.time_input("Après-midi de", time(13, 0))
with c4: a_fin = st.time_input("à", time(17, 0))

# Calculs
t1 = (datetime.combine(datetime.today(), m_fin) - datetime.combine(datetime.today(), m_deb)).total_seconds() / 3600
t2 = (datetime.combine(datetime.today(), a_deb) - datetime.combine(datetime.today(), a_deb)).total_seconds() / 3600 # Correction erreur calcul aprem
t2 = (datetime.combine(datetime.today(), a_fin) - datetime.combine(datetime.today(), a_deb)).total_seconds() / 3600
total_jour = t1 + t2

if st.button("Enregistrer cette journée"):
    if 'db' not in st.session_state:
        st.session_state.db = pd.DataFrame(columns=["Date", "Matin", "Après-midi", "Total"])
    
    nouvelle_ligne = {"Date": datetime.now().strftime("%d/%m/%Y"), "Matin": f"{m_deb}-{m_fin}", "Après-midi": f"{a_deb}-{a_fin}", "Total": total_jour}
    st.session_state.db = pd.concat([st.session_state.db, pd.DataFrame([nouvelle_ligne])], ignore_index=True)
    st.success("Journée ajoutée !")

# Affichage des résultats
if 'db' in st.session_state and not st.session_state.db.empty:
    st.divider()
    prestees = st.session_state.db["Total"].sum()
    solde = prestees - heures_dispo

    k1, k2, k3 = st.columns(3)
    k1.metric("Heures Disponibles", f"{heures_dispo}h")
    k2.metric("Heures Prestées Total", f"{prestees:.2f}h")
    k3.metric("Solde", f"{solde:.2f}h", delta=f"{solde:.2f}h")

    st.table(st.session_state.db)

    csv = st.session_state.db.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Télécharger l'export Excel (CSV)", csv, f"heures_{mois}_{annee}.csv", "text/csv")
else:
    st.info("Aucune donnée enregistrée pour le moment.")
