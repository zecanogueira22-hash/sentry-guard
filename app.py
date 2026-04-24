import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from PIL import Image
import io

# Configuração Master
st.set_page_config(page_title="Sentry Guard Full", layout="wide")

# --- APLICAÇÃO DA PALETA DE CORES (Luca Davincci) ---
st.markdown(f"""
    <style>
    /* Fundo Principal - 1A334A */
    .stApp {{
        background: #1A334A;
        color: white;
    }}
    
    /* Cards e Seções - 1E536E */
    .tactic-card {{
        background: rgba(30, 83, 110, 0.4);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #18A3B7;
        margin-bottom: 10px;
    }}
    
    /* Títulos e Acentos Neon - 27E6EC */
    .section-title, h1, h2, h3 {{
        color: #27E6EC !important;
        text-shadow: 0 0 5px rgba(39, 230, 236, 0.2);
    }}

    /* Abas Personalizadas */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background-color: #1E536E;
        border-radius: 5px 5px 0px 0px;
        color: #5AA5CD;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: #27E6EC !important;
        color: #1A334A !important;
        font-weight: bold;
    }}

    /* Botões - 18A3B7 */
    .stButton>button {{
        background: #18A3B7;
        color: white;
        border-radius: 8px;
        border: none;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        background: #27E6EC;
        color: #1A334A;
    }}
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
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(190, 7, secao, 0, 1, 'L', fill=True)
        pdf.set_font("Arial", size=9)
        for k, v in info.items():
            if v:
                pdf.multi_cell(190, 6, f"{k}: {v}", 0, 'L')
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

st.markdown("<h1>🛡️ SENTRY GUARD COMMAND</h1>", unsafe_allow_html=True)

# Estrutura de Abas (Mantida conforme solicitado)
t_geral, t_vitimas, t_suspeitos, t_relato, t_fotos = st.tabs([
    "📍 Local/Guarnição", "👤 Vítimas", "🚨 Suspeitos", "📖 Relato/Apreensão", "📄 Finalizar"
])

# ABA 1: LOCAL E GUARNIÇÃO
with t_geral:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    end_fato = st.text_input("Endereço do Fato")
    col_g1, col_g2 = st.columns(2)
    prefixo = col_g1.text_input("Viatura/Prefixo")
    agentes = col_g2.text_area("Guarnição (Nomes/Matrículas)")
    st.markdown('</div>', unsafe_allow_html=True)

# ABA 2: VÍTIMAS (2 Espaços)
with t_vitimas:
    v_dados = {}
    with st.expander("➕ Adicionar/Editar Vítima 01"):
        v1_n = st.text_input("Nome (V1)")
        v1_d = st.text_input("Documento (V1)")
        v1_t = st.text_input("Telefone (V1)")
        v_dados["Vítima 01"] = f"Nome: {v1_n} | Doc: {v1_d} | Tel: {v1_t}" if v1_n else ""
        
    with st.expander("➕ Adicionar/Editar Vítima 02"):
        v2_n = st.text_input("Nome (V2)")
        v2_d = st.text_input("Documento (V2)")
        v2_t = st.text_input("Telefone (V2)")
        v_dados["Vítima 02"] = f"Nome: {v2_n} | Doc: {v2_d} | Tel: {v2_t}" if v2_n else ""

# ABA 3: SUSPEITOS (3 Espaços)
with t_suspeitos:
    s_dados = {}
    for i in range(1, 4):
        with st.expander(f"➕ Adicionar/Editar Suspeito 0{i}"):
            sn = st.text_input(f"Nome/Alcunha (S{i})")
            sd = st.text_input(f"Documento (S{i})")
            sm = st.text_input(f"Nome da Mãe (S{i})")
            s_dados[f"Suspeito 0{i}"] = f"Nome: {sn} | Doc: {sd} | Mãe: {sm}" if sn else ""

# ABA 4: RELATO E APREENSÃO
with t_relato:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    tipo_crime = st.selectbox("Tipificação", [
        "BAIXO POTENCIAL: Ameaça / Desobediência / Lesão Leve",
        "MÉDIO POTENCIAL: Furto / Dano / Estelionato",
        "ALTO POTENCIAL: Roubo / Homicídio / Latrocínio",
        "LEI ESPECIAL: Tráfico de Drogas (Lei 11.343)",
        "LEI ESPECIAL: Maria da Penha (Lei 11.340)",
        "LEI ESPECIAL: Estatuto do Desarmamento"
    ])
    relato = st.text_area("Histórico Detalhado", height=150)
    materiais = st.text_area("Materiais Apreendidos")
    st.markdown('</div>', unsafe_allow_html=True)

# ABA 5: FOTOS E FINALIZAÇÃO
with t_fotos:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    col_f1, col_f2 = st.columns(2)
    f_susp = col_f1.file_uploader("📸 Foto do Suspeito", type=['jpg','png'])
    f_mat = col_f2.file_uploader("📸 Foto Apreensões", type=['jpg','png'])
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🏁 GERAR BOLETIM FINAL", use_container_width=True):
        resumo = {
            "1. EQUIPE E LOCAL": {"Viatura": prefixo, "Agentes": agentes, "Local": end_fato},
            "2. VÍTIMAS": v_dados,
            "3. SUSPEITOS": s_dados,
            "4. OCORRÊNCIA": {"Crime": tipo_crime, "Relato": relato, "Apreensões": materiais}
        }
        pdf = gerar_pdf_completo(resumo, f_susp, f_mat)
        st.download_button("⬇️ BAIXAR PDF COMPLETO", data=pdf, file_name="BO_Sentry_Paleta.pdf")
