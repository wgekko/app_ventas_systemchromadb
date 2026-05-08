import streamlit as st
import base64
from pathlib import Path
import streamlit.components.v1 as components

# --- Configuración página ---
st.set_page_config(
    page_title="App System ChromeDB Ventas", 
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


# --- CARGA DE CSS PARA BOTONES HOLOGRAMA ---
try:
    # Se asume que el CSS está en static/boton.css según tu solicitud anterior
    boton_css_raw = Path("static/boton.css").read_text(encoding="utf-8")
    hologram_css = f"<style>{boton_css_raw}</style>"
except:
    # Fallback al CSS embebido si el archivo no existe
    hologram_css = """
    <style>
    div[data-testid="stButton"] > button {
        width: 100% !important; /* Fuerza el ancho total */
        position: relative;
        padding: 1.2rem 1rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #fff !important;
        background: rgba(0, 255, 255, 0.1) !important;
        border: 2px solid rgba(0, 255, 255, 0.5) !important;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.3) !important;
        backdrop-filter: blur(5px) !important;
        text-transform: uppercase;
        transition: all 0.4s ease !important;
    }
    div[data-testid="stButton"] > button:hover {
        background: rgba(0, 255, 255, 0.2) !important;
        box-shadow: 0 0 25px rgba(0, 255, 255, 0.5) !important;
        border-color: rgba(0, 255, 255, 0.8) !important;
    }
    </style>
    """

#st.subheader("Dashboard de Análisis de Ventas")
#st.info("aplicando concepto de búsqueda semántica (Vectores)")
col_izq, col_central, col_der = st.columns([1, 10, 1])

with col_central:
    # 1. Subheader centrado usando el parámetro nativo
    st.header("Dashboard de Análisis de Ventas", anchor=False, text_alignment="center")

    # 2. CSS para centrar el texto dentro de los componentes st.info (o alertas)
    st.markdown("""
        <style>
        .stAlert > div {
            text-align: center;
            display: flex;
            justify-content: center;
        }
        </style>
    """, unsafe_allow_html=True)

    # 3. Cuadro de información centrado
    st.info("aplicando concepto de búsqueda semántica (Vectores)")

    # (Aquí continuarían tus animaciones y botones...)
    v1, v2 = st.columns(2)

# --- Carga de Animaciones ---
def load_html(file_name):
    return Path(file_name).read_text(encoding="utf-8")

try:
    tunnel_html = load_html("static/3d-perspective-data-""tunnel.html") #
    crt_html = load_html("static/crt-boot-sequence.html") #
except:
    tunnel_html = crt_html = ""

# --- Función para cargar HTML como Data URL para st.iframe ---
def get_html_data_url(file_path):
    try:
        content = Path(file_path).read_text(encoding="utf-8")
        b64 = base64.b64encode(content.encode()).decode()
        return f"data:text/html;base64,{b64}"
    except:
        return ""

tunnel_url = get_html_data_url("static/3d-perspective-data-tunnel.html")
crt_url = get_html_data_url("static/crt-boot-sequence.html")
# --- RENDERIZADO ---
col_izq, col_central, col_der = st.columns([1, 10, 1]) #

with col_central:
    # 1. Animaciones en ventanas paralelas
    v1, v2 = st.columns(2)
    with v1:        
        #components.html(tunnel_html, height=400, scrolling=False)
        if tunnel_url:
            st.iframe(tunnel_url, height=400)
    with v2:
        #components.html(crt_html, height=400, scrolling=False)
        if crt_url:
            st.iframe(crt_url, height=400)

    st.write("") 
    
    # 2. Inyectamos el CSS para que afecte a los botones de abajo
    st.markdown(hologram_css, unsafe_allow_html=True)
    
    # 3. Contenedor de botones ajustado
    # Para que los botones coincidan con el ancho de las animaciones,
    # usamos las mismas columnas (2) sin márgenes internos extra.
    with st.container(border=True):
        st.subheader("Acceso a modelos de Análisis", anchor=False, text_alignment="center")
        
        # Usamos width='stretch' para que ocupen todo el espacio de su columna
        b1, b2 = st.columns(2)
        with b1:
            if st.button("Modelo descriptivo", key="acceso", width='stretch'):
                st.switch_page("pages/metrica_descriptiva.py")
        with b2:
            if st.button("Modelo predictivo", key="acceso1", width='stretch'):
                st.switch_page("pages/metrica_predictiva.py")
    st.markdown("---")            