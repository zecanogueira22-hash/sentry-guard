import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from PIL import Image
import io

# Configuração Master
st.set_page_config(page_title="Sentry Guard Pro", layout="wide")

# --- ESTÉTICA TÁTICA ---
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: white; }
    .tactic-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #38bdf8;
        margin-bottom: 25px;
    }
    .section-title { color: #38bdf8; font-size: 24px; font-weight: bold; margin-bottom: 15px; border-bottom: 1px solid #38bdf8; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO GERADORA DE PDF ---
def gerar_pdf_final(dados, foto_s, foto_m):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "SENTRY GUARD - RELATÓRIO OPERACIONAL", 1, 1, 'C')
    pdf.ln(10)

    for secao, info in dados.items():
        pdf.set_font("Arial", 'B', 12)
        pdf.set_fill_color(200, 220, 255)
        pdf.cell(190, 8, secao, 0, 1, 'L', fill=True)
        pdf.set_font("Arial", size=11)
        if isinstance(info, dict):
            for k, v in info.items():
                pdf.multi_cell(190, 7, f"{k}: {v}", 0, 'L')
        else:
            pdf.multi_cell(190, 7, str(info), 0, 'L')
        pdf.ln(5)

    # Anexo Foto Suspeito
    if foto_s:
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(190, 10, "ANEXO I - FOTO DO SUSPEITO", 0, 1, 'L')
        img_s = Image.open(foto_s)
        img_s.save("temp_s.png")
        pdf.image("temp_s.png", x=10, y=30, w=120)
    
    # Anexo Foto Material
    if foto_m:
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(190, 10, "ANEXO II - MATERIAL APREENDIDO", 0, 1, 'L')
        img_m = Image.open(foto_m)
        img_m.save("temp_m.png")
        pdf.image("temp_m.png", x=10, y=30, w=120)

    return pdf.output()

# --- INTERFACE ---
st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🛡️ SENTRY GUARD COMMAND</h1>", unsafe_allow_html=True)

# SEÇÃO 1: LOCALIZAÇÃO DO FATO
st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
st.markdown('<p class="section-title">📍 1. LOCALIZAÇÃO DO CRIME</p>', unsafe_allow_html=True)
local_fato = st.text_input("Endereço Completo (Rua, Nº, Bairro, Cidade)", placeholder="Ex: Rua das Flores, 123, Centro, São Paulo")
natureza = st.selectbox("Natureza da Ocorrência", ["Tráfico de Drogas", "Roubo", "Furto", "Porte de Arma", "Ameaça", "Lei Maria da Penha", "Outros"])
st.markdown('</div>', unsafe_allow_html=True)

# SEÇÃO 2: SUSPEITO E FOTO
st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
st.markdown('<p class="section-title">🚨 2. QUALIFICAÇÃO DO SUSPEITO</p>', unsafe_allow_html=True)
col_s1, col_s2 = st.columns()
with col_s1:
    s_nome = st.text_input("Nome Completo / Alcunha")
    s_doc = st.text_input("Documento (RG ou CPF)")
    s_mae = st.text_input("Nome da Mãe")
with col_s2:
    foto_suspeito = st.file_uploader("📷 TIRAR FOTO DO SUSPEITO", type=['jpg', 'png', 'jpeg'], key="f_susp")
    if foto_suspeito:
        st.image(foto_suspeito, caption="Preview Suspeito", width=200)
st.markdown('</div>', unsafe_allow_html=True)

# SEÇÃO 3: APREENSÕES E FOTO
st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
st.markdown('<p class="section-title">📦 3. OBJETOS / MATERIAIS APREENDIDOS</p>', unsafe_allow_html=True)
col_m1, col_m2 = st.columns()
with col_m1:
    detalhes_material = st.text_area("Descreva os itens (Ex: 50g de substância análoga à cocaína, 01 faca, R$ 200,00)")
with col_m2:
    foto_material = st.file_uploader("📷 TIRAR FOTO DO MATERIAL", type=['jpg', 'png', 'jpeg'], key="f_mat")
    if foto_material:
        st.image(foto_material, caption="Preview Material", width=200)
st.markdown('</div>', unsafe_allow_html=True)

# BOTÃO DE FINALIZAÇÃO
if st.button("🏁 FINALIZAR OCORRÊNCIA E GERAR PDF", use_container_width=True):
    if not local_fato or not s_nome:
        st.error("⚠️ Por favor, preencha ao menos o Local e o Nome do Suspeito.")
    else:
        dados = {
            "DADOS DA OCORRÊNCIA": {"Local": local_fato, "Natureza": natureza, "Data/Hora": datetime.now().strftime("%d/%m/%Y %H:%M")},
            "QUALIFICAÇÃO DO SUSPEITO": {"Nome": s_nome, "Documento": s_doc, "Mãe": s_mae},
            "MATERIAIS APREENDIDOS": {"Descrição": detalhes_material}
        }
        pdf_out = gerar_pdf_final(dados, foto_suspeito, foto_material)
        st.download_button("⬇️ BAIXAR RELATÓRIO COMPLETO (PDF)", data=pdf_out, file_name=f"BO_{s_nome}.pdf", mime="application/pdf")
        st.success("Relatório gerado com sucesso!")
