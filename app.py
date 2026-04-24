import streamlit as st
import pandas as pd
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="Sentry Guard GPS", layout="wide")

# Menu Lateral
st.sidebar.title("🛡️ SENTRY GUARD")
page = st.sidebar.radio("Navegação", ["Dashboard", "Registro de Campo"])

if page == "Dashboard":
    st.title("📊 Mapa de Calor Real")
    # Aqui, no futuro, leremos os dados que você salvou
    st.info("O mapa abaixo mostra pontos fixos. Quando ligarmos o banco de dados, ele mostrará o GPS real das ocorrências.")
    df = pd.DataFrame({'lat': [-23.55], 'lon': [-46.63]})
    st.map(df)

elif page == "Registro de Campo":
    st.title("📝 Nova Ocorrência com GPS")
    
    # --- BLOCO DO GPS ---
    st.subheader("📍 Localização por Satélite")
    if st.button("📍 Capturar Coordenadas do GPS"):
        loc = streamlit_js_eval(js_expressions="navigator.geolocation.getCurrentPosition(x => console.log(x))", key="getLocation")
        # O navegador vai pedir permissão para usar o GPS. O usuário deve clicar em "Permitir".
        location = streamlit_js_eval(js_expressions="navigator.geolocation.getCurrentPosition(success => { return success.coords })", key="pos")
        
        if location:
            st.success(f"Coordenadas capturadas: Lat {location['latitude']}, Lon {location['longitude']}")
            st.session_state['gps'] = f"{location['latitude']}, {location['longitude']}"
        else:
            st.warning("Aguardando sinal do GPS ou permissão do navegador...")
    
    # --- FORMULÁRIO ---
    with st.form("form_policia"):
        agente = st.text_input("ID do Agente")
        tipo = st.selectbox("Natureza", ["Roubo", "Furto", "Tráfico", "Maria da Penha", "Homicídio", "Agressão"])
        gps_final = st.text_input("Coordenadas (Auto)", value=st.session_state.get('gps', 'Clique no botão acima'))
        relato = st.text_area("Relato")
        
        if st.form_submit_button("Transmitir Ocorrência"):
            st.success("Dados enviados para a central!")
    
