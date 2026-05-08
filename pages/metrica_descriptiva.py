import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
import pandas as pd
import plotly.express as px
import numpy as np

# --- Configuración de la página ---
st.set_page_config(page_title="Análisis descriptiva de Ventas", page_icon=":material/analytics:", layout="wide")

# --- Conexión a la Base de Datos Vectorial ---
@st.cache_resource
def init_db():
    # Usamos la ruta y colección que definimos en crearvectorDB.py
    client = chromadb.PersistentClient(path="./sales_vector_db")
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    return client.get_collection(name="sales_collection", embedding_function=emb_fn)

try:
    collection = init_db()
except Exception:
    st.error("Error: No se encontró la base de datos. Ejecuta primero 'crearvectorDB.py'.")
    st.stop()

# --- Interfaz de Usuario ---
st.title(":material/analytics: Dashboard Analítico de Ventas")
st.markdown("""
Esta herramienta utiliza **Inteligencia Artificial** para encontrar transacciones y generar estadísticas automáticas. 
Prueba con frases como: *'Ventas de smartphones en 2025'*, *'Laptops más caras en Perú'* o *'Movimientos en Colombia'*.
""")

query = st.text_input("🔍 Consulta tus datos:", placeholder="Ej: Tablets vendidas en 2024")

if query:
    # Aumentamos n_results a 50 para tener una muestra estadística significativa
    results = collection.query(query_texts=[query], n_results=50)
    
    if results['metadatas'][0]:
        # 1. Convertir metadatas a DataFrame para análisis
        df_res = pd.DataFrame(results['metadatas'][0])
        
        # Aseguramos tipos numéricos
        df_res['Sales'] = pd.to_numeric(df_res['Sales'])
        df_res['transaction_qty'] = pd.to_numeric(df_res['transaction_qty'])

        # --- SECCIÓN 1: Estadísticas Descriptivas ---
        st.subheader(":material/dashboard: Indicadores Clave (KPIs)")
        m1, m2, m3, m4 = st.columns(4)
        
        total_v = df_res['Sales'].sum()
        media_v = df_res['Sales'].mean()
        varianza_v = df_res['Sales'].var()
        cant_total = df_res['transaction_qty'].sum()
        
        m1.metric("Ventas Totales", f"${total_v:,.2f}")
        m2.metric("Venta Promedio", f"${media_v:,.2f}")
        m3.metric("Unidades Totales", f"{int(cant_total)}")
        m4.metric("Varianza (Riesgo)", f"{varianza_v:,.2f}")

        # --- SECCIÓN 2: Análisis de Probabilidad y Outliers ---
        st.divider()
        st.subheader(":material/query_stats: Análisis de Probabilidad y Outliers")
        
        # Cálculo de Z-Score para detectar anomalías (ventas muy por encima de la media)
        mean_s = df_res['Sales'].mean()
        std_s = df_res['Sales'].std()
        df_res['z_score'] = (df_res['Sales'] - mean_s) / std_s
        outliers = df_res[df_res['z_score'].abs() > 2]
        
        p1, p2 = st.columns(2)
        with p1:
            prob_superior = (df_res['Sales'] > mean_s).mean() * 100
            st.info(f"**Probabilidad de éxito:** Existe un **{prob_superior:.1f}%** de probabilidad de que una venta supere la media actual en este segmento.")
        with p2:
            st.warning(f"**Detección de anomalías:** Se han identificado **{len(outliers)}** transacciones atípicas (Outliers) en tu búsqueda.")

        # --- SECCIÓN 3: Gráficos Dinámicos ---
        st.divider()
        g1, g2 = st.columns(2)
        
        with g1:
            st.write("#### Distribución de Ingresos")
            fig_hist = px.histogram(df_res, x="Sales", nbins=15, marginal="rug", 
                                    title="Frecuencia de montos", color_discrete_sequence=['#636EFA'])
            st.plotly_chart(fig_hist, width='stretch')
            
        with g2:
            st.write("#### Desempeño por Ubicación")
            fig_bar = px.bar(df_res, x='store_location', y='Sales', color='product_category',
                             title="Ventas por país y categoría", barmode='group')
            st.plotly_chart(fig_bar, width='stretch')

        # --- SECCIÓN 4: Detalle de Transacciones ---
        st.divider()
        with st.expander(":material/table_sign: Ver detalle de las 50 transacciones encontradas"):
            st.dataframe(df_res.drop(columns=['z_score']), width='stretch')

    else:
        st.warning(":material/warning: No se encontraron resultados para esa consulta.")

else:
    # Estado inicial: Mostrar algo de información general si no hay búsqueda
    st.info("Introduce una consulta arriba para activar el análisis estadístico.")

st.divider() 