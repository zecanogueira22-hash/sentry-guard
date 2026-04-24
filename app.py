import streamlit as st
from fpdf import FPDF
from PIL import Image
import io
import urllib.parse

# 1. CONFIGURAÇÃO DE NOME E ÍCONE
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

def gerar_pdf_operacional(titulo_dinamico, dados, f_susp, f_mat):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    
    # Título que muda conforme a natureza escolhida
    pdf.cell(190, 10, titulo_dinamico, 1, 1, 'C')
    pdf.ln(5)

    for secao, info in dados.items():
        pdf.set_font("Arial", 'B', 11)
        pdf.set_fill_color(230, 230, 240)
        pdf.cell(190, 7, secao, 0, 1, 'L', fill=True)
        pdf.set_font("Arial", size=9)
        
        for k, v in info.items():
            if v:
                txt = f"{k}: {v}".encode('latin-1', 'replace').decode('latin-1')
                pdf.multi_cell(190, 6, txt, 0, 'L')
        pdf.ln(2)

    # Fotos (Anexos)
    for foto, label in [(f_susp, "SUSPEITO"), (f_mat, "MATERIAL")]:
        if foto:
            try:
                pdf.add_page()
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(190, 10, f"ANEXO - FOTO {label}", 0, 1, 'L')
                img = Image.open(foto).convert("RGB")
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='JPEG')
                img_byte_arr.seek(0)
                pdf.image(img_byte_arr, x=10, y=30, w=100)
            except: pass
    
    return pdf.output(dest='S')

st.markdown("<h1>🛡️ B.O. FÁCIL</h1>", unsafe_allow_html=True)

t_local, t_vitimas, t_suspeitos, t_relato, t_final = st.tabs([
    "📍 Local", "👤 Vítimas", "🚨 Suspeitos", "📖 Relato", "📄 Finalizar"
])

with t_local:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    end_fato = st.text_input("Endereço Completo")
    prefixo = st.text_input("Viatura")
    agentes = st.text_area("Guarnição")
    st.markdown('</div>', unsafe_allow_html=True)

with t_vitimas:
    v_dados = {}
    for i in range(1, 3):
        with st.expander(f"👤 Vítima 0{i}"):
            vn = st.text_input(f"Nome (V{i})")
            vd = st.text_input(f"Doc (V{i})")
            v_dados[f"Vítima 0{i}"] = f"Nome: {vn} | Doc: {vd}" if vn else ""

with t_suspeitos:
    s_dados = {}
    for i in range(1, 4):
        with st.expander(f"🚨 Suspeito 0{i}"):
            sn = st.text_input(f"Nome (S{i})")
            sd = st.text_input(f"Doc (S{i})")
            sm = st.text_input(f"Mãe (S{i})")
            s_dados[f"Suspeito 0{i}"] = f"Nome: {sn} | Doc: {sd} | Mãe: {sm}" if sn else ""

with t_relato:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    
    # Separação clara para o sistema identificar TCO ou BO
    crimes_tco = ["Ameaca (Art. 147)", "Lesao Corporal Leve", "Desobediencia", "Desacato", "Posse de Entorpecentes (Uso)"]
    crimes_bo = ["Roubo (Art. 157)", "Furto", "Trafico de Drogas", "Maria da Penha", "Homicidio", "Porte Ilegal de Arma", "Outros"]
    
    tipo = st.selectbox("Natureza da Ocorrência", crimes_tco + crimes_bo)
    
    relato_texto = st.text_area("Histórico Detalhado da Ocorrência", height=150)
    materiais_texto = st.text_area("Apreensões e Objetos")
    st.markdown('</div>', unsafe_allow_html=True)

with t_final:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    f_susp = st.file_uploader("📸 Foto Suspeito", type=['jpg','png','jpeg'])
    f_mat = st.file_uploader("📸 Foto Material", type=['jpg','png','jpeg'])
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🏁 GERAR DOCUMENTO E FINALIZAR", use_container_width=True):
        # Lógica do Título Dinâmico
        if tipo in crimes_tco:
            titulo_doc = "Termo Circunstanciado de Ocorrencia"
            nome_arquivo = "TCO_OPERACIONAL.pdf"
        else:
            titulo_doc = "Boletim de Ocorrencia"
            nome_arquivo = "BO_OPERACIONAL.pdf"

        resumo = {
            "DADOS DA EQUIPE": {"Viatura": prefixo, "Agentes": agentes, "Local": end_fato},
            "VITIMAS": v_dados,
            "SUSPEITOS": s_dados,
            "HISTORICO DA OCORRENCIA": {"Natureza": tipo, "Relato": relato_texto, "Materiais": materiais_texto}
        }
        
        try:
            pdf_result = gerar_pdf_operacional(titulo_doc, resumo, f_susp, f_mat)
            
            st.download_button(
                label=f"⬇️ BAIXAR {titulo_doc.upper()}",
                data=pdf_result,
                file_name=nome_arquivo,
                mime="application/pdf"
            )
            
            # WhatsApp
            link_wa = f"https://wa.me/?text={urllib.parse.quote(f'🛡️ *{titulo_doc.upper()}*\n🚨 *Natureza:* {tipo}\n🚔 *Viatura:* {prefixo}')}"
            st.markdown(f'<a href="{link_wa}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:8px; font-weight:bold; cursor:pointer;">📲 NOTIFICAR WHATSAPP</button></a>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Erro ao gerar: {e}")
        
