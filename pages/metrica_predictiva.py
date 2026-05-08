# import streamlit as st
# import chromadb
# from chromadb.utils import embedding_functions
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import numpy as np
# from scipy.stats import norm

# # --- Configuración de la página ---
# st.set_page_config(page_title="Análisis predictiva de Ventas", page_icon=":material/analytics:", layout="wide")

# # --- Conexión a la Base de Datos Vectorial ---
# @st.cache_resource
# def init_db():
#     client = chromadb.PersistentClient(path="./sales_vector_db")
#     emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
#     return client.get_collection(name="sales_collection", embedding_function=emb_fn)

# try:
#     collection = init_db()
# except Exception:
#     st.error("Error: Ejecuta primero 'crearvectorDB.py' para procesar los datos.")
#     st.stop()

# # --- Interfaz Principal ---
# st.title(":material/analytics: Plataforma de Soporte a Decisiones (DSS)")
# query = st.text_input("🔍 Consulta Estratégica:", placeholder="Ej: Análisis de laptops en Sudamérica 2025")

# if query:
#     # Recuperamos una muestra amplia para solidez estadística
#     results = collection.query(query_texts=[query], n_results=100)
    
#     if results['metadatas'][0]:
#         df = pd.DataFrame(results['metadatas'][0])
#         df['Sales'] = pd.to_numeric(df['Sales'])
#         df['transaction_qty'] = pd.to_numeric(df['transaction_qty'])
#         df['unit_price'] = df['Sales'] / df['transaction_qty']

#         # --- CÁLCULOS AVANZADOS ---
#         media = df['Sales'].mean()
#         desv_std = df['Sales'].std()
#         cv = (desv_std / media) * 100 if media != 0 else 0
        
#         # Pestañas para organizar el análisis
#         tab1, tab2, tab3, tab4 = st.tabs([":material/description: Descriptivo & Calidad", ":material/monitoring: Probabilidad & Riesgo", ":material/stacked_line_chart: Dispersión", ":material/table_rows_narrow: Detalle"])

#         with tab1:
#             st.subheader("Métricas de Calidad de Decisión")
#             c1, c2, c3, c4 = st.columns(4)
#             c1.metric("Ventas Totales", f"${df['Sales'].sum():,.2f}")
#             c2.metric("Promedio Unitario", f"${media:,.2f}")
            
#             # Semáforo de estabilidad (CV)
#             if cv < 15:
#                 c3.metric("Estabilidad (CV)", f"{cv:.1f}%", help="Ventas estables y predecibles")
#             elif cv < 30:
#                 c3.metric("Estabilidad (CV)", f"{cv:.1f}%", delta="- Volatilidad Media", delta_color="normal")
#             else:
#                 c3.metric("Estabilidad (CV)", f"{cv:.1f}%", delta="ALTA VOLATILIDAD", delta_color="inverse")
            
#             # Análisis de Pareto (80/20) simplificado
#             df_pareto = df.groupby('product_type')['Sales'].sum().sort_values(ascending=False).reset_index()
#             df_pareto['cum_perc'] = 100 * df_pareto['Sales'].cumsum() / df_pareto['Sales'].sum()
#             top_products = df_pareto[df_pareto['cum_perc'] <= 85]['product_type'].tolist()
#             c4.metric("Concentración", f"{len(top_products)} Prod. generan 85%", help="Productos clave según Pareto")

#             if cv > 35:
#                 st.warning(f":material/warning: **Alerta de Umbral:** La varianza es muy alta ({cv:.1f}%). Los promedios no son una base segura para presupuestar este segmento.")
            
#             st.divider()
#             # BoxPlot para comparativa de países
#             st.write("#### Comparativa de Dispersión por Ubicación")
#             fig_box = px.box(df, x="store_location", y="Sales", color="store_location", points="all",
#                              title="Distribución de precios y Outliers por país")
#             st.plotly_chart(fig_box, width='stretch')

#         with tab2:
#             st.subheader("Análisis Diagnóstico y Predictivo")
#             col_a, col_b = st.columns([2, 1])
            
#             with col_a:
#                 # Campana de Gauss vs Distribución Real
#                 x = np.linspace(df['Sales'].min(), df['Sales'].max(), 100)
#                 y = norm.pdf(x, media, desv_std)
                
