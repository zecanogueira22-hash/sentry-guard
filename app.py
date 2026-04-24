import streamlit as st
from fpdf import FPDF
from PIL import Image
import io

# 1. CONFIGURAÇÃO MÍNIMA
st.set_page_config(page_title="B.O. FÁCIL OFICIAL", layout="wide")

# Estilo para as cores da polícia
st.markdown("<style>.stApp {background-color: #1A334A; color: white;} .stButton>button {background-color: #18A3B7; color: white;}</style>", unsafe_allow_html=True)

# 2. FUNÇÃO DE APOIO (Limpa erros de acento)
def formatar(texto):
    if not texto: return ""
    return str(texto).encode('latin-1', 'replace').decode('latin-1')

# 3. GERADOR DE PDF MELHORADO
def criar_documento(tipo, local, vits, tests, susps, hist, img_s, img_m):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    
    # Cabeçalho
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 15, formatar(tipo.upper()), 1, 1, 'C')
    pdf.ln(5)

    # Função para blocos de texto
    def bloco(titulo, lista):
        if lista:
            pdf.set_font("Arial", 'B', 11)
            pdf.set_fill_color(230, 230, 240)
            pdf.cell(190, 8, formatar(titulo), 0, 1, 'L', fill=True)
            pdf.set_font("Arial", size=10)
            pdf.ln(2)
            for linha in lista:
                pdf.multi_cell(0, 6, formatar(linha), 0, 'L')
            pdf.ln(4)

    bloco("DADOS DA EQUIPE", [f"Viatura: {local['v']}", f"Local: {local['l']}", f"Agentes: {local['a']}"])
    bloco("VÍTIMAS", vits)
    bloco("TESTEMUNHAS", tests)
    bloco("SUSPEITOS", susps)

    # Relato (Ocupa a largura toda e pula página)
    pdf.set_font("Arial", 'B', 11)
    pdf.set_fill_color(230, 230, 240)
    pdf.cell(190, 8, "HISTÓRICO DA OCORRÊNCIA", 0, 1, 'L', fill=True)
    pdf.ln(2)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 6, formatar(f"NATUREZA: {hist['n']}"), 0, 1, 'L')
    pdf.ln(2)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 6, formatar(hist['r']), 0, 'L')
    
    if hist['m']:
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 6, "MATERIAIS/APREENSÕES:", 0, 1, 'L')
        pdf.multi_cell(0, 6, formatar(hist['m']), 0, 'L')

    # Fotos (Página exclusiva)
    for f, label in [(img_s, "SUSPEITO"), (img_m, "MATERIAL")]:
        if f:
            pdf.add_page()
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, formatar(f"FOTO {label}"), 0, 1, 'C')
            pic = Image.open(f).convert("RGB")
            buf = io.BytesIO()
            pic.save(buf, format='JPEG')
            buf.seek(0)
            pdf.image(buf, x=15, y=30, w=180)

    return pdf.output(dest='S')

# 4. INTERFACE (ABAS)
st.title("🛡️ B.O. FÁCIL")

t1, t2, t3, t4, t5, t6 = st.tabs(["📍 Local", "👤 Vítimas", "👥 Testemunhas", "🚨 Suspeitos", "📖 Relato", "🏁 Finalizar"])

with t1:
    viatura = st.text_input("Viatura", key="v_1")
    endereco = st.text_input("Endereço", key="v_2")
    equipe = st.text_area("Agentes", key="v_3")

with t2:
    v_lista = []
    for i in range(1, 3):
        n_v = st.text_input(f"Vítima {i} - Nome", key=f"vn_{i}")
        d_v = st.text_input(f"Vítima {i} - CPF/RG", key=f"vd_{i}")
        if n_v: v_lista.append(f"Vítima {i}: {n_v} (Doc: {d_v})")

with t3:
    t_lista = []
    for i in range(1, 3):
        n_t = st.text_input(f"Testemunha {i} - Nome", key=f"tn_{i}")
        d_t = st.text_input(f"Testemunha {i} - CPF/RG", key=f"td_{i}")
        if n_t: t_lista.append(f"Testemunha {i}: {n_t} (Doc: {d_t})")

with t4:
    s_lista = []
    for i in range(1, 3):
        with st.expander(f"Suspeito {i}"):
            ns = st.text_input(f"Nome S{i}", key=f"sn_{i}")
            ms = st.text_input(f"Mãe S{i}", key=f"sm_{i}")
            ds = st.text_input(f"Doc S{i}", key=f"sd_{i}")
            if ns: s_lista.append(f"Suspeito {i}: {ns} | Mãe: {ms} | Doc: {ds}")

with t5:
    naturezas = ["Ameaça", "Lesão Corporal", "Desacato", "Dano", "Vias de Fato", "Outros"]
    nat = st.selectbox("Natureza", naturezas, key="nat_sel")
    relato = st.text_area("Relato Completo", height=250, key="rel_campo")
    apreensoes = st.text_area("Materiais", key="mat_campo")

with t6:
    f_susp = st.file_uploader("Foto Suspeito", type=['jpg','png'], key="f_1")
    f_mat = st.file_uploader("Foto Material", type=['jpg','png'], key="f_2")
    
    if st.button("GERAR PDF AGORA"):
        tipo_bo = "Termo Circunstanciado" if nat != "Outros" else "Boletim de Ocorrência"
        try:
            pdf_final = criar_documento(tipo_bo, {'v':viatura, 'l':endereco, 'a':equipe}, v_lista, t_lista, s_lista, {'n':nat, 'r':relato, 'm':apreensoes}, f_susp, f_mat)
            st.download_button("⬇️ BAIXAR PDF", data=bytes(pdf_final), file_name="Relatorio.pdf", mime="application/pdf")
            st.success("PDF Gerado com Sucesso!")
        except Exception as e:
            st.error(f"Erro no sistema: {e}")
    
