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
    .stButton>button { background: #18A3B7 !important; color: white !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

class PDF_Operacional(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 10)
        self.set_text_color(150, 150, 150)
        if self.page_no() > 1:
            self.cell(0, 10, f'Continuação - Página {self.page_no()}', 0, 1, 'R')

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
                texto = str(item).encode('latin-1', 'replace').decode('latin-1')
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
    pdf.cell(190, 6, f"NATUREZA: {str(d_relato['natureza']).upper()}".encode('latin-1', 'replace').decode('latin-1'), 0, 1, 'L')
    pdf.ln(2)
    
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(190, 6, "RELATO DETALHADO:", 0, 1, 'L')
    pdf.set_font("Arial", size=10)
    rel_texto = str(d_relato['relato']).encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 6, rel_texto, 0, 'L')
    
    if d_relato['materiais']:
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(190, 6, "MATERIAIS E APREENSÕES:", 0, 1, 'L')
        pdf.set_font("Arial", size=10)
        mat_texto = str(d_relato['materiais']).encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 6, mat_texto, 0, 'L')

    # 6. FOTOS
    for foto, label in [(f_susp, "DO SUSPEITO"), (f_mat, "DO MATERIAL")]:
        if foto:
            try:
                pdf.add_page()
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, f"ANEXO FOTOGRÁFICO - {label}", 0, 1, 'C')
                img = Image.open(foto).convert("RGB")
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format='JPEG')
                img_byte_arr.seek(0)
                pdf.image(img_byte_arr, x=15, y=30, w=180)
            except:
                pass

    return pdf.output(dest='S')

# --- INTERFACE ---
st.markdown("<h1>🛡️ B.O. FÁCIL</h1>", unsafe_allow_html=True)

abas = st.tabs(["📍 Local", "👤 Vítimas", "👥 Testemunhas", "🚨 Suspeitos", "📖 Relato", "🏁 Finalizar"])

with abas:
    vtr = st.text_input("Viatura", key="vtr_final")
    loc = st.text_input("Local da Ocorrência", key="loc_final")
    guarnicao = st.text_area("Guarnição", key="gua_final")

[span_0](start_span)[span_1](start_span)with abas[1]:
    v_lista = []
    for i in range(1, 3):
        vn = st.text_input(f"Nome Vítima {i}", key=f"vnome_f_{i}")
        vd = st.text_input(f"Doc Vítima {i}", key=f"vdoc_f_{i}")
        if vn: v_lista.append(f"Vítima {i}: {vn} (Doc: {vd})")

[cite_start]with abas[2]: # TESTEMUNHAS
    t_lista = []
    for i in range(1, 3):
        tn = st.text_input(f"Nome Testemunha {i}", key=f"tnome_f_{i}")
        td = st.text_input(f"Doc Testemunha {i}", key=f"tdoc_f_{i}")
        if tn: t_lista.append(f"Testemunha {i}: {tn} (Doc: {td})")

[cite_start]with abas[3]:
    s_lista = []
    for i in range(1, 4):
        with st.expander(f"Suspeito {i}"):
            sn = st.text_input(f"Nome S{i}", key=f"snome_f_{i}")
            sm = st.text_input(f"Mãe S{i}", key=f"smae_f_{i}")
            sd = st.text_input(f"Doc S{i}", key=f"sdoc_f_{i}")
            if sn: s_lista.append(f"Suspeito {i}: {sn} | Mãe: {sm} | Doc: {sd}")

[cite_start]with abas[4]:
    crimes_tco = ["Ameaça", "Lesão Corporal", "Desacato", "Vias de Fato", "Dano"]
    nat = st.selectbox("Natureza", crimes_tco + ["Roubo", "Tráfico", "Outros"], key="nat_f_select")
    rel = st.text_area("Relato da Ocorrência", height=300, key="rel_f_input")
    mat = st.text_area("Materiais Apreendidos", key="mat_f_input")

[cite_start]with abas[5]:
    f_s = st.file_uploader("Foto Suspeito", type=['jpg','jpeg','png'], key="fs_f_upload")
    f_m = st.file_uploader("Foto Material", type=['jpg','jpeg','png'], key="fm_f_upload")
    
    if st.button("GERAR PDF E FINALIZAR", key="btn_f_gerar"):
        titulo = "Termo Circunstanciado de Ocorrencia" if nat in crimes_tco else "Boletim de Ocorrencia"
        
        try:
            pdf_output = gerar_pdf_final(
                titulo,
                {"Viatura": vtr, "Local": loc, "Agentes": guarnicao},
                v_lista, t_lista, s_lista,
                {"natureza": nat, "relato": rel, "materiais": mat},
                f_s, f_m
            )
            
            # Converte para bytes se necessário para evitar erro de 'bytearray'
            pdf_bytes = bytes(pdf_output) if isinstance(pdf_output, (bytearray, list)) else pdf_output
            
            st.download_button(
                label="⬇️ BAIXAR RELATÓRIO PDF",
                data=pdf_bytes,
                file_name="Relatorio_Final.pdf",
                mime="application/pdf",
                key="btn_f_download"
            )
        except Exception as e:
            st.error(f"Erro ao gerar: {str(e)}")
    
