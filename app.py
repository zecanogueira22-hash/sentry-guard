import streamlit as st
from fpdf import FPDF
from PIL import Image
import io
import urllib.parse

# 1. CONFIGURAÇÃO DO APP
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
    .stButton>button { background: #18A3B7; color: white; border-radius: 8px; width: 100%; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

class PDF_Operacional(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 10)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, 'DOCUMENTO GERADO VIA B.O. FÁCIL', 0, 1, 'R')

def gerar_pdf_final(titulo_doc, d_equipe, d_vitimas, d_testemunhas, d_suspeitos, d_relato, f_susp, f_mat):
    pdf = PDF_Operacional()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    
    # Título Principal
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 12, titulo_doc.upper(), 1, 1, 'C')
    pdf.ln(5)

    def criar_secao_vertical(titulo, lista_conteudo):
        if lista_conteudo:
            pdf.set_font("Arial", 'B', 11)
            pdf.set_fill_color(230, 230, 240)
            pdf.cell(190, 8, titulo, 0, 1, 'L', fill=True)
            pdf.set_font("Arial", size=10)
            pdf.ln(2)
            for item in lista_conteudo:
                texto = item.encode('latin-1', 'replace').decode('latin-1')
                pdf.multi_cell(0, 6, texto, 0, 'L')
            pdf.ln(4)

    # 1. Equipe
    lista_eq = [f"{k}: {v}" for k, v in d_equipe.items() if v]
    criar_secao_vertical("DADOS DA EQUIPE E LOCAL", lista_eq)
    
    # 2. Vítimas
    criar_secao_vertical("ENVOLVIDOS (VÍTIMAS)", d_vitimas)

    # 3. Testemunhas
    criar_secao_vertical("TESTEMUNHAS", d_testemunhas)
        
    # 4. Suspeitos
    criar_secao_vertical("ENVOLVIDOS (SUSPEITOS)", d_suspeitos)

    # 5. HISTÓRICO
    pdf.set_font("Arial", 'B', 11)
    pdf.set_fill_color(230, 230, 240)
    pdf.cell(190, 8, "HISTÓRICO DA OCORRÊNCIA", 0, 1, 'L', fill=True)
    pdf.ln(2)
    
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(190, 6, f"NATUREZA: {d_relato['natureza']}".upper(), 0, 1, 'L')
    pdf.ln(2)
    
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(190, 6, "RELATO DETALHADO:", 0, 1, 'L')
    pdf.set_font("Arial", size=10)
    # multi_cell(0) garante que o relato use a largura toda e pule de página
    pdf.multi_cell(0, 6, d_relato['relato'].encode('latin-1', 'replace').decode('latin-1'), 0, 'L')
    
    if d_relato['materiais']:
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(190, 6, "MATERIAIS E APREENSÕES:", 0, 1, 'L')
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 6, d_relato['materiais'].encode('latin-1', 'replace').decode('latin-1'), 0, 'L')

    # 6. FOTOS (Em páginas novas)
    for foto, label in [(f_susp, "DO SUSPEITO"), (f_mat, "DO MATERIAL")]:
        if foto:
            pdf.add_page()
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, f"ANEXO FOTOGRÁFICO - {label}", 0, 1, 'C')
            img = Image.open(foto).convert("RGB")
            # Ajuste de tamanho da foto para caber na vertical
            pdf.image(img, x=15, y=30, w=180)

    return bytes(pdf.output(dest='S'))

# --- INTERFACE STREAMLIT ---
st.markdown("<h1>🛡️ B.O. FÁCIL</h1>", unsafe_allow_html=True)

abas = st.tabs(["📍 Local", "👤 Vítimas", "👥 Testemunhas", "🚨 Suspeitos", "📖 Relato", "🏁 Finalizar"])

with abas:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    vtr = st.text_input("Viatura/Prefixo")
    loc = st.text_input("Local da Ocorrência (Endereço)")
    guarnicao = st.text_area("Guarnição (Nomes e Matrículas)")
    st.markdown('</div>', unsafe_allow_html=True)

with abas:
    v_lista = []
    for i in range(1, 3):
        with st.expander(f"Vítima {i}"):
            n = st.text_input(f"Nome Vítima {i}", key=f"v_nome_{i}")
            d = st.text_input(f"Doc Vítima {i}", key=f"v_doc_{i}")
            if n: v_lista.append(f"Vítima {i}: {n} - Doc: {d}")

with abas: # ABA TESTEMUNHAS SOLICITADA
    t_lista = []
    for i in range(1, 3):
        with st.expander(f"Testemunha {i}"):
            tn = st.text_input(f"Nome Testemunha {i}", key=f"t_nome_{i}")
            td = st.text_input(f"Doc Testemunha {i}", key=f"t_doc_{i}")
            if tn: t_lista.append(f"Testemunha {i}: {tn} - Doc: {td}")

with abas:
    s_lista = []
    for i in range(1, 4):
        with st.expander(f"Suspeito {i}"):
            sn = st.text_input(f"Nome S{i}", key=f"s_nome_{i}")
            sm = st.text_input(f"Nome da Mãe S{i}", key=f"s_mae_{i}")
            sd = st.text_input(f"Doc S{i}", key=f"s_doc_{i}")
            if sn: s_lista.append(f"Suspeito {i}: {sn} | Mãe: {sm} | Doc: {sd}")

with abas:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    crimes_tco = ["Ameaça", "Lesão Corporal", "Desacato", "Vias de Fato", "Dano"]
    nat = st.selectbox("Natureza", crimes_tco + ["Roubo", "Tráfico", "Furto", "Homicídio", "Outros"])
    rel = st.text_area("Relato da Ocorrência (Sem limite de texto)", height=300)
    mat = st.text_area("Materiais Apreendidos")
    st.markdown('</div>', unsafe_allow_html=True)

with abas:
    f_s = st.file_uploader("📸 Foto Suspeito", type=['jpg','jpeg','png'])
    f_m = st.file_uploader("📸 Foto Material", type=['jpg','jpeg','png'])
    
    if st.button("🏁 GERAR RELATÓRIO FINAL", use_container_width=True):
        # Lógica de Título Dinâmico
        titulo = "Termo Circunstanciado de Ocorrencia" if nat in crimes_tco else "Boletim de Ocorrencia"
        
        try:
            pdf_bytes = gerar_pdf_final(
                titulo,
                {"Viatura": vtr, "Local": loc, "Agentes": guarnicao},
                v_lista, t_lista, s_lista,
                {"natureza": nat, "relato": rel, "materiais": mat},
                f_s, f_m
            )
            
            st.download_button(
                label=f"⬇️ BAIXAR {titulo.upper()}",
                data=pdf_bytes,
                file_name=f"Relatorio_{nat}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            
            # WhatsApp
            msg_wa = f"🛡️ *{titulo.upper()}*\n🚨 *Natureza:* {nat}\n🚔 *Viatura:* {vtr}"
            st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(msg_wa)}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:8px; font-weight:bold; cursor:pointer;">📲 NOTIFICAR VIA WHATSAPP</button></a>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Erro ao gerar documento: {e}")
        
