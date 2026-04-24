import streamlit as st
from fpdf import FPDF
from PIL import Image
import io

# 1. CONFIGURAÇÃO BÁSICA (Obrigatória para o Streamlit)
st.set_page_config(page_title="B.O. FÁCIL", layout="wide")

# 2. TRATAMENTO DE TEXTO (Para não dar erro com acentos)
def txt(texto):
    if not texto: return ""
    return str(texto).encode('latin-1', 'replace').decode('latin-1')

# 3. MOTOR DO PDF
class GeradorPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 9)
        self.set_text_color(150)
        if self.page_no() > 1:
            self.cell(0, 10, txt(f'Continuação - Página {self.page_no()}'), 0, 1, 'R')

def finalizar_pdf(titulo, dados_guarda, vits, tests, susps, relato_final, f1, f2):
    pdf = GeradorPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Título
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(190, 15, txt(titulo.upper()), 1, 1, 'C')
    pdf.ln(5)

    # Função para criar blocos simples na vertical
    def secao(titulo_secao, conteudo_lista):
        if conteudo_lista:
            pdf.set_font("Arial", 'B', 11)
            pdf.set_fill_color(230, 230, 240)
            pdf.cell(0, 8, txt(titulo_secao), 0, 1, 'L', fill=True)
            pdf.set_font("Arial", size=10)
            pdf.ln(2)
            for linha in conteudo_lista:
                pdf.multi_cell(0, 6, txt(linha), 0, 'L')
            pdf.ln(4)

    # Preenchendo os dados
    secao("DADOS DA EQUIPE E LOCAL", [f"Viatura: {dados_guarda['v']}", f"Local: {dados_guarda['l']}", f"Agentes: {dados_guarda['a']}"])
    secao("VÍTIMAS", vits)
    secao("TESTEMUNHAS", tests)
    secao("SUSPEITOS", susps)

    # Histórico (Ocupando a página toda conforme necessário)
    pdf.set_font("Arial", 'B', 11)
    pdf.set_fill_color(230, 230, 240)
    pdf.cell(0, 8, txt("HISTÓRICO DA OCORRÊNCIA"), 0, 1, 'L', fill=True)
    pdf.ln(2)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 6, txt(f"NATUREZA: {relato_final['n']}"), 0, 1, 'L')
    pdf.ln(2)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 6, txt(relato_final['r']), 0, 'L')
    
    if relato_final['m']:
        pdf.ln(4)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 6, txt("MATERIAIS / APREENSÕES:"), 0, 1, 'L')
        pdf.multi_cell(0, 6, txt(relato_final['m']), 0, 'L')

    # Fotos (Uma por página para evitar erros de tamanho)
    for foto, nome_foto in [(f1, "SUSPEITO"), (f2, "MATERIAL")]:
        if foto:
            pdf.add_page()
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, txt(f"FOTO DO {nome_foto}"), 0, 1, 'C')
            img_aberta = Image.open(foto).convert("RGB")
            img_temp = io.BytesIO()
            img_aberta.save(img_temp, format='JPEG')
            img_temp.seek(0)
            pdf.image(img_temp, x=15, y=30, w=180)

    return pdf.output(dest='S')

# 4. INTERFACE DO USUÁRIO (Streamlit)
st.title("🛡️ B.O. FÁCIL")

aba1, aba2, aba3, aba4, aba5, aba6 = st.tabs(["📍 Local", "👤 Vítimas", "👥 Testemunhas", "🚨 Suspeitos", "📖 Relato", "🏁 Finalizar"])

with aba1:
    vtr = st.text_input("Viatura", key="key_vtr")
    loc = st.text_input("Local da Ocorrência", key="key_loc")
    agt = st.text_area("Guarnição", key="key_agt")

with aba2:
    v_list = []
    for i in range(1, 3):
        n = st.text_input(f"Nome Vítima {i}", key=f"key_vn{i}")
        d = st.text_input(f"Documento Vítima {i}", key=f"key_vd{i}")
        if n: v_list.append(f"Vítima {i}: {n} (Doc: {d})")

with aba3: # NOVA ABA DE TESTEMUNHAS
    t_list = []
    for i in range(1, 3):
        tn = st.text_input(f"Nome Testemunha {i}", key=f"key_tn{i}")
        td = st.text_input(f"Documento Testemunha {i}", key=f"key_td{i}")
        if tn: t_list.append(f"Testemunha {i}: {tn} (Doc: {td})")

with aba4:
    s_list = []
    for i in range(1, 3):
        with st.expander(f"Suspeito {i}"):
            sn = st.text_input(f"Nome do Suspeito {i}", key=f"key_sn{i}")
            sm = st.text_input(f"Nome da Mãe do Suspeito {i}", key=f"key_sm{i}")
            sd = st.text_input(f"Documento do Suspeito {i}", key=f"key_sd{i}")
            if sn: s_list.append(f"Suspeito {i}: {sn} | Mãe: {sm} | Doc: {sd}")

with aba5:
    nat = st.selectbox("Natureza", ["Ameaça", "Lesão Corporal", "Desacato", "Dano", "Vias de Fato", "Outros"], key="key_nat")
    rel = st.text_area("Relato da Ocorrência", height=250, key="key_rel")
    mat = st.text_area("Materiais Apreendidos", key="key_mat")

with aba6:
    f_s = st.file_uploader("Foto do Suspeito", type=['jpg', 'png', 'jpeg'], key="key_f1")
    f_m = st.file_uploader("Foto do Material", type=['jpg', 'png', 'jpeg'], key="key_f2")
    
    if st.button("GERAR DOCUMENTO FINAL"):
        titulo_final = "Termo Circunstanciado de Ocorrencia" if nat != "Outros" else "Boletim de Ocorrencia"
        try:
            pdf_resultado = finalizar_pdf(titulo_final, {'v':vtr, 'l':loc, 'a':agt}, v_list, t_list, s_list, {'n':nat, 'r':rel, 'm':mat}, f_s, f_m)
            
            # DOWNLOAD SEM ERRO
            st.download_button(
                label="⬇️ BAIXAR RELATÓRIO COMPLETO",
                data=bytes(pdf_resultado),
                file_name="Relatorio.pdf",
                mime="application/pdf"
            )
            st.success("PDF gerado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao gerar PDF: {e}")
    
