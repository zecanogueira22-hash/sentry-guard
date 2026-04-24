import streamlit as st
from fpdf import FPDF
from PIL import Image
import io
import urllib.parse

# 1. CONFIGURAÇÃO INICIAL
try:
    img_icone = Image.open("20251007185025621.webp")
except:
    img_icone = "🛡️"

st.set_page_config(page_title="B.O. FÁCIL", page_icon=img_icone, layout="wide")

# ESTÉTICA TÁTICA
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
    
    # Título Dinâmico (B.O. ou T.C.O.)
    pdf.cell(190, 10, titulo_dinamico.upper(), 1, 1, 'C')
    pdf.ln(5)

    for secao, info in dados.items():
        pdf.set_font("Arial", 'B', 11)
        pdf.set_fill_color(230, 230, 240)
        pdf.cell(190, 7, secao, 0, 1, 'L', fill=True)
        pdf.set_font("Arial", size=9)
        
        for k, v in info.items():
            if v:
                # encode/decode para evitar erro de acento e multi_cell para o relato longo
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
    
    # CONVERSÃO COMPATÍVEL: Transforma qualquer saída em Bytes puros
    saida = pdf.output(dest='S')
    if isinstance(saida, str):
        return saida.encode('latin-1', 'replace')
    return bytes(saida)

st.markdown("<h1>🛡️ B.O. FÁCIL</h1>", unsafe_allow_html=True)

t_local, t_vitimas, t_suspeitos, t_relato, t_final = st.tabs([
    "📍 Local", "👤 Vítimas", "🚨 Suspeitos", "📖 Relato", "📄 Finalizar"
])

with t_local:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    end_fato = st.text_input("Endereço Completo")
    prefixo = st.text_input("Viatura")
    agentes = st.text_area("Guarnição (Nomes e Matrículas)")
    st.markdown('</div>', unsafe_allow_html=True)

with t_vitimas:
    v_dados = {}
    for i in range(1, 3):
        with st.expander(f"👤 Vítima 0{i}"):
            vn = st.text_input(f"Nome V{i}")
            vd = st.text_input(f"Doc V{i}")
            v_dados[f"Vítima 0{i}"] = f"Nome: {vn} | Doc: {vd}" if vn else ""

with t_suspeitos:
    s_dados = {}
    for i in range(1, 4):
        with st.expander(f"🚨 Suspeito 0{i}"):
            sn = st.text_input(f"Nome S{i}")
            sd = st.text_input(f"Doc S{i}")
            sm = st.text_input(f"Mãe S{i}") # CAMPO DA MÃE MANTIDO
            s_dados[f"Suspeito 0{i}"] = f"Nome: {sn} | Doc: {sd} | Mãe: {sm}" if sn else ""

with t_relato:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    crimes_tco = ["Ameaça", "Lesão Corporal Leve", "Desobediência", "Desacato", "Dano", "Vias de Fato"]
    crimes_bo = ["Roubo", "Furto", "Tráfico de Drogas", "Homicídio", "Maria da Penha", "Outros"]
    
    tipo = st.selectbox("Natureza da Ocorrência", crimes_tco + crimes_bo)
    relato_texto = st.text_area("Histórico Detalhado", height=150)
    materiais_texto = st.text_area("Objetos e Apreensões")
    st.markdown('</div>', unsafe_allow_html=True)

with t_final:
    f_susp = st.file_uploader("📸 Foto Suspeito", type=['jpg','png','jpeg'])
    f_mat = st.file_uploader("📸 Foto Material", type=['jpg','png','jpeg'])
    
    if st.button("🏁 GERAR DOCUMENTO E FINALIZAR", use_container_width=True):
        # Título Condicional
        titulo_doc = "Termo Circunstanciado de Ocorrencia" if tipo in crimes_tco else "Boletim de Ocorrencia"
        
        resumo = {
            "DADOS DA EQUIPE": {"Viatura": prefixo, "Agentes": agentes, "Local": end_fato},
            "DADOS DAS VITIMAS": v_dados,
            "DADOS DOS SUSPEITOS": s_dados,
            "HISTORICO E RELATO": {"Natureza": tipo, "Relato": relato_texto, "Materiais": materiais_texto}
        }
        
        try:
            pdf_bytes = gerar_pdf_operacional(titulo_doc, resumo, f_susp, f_mat)
            
            # Força o Streamlit a ler como binário puro
            st.download_button(
                label=f"⬇️ BAIXAR {titulo_doc.upper()}",
                data=pdf_bytes,
                file_name="RELATORIO.pdf",
                mime="application/pdf"
            )
            
            msg_wa = f"🛡️ *{titulo_doc.upper()}*\n🚨 *Natureza:* {tipo}\n🚔 *Viatura:* {prefixo}"
            url_wa = f"https://wa.me/?text={urllib.parse.quote(msg_wa)}"
            st.markdown(f'<a href="{url_wa}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:8px; font-weight:bold; cursor:pointer;">📲 NOTIFICAR WHATSAPP</button></a>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Erro Crítico: {e}")
