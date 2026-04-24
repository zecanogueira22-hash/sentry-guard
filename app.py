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
    pdf.multi_cell(0, 6, d_relato['relato'].encode('latin-1', 'replace').decode('
    
