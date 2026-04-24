import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from PIL import Image # Certifique-se de que o Pillow está no requirements.txt
import io

# Tenta abrir a imagem do ícone. Se não conseguir, usa o emoji.
try:
    icon_image = Image.open("icone.png")
except FileNotFoundError:
    icon_image = "🛡️" # Fallback

# 1. NOME NA ABA E NO ÍCONE DO CELULAR (Atualizado com sua imagem)
st.set_page_config(
    page_title="B.O. FÁCIL", 
    page_icon=icon_image, 
    layout="wide"
)

# ... (resto do código do app segue igual)
