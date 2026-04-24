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

st.set_page_config(
    page_title="B.O. FÁCIL", 
    page_icon=img_icone, 
    layout="wide"
)

# --- ESTÉTICA TÁTICA ---
st.markdown("""
    <style>
    .stApp { background: #1A334A; color: white; }
    .tactic-card {
        background: rgba(30, 83, 110, 0.4);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #18A3B7;
        margin-bottom: 10px;
    }
    .section-title, h1, h2, h3 { color: #27E6EC !important; }
    .stTabs [aria-selected="true"] {
        background-color: #27E6EC !important;
        color: #1A334A !important;
        font-weight: bold;
    }
    .stButton>button {
        background: #18A3B7;
        color: white;
        border-radius: 8px;
        width: 100%;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

def gerar_pdf_completo(dados, f_susp, f_mat):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 10, "B.O. FACIL - RELATORIO OPERACIONAL", 1, 1, 'C')
    pdf.ln(5)

    for secao, info in dados.items():
        pdf.set_font("Arial", 'B', 11)
        pdf.set_fill_color(230, 230, 240)
        pdf.cell(190, 7, secao, 0, 1, 'L', fill=True)
        pdf.set_font("Arial", size=9)
        if isinstance(info, dict):
            for k, v in info.items():
                if v: 
                    texto = f"{k}: {v}".encode('ascii', 'ignore').decode('ascii')
                    pdf.multi_cell(190, 6, texto, 0, 'L')
        pdf.ln(2)

    # Fotos (Método de salvamento temporário para evitar erros de memória)
    if f_susp:
        try:
            pdf.add_page()
            pdf.cell(190, 10, "ANEXO - FOTO DO SUSPEITO", 0, 1, 'L')
            img_s = Image.open(f_susp).convert("RGB")
            img_s.save("temp_s.jpg")
            pdf.image("temp_s.jpg", x=10, y=30, w=100)
        except: pass
    
    if f_mat:
        try:
            pdf.add_page()
            pdf.cell(190, 10, "ANEXO - MATERIAL APREENDIDO", 0, 1, 'L')
            img_m = Image.open(f_mat).convert("RGB")
            img_m.save("temp_m.jpg")
            pdf.image("temp_m.jpg", x=10, y=30, w=100)
        except: pass

    # --- O PULO DO GATO PARA BYTES ---
    # Geramos o PDF como uma string e codificamos em latin-1
    pdf_output = pdf.output(dest='S').encode('latin-1')
    return pdf_output

st.markdown("<h1>🛡️ B.O. FÁCIL</h1>", unsafe_allow_html=True)

t_geral, t_vitimas, t_suspeitos, t_relato, t_fotos = st.tabs([
    "📍 Local/Guarnição", "👤 Vítimas", "🚨 Suspeitos", "📖 Relato/Apreensão", "📄 Finalizar"
])

with t_geral:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    end_fato = st.text_input("Endereço Completo do Fato")
    col_g1, col_g2 = st.columns(2)
    prefixo = col_g1.text_input("Viatura/Prefixo")
    agentes = col_g2.text_area("Guarnição (Nomes/Matrículas)")
    st.markdown('</div>', unsafe_allow_html=True)

with t_vitimas:
    v_dados = {}
    with st.expander("👤 Dados da Vítima 01"):
        v1_n = st.text_input("Nome (V1)")
        v1_d = st.text_input("Doc (V1)")
        v_dados["Vítima 01"] = f"Nome: {v1_n} | Doc: {v1_d}" if v1_n else ""
    with st.expander("👤 Dados da Vítima 02"):
        v2_n = st.text_input("Nome (V2)")
        v2_d = st.text_input("Doc (V2)")
        v_dados["Vítima 02"] = f"Nome: {v2_n} | Doc: {v2_d}" if v2_n else ""

with t_suspeitos:
    s_dados = {}
    for i in range(1, 4):
        with st.expander(f"🚨 Dados do Suspeito 0{i}"):
            sn = st.text_input(f"Nome (S{i})")
            sd = st.text_input(f"Doc (S{i})")
            sm = st.text_input(f"Mãe (S{i})")
            s_dados[f"Suspeito 0{i}"] = f"Nome: {sn} | Doc: {sd} | Mãe: {sm}" if sn else ""

with t_relato:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    tipo_crime = st.selectbox("Natureza da Ocorrência", ["Ameaça", "Lesão Corporal", "Roubo", "Furto", "Tráfico", "Maria da Penha", "Outros"])
    relato = st.text_area("Histórico da Ocorrência", height=150)
    materiais = st.text_area("Materiais Apreendidos")
    st.markdown('</div>', unsafe_allow_html=True)

with t_fotos:
    st.markdown('<div class="tactic-card">', unsafe_allow_html=True)
    f_susp = st.file_uploader("📸 Foto do Suspeito", type=['jpg','png','jpeg'])
    f_mat = st.file_uploader("📸 Foto Apreensões", type=['jpg','png','jpeg'])
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🏁 FINALIZAR E GERAR PDF", use_container_width=True):
        resumo_dict = {
            "EQUIPE": {"Viatura": prefixo, "Agentes": agentes, "Local": end_fato},
            "VITIMAS": v_dados,
            "SUSPEITOS": s_dados,
            "OCORRENCIA": {"Natureza": tipo_crime, "Histórico": relato, "Apreensões": materiais}
        }
        
        try:
            pdf_data = gerar_pdf_completo(resumo_dict, f_susp, f_mat)
            
            # CRIAMOS UM BUFFER DE BYTES REAL
            buffer = io.BytesIO()
            buffer.write(pdf_data)
            buffer.seek(0)
            
            st.download_button(
                label="⬇️ 1. BAIXAR PDF B.O. FÁCIL",
                data=buffer,
                file_name="BO_FACIL.pdf",
                mime="application/pdf"
            )

            msg = f"🛡️ *B.O. FÁCIL*\n🚨 *Natureza:* {tipo_crime}\n📍 *Local:* {end_fato}"
            url = f"https://wa.me/?text={urllib.parse.quote(msg)}"
            st.markdown(f'<a href="{url}" target="_blank"><button style="width:100%; background-color:#25D366; color:white; border:none; padding:12px; border-radius:8px; font-weight:bold; cursor:pointer;">📲 2. NOTIFICAR PELO WHATSAPP</button></a>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Erro ao gerar PDF: {e}")
        
