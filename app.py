import streamlit as st
from fpdf import FPDF
from PIL import Image
import io
import urllib.parse

# 1. CONFIGURAÇÃO DE NOME E ÍCONE (GOLLUM)
try:
    img_icone = Image.open("20251007185025621.webp")
except:
    img_icone = "🛡️"

st.set_page_config(page_title="B.O. FÁCIL", page_icon=img_icone, layout="wide")

# --- ESTÉTICA TÁTICA AZUL ---
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

def gerar_pdf_blindado(dados, f_susp, f_mat):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "B.O. FACIL - RELATORIO OPERACIONAL", 1, 1, 'C')
    pdf.ln(5)

    for secao, info in dados.items():
        pdf.set_font("Arial", 'B', 11)
        pdf.set_fill_color(230, 230, 240)
        pdf.cell(190, 7, secao, 0, 1, 'L', fill=True)
        pdf.set_font("Arial", size=9)
        for k, v in info.items():
            if v:
                # Tratamento de texto para evitar erro de acento ou caractere especial
                txt = f"{k}: {v}".encode('latin-1', 'replace').decode('latin-1')
                pdf.multi_cell(190, 6, txt, 0, 'L')
        pdf.ln(2)

    # Inclusão de Fotos
    for foto, label in [(f_susp, "SUSPEITO"), (f_mat, "MATERIAL")]:
        if foto:
            try:
                pdf.add_page()
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(190, 10, f"ANEXO - FOTO {label}", 0, 1, 'L')
                img = Image.open(foto).convert("RGB")
                img_temp = io.BytesIO()
                img.save(img_temp, format="JPEG")
                img_temp.seek(0)
                pdf.image(img_temp, x=10, y=30, w=100)
            except: pass
    
    # SAÍDA BLINDADA: Detecta automaticamente se precisa converter ou não
    saida_bruta = pdf.output(dest='S')
    if isinstance(saida_bruta, str):
        return saida_bruta.encode('latin-1', 'replace')
    return bytes(saida_bruta)

st.markdown("<h1>🛡️ B.O. FÁCIL</h1>", unsafe_allow_html=True)

t_local, t_vitimas, t_suspeitos, t_relato, t_final = st.tabs([
    "📍 Local", "👤 Vítimas", "🚨 Suspeitos", "📖 Relato", "📄 Finalizar"
])

with t_local:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    end_fato = st.text_input("Endereço Completo do Fato")
    prefixo = st.text_input("Viatura/Prefixo")
    agentes = st.text_area("Guarnição (Nomes e Matrículas)")
    st.markdown('</div>', unsafe_allow_html=True)

with t_vitimas:
    v_dados = {}
    for i in range(1, 3):
        with st.expander(f"👤 Vítima 0{i}"):
            vn = st.text_input(f"Nome Completo (V{i})")
            vd = st.text_input(f"Documento/RG (V{i})")
            v_dados[f"Vítima 0{i}"] = f"Nome: {vn} | Doc: {vd}" if vn else ""

with t_suspeitos:
    s_dados = {}
    for i in range(1, 4):
        with st.expander(f"🚨 Suspeito 0{i}"):
            sn = st.text_input(f"Nome ou Alcunha (S{i})")
            sd = st.text_input(f"Documento (S{i})")
            sm = st.text_input(f"Nome da Mãe (S{i})")
            s_dados[f"Suspeito 0{i}"] = f"Nome: {sn} | Doc: {sd} | Mãe: {sm}" if sn else ""

with t_relato:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    tipo = st.selectbox("Natureza da Ocorrência", ["Ameaça", "Roubo", "Furto", "Tráfico", "Maria da Penha", "Lesão Corporal", "Outros"])
    relato = st.text_area("Histórico Detalhado", height=150)
    materiais = st.text_area("Materiais Apreendidos (Descritivo)")
    st.markdown('</div>', unsafe_allow_html=True)

with t_final:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    f_susp = st.file_uploader("📸 Foto do Suspeito", type=['jpg','png','jpeg'])
    f_mat = st.file_uploader("📸 Foto do Material", type=['jpg','png','jpeg'])
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🏁 GERAR PDF E FINALIZAR", use_container_width=True):
        resumo = {
            "DADOS DA EQUIPE": {"Viatura": prefixo, "Agentes": agentes, "Local": end_fato},
            "DADOS DAS VITIMAS": v_dados,
            "DADOS DOS SUSPEITOS": s_dados,
            "HISTORICO": {"Natureza": tipo, "Relato": relato, "Materiais": materiais}
        }
        try:
            pdf_bytes = gerar_pdf_blindado(resumo, f_susp, f_mat)
            
            st.download_button(
                label="⬇️ 1. BAIXAR RELATÓRIO PDF",
                data=pdf_bytes,
                file_name="BO_FACIL.pdf",
                mime="application/pdf"
            )
            
            # Link para WhatsApp
            msg_wa = f"🛡️ *B.O. FÁCIL*\n🚨 *Natureza:* {tipo}\n🚔 *Viatura:* {prefixo}\n📍 *Local:* {end_fato}"
            url_wa = f"https://wa.me/?text={urllib.parse.quote(msg_wa)}"
            st.markdown(f'<a href="{url_wa}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:8px; font-weight:bold; cursor:pointer;">📲 2. NOTIFICAR VIA WHATSAPP</button></a>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Erro no processamento: {e}")
    
