import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="Sentry Guard Pro", layout="wide")

# --- FUNÇÃO PARA ENVIAR E-MAIL ---
def enviar_email(agente, tipo, gps, relato):
    remetente = "zecanogueira22@gmail.com"
    destinatario = "zecanogueira22@gmail.com"
    # IMPORTANTE: Aqui você precisará de uma "Senha de App" do Google
    senha = "SUA_SENHA_DE_APP_AQUI" 

    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = f"🚨 OCORRÊNCIA: {tipo} - Agente {agente}"

    corpo = f"""
    RELATÓRIO DE OCORRÊNCIA - SENTRY GUARD
    --------------------------------------
    Agente Responsável: {agente}
    Natureza do Crime: {tipo}
    Localização (GPS): {gps}
    
    RELATO DOS FATOS:
    {relato}
    --------------------------------------
    Enviado automaticamente via Sentry Guard Pro.
    """
    msg.attach(MIMEText(corpo, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remetente, senha)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Erro: {e}")
        return False

# --- INTERFACE ---
st.sidebar.title("🛡️ SENTRY GUARD")
page = st.sidebar.radio("Navegação", ["Dashboard", "Registro de Campo"])

if page == "Dashboard":
    st.title("📊 Painel de Controle")
    st.map(pd.DataFrame({'lat': [-23.55], 'lon': [-46.63]}))

elif page == "Registro de Campo":
    st.title("📝 Nova Ocorrência")
    
    # Captura de GPS
    if st.button("📍 Capturar GPS Atual"):
        location = streamlit_js_eval(js_expressions="navigator.geolocation.getCurrentPosition(success => { return success.coords })", key="pos")
        if location:
            st.session_state['gps'] = f"{location['latitude']}, {location['longitude']}"
            st.success("Localização capturada!")

    with st.form("form_ocorrencia"):
        agente = st.text_input("ID/Nome do Agente")
        tipo = st.selectbox("Natureza", ["Roubo", "Tráfico", "Homicídio", "Maria da Penha", "Agressão", "Outros"])
        gps = st.text_input("Coordenadas", value=st.session_state.get('gps', 'Não capturado'))
        relato = st.text_area("Relato Detalhado")
        
        enviar = st.form_submit_button("Finalizar e Enviar p/ E-mail")
        
        if enviar:
            if enviar_email(agente, tipo, gps, relato):
                st.success(f"✅ Relatório enviado com sucesso para zecanogueira22@gmail.com")
            else:
                st.error("❌ Erro ao enviar e-mail. Verifique a Senha de App.")
