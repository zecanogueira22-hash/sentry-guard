import streamlit as st
from fpdf import FPDF
from PIL import Image
import io

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="B.O. FÁCIL V3", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #1A334A; color: white; }
    .stButton>button { background: #18A3B7 !important; color: white !important; font-weight: bold !important; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO DE TRATAMENTO DE TEXTO ---
def limpar_texto(txt):
    if not txt: return ""
    return str(txt).encode('latin-1', 'replace').decode('latin-1')

# --- CLASSE DO PDF ---
class MeuPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 10)
        self.set_text_color(150, 150, 150)
        if self.page_no() > 1:
            self.cell(0, 10, f'Folha {self.page_no()}', 0, 1, 'R')

def criar_relatorio(titulo, eq, vits, tests, susps, relato_final, f_s, f_m):
    pdf = MeuPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    
    # Cabeçalho
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 12, limpar_texto(titulo.upper()), 1, 1, 'C')
    pdf.ln(5)

    def add_bloco(t, lista):
        if lista:
            pdf.set_font("Arial", 'B', 11)
            pdf.set_fill_color(230, 230, 240)
            pdf.cell(190, 8, limpar_texto(t), 0, 1, 'L', fill=True)
            pdf.set_font("Arial", size=10)
            pdf.ln(2)
            for item in lista:
                pdf.multi_cell(0, 6, limpar_texto(item), 0, 'L')
            pdf.ln(4)

    # 1. Equipe
    add_bloco("DADOS DA EQUIPE", [f"Viatura: {eq['v']}", f"Local: {eq['l']}", f"Agentes: {eq['a']}"])
    
    # 2. Vítimas
    add_bloco("VÍTIMAS", vits)

    # 3. Testemunhas
    add_bloco("TESTEMUNHAS", tests)
        
    # 4. Suspeitos
    add_bloco("SUSPEITOS", susps)

    # 5. Histórico
    pdf.set_font("Arial", 'B', 11)
    pdf.set_fill_color(230, 230, 240)
    pdf.cell(190, 8, "HISTÓRICO DA OCORRÊNCIA", 0, 1, 'L', fill=True)
    pdf.ln(2)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 6, limpar_texto(f"NATUREZA: {relato_final['n']}"), 0, 1, 'L')
    pdf.ln(2)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 6, limpar_texto(relato_final['r']), 0, 'L')
    
    if relato_final['m']:
        pdf.ln(4)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 6, "MATERIAIS:", 0, 1, 'L')
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 6, limpar_texto(relato_final['m']), 0, 'L')

    # 6. Fotos
    for f, label in [(f_s, "SUSPEITO"), (f_m, "MATERIAL")]:
        if f:
            pdf.add_page()
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, limpar_texto(f"FOTO {label}"), 0, 1, 'C')
            img = Image.open(f).convert("RGB")
            img_io = io.BytesIO()
            img.save(img_io, format='JPEG')
            img_io.seek(0)
            pdf.image(img_io, x=15, y=30, w=180)

    return pdf.output(dest='S')

# --- INTERFACE ---
st.title("🛡️ B.O. FÁCIL")

tabs = st.tabs(["📍 Local", "👤 Vítimas", "👥 Testemunhas", "🚨 Suspeitos", "📖 Relato", "🏁 Finalizar"])

with tabs:
    vtr = st.text_input("Viatura", key="k_vtr")
    loc = st.text_input("Endereço", key="k_loc")
    gua = st.text_area("Agentes", key="k_gua")

with tabs:
    v_l = []
    for i in range(1, 3):
        n = st.text_input(f"Nome Vítima {i}", key=f"k_vn_{i}")
        d = st.text_input(f"Doc Vítima {i}", key=f"k_vd_{i}")
        if n: v_l.append(f"{n} (Doc: {d})")

with tabs:
    t_l = []
    for i in range(1, 3):
        tn = st.text_input(f"Nome Testemunha {i}", key=f"k_tn_{i}")
        td = st.text_input(f"Doc Testemunha {i}", key=f"k_td_{i}")
        if tn: t_l.append(f"{tn} (Doc: {td})")

with tabs:
    s_l = []
    for i in range(1, 4):
        with st.expander(f"Suspeito {i}"):
            sn = st.text_input(f"Nome S{i}", key=f"k_sn_{i}")
            sm = st.text_input(f"Mãe S{i}", key=f"k_sm_{i}")
            sd = st.text_input(f"Doc S{i}", key=f"k_sd_{i}")
            if sn: s_l.append(f"Nome: {sn} | Mãe: {sm} | Doc: {sd}")

with tabs:
    c_tco = ["Ameaça", "Lesão Corporal", "Desacato", "Dano"]
    nat = st.selectbox("Natureza", c_tco + ["Roubo", "Tráfico", "Outros"], key="k_nat")
    rel = st.text_area("Relato", height=250, key="k_rel")
    mat = st.text_area("Objetos", key="k_mat")

with tabs:
    f1 = st.file_uploader("Foto Suspeito", type=['jpg','png'], key="k_f1")
    f2 = st.file_uploader("Foto Material", type=['jpg','png'], key="k_f2")
    
    if st.button("GERAR DOCUMENTO AGORA"):
        t_doc = "Termo Circunstanciado" if nat in c_tco else "Boletim de Ocorrência"
        try:
            res_pdf = criar_relatorio(t_doc, {'v':vtr, 'l':loc, 'a':gua}, v_l, t_l, s_l, {'n':nat, 'r':rel, 'm':mat}, f1, f2)
            st.download_button("⬇️ BAIXAR PDF", data=bytes(res_pdf), file_name="Relatorio.pdf", mime="application/pdf")
        except Exception as e:
            st.error(f"Erro: {e}")
            
