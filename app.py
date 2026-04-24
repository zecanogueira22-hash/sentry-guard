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
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    
    # Cabeçalho Centralizado
    pdf.cell(190, 10, titulo_dinamico.upper(), 1, 1, 'C')
    pdf.ln(5)

    for secao, info in dados.items():
        # Título da Seção (Faixa Cinza)
        pdf.set_font("Arial", 'B', 11)
        pdf.set_fill_color(230, 230, 240)
        pdf.cell(190, 7, secao, 0, 1, 'L', fill=True)
        pdf.set_font("Arial", size=10)
        pdf.ln(1)
        
        # Conteúdo da Seção
        for k, v in info.items():
            if v:
                # Tratamento para não bugar com acentos
                linha = f"{k}: {v}".encode('latin-1', 'replace').decode('latin-1')
                # multi_cell é vital para o HISTÓRICO não sumir
                pdf.multi_cell(190, 6, linha, 0, 'L')
        pdf.ln(3)

    # Anexos (Fotos)
    for foto, label in [(f_susp, "DO SUSPEITO"), (f_mat, "DO MATERIAL")]:
        if foto:
            try:
                pdf.add_page()
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(190, 10, f"ANEXO - FOTO {label}", 0, 1, 'L')
                img = Image.open(foto).convert("RGB")
                img_io = io.BytesIO()
                img.save(img_io, format='JPEG', quality=80)
                img_io.seek(0)
                pdf.image(img_io, x=10, y=30, w=120)
            except: pass
    
    # Conversão de segurança para download
    saida = pdf.output(dest='S')
    return bytes(saida) if not isinstance(saida, str) else saida.encode('latin-1', 'replace')

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
            vn = st.text_input(f"Nome V{i}")
            vd = st.text_input(f"Documento V{i}")
            if vn: v_dados[f"Vítima 0{i}"] = f"{vn} (Doc: {vd})"

with t_suspeitos:
    s_dados = {}
    for i in range(1, 4):
        with st.expander(f"🚨 Suspeito 0{i}"):
            sn = st.text_input(f"Nome S{i}")
            sd = st.text_input(f"Documento S{i}")
            sm = st.text_input(f"Nome da Mãe S{i}") # MANTIDO
            if sn: s_dados[f"Suspeito 0{i}"] = f"Nome: {sn} | Mãe: {sm} | Doc: {sd}"

with t_relato:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    crimes_tco = ["Ameaça", "Lesão Corporal Leve", "Desobediência", "Desacato", "Dano", "Vias de Fato"]
    crimes_bo = ["Roubo", "Furto", "Tráfico de Drogas", "Homicídio", "Maria da Penha", "Porte de Arma", "Outros"]
    
    tipo = st.selectbox("Natureza da Ocorrência", crimes_tco + crimes_bo)
    # AQUI ESTÁ O QUE VAI APARECER NO PDF
    relato_digitado = st.text_area("Histórico Detalhado", placeholder="Descreva a ocorrência aqui...", height=200)
    materiais_digitados = st.text_area("Objetos e Apreensões", placeholder="Descreva o que foi apreendido...")
    st.markdown('</div>', unsafe_allow_html=True)

with t_final:
    f_susp = st.file_uploader("📸 Foto Suspeito", type=['jpg','png','jpeg'])
    f_mat = st.file_uploader("📸 Foto Material", type=['jpg','png','jpeg'])
    
    if st.button("🏁 FINALIZAR E GERAR DOCUMENTO", use_container_width=True):
        # Lógica de Título
        tit = "Termo Circunstanciado de Ocorrencia" if tipo in crimes_tco else "Boletim de Ocorrencia"
        
        info_pdf = {
            "EQUIPE E LOCAL": {"Viatura": prefixo, "Agentes": agentes, "Endereço": end_fato},
            "ENVOLVIDOS (VITIMAS)": v_dados,
            "ENVOLVIDOS (SUSPEITOS)": s_dados,
            "HISTORICO DA OCORRENCIA": {"Natureza": tipo, "Relato": relato_digitado, "Apreensoes": materiais_digitados}
        }
        
        try:
            arquivo_final = gerar_pdf_operacional(tit, info_pdf, f_susp, f_mat)
            
            st.download_button(
                label=f"⬇️ BAIXAR {tit.upper()}",
                data=arquivo_final,
                file_name=f"{tit.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )
            
            # WhatsApp
            link_wa = f"https://wa.me/?text={urllib.parse.quote(f'🛡️ *{tit.upper()}*\n🚨 *Natureza:* {tipo}\n🚔 *Viatura:* {prefixo}')}"
            st.markdown(f'<a href="{link_wa}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:8px; font-weight:bold; cursor:pointer;">📲 NOTIFICAR VIA WHATSAPP</button></a>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Erro ao processar PDF: {e}")
        
