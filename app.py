import streamlit as st
from fpdf import FPDF
from PIL import Image
import io

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
    
    # [span_0](start_span)[span_1](start_span)Título Principal[span_0](end_span)[span_1](end_span)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 12, str(titulo_doc).upper().encode('latin-1', 'replace').decode('latin-1'), 1, 1, 'C')
    pdf.ln(5)

    def criar_secao_vertical(titulo, lista_conteudo):
        if lista_conteudo:
            pdf.set_font("Arial", 'B', 11)
            pdf.set_fill_color(230, 230, 240)
            pdf.cell(190, 8, titulo.encode('latin-1', 'replace').decode('latin-1'), 0, 1, 'L', fill=True)
            pdf.set_font("Arial", size=10)
            pdf.ln(2)
            for item in lista_conteudo:
                texto = str(item).encode('latin-1', 'replace').decode('latin-1')
                pdf.multi_cell(0, 6, texto, 0, 'L')
            pdf.ln(4)

    # 1. [span_2](start_span)Equipe e Local[span_2](end_span)
    lista_eq = [f"{k}: {v}" for k, v in d_equipe.items() if v]
    criar_secao_vertical("DADOS DA EQUIPE E LOCAL", lista_eq)
    
    # 2. [span_3](start_span)Vítimas[span_3](end_span)
    criar_secao_vertical("ENVOLVIDOS (VÍTIMAS)", d_vitimas)

    # 3. Testemunhas (Solicitado)
    criar_secao_vertical("TESTEMUNHAS", d_testemunhas)
        
    # 4. [span_4](start_span)[span_5](start_span)Suspeitos[span_4](end_span)[span_5](end_span)
    criar_secao_vertical("ENVOLVIDOS (SUSPEITOS)", d_suspeitos)

    # 5. [span_6](start_span)HISTÓRICO[span_6](end_span)
    pdf.set_font("Arial", 'B', 11)
    pdf.set_fill_color(230, 230, 240)
    pdf.cell(190, 8, "HISTÓRICO DA OCORRÊNCIA", 0, 1, 'L', fill=True)
    pdf.ln(2)
    
    pdf.set_font("Arial", 'B', 10)
    nat_texto = f"NATUREZA: {d_relato['natureza']}".upper().encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(190, 6, nat_texto, 0, 1, 'L')
    pdf.ln(2)
    
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(190, 6, "RELATO DETALHADO:", 0, 1, 'L')
    pdf.set_font("Arial", size=10)
    rel_texto = str(d_relato['relato']).encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 6, rel_texto, 0, 'L') # multi_cell garante que o texto use a largura toda e pule de página
    
    if d_relato['materiais']:
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(190, 6, "MATERIAIS E APREENSÕES:", 0, 1, 'L')
        pdf.set_font("Arial", size=10)
        mat_texto = str(d_relato['materiais']).encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 6, mat_texto, 0, 'L')

    # 6. [span_7](start_span)FOTOS (Páginas novas)[span_7](end_span)
    for foto, label in [(f_susp, "DO SUSPEITO"), (f_mat, "DO MATERIAL")]:
        if foto:
            try:
                pdf.add_page()
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 10, f"ANEXO FOTOGRÁFICO - {label}".encode('latin-1', 'replace').decode('latin-1'), 0, 1, 'C')
                img = Image.open(foto).convert("RGB")
                img_temp = io.BytesIO()
                img.save(img_temp, format="JPEG")
                img_temp.seek(0)
                pdf.image(img_temp, x=15, y=30, w=180)
            except:
                pass

    return pdf.output(dest='S')

# --- INTERFACE ---
st.markdown("<h1>🛡️ B.O. FÁCIL</h1>", unsafe_allow_html=True)

abas = st.tabs(["📍 Local", "👤 Vítimas", "👥 Testemunhas", "🚨 Suspeitos", "📖 Relato", "🏁 Finalizar"])

with abas:
    vtr_in = st.text_input("Viatura", key="vtr_final")
    loc_in = st.text_input("Local da Ocorrência", key="loc_final")
    gua_in = st.text_area("Guarnição", key="gua_final")

[span_8](start_span)[span_9](start_span)with abas[1]:
    v_lista = []
    for i in range(1, 3):
        vn = st.text_input(f"Nome Vítima {i}", key=f"vnome_{i}")
        vd = st.text_input(f"Doc Vítima {i}", key=f"vdoc_{i}")
        if vn: v_lista.append(f"Vítima {i}: {vn} (Doc: {vd})")

[cite_start]with abas[2]: # ABA TESTEMUNHAS
    t_lista = []
    for i in range(1, 3):
        tn = st.text_input(f"Nome Testemunha {i}", key=f"tnome_{i}")
        td = st.text_input(f"Doc Testemunha {i}", key=f"tdoc_{i}")
        if tn: t_lista.append(f"Testemunha {i}: {tn} (Doc: {td})")

[cite_start]with abas[3]:
    s_lista = []
    for i in range(1, 4):
        with st.expander(f"Suspeito {i}"):
            sn = st.text_input(f"Nome S{i}", key=f"snome_{i}")
            [cite_start]sm = st.text_input(f"Mãe S{i}", key=f"smae_{i}") # Campo Mãe[span_8](end_span)[span_9](end_span)
            sd = st.text_input(f"Doc S{i}", key=f"sdoc_{i}")
            if sn: s_lista.append(f"Suspeito {i}: {sn} | Mãe: {sm} | Doc: {sd}")

[cite_start]with abas[4]:
    crimes_tco = ["Ameaça", "Lesão Corporal", "Desacato", "Vias de Fato", "Dano"]
    nat_in = st.selectbox("Natureza", crimes_tco + ["Roubo", "Tráfico", "Outros"], key="nat_final")
    rel_in = st.text_area("Relato da Ocorrência", height=300, key="rel_final")
    mat_in = st.text_area("Materiais Apreendidos", key="mat_final")

[cite_start]with abas[5]:
    f_susp_in = st.file_uploader("Foto Suspeito", type=['jpg','jpeg','png'], key="fs_final")
    f_mat_in = st.file_uploader("Foto Material", type=['jpg','jpeg','png'], key="fm_final")
    
    if st.button("GERAR PDF E FINALIZAR", key="btn_gerar_final"):
        tipo_doc = "Termo Circunstanciado de Ocorrencia" if nat_in in crimes_tco else "Boletim de Ocorrencia"
        
        try:
            # A correção do erro de 'bytearray' está aqui:
            pdf_bruto = gerar_pdf_final(
                tipo_doc,
                {"Viatura": vtr_in, "Local": loc_in, "Agentes": gua_in},
                v_lista, t_lista, s_lista,
                {"natureza": nat_in, "relato": rel_in, "materiais": mat_in},
                f_susp_in, f_mat_in
            )
            
            # Converte o resultado para bytes antes do download
            st.download_button(
                label="⬇️ BAIXAR RELATÓRIO FINAL",
                data=bytes(pdf_bruto),
                file_name="Relatorio_Final.pdf",
                mime="application/pdf",
                key="download_final"
            )
        except Exception as e:
            st.error(f"Erro ao gerar: {str(e)}")
