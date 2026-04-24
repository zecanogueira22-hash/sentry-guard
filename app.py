import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from PIL import Image
import io

# Configuração Master
st.set_page_config(page_title="Sentry Guard Pro", layout="wide")

# Estética Tática e Organização de Abas
st.markdown("""
    <style>
    .stApp { background: #0f172a; color: white; }
    .tactic-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #38bdf8;
        margin-bottom: 15px;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 5px;
        padding: 10px;
        color: white;
    }
    .stTabs [aria-selected="true"] { background-color: #38bdf8 !important; color: #000 !important; }
    </style>
    """, unsafe_allow_html=True)

# Função para Gerar o PDF Completo
def gerar_pdf_operacional(dados, foto_s, foto_m):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(190, 10, "RELATÓRIO OPERACIONAL DE OCORRÊNCIA", 1, 1, 'C')
    pdf.ln(5)

    for secao, info in dados.items():
        pdf.set_font("Arial", 'B', 11)
        pdf.set_fill_color(220, 220, 220)
        pdf.cell(190, 7, secao, 0, 1, 'L', fill=True)
        pdf.set_font("Arial", size=10)
        for k, v in info.items():
            pdf.multi_cell(190, 6, f"{k}: {v}", 0, 'L')
        pdf.ln(3)

    if foto_s:
        pdf.add_page()
        pdf.cell(190, 10, "ANEXO I - FOTO DO SUSPEITO", 0, 1, 'L')
        img_s = Image.open(foto_s).convert("RGB")
        img_s.save("s.jpg")
        pdf.image("s.jpg", x=10, y=30, w=100)

    if foto_m:
        pdf.add_page()
        pdf.cell(190, 10, "ANEXO II - MATERIAL APREENDIDO", 0, 1, 'L')
        img_m = Image.open(foto_m).convert("RGB")
        img_m.save("m.jpg")
        pdf.image("m.jpg", x=10, y=30, w=100)

    return pdf.output()

st.title("🛡️ SENTRY GUARD COMMAND")
st.write(f"📅 {datetime.now().strftime('%d/%m/%Y')} | Unidade Móvel")

# Criação das Abas para Organização
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🚔 Guarnição/Local", "👤 Vítima", "🚨 Suspeito", "📦 Apreensões", "📖 Relato"])

with tab1:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    st.subheader("Dados da Guarnição e Local")
    g1, g2 = st.columns(2)
    guarnicao = g1.text_input("VTR / Prefixo")
    comandante = g2.text_input("Comandante da Guarnição")
    local_fato = st.text_input("Endereço Exato do Fato")
    natureza = st.selectbox("Tipificação Criminal", [
        "BAIXO: Ameaça (Art. 147)", "BAIXO: Lesão Leve", "BAIXO: TCO Outros",
        "MÉDIO: Furto (Art. 155)", "MÉDIO: Dano",
        "ALTO: Roubo (Art. 157)", "ALTO: Tráfico (Lei 11.343)", "ALTO: Homicídio",
        "ESPECIAL: Maria da Penha", "ESPECIAL: Porte de Arma", "ESPECIAL: Ambiental"
    ])
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    st.subheader("Qualificação da Vítima")
    v1, v2 = st.columns(2)
    v_nome = v1.text_input("Nome da Vítima")
    v_doc = v2.text_input("CPF/RG Vítima")
    v_nasc = v1.text_input("Data Nasc. Vítima")
    v_mae = v2.text_input("Nome da Mãe (Vítima)")
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    st.subheader("Qualificação do Suspeito")
    s1, s2 = st.columns(2)
    s_nome = s1.text_input("Nome/Alcunha Suspeito")
    s_doc = s2.text_input("Documento Suspeito")
    f_susp = st.file_uploader("📸 Foto do Suspeito", type=['jpg','png','jpeg'])
    if f_susp: st.image(f_susp, width=200)
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    st.subheader("Materiais e Apreensões")
    mat_desc = st.text_area("Listagem de Materiais")
    f_mat = st.file_uploader("📸 Foto dos Materiais", type=['jpg','png','jpeg'])
    if f_mat: st.image(f_mat, width=200)
    st.markdown('</div>', unsafe_allow_html=True)

with tab5:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    st.subheader("Histórico da Ocorrência")
    relato = st.text_area("Relato detalhado dos fatos", height=200)
    
    if st.button("🏁 FINALIZAR E GERAR PDF COMPLETO", use_container_width=True):
        dados_completos = {
            "1. GUARNIÇÃO E LOCAL": {"VTR": guarnicao, "CMT": comandante, "Local": local_fato, "Natureza": natureza},
            "2. VÍTIMA": {"Nome": v_nome, "Doc": v_doc, "Mãe": v_mae},
            "3. SUSPEITO": {"Nome": s_nome, "Doc": s_doc},
            "4. APREENSÕES": {"Itens": mat_desc},
            "5. RELATO": relato
        }
        pdf_bytes = gerar_pdf_operacional(dados_completos, f_susp, f_mat)
        st.download_button("⬇️ BAIXAR RELATÓRIO OFICIAL", data=pdf_bytes, file_name=f"RELATORIO_{datetime.now().strftime('%d%m%Y')}.pdf")
    st.markdown('</div>', unsafe_allow_html=True)
