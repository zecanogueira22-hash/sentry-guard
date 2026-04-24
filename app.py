import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from PIL import Image
import io

# Configuração de Interface
st.set_page_config(page_title="Sentry Guard Pro", layout="wide")

# Estilo visual tático (CSS)
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: white; }
    .tactic-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #38bdf8;
        margin-bottom: 25px;
    }
    .section-title { color: #38bdf8; font-size: 20px; font-weight: bold; border-bottom: 1px solid #38bdf8; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# Função para criar o PDF oficial
def gerar_pdf(dados, foto_s, foto_m):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "SENTRY GUARD - RELATÓRIO OPERACIONAL", 1, 1, 'C')
    pdf.ln(10)
    
    for secao, info in dados.items():
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(190, 8, secao, 0, 1, 'L', fill=False)
        pdf.set_font("Arial", size=11)
        for k, v in info.items():
            pdf.multi_cell(190, 7, f"{k}: {v}", 0, 'L')
        pdf.ln(5)

    if foto_s:
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(190, 10, "FOTO DO SUSPEITO", 0, 1, 'L')
        img_s = Image.open(foto_s).convert("RGB")
        img_s.save("s.jpg")
        pdf.image("s.jpg", x=10, y=30, w=120)

    if foto_m:
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(190, 10, "MATERIAL APREENDIDO", 0, 1, 'L')
        img_m = Image.open(foto_m).convert("RGB")
        img_m.save("m.jpg")
        pdf.image("m.jpg", x=10, y=30, w=120)

    return pdf.output()

st.title("🛡️ SENTRY GUARD COMMAND")

# 1. LOCALIZAÇÃO E NATUREZA
st.markdown('<div class="tactic-card"><p class="section-title">📍 1. LOCALIZAÇÃO DO FATO</p>', unsafe_allow_html=True)
local_fato = st.text_input("Endereço Completo (Rua, Nº, Bairro, Cidade)")
natureza = st.selectbox("Natureza Criminal", [
    "Tráfico de Drogas", "Roubo / Furto", "Porte de Arma", "Maria da Penha", "Ameaça", "TCO - Outros"
])
st.markdown('</div>', unsafe_allow_html=True)

# 2. SUSPEITO
st.markdown('<div class="tactic-card"><p class="section-title">🚨 2. QUALIFICAÇÃO DO SUSPEITO</p>', unsafe_allow_html=True)
s_nome = st.text_input("Nome / Alcunha")
s_doc = st.text_input("RG / CPF")
s_mae = st.text_input("Filiação (Mãe)")
foto_susp = st.file_uploader("📷 TIRAR FOTO DO SUSPEITO", type=['jpg', 'png', 'jpeg'])
if foto_susp: st.image(foto_susp, width=250)
st.markdown('</div>', unsafe_allow_html=True)

# 3. APREENSÕES
st.markdown('<div class="tactic-card"><p class="section-title">📦 3. MATERIAIS APREENDIDOS</p>', unsafe_allow_html=True)
materiais = st.text_area("Descreva as apreensões (Drogas, Armas, Valores)")
foto_mat = st.file_uploader("📷 TIRAR FOTO DOS MATERIAIS", type=['jpg', 'png', 'jpeg'])
if foto_mat: st.image(foto_mat, width=250)
st.markdown('</div>', unsafe_allow_html=True)

# BOTÃO FINAL
if st.button("🏁 FINALIZAR E GERAR PDF", use_container_width=True):
    if not local_fato or not s_nome:
        st.warning("Preencha ao menos o Local e o Nome para gerar o PDF.")
    else:
        dados_relatorio = {
            "DADOS DA OCORRÊNCIA": {"Endereço": local_fato, "Natureza": natureza, "Data": datetime.now().strftime("%d/%m/%Y %H:%M")},
            "QUALIFICAÇÃO DO SUSPEITO": {"Nome": s_nome, "Doc": s_doc, "Mãe": s_mae},
            "RELATO DE APREENSÃO": {"Itens": materiais}
        }
        pdf_bytes = gerar_pdf(dados_relatorio, foto_susp, foto_mat)
        st.download_button("⬇️ BAIXAR RELATÓRIO EM PDF", data=pdf_bytes, file_name=f"BO_{s_nome}.pdf")
        st.success("PDF pronto para baixar!")
        
