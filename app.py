import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from PIL import Image
import io

# Configuração de Página
st.set_page_config(page_title="Sentry Guard Full", layout="wide")

# Estética Tática
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: white; }
    .tactic-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #38bdf8;
        margin-bottom: 10px;
    }
    .stTabs [aria-selected="true"] { background-color: #38bdf8 !important; color: #000 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

def gerar_pdf_completo(dados, f_susp, f_mat):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "SENTRY GUARD - RELATÓRIO OPERACIONAL", 1, 1, 'C')
    pdf.ln(5)

    for secao, info in dados.items():
        pdf.set_font("Arial", 'B', 11)
        pdf.set_fill_color(220, 230, 240)
        pdf.cell(190, 7, secao, 0, 1, 'L', fill=True)
        pdf.set_font("Arial", size=9)
        for k, v in info.items():
            if v: # Só imprime se houver dado
                pdf.multi_cell(190, 6, f"{k}: {v}", 0, 'L')
        pdf.ln(2)

    if f_susp:
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(190, 10, "ANEXO - FOTO DO SUSPEITO PRINCIPAL", 0, 1, 'L')
        Image.open(f_susp).convert("RGB").save("s.jpg")
        pdf.image("s.jpg", x=10, y=30, w=100)
    
    if f_mat:
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(190, 10, "ANEXO - MATERIAIS APREENDIDOS", 0, 1, 'L')
        Image.open(f_mat).convert("RGB").save("m.jpg")
        pdf.image("m.jpg", x=10, y=30, w=100)

    return pdf.output()

st.title("🛡️ SENTRY GUARD COMMAND")

# Estrutura de Abas
t_geral, t_vitimas, t_suspeitos, t_relato, t_fotos = st.tabs([
    "📍 Local/Guarnição", "👤 Vítimas", "🚨 Suspeitos", "📖 Relato/Apreensão", "📄 Finalizar"
])

# --- ABA 1: LOCAL E GUARNIÇÃO ---
with t_geral:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    end_fato = st.text_input("Endereço do Fato")
    col_g1, col_g2 = st.columns(2)
    prefixo = col_g1.text_input("Viatura/Prefixo")
    agentes = col_g2.text_area("Guarnição (Nomes/Matrículas)")
    st.markdown('</div>', unsafe_allow_html=True)

# --- ABA 2: VÍTIMAS (Múltiplas) ---
with t_vitimas:
    st.info("Clique nos botões abaixo para expandir os dados de cada vítima.")
    v_dados = {}
    with st.expander("👤 Dados da Vítima 01"):
        v1_n = st.text_input("Nome (V1)")
        v1_d = st.text_input("Documento (V1)")
        v1_t = st.text_input("Telefone (V1)")
        v_dados["Vítima 01"] = f"Nome: {v1_n} | Doc: {v1_d} | Tel: {v1_t}"
        
    with st.expander("👤 Dados da Vítima 02"):
        v2_n = st.text_input("Nome (V2)")
        v2_d = st.text_input("Documento (V2)")
        v2_t = st.text_input("Telefone (V2)")
        v_dados["Vítima 02"] = f"Nome: {v2_n} | Doc: {v2_d} | Tel: {v2_t}"

# --- ABA 3: SUSPEITOS (Múltiplos) ---
with t_suspeitos:
    st.info("Clique nos botões abaixo para expandir os dados de cada suspeito.")
    s_dados = {}
    for i in range(1, 4):
        with st.expander(f"🚨 Dados do Suspeito 0{i}"):
            sn = st.text_input(f"Nome/Alcunha (S{i})")
            sd = st.text_input(f"Documento (S{i})")
            sm = st.text_input(f"Nome da Mãe (S{i})")
            s_dados[f"Suspeito 0{i}"] = f"Nome: {sn} | Doc: {sd} | Mãe: {sm}"

# --- ABA 4: RELATO E APREENSÃO ---
with t_relato:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    tipo_crime = st.selectbox("Tipificação", [
        "TCO: Ameaça / Desobediência / Lesão Leve",
        "BO: Roubo / Furto / Homicídio",
        "ESPECIAL: Lei Maria da Penha",
        "ESPECIAL: Tráfico de Drogas",
        "ESPECIAL: Estatuto do Desarmamento"
    ])
    relato = st.text_area("Histórico Detalhado", height=150)
    materiais = st.text_area("Materiais Apreendidos (Quantidades/Tipos)")
    st.markdown('</div>', unsafe_allow_html=True)

# --- ABA 5: FOTOS E FINALIZAÇÃO ---
with t_fotos:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    col_f1, col_f2 = st.columns(2)
    f_susp = col_f1.file_uploader("📸 Foto do Suspeito Principal", type=['jpg','png'])
    f_mat = col_f2.file_uploader("📸 Foto das Apreensões", type=['jpg','png'])
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🏁 GERAR RELATÓRIO FINAL", use_container_width=True):
        resumo = {
            "1. EQUIPE E LOCAL": {"Viatura": prefixo, "Agentes": agentes, "Local": end_fato},
            "2. VÍTIMAS": v_dados,
            "3. SUSPEITOS": s_dados,
            "4. OCORRÊNCIA": {"Crime": tipo_crime, "Relato": relato, "Apreensões": materiais}
        }
        pdf = gerar_pdf_completo(resumo, f_susp, f_mat)
        st.download_button("⬇️ BAIXAR PDF COMPLETO", data=pdf, file_name="BO_Sentry_Guard.pdf")
                    