#                 fig_gauss = pg = go.Figure()
#                 fig_gauss.add_trace(go.Histogram(x=df['Sales'], nbinsx=20, name='Frecuencia Real', histnorm='probability density'))
#                 fig_gauss.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Curva Teórica (Normal)', line=dict(color='red', width=3)))
#                 fig_gauss.update_layout(title="Distribución Real vs. Campana de Gauss", xaxis_title="Monto de Venta")
#                 st.plotly_chart(fig_gauss, width='stretch')
            
#             with col_b:
#                 st.info("**Explicabilidad (XAI):** La curva roja muestra el comportamiento ideal. Si tus barras azules están muy a la izquierda, tu volumen depende de ventas pequeñas.")
#                 # Probabilidad Condicional
#                 pais_top = df['store_location'].mode()[0]
#                 prob_cond = (df[df['store_location'] == pais_top]['Sales'] > media).mean() * 100
#                 st.write(f"**Probabilidad Condicional:**")
#                 st.write(f"Si la venta ocurre en **{pais_top}**, hay un **{prob_cond:.1f}%** de probabilidad de superar la media.")

#         with tab3:
#             st.subheader("Visualización de Impacto en Decisiones")
#             g_left, g_right = st.columns(2)
            
#             with g_left:
#                 st.write("#### Mapa de Jerarquía (Treemap)")
#                 fig_tree = px.treemap(df, path=['store_location', 'product_category', 'product_type'], 
#                                      values='Sales', color='Sales', title="Concentración de Ingresos")
#                 st.plotly_chart(fig_tree, width='stretch')
            
#             with g_right:
#                 st.write("#### Elasticidad: Precio vs Cantidad")
#                 fig_scat = px.scatter(df, x="unit_price", y="transaction_qty", color="product_category",
#                                      size="Sales", hover_data=['product_type'], title="Relación Precio-Volumen")
#                 st.plotly_chart(fig_scat, width='stretch')

#         with tab4:
#             st.dataframe(df, width='stretch')

#     else:
#         st.warning(":material/warning: No se encontraron datos para esta consulta.")

# st.divider()
import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy.stats import norm

# --- Configuración de la página ---
st.set_page_config(page_title="Análisis predictivo de Ventas", page_icon=":material/analytics:", layout="wide")

# --- Conexión a la Base de Datos Vectorial ---
@st.cache_resource
def init_db():
    client = chromadb.PersistentClient(path="./sales_vector_db")
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    return client.get_collection(name="sales_collection", embedding_function=emb_fn)

try:
    collection = init_db()
except Exception:
    st.error("Error: Ejecuta primero 'crearvectorDB.py' para procesar los datos.")
    st.stop()

# --- Interfaz Principal ---
st.title(":material/analytics: Plataforma de Soporte a Decisiones (DSS)")
query = st.text_input("🔍 Consulta Estratégica:", placeholder="Ej: Análisis de laptops en Sudamérica 2025")

