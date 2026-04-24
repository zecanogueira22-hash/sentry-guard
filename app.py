import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from PIL import Image
import io

# Configuração da página
st.set_page_config(page_title="Sentry Guard Pro", layout="wide")

# Estilo visual tático
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: white; }
    .tactic-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #38bdf8;
        margin-bottom: 20px;
    }
    .section-title { color: #38bdf8; font-size: 20px; font-weight: bold; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Função para gerar o PDF
def gerar_pdf(dados, foto_s, foto_m):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "SENTRY GUARD - RELATÓRIO OPERACIONAL", 1, 1, 'C')
    pdf.ln(10)
    
    for secao, info in dados.items():
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(190, 8, secao, 0, 1, 'L')
        pdf.set_font("Arial", size=10)
        for k, v in info.items():
            pdf.multi_cell(190, 7, f"{k}: {v}", 0, 'L')
        pdf.ln(5)

    if foto_s:
        pdf.add_page()
        pdf.cell(190, 10, "FOTO DO SUSPEITO", 0, 1, 'L')
        img_s = Image.open(foto_s).convert("RGB")
        img_s.save("s.jpg")
        pdf.image("s.jpg", x=10, y=30, w=100)

    if foto_m:
        pdf.add_page()
        pdf.cell(190, 10, "MATERIAL APREENDIDO", 0, 1, 'L')
        img_m = Image.open(foto_m).convert("RGB")
        img_m.save("m.jpg")
        pdf.image("m.jpg", x=10, y=30, w=100)

    return pdf.output()

st.title("🛡️ SENTRY GUARD COMMAND")

# --- 1. LOCALIZAÇÃO E NATUREZA ---
st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
st.markdown('<p class="section-title">📍 LOCALIZAÇÃO E NATUREZA</p>', unsafe_allow_html=True)
end_fato = st.text_input("Endereço Completo do Fato", placeholder="Rua, Número, Bairro, Cidade")

tipo_crime = st.selectbox("Natureza da Ocorrência", [
    "-- Baixo Potencial (TCO) --",
    "Ameaça (Art. 147)", "Lesão Corporal Leve", "Desobediência / Desacato",
    "-- Médio/Alto Potencial (BO) --",
    "Roubo (Art. 157)", "Furto Qualificado", "Tráfico de Drogas", "Homicídio",
    "-- Legislação Especial --",
    "Lei Maria da Penha", "Estatuto do Desarmamento", "Crime Ambiental"
])
st.markdown('</div>', unsafe_allow_html=True)

# --- 2. QUALIFICAÇÃO DO SUSPEITO ---
st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
st.markdown('<p class="section-title">🚨 QUALIFICAÇÃO DO SUSPEITO</p>', unsafe_allow_html=True)
col_s1, col_s2 = st.columns(2) # Aqui estava o erro! Coloquei o número 2.
with col_s1:
    s_nome = st.text_input("Nome / Alcunha")
    s_nasc = st.text_input("Data de Nascimento (ou Idade)")
    s_mae = st.text_input("Filiação (Mãe)")
with col_s2:
    f_susp = st.file_uploader("📷 FOTO DO SUSPEITO", type=['jpg', 'png', 'jpeg'])
    if f_susp: st.image(f_susp, width=150)
st.markdown('</div>', unsafe_allow_html=True)

# --- 3. MATERIAIS APREENDIDOS ---
st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
st.markdown('<p class="section-title">📦 MATERIAIS APREENDIDOS</p>', unsafe_allow_html=True)
col_m1, col_m2 = st.columns(2)
with col_m1:
    mat_desc = st.text_area("Descrição (Armas, Drogas, Valores)")
with col_m2:
    f_mat = st.file_uploader("📷 FOTO DO MATERIAL", type=['jpg', 'png', 'jpeg'])
    if f_mat: st.image(f_mat, width=150)
st.markdown('</div>', unsafe_allow_html=True)

# Botão Final
if st.button("🏁 FINALIZAR E GERAR PDF", use_container_width=True):
    dados = {
        "DADOS DO FATO": {"Endereço": end_fato, "Natureza": tipo_crime, "Data": datetime.now().strftime("%d/%m/%Y")},
        "SUSPEITO": {"Nome": s_nome, "Nascimento": s_nasc, "Mãe": s_mae},
        "APREENSÕES": {"Relato": mat_desc}
    }
    pdf_bytes = gerar_pdf(dados, f_susp, f_mat)
    st.download_button("⬇️ BAIXAR RELATÓRIO", data=pdf_bytes, file_name="BO_Sentry.pdf")
    
