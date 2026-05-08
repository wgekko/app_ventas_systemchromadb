# Plataforma de Soporte a Decisiones Estratégicas (DSS) con IA

Este proyecto es una herramienta avanzada de **Business Intelligence (BI)** y **Data Science** que utiliza Inteligencia Artificial para transformar el análisis de datos financieros y de ventas. A diferencia de un dashboard tradicional, este sistema utiliza **búsqueda semántica (Vectores)** para permitir consultas en lenguaje natural y genera diagnósticos estadísticos automáticos de alto impacto.

## Características Principales

### Búsqueda Semántica con IA
Implementada con `ChromaDB` y `Sentence-Transformers` (`all-MiniLM-L6-v2`), permitiendo encontrar transacciones por contexto y significado, no solo por coincidencia de palabras clave.

### Inteligencia de Negocio y Estadística
- **Métricas de Calidad de Decisión:** Cálculo del **Coeficiente de Variación (CV)** para identificar la volatilidad y confiabilidad de los promedios.
- **Análisis de Pareto (80/20):** Identificación automática de los productos y regiones que generan el 85% de los ingresos.
- **Diagnóstico de Riesgo:** Detección de **Outliers** (valores atípicos) mediante cálculos de Z-Score.

### Probabilidad y Predicción
- **Campana de Gauss:** Comparativa visual entre la distribución real de ventas y la distribución normal teórica.
- **Probabilidad Condicional:** Estimación de éxito de ventas basada en variables geográficas y de categoría.

### Visualizaciones Avanzadas
- **Treemaps:** Para visualizar la jerarquía y concentración del capital.
- **Box Plots:** Para entender la dispersión y los rangos intercuartílicos por país.
- **Scatter Plots:** Análisis de elasticidad (Precio unitario vs. Cantidad).

## Stack Tecnológico

- **Lenguaje:** Python 3.12+
- **Interfaz:** Streamlit
- **Base de Datos Vectorial:** ChromaDB
- **Procesamiento de Datos:** Pandas, NumPy, SciPy
- **Visualización:** Plotly Express & Graph Objects

para mantener las misma configuración de este repo se debe crear una carpeta
.streamlit 
dentro crear un archivo llamado 
config.toml
-------------------------
[server]
# Importante: Si vas a usar fuentes locales, esto debe estar en true.
# Pero para facilitar todo, usaremos Google Fonts (Inter).
enableStaticServing = true

[[theme.fontFaces]]
family = "Inter"
url = "https://fonts.gstatic.com/s/inter/v13/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuLyfAZ9hiA.woff2"
style = "normal"
weight = "400"

[theme]
base = "dark"
primaryColor = "#FF8C00" # Naranja vibrante para acciones principales (Botones, Sliders)
backgroundColor = "#0B121E" # Azul noche profundo (más elegante que el negro puro)
secondaryBackgroundColor = "#161E2D" # Azul grisáceo para tarjetas y contenedores
textColor = "#E0E0E0" # Blanco suave para no cansar la vista
linkColor = "#FFB347" # Naranja claro para enlaces
borderColor = "#2D3748" # Bordes sutiles para separar secciones
showWidgetBorder = true
baseRadius = "0.75rem" # Esquinas redondeadas modernas
buttonRadius = "0.5rem"
font = "Inter"

# Tipografía para títulos: Mayor peso para jerarquía visual
headingFontWeights = [700, 600, 500, 500, 500, 500]
headingFontSizes = ["2.8rem", "2rem", "1.6rem", "1.4rem", "1.2rem", "1rem"]

# Paleta de colores para los gráficos (Plotly/Streamlit)
# He diseñado un degradado que va del Naranja al Azul Profesional
chartCategoricalColors = [
    "#FF8C00", # Orange (Principal)
    "#3B82F6", # Azul Eléctrico
    "#F59E0B", # Ámbar
    "#10B981", # Esmeralda
    "#8B5CF6", # Violeta
    "#6366F1", # Índigo
    "#EC4899", # Rosado
    "#06B6D4"  # Cian
]

[theme.sidebar]
backgroundColor = "#080D16" # Sidebar un poco más oscuro que el fondo
secondaryBackgroundColor = "#161E2D"
borderColor = "#1E293B"

[theme.dataframe]
# Estilo para las tablas de datos
headerBackgroundColor = "#1E293B"
headerTextColor = "#FFA500"
-------------------------

## Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/wgekko/app_ventas_systemchromadb.git


video demo






