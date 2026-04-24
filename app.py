import streamlit as st

st.set_page_config(page_title="Sentry Guard", page_icon="🛡️")

st.title("🛡️ Sentry Guard")
st.subheader("Registro de Ocorrências Inteligente")

with st.form("registro_ocorrencia"):
    nome_agente = st.text_input("Nome do Policial")
    tipo_crime = st.selectbox("Tipo de Crime", ["Roubo", "Furto", "Agressão", "Tráfico"])
    relato = st.text_area("Relato dos Fatos")
    
    enviar = st.form_submit_button("Finalizar Ocorrência")
    
    if enviar:
        st.success(f"Ocorrência de {tipo_crime} registrada com sucesso!")
        st.info(f"Agente responsável: {nome_agente}")
      
