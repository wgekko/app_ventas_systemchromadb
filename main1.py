import streamlit as st
import base64
from pathlib import Path
import streamlit.components.v1 as components

# --- Configuración página ---
st.set_page_config(
    page_title="App System ChromeDB", 
    layout="wide", 
    page_icon=":material/chrome_reader_mode:", 
    initial_sidebar_state="collapsed"
)

# --- Estilos Globales (Ocultar elementos de Streamlit) ---
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stAppViewContainer"] { margin-left: 0px; }
    </style>
""", unsafe_allow_html=True)

# --- CSS PARA BOTONES HOLOGRAMA ---
hologram_css = """
<style>
div[data-testid="stButton"] > button {
    position: relative;
    padding: 1.5rem 2rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: #fff !important;
    background: rgba(0, 255, 255, 0.1) !important;
    border: 2px solid rgba(0, 255, 255, 0.5) !important;
    box-shadow: 0 0 15px rgba(0, 255, 255, 0.3) !important;
    backdrop-filter: blur(5px) !important;
    cursor: pointer;
    overflow: hidden;
    transition: all 0.4s ease !important;
    text-transform: uppercase;
    width: 100% !important;
}

div[data-testid="stButton"] > button:hover {
    background: rgba(0, 255, 255, 0.2) !important;
    box-shadow: 0 0 25px rgba(0, 255, 255, 0.5) !important;
    border-color: rgba(0, 255, 255, 0.8) !important;
}

div[data-testid="stButton"] > button::before {
    content: "";
    position: absolute;
    width: 100%;
    height: 2px;
    background: linear-gradient(to right, transparent, rgba(0, 255, 255, 0.8), transparent);
    top: 0;
    left: 0;
    animation: scan 2s linear infinite;
    z-index: 2;
}

div[data-testid="stButton"] > button:hover div[data-testid="stMarkdownContainer"] p {
    animation: glitch 0.3s infinite;
    text-shadow: 2px 0 #ff00ff, -2px 0 #00ffff;
}

@keyframes scan {
    0% { top: -10%; }
    100% { top: 110%; }
}

@keyframes glitch {
    0%, 100% { transform: translate(0); }
    33% { transform: translate(-2px, 1px); }
    66% { transform: translate(2px, -1px); }
}
</style>
"""

# --- Carga de Animaciones ---
def load_html(file_name):
    # Carga el contenido de los archivos HTML proporcionados
    return Path(file_name).read_text(encoding="utf-8")

try:
    tunnel_html = load_html("static/3d-perspective-data-tunnel.html") #
    crt_html = load_html("static/crt-boot-sequence.html") #
except Exception as e:
    st.error(f"Error cargando animaciones: {e}")
    tunnel_html = crt_html = ""

# --- RENDERIZADO ---
# Definición de columnas principales para centrar el contenido
col_izq, col_central, col_der = st.columns([1, 10, 1])

with col_central:
    # Creamos dos columnas paralelas para las animaciones
    v1, v2 = st.columns(2)
    
    with v1:
        # Ventana 1: 3D Perspective Data Tunnel
        components.html(tunnel_html, height=400, scrolling=False)
    
    with v2:
        # Ventana 2: CRT Boot Sequence
        components.html(crt_html, height=400, scrolling=False)

    st.write("") # Espaciador visual
    
    # Inyectamos el estilo holograma para los botones
    st.markdown(hologram_css, unsafe_allow_html=True)
    
    # Contenedor de botones de navegación
    with st.container(border=True):
        st.subheader("Acceso a modelos de Análisis", anchor=False, text_alignment="center")
        
        b1, b2 = st.columns(2)
        with b1:
            if st.button("Modelo descriptivo", key="acceso"):
                st.switch_page("pages/metrica_descriptiva.py")
        with b2:
            if st.button("Modelo predictivo", key="acceso1"):
                st.switch_page("pages/metrica_predictiva.py")