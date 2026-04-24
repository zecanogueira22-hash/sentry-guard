import streamlit as st
from fpdf import FPDF
from PIL import Image
import io
import urllib.parse

# 1. CONFIGURAÇÃO (ÍCONE DO GOLLUM CORRIGIDO)
try:
    img_icone = Image.open("20251007185025621.webp")
except:
    img_icone = "🛡️"

st.set_page_config(page_title="B.O. FÁCIL", page_icon=img_icone, layout="wide")

# --- ESTÉTICA TÁTICA ---
st.markdown("""
    <style>
    .stApp { background: #1A334A; color: white; }
    .tactic-card {
        background: rgba(30, 83, 110, 0.4);
        padding: 15px; border-radius: 10px; border: 1px solid #18A3B7; margin-bottom: 10px;
    }
    .stTabs [aria-selected="true"] { background-color: #27E6EC !important; color: #1A334A !important; font-weight: bold; }
    .stButton>button { background: #18A3B7; color: white; border-radius: 8px; width: 100%; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

def gerar_pdf_final(dados, f_susp, f_mat):
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
        for k, v in info.items():
            if v:
                # encode/decode para evitar erro de acento sem travar o app
                txt = f"{k}: {v}".encode('latin-1', 'replace').decode('latin-1')
                pdf.multi_cell(190, 6, txt, 0, 'L')
        pdf.ln(2)

    # Fotos
    for foto, label in [(f_susp, "SUSPEITO"), (f_mat, "MATERIAL")]:
        if foto:
            try:
                pdf.add_page()
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(190, 10, f"ANEXO - FOTO {label}", 0, 1, 'L')
                img = Image.open(foto).convert("RGB")
                img_path = f"temp_{label.lower()}.jpg"
                img.save(img_path)
                pdf.image(img_path, x=10, y=30, w=100)
            except: pass
    
    # O SEGREDO DO ERRO: Retornar como bytes de forma limpa
    return pdf.output(dest='S').encode('latin-1', errors='ignore')

st.markdown("<h1>🛡️ B.O. FÁCIL</h1>", unsafe_allow_html=True)

t_local, t_vitimas, t_suspeitos, t_relato, t_final = st.tabs([
    "📍 Local", "👤 Vítimas", "🚨 Suspeitos", "📖 Relato", "📄 Finalizar"
])

with t_local:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    end_fato = st.text_input("Endereço do Fato")
    prefixo = st.text_input("Viatura/Prefixo")
    agentes = st.text_area("Guarnição (Nomes/Matrículas)")
    st.markdown('</div>', unsafe_allow_html=True)

with t_vitimas:
    v_dados = {}
    for i in range(1, 3):
        with st.expander(f"👤 Vítima 0{i}"):
            vn = st.text_input(f"Nome (V{i})")
            vd = st.text_input(f"Documento (V{i})")
            v_dados[f"Vítima 0{i}"] = f"Nome: {vn} | Doc: {vd}" if vn else ""

with t_suspeitos:
    s_dados = {}
    for i in range(1, 4):
        with st.expander(f"🚨 Suspeito 0{i}"):
            sn = st.text_input(f"Nome/Alcunha (S{i})")
            sd = st.text_input(f"Documento (S{i})")
            sm = st.text_input(f"Nome da Mãe (S{i})")
            s_dados[f"Suspeito 0{i}"] = f"Nome: {sn} | Doc: {sd} | Mãe: {sm}" if sn else ""

with t_relato:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    tipo = st.selectbox("Natureza", ["Ameaça", "Roubo", "Furto", "Tráfico", "Maria da Penha", "Outros"])
    relato = st.text_area("Histórico", height=150)
    materiais = st.text_area("Materiais Apreendidos")
    st.markdown('</div>', unsafe_allow_html=True)

with t_final:
    f_susp = st.file_uploader("📸 Foto Suspeito", type=['jpg','png','jpeg'])
    f_mat = st.file_uploader("📸 Foto Material", type=['jpg','png','jpeg'])
    
    if st.button("🏁 GERAR PDF E FINALIZAR"):
        resumo = {
            "LOCAL E EQUIPE": {"Viatura": prefixo, "Agentes": agentes, "Endereço": end_fato},
            "VÍTIMAS": v_dados,
            "SUSPEITOS": s_dados,
            "OCORRÊNCIA": {"Natureza": tipo, "Relato": relato, "Materiais": materiais}
        }
        try:
            pdf_out = gerar_pdf_final(resumo, f_susp, f_mat)
            st.download_button("⬇️ BAIXAR PDF", data=pdf_out, file_name="BO_FACIL.pdf", mime="application/pdf")
            
            # WhatsApp
            link_wa = f"https://wa.me/?text={urllib.parse.quote(f'🛡️ *B.O. FÁCIL*\n🚨 *Natureza:* {tipo}\n🚔 *Viatura:* {prefixo}')}"
            st.markdown(f'<a href="{link_wa}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:8px; font-weight:bold; cursor:pointer;">📲 ENVIAR WHATSAPP</button></a>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Erro: {e}")
            
