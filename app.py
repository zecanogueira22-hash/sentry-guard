import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from PIL import Image
import io

# Configuração de Interface
st.set_page_config(page_title="Sentry Guard Pro", layout="wide")

# --- ESTÉTICA TÁTICA ---
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: white; }
    .tactic-card {
        background: rgba(255, 255, 255, 0.03);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(56, 189, 248, 0.3);
        margin-bottom: 20px;
    }
    .neon-text { color: #38bdf8; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO GERADORA DE PDF ---
def gerar_pdf_final(dados, foto_s, foto_m):
    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "SENTRY GUARD - RELATÓRIO OPERACIONAL", 1, 1, 'C')
    pdf.ln(5)

    # Texto do Relatório
    for secao, info in dados.items():
        pdf.set_font("Arial", 'B', 12)
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(190, 8, secao, 0, 1, 'L', fill=True)
        pdf.set_font("Arial", size=10)
        if isinstance(info, dict):
            for k, v in info.items():
                pdf.multi_cell(190, 6, f"{k}: {v}", 0, 'L')
        else:
            pdf.multi_cell(190, 6, str(info), 0, 'L')
        pdf.ln(4)

    # Anexo: Foto do Suspeito
    if foto_s:
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(190, 10, "ANEXO I - IDENTIFICAÇÃO DO SUSPEITO", 0, 1, 'L')
        img_s = Image.open(foto_s)
        img_s.save("temp_s.png")
        pdf.image("temp_s.png", x=10, y=30, w=100)
        pdf.ln(110)
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(190, 10, f"Legenda: {dados['2. SUSPEITO']['Nome']}", 0, 1, 'L')

    # Anexo: Materiais Apreendidos
    if foto_m:
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(190, 10, "ANEXO II - MATERIAIS APREENDIDOS", 0, 1, 'L')
        img_m = Image.open(foto_m)
        img_m.save("temp_m.png")
        pdf.image("temp_m.png", x=10, y=30, w=100)
        pdf.ln(110)
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(190, 10, f"Descrição: {dados['3. APREENSÕES']['Itens']}", 0, 1, 'L')

    return pdf.output()

# --- INTERFACE DO APP ---
st.sidebar.markdown("<h1 class='neon-text'>🛡️ SENTRY GUARD</h1>", unsafe_allow_html=True)
menu = st.sidebar.radio("Módulo", ["Novo BO / TCO", "Mancha Criminal"])

if menu == "Novo BO / TCO":
    st.markdown("<h2 class='neon-text'>📝 REGISTRO OPERACIONAL COMPLETO</h2>", unsafe_allow_html=True)

    # 1. Local e Natureza
    with st.container():
        st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
        st.markdown("### 📍 Dados do Fato")
        col1, col2 = st.columns(2)
        nat = col1.selectbox("Natureza", ["Tráfico", "Roubo", "Porte de Arma", "Ameaça", "TCO - Outros"])
        loc_fato = col2.text_input("Localização do Crime (Endereço)")
        st.markdown('</div>', unsafe_allow_html=True)

    # 2. Suspeito e Foto
    with st.container():
        st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
        st.markdown("### 🚨 Qualificação do Suspeito")
        s_col1, s_col2 = st.columns(2)
        with s_col1:
            s_nome = st.text_input("Nome/Alcunha")
            s_doc = st.text_input("Documento (RG/CPF)")
            s_mae = st.text_input("Filiação (Mãe)")
        with s_col2:
            f_suspeito = st.file_uploader("📸 Foto do Suspeito", type=['jpg','png'])
            if f_suspeito: st.image(f_suspeito, width=150)
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. Apreensões e Foto
    with st.container():
        st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
        st.markdown("### 📦 Materiais Apreendidos")
        m_col1, m_col2 = st.columns(2)
        with m_col1:
            materiais = st.text_area("Descrição (Armas, Drogas, Valores)")
        with m_col2:
            f_material = st.file_uploader("📸 Foto do Material", type=['jpg','png'])
            if f_material: st.image(f_material, width=150)
        st.markdown('</div>', unsafe_allow_html=True)

    # Botão Final
    if st.button("🚀 GERAR RELATÓRIO FINAL"):
        dados_bo = {
            "1. DADOS": {"Natureza": nat, "Local": loc_fato},
            "2. SUSPEITO": {"Nome": s_nome, "Doc": s_doc, "Mãe": s_mae},
            "3. APREENSÕES": {"Itens": materiais}
        }
        pdf = gerar_pdf_final(dados_bo, f_suspeito, f_material)
        st.download_button("⬇️ BAIXAR PDF COM FOTOS", data=pdf, file_name="Relatorio_Sentry.pdf")

elif menu == "Mancha Criminal":
    st.title("📍 Inteligência de Mancha Criminal")
    st.info("Aqui serão plotados os endereços digitados nos BOs.")
    
