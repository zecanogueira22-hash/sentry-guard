import streamlit as st
import pandas as pd
from streamlit_js_eval import streamlit_js_eval

# Configuração de Interface
st.set_page_config(page_title="Sentry Guard Command", layout="wide")

# Estilo CSS para melhorar a aparência
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .section-pnl { padding: 20px; border-radius: 10px; background-color: #1d2129; margin-bottom: 20px; border-left: 5px solid #007bff; }
    h3 { color: #007bff; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.title("🛡️ SENTRY GUARD")
st.sidebar.markdown("---")
page = st.sidebar.selectbox("Navegação", ["Dashboard", "Novo Registro (BO/TCO)"])

if page == "Dashboard":
    st.title("📊 Estatística Operacional")
    col1, col2, col3 = st.columns(3)
    col1.metric("Ocorrências Hoje", "12", "+2")
    col2.metric("TCOs Lavrados", "05", "+1")
    col3.metric("Mandados Positivos", "02", "0")
    st.map(pd.DataFrame({'lat': [-23.55], 'lon': [-46.63]}))

elif page == "Novo Registro (BO/TCO)":
    st.title("📝 Registro de Ocorrência Detalhado")
    
    # --- DADOS DA OCORRÊNCIA ---
    st.markdown('<div class="section-pnl"><h3>1. Natureza da Ocorrência</h3>', unsafe_allow_html=True)
    col_nat1, col_nat2 = st.columns(2)
    with col_nat1:
        tipo_crime = st.selectbox("Tipificação GEP (Grau de Potencial)", [
            "-- Baixo Potencial (TCO) --",
            "Ameaça (Art. 147 CP)", "Lesão Corporal Leve (Art. 121 CP)", "Desobediência (Art. 330 CP)", "Desacato (Art. 331 CP)",
            "-- Médio/Alto Potencial (BO/Inquérito) --",
            "Roubo (Art. 157 CP)", "Furto Qualificado (Art. 155 CP)", "Homicídio (Art. 121 CP)", "Estupro (Art. 213 CP)",
            "-- Legislações Especiais --",
            "Tráfico de Drogas (Lei 11.343/06)", "Porte Ilegal de Arma (Lei 10.826/03)", "Maria da Penha (Lei 11.340/06)", "Crime Ambiental (Lei 9.605/98)", "Estatuto do Idoso"
        ])
    with col_nat2:
        if st.button("📍 Capturar GPS da Viatura"):
            loc = streamlit_js_eval(js_expressions="navigator.geolocation.getCurrentPosition(s => {return s.coords})", key="gps")
            if loc: st.session_state['gps'] = f"{loc['latitude']}, {loc['longitude']}"
        gps_input = st.text_input("Coordenadas", value=st.session_state.get('gps', ''))
    st.markdown('</div>', unsafe_allow_html=True)

    # --- QUALIFICAÇÃO DA VÍTIMA ---
    st.markdown('<div class="section-pnl"><h3>2. Qualificação da Vítima</h3>', unsafe_allow_html=True)
    v_col1, v_col2 = st.columns(2)
    with v_col1:
        v_nome = st.text_input("Nome Completo (Vítima)")
        v_data_nasc = st.date_input("Data de Nascimento", key="v_data", min_value=pd.to_datetime('1920-01-01'))
    with v_col2:
        v_doc = st.text_input("RG ou CPF (Vítima)")
        v_mae = st.text_input("Nome da Mãe (Vítima)")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- QUALIFICAÇÃO DO SUSPEITO ---
    st.markdown('<div class="section-pnl"><h3>3. Qualificação do Suspeito / Autor</h3>', unsafe_allow_html=True)
    s_col1, s_col2 = st.columns(2)
    with s_col1:
        s_nome = st.text_input("Nome ou Apelido (Suspeito)")
        s_data_nasc = st.date_input("Data de Nascimento", key="s_data", min_value=pd.to_datetime('1920-01-01'))
    with s_col2:
        s_doc = st.text_input("Documento/Alcunha")
        s_mae = st.text_input("Nome da Mãe (Suspeito)")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- RELATO ---
    st.markdown('<div class="section-pnl"><h3>4. Histórico da Ocorrência</h3>', unsafe_allow_html=True)
    relato = st.text_area("Descreva detalhadamente a dinâmica dos fatos...")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🚀 FINALIZAR E GERAR RELATÓRIO"):
        st.success("Relatório gerado localmente! Pronto para envio.")
        # Aqui entra a função de e-mail que configuramos antes
    
