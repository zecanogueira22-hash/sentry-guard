import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from PIL import Image
import io

# Configuração Master
st.set_page_config(page_title="Sentry Guard Intelligence", layout="wide")

# Estética Tática
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: white; }
    .tactic-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #38bdf8;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
        color: white;
    }
    .stTabs [aria-selected="true"] { background-color: #38bdf8 !important; color: #000 !important; }
    </style>
    """, unsafe_allow_html=True)

def gerar_pdf_completo(dados, f_susp, f_mat):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "SENTRY GUARD - RELATÓRIO OPERACIONAL COMPLETO", 1, 1, 'C')
    pdf.ln(5)

    for secao, info in dados.items():
        pdf.set_font("Arial", 'B', 12)
        pdf.set_fill_color(220, 230, 240)
        pdf.cell(190, 8, secao, 0, 1, 'L', fill=True)
        pdf.set_font("Arial", size=10)
        for k, v in info.items():
            pdf.multi_cell(190, 7, f"{k}: {v}", 0, 'L')
        pdf.ln(3)

    if f_susp:
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(190, 10, "ANEXO I - IDENTIFICAÇÃO DO SUSPEITO", 0, 1, 'L')
        Image.open(f_susp).convert("RGB").save("s.jpg")
        pdf.image("s.jpg", x=10, y=30, w=100)
    
    if f_mat:
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(190, 10, "ANEXO II - MATERIAIS APREENDIDOS", 0, 1, 'L')
        Image.open(f_mat).convert("RGB").save("m.jpg")
        pdf.image("m.jpg", x=10, y=30, w=100)

    return pdf.output()

st.title("🛡️ SENTRY GUARD PRO")

# --- ORGANIZAÇÃO POR ABAS (COMO SE FOSSEM BOTÕES) ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📍 Local/Guarnição", "👤 Envolvidos", "🚨 Crime/Relato", "📦 Materiais/Fotos", "📄 Finalizar"])

with tab1:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    st.subheader("📍 Dados da Localização e Equipe")
    end_fato = st.text_input("Local da Ocorrência (Endereço Completo)")
    col_g1, col_g2 = st.columns(2)
    prefixo = col_g1.text_input("Prefixo da Viatura")
    agentes = col_g2.text_area("Composição da Guarnição (Nomes/Matrículas)")
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    col_v, col_s = st.columns(2)
    with col_v:
        st.subheader("👤 Dados da Vítima")
        v_nome = st.text_input("Nome da Vítima")
        v_nasc = st.text_input("Data Nasc. Vítima")
        v_doc = st.text_input("Doc. Vítima")
    with col_s:
        st.subheader("🚨 Dados do Suspeito")
        s_nome = st.text_input("Nome/Alcunha Suspeito")
        s_nasc = st.text_input("Data Nasc. Suspeito")
        s_mae = st.text_input("Nome da Mãe Suspeito")
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    st.subheader("📖 Tipificação e Relato")
    tipo_crime = st.selectbox("Classificação da Ocorrência", [
        "BAIXO POTENCIAL: Ameaça / Desobediência / Lesão Leve",
        "MÉDIO POTENCIAL: Furto / Dano / Estelionato",
        "ALTO POTENCIAL: Roubo / Homicídio / Latrocínio",
        "LEI ESPECIAL: Tráfico de Drogas (Lei 11.343)",
        "LEI ESPECIAL: Maria da Penha (Lei 11.340)",
        "LEI ESPECIAL: Estatuto do Desarmamento"
    ])
    relato = st.text_area("Histórico Detalhado", height=200)
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    st.subheader("📷 Evidências e Apreensões")
    desc_mat = st.text_area("Materiais Apreendidos (Discriminar quantidades)")
    c_f1, c_f2 = st.columns(2)
    f_susp = c_f1.file_uploader("📸 Foto do Suspeito", type=['jpg','jpeg','png'])
    f_mat = c_f2.file_uploader("📸 Foto do Material", type=['jpg','jpeg','png'])
    st.markdown('</div>', unsafe_allow_html=True)

with tab5:
    st.subheader("🏁 Encerramento")
    if st.button("GERAR BOLETIM COMPLETO", use_container_width=True):
        dados = {
            "1. GUARNIÇÃO E LOCAL": {"Prefixo": prefixo, "Agentes": agentes, "Local": end_fato},
            "2. VÍTIMA": {"Nome": v_nome, "Nascimento": v_nasc, "Documento": v_doc},
            "3. SUSPEITO": {"Nome": s_nome, "Nascimento": s_nasc, "Mãe": s_mae},
            "4. OCORRÊNCIA": {"Natureza": tipo_crime, "Relato": relato},
            "5. APREENSÕES": {"Itens": desc_mat}
        }
        pdf_out = gerar_pdf_completo(dados, f_susp, f_mat)
        st.download_button("⬇️ BAIXAR PDF", data=pdf_out, file_name="BO_COMPLETO.pdf")
        
