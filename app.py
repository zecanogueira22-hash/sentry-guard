import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from PIL import Image
import io

# 1. NOME NA ABA E NO ÍCONE DO CELULAR
st.set_page_config(
    page_title="B.O. FÁCIL", 
    page_icon="🛡️", 
    layout="wide"
)

# --- ESTÉTICA COM SUA PALETA DE CORES ---
st.markdown(f"""
    <style>
    .stApp {{
        background: #1A334A;
        color: white;
    }}
    .tactic-card {{
        background: rgba(30, 83, 110, 0.4);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #18A3B7;
        margin-bottom: 10px;
    }}
    .section-title, h1, h2, h3 {{
        color: #27E6EC !important;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: #27E6EC !important;
        color: #1A334A !important;
        font-weight: bold;
    }}
    .stButton>button {{
        background: #18A3B7;
        color: white;
        border-radius: 8px;
        width: 100%;
    }}
    </style>
    """, unsafe_allow_html=True)

def gerar_pdf_completo(dados, f_susp, f_mat):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "B.O. FÁCIL - RELATÓRIO OPERACIONAL", 1, 1, 'C')
    pdf.ln(5)

    for secao, info in dados.items():
        pdf.set_font("Arial", 'B', 11)
        pdf.set_fill_color(230, 230, 240)
        pdf.cell(190, 7, secao, 0, 1, 'L', fill=True)
        pdf.set_font("Arial", size=9)
        if isinstance(info, dict):
            for k, v in info.items():
                if v: pdf.multi_cell(190, 6, f"{k}: {v}", 0, 'L')
        pdf.ln(2)

    if f_susp:
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(190, 10, "ANEXO - FOTO DO SUSPEITO", 0, 1, 'L')
        Image.open(f_susp).convert("RGB").save("s.jpg")
        pdf.image("s.jpg", x=10, y=30, w=100)
    
    if f_mat:
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(190, 10, "ANEXO - MATERIAL APREENDIDO", 0, 1, 'L')
        Image.open(f_mat).convert("RGB").save("m.jpg")
        pdf.image("m.jpg", x=10, y=30, w=100)

    return pdf.output()

# 2. TÍTULO PRINCIPAL NA TELA
st.markdown("<h1>🛡️ B.O. FÁCIL</h1>", unsafe_allow_html=True)

t_geral, t_vitimas, t_suspeitos, t_relato, t_fotos = st.tabs([
    "📍 Local/Guarnição", "👤 Vítimas", "🚨 Suspeitos", "📖 Relato/Apreensão", "📄 Finalizar"
])

with t_geral:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    end_fato = st.text_input("Endereço do Fato")
    col_g1, col_g2 = st.columns(2)
    prefixo = col_g1.text_input("Viatura/Prefixo")
    agentes = col_g2.text_area("Guarnição (Nomes/Matrículas)")
    st.markdown('</div>', unsafe_allow_html=True)

with t_vitimas:
    v_dados = {}
    with st.expander("👤 Vítima 01"):
        v1_n = st.text_input("Nome (V1)")
        v1_d = st.text_input("Documento (V1)")
        v_dados["Vítima 01"] = f"Nome: {v1_n} | Doc: {v1_d}" if v1_n else ""
    with st.expander("👤 Vítima 02"):
        v2_n = st.text_input("Nome (V2)")
        v2_d = st.text_input("Documento (V2)")
        v_dados["Vítima 02"] = f"Nome: {v2_n} | Doc: {v2_d}" if v2_n else ""

with t_suspeitos:
    s_dados = {}
    for i in range(1, 4):
        with st.expander(f"🚨 Suspeito 0{i}"):
            sn = st.text_input(f"Nome/Alcunha (S{i})")
            sd = st.text_input(f"Doc (S{i})")
            sm = st.text_input(f"Mãe (S{i})")
            s_dados[f"Suspeito 0{i}"] = f"Nome: {sn} | Doc: {sd} | Mãe: {sm}" if sn else ""

with t_relato:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    tipo_crime = st.selectbox("Tipificação", ["TCO", "BO Comum", "Lei Maria da Penha", "Tráfico", "Estatuto Desarmamento"])
    relato = st.text_area("Histórico", height=150)
    materiais = st.text_area("Apreensões")
    st.markdown('</div>', unsafe_allow_html=True)

with t_fotos:
    col_f1, col_f2 = st.columns(2)
    f_susp = col_f1.file_uploader("📸 Foto Suspeito", type=['jpg','png'])
    f_mat = col_f2.file_uploader("📸 Foto Materiais", type=['jpg','png'])
    
    if st.button("🏁 FINALIZAR E GERAR PDF"):
        resumo = {
            "EQUIPE/LOCAL": {"Viatura": prefixo, "Local": end_fato},
            "VÍTIMAS": v_dados,
            "SUSPEITOS": s_dados,
            "OCORRÊNCIA": {"Crime": tipo_crime, "Relato": relato, "Materiais": materiais}
        }
        pdf = gerar_pdf_completo(resumo, f_susp, f_mat)
        st.download_button("⬇️ BAIXAR B.O.", data=pdf, file_name="BO_FACIL.pdf")