if query:
    # Recuperamos una muestra amplia para solidez estadística
    results = collection.query(query_texts=[query], n_results=100)
    
    if results['metadatas'][0]:
        df = pd.DataFrame(results['metadatas'][0])
        df['Sales'] = pd.to_numeric(df['Sales'])
        df['transaction_qty'] = pd.to_numeric(df['transaction_qty'])
        df['unit_price'] = df['Sales'] / df['transaction_qty']

        # --- CÁLCULOS AVANZADOS ---
        media = df['Sales'].mean()
        desv_std = df['Sales'].std()
        cv = (desv_std / media) * 100 if media != 0 else 0
        
        # Pestañas para organizar el análisis
        tab1, tab2, tab3, tab4 = st.tabs([
            ":material/description: Descriptivo & Calidad", 
            ":material/monitoring: Probabilidad & Riesgo", 
            ":material/stacked_line_chart: Dispersión", 
            ":material/table_rows_narrow: Detalle"
        ])

        with tab1:
            st.subheader("Métricas de Calidad de Decisión")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Ventas Totales", f"${df['Sales'].sum():,.2f}")
            c2.metric("Promedio Unitario", f"${media:,.2f}")
            
            # Semáforo de estabilidad (CV)
            if cv < 15:
                c3.metric("Estabilidad (CV)", f"{cv:.1f}%", help="Ventas estables y predecibles")
            elif cv < 30:
                c3.metric("Estabilidad (CV)", f"{cv:.1f}%", delta="- Volatilidad Media", delta_color="normal")
            else:
                c3.metric("Estabilidad (CV)", f"{cv:.1f}%", delta="ALTA VOLATILIDAD", delta_color="inverse")
            
            # Análisis de Pareto (80/20) simplificado
            df_pareto = df.groupby('product_type')['Sales'].sum().sort_values(ascending=False).reset_index()
            df_pareto['cum_perc'] = 100 * df_pareto['Sales'].cumsum() / df_pareto['Sales'].sum()
            top_products = df_pareto[df_pareto['cum_perc'] <= 85]['product_type'].tolist()
            c4.metric("Concentración", f"{len(top_products)} Prod. generan 85%", help="Productos clave según Pareto")

            if cv > 35:
                st.warning(f":material/warning: **Alerta de Umbral:** La varianza es muy alta ({cv:.1f}%). Los promedios no son una base segura para presupuestar este segmento.")
            
            st.divider()
            
            # --- SECCIÓN MODIFICADA: BOXPLOT CON COLORES VISIBLES ---
            st.write("#### Comparativa de Dispersión por Ubicación")
            
            # Usamos una paleta cualitativa que evita el negro y colores oscuros
            # 'Safe' o 'Prism' son excelentes para fondos oscuros
            paleta_visible = px.colors.qualitative.Safe

            fig_box = px.box(
                df, 
                x="store_location", 
                y="Sales", 
                color="store_location", 
                points="all",
                title="Distribución de precios y Outliers por país",
                color_discrete_sequence=paleta_visible
            )
            
            # Ajustes estéticos para modo oscuro
            fig_box.update_layout(
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#E0E0E0"),
                xaxis=dict(showgrid=False),
                yaxis=dict(gridcolor="#444")
            )
            
            st.plotly_chart(fig_box, width='stretch')

        with tab2:
            st.subheader("Análisis Diagnóstico y Predictivo")
            col_a, col_b = st.columns([2, 1])
            
            with col_a:
                # Campana de Gauss vs Distribución Real
                x_axis = np.linspace(df['Sales'].min(), df['Sales'].max(), 100)
                y_axis = norm.pdf(x_axis, media, desv_std)
                
                fig_gauss = go.Figure()
                fig_gauss.add_trace(go.Histogram(
                    x=df['Sales'], 
                    nbinsx=20, 
                    name='Frecuencia Real', 
                    histnorm='probability density',
                    marker_color='#636EFA'
                ))
                fig_gauss.add_trace(go.Scatter(
                    x=x_axis, 
                    y=y_axis, 
                    mode='lines', 
                    name='Curva Teórica (Normal)', 
                    line=dict(color='#EF553B', width=3)
                ))
                fig_gauss.update_layout(
                    template="plotly_dark",
                    title="Distribución Real vs. Campana de Gauss", 
                    xaxis_title="Monto de Venta",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_gauss, width='stretch')
            
            with col_b:
                st.info("**Explicabilidad (XAI):** La curva roja muestra el comportamiento ideal. Si tus barras azules están muy a la izquierda, tu volumen depende de ventas pequeñas.")
                # Probabilidad Condicional
                pais_top = df['store_location'].mode()[0]
                prob_cond = (df[df['store_location'] == pais_top]['Sales'] > media).mean() * 100
                st.write(f"**Probabilidad Condicional:**")
                st.write(f"Si la venta ocurre en **{pais_top}**, hay un **{prob_cond:.1f}%** de probabilidad de superar la media.")

        with tab3:
            st.subheader("Visualización de Impacto en Decisiones")
            g_left, g_right = st.columns(2)
            
            with g_left:
                st.write("#### Mapa de Jerarquía (Treemap)")
                fig_tree = px.treemap(
                    df, 
                    path=['store_location', 'product_category', 'product_type'], 
                    values='Sales', 
                    color='Sales', 
                    color_continuous_scale='Viridis',
                    title="Concentración de Ingresos"
                )
                fig_tree.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_tree, width='stretch')
            
            with g_right:
                st.write("#### Elasticidad: Precio vs Cantidad")
                fig_scat = px.scatter(
                    df, 
                    x="unit_price", 
                    y="transaction_qty", 
                    color="product_category",
                    size="Sales", 
                    hover_data=['product_type'], 
                    title="Relación Precio-Volumen",
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig_scat.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_scat, width='stretch')

        with tab4:
            st.dataframe(df, width='stretch')

    else:
        st.warning(":material/warning: No se encontraron datos para esta consulta.")

st.divider()