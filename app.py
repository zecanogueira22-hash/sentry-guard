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

def gerar_pdf_operacional(titulo_dinamico, equipe, vitimas, suspeitos, ocorrencia, f_susp, f_mat):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Cabeçalho
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 12, titulo_dinamico.upper(), 1, 1, 'C')
    pdf.ln(5)

    # 1. EQUIPE E LOCAL
    pdf.set_font("Arial", 'B', 11)
    pdf.set_fill_color(230, 230, 240)
    pdf.cell(190, 8, "DADOS DA EQUIPE E LOCAL", 0, 1, 'L', fill=True)
    pdf.set_font("Arial", size=10)
    pdf.ln(2)
    for k, v in equipe.items():
        if v:
            txt = f"{k}: {v}".encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(190, 6, txt, 0, 'L')
    pdf.ln(4)

    # 2. VÍTIMAS
    if vitimas:
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(190, 8, "ENVOLVIDOS (VITIMAS)", 0, 1, 'L', fill=True)
        pdf.set_font("Arial", size=10)
        pdf.ln(2)
        for v in vitimas.values():
            txt = v.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(190, 6, txt, 0, 'L')
        pdf.ln(4)

    # 3. SUSPEITOS
    if suspeitos:
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(190, 8, "ENVOLVIDOS (SUSPEITOS)", 0, 1, 'L', fill=True)
        pdf.set_font("Arial", size=10)
        pdf.ln(2)
        for s in suspeitos.values():
            txt = s.encode('latin-1', 'replace').decode('latin-1')
            pdf.multi_cell(190, 6, txt, 0, 'L')
        pdf.ln(4)

    # 4. HISTÓRICO (CORREÇÃO DEFINITIVA)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(190, 8, "HISTORICO DA OCORRENCIA", 0, 1, 'L', fill=True)
    pdf.ln(2)
    
    # Natureza
    pdf.set_font("Arial", 'B', 10)
    pdf.write(6, "Natureza: ")
    pdf.set_font("Arial", size=10)
    pdf.write(6, ocorrencia['natureza'].encode('latin-1', 'replace').decode('latin-1'))
    pdf.ln(8)
    
    # Relato
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(190, 6, "RELATO:", 0, 1, 'L')
    pdf.set_font("Arial", size=10)
    # AQUI ESTÁ A MUDANÇA: Multi_cell de 190 (largura total) para o texto não ser espremido
    relato_formatado = ocorrencia['relato'].encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(190, 6, relato_formatado, 0, 'J') # 'J' para justificado
    
    if ocorrencia['materiais']:
        pdf.ln(6)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(190, 6, "MATERIAIS/APREENSOES:", 0, 1, 'L')
        pdf.set_font("Arial", size=10)
        materiais_formatados = ocorrencia['materiais'].encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(190, 6, materiais_formatados, 0, 'J')

    # Anexos
    for foto, label in [(f_susp, "DO SUSPEITO"), (f_mat, "DO MATERIAL")]:
        if foto:
            try:
                pdf.add_page()
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(190, 10, f"ANEXO - FOTO {label}", 0, 1, 'L')
                img = Image.open(foto).convert("RGB")
                img_io = io.BytesIO()
                img.save(img_io, format='JPEG', quality=70)
                img_io.seek(0)
                pdf.image(img_io, x=10, y=30, w=150)
            except: pass
    
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
            vn = st.text_input(f"Nome V{i}", key=f"vn{i}")
            vd = st.text_input(f"Doc V{i}", key=f"vd{i}")
            if vn: v_dados[f"v{i}"] = f"Vítima 0{i}: {vn} (Doc: {vd})"

with t_suspeitos:
    s_dados = {}
    for i in range(1, 4):
        with st.expander(f"🚨 Suspeito 0{i}"):
            sn = st.text_input(f"Nome S{i}", key=f"sn{i}")
            sd = st.text_input(f"Doc S{i}", key=f"sd{i}")
            sm = st.text_input(f"Mãe S{i}", key=f"sm{i}")
            if sn: s_dados[f"s{i}"] = f"Suspeito 0{i}: {sn} | Mãe: {sm} | Doc: {sd}"

with t_relato:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    crimes_tco = ["Ameaça", "Lesão Corporal Leve", "Desobediência", "Desacato", "Dano", "Vias de Fato"]
    crimes_bo = ["Roubo", "Furto", "Tráfico de Drogas", "Homicídio", "Maria da Penha", "Outros"]
    tipo = st.selectbox("Natureza da Ocorrência", crimes_tco + crimes_bo)
    
    # Variáveis únicas para o relato
    texto_relato = st.text_area("Histórico Detalhado", height=300)
    texto_materiais = st.text_area("Objetos e Apreensões")
    st.markdown('</div>', unsafe_allow_html=True)

with t_final:
    f_susp = st.file_uploader("📸 Foto Suspeito", type=['jpg','png','jpeg'])
    f_mat = st.file_uploader("📸 Foto Material", type=['jpg','png','jpeg'])
    
    if st.button("🏁 FINALIZAR E GERAR DOCUMENTO", use_container_width=True):
        tit = "Termo Circunstanciado de Ocorrencia" if tipo in crimes_tco else "Boletim de Ocorrencia"
        
        d_equipe = {"Viatura": prefixo, "Agentes": agentes, "Local": end_fato}
        d_ocorrencia = {"natureza": tipo, "relato": texto_relato, "materiais": texto_materiais}
        
        try:
            arquivo_final = gerar_pdf_operacional(tit, d_equipe, v_dados, s_dados, d_ocorrencia, f_susp, f_mat)
            st.download_button(label=f"⬇️ BAIXAR {tit.upper()}", data=arquivo_final, file_name="RELATORIO.pdf", mime="application/pdf")
            
            link_wa = f"https://wa.me/?text={urllib.parse.quote(f'🛡️ *{tit.upper()}*\n🚨 *Natureza:* {tipo}\n🚔 *Viatura:* {prefixo}')}"
            st.markdown(f'<a href="{link_wa}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:8px; font-weight:bold; cursor:pointer;">📲 NOTIFICAR WHATSAPP</button></a>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Erro: {e}")
    
