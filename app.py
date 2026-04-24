import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Sentry Guard Command", layout="wide")

st.sidebar.title("🛡️ SENTRY GUARD")
page = st.sidebar.radio("Navegação", ["Dashboard", "Registro", "Consulta"])

if page == "Dashboard":
    st.header("📊 Painel de Controle")
    col1, col2 = st.columns(2)
    col1.metric("Ocorrências Hoje", "14", "+2")
    col2.metric("Tempo Resposta", "12 min", "-2 min")
    st.subheader("📍 Mancha Criminal")
    map_data = pd.DataFrame({'lat': [-23.55], 'lon': [-46.63]})
    st.map(map_data)

elif page == "Registro":
    st.header("📝 Nova Ocorrência")
    with st.form("registro"):
        tipo = st.selectbox("Natureza", ["Roubo", "Furto", "Entorpecentes"])
        relato = st.text_area("Histórico")
        if st.form_submit_button("Transmitir"):
            st.success("✅ Transmitido!")

elif page == "Consulta":
    st.header("🔍 Inteligência")
    cpf = st.text_input("Consultar CPF")
    if st.button("Buscar"):
        st.success("✅ Nada Consta")
        
