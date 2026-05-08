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

## Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone <tu-url-del-repositorio>
   cd <nombre-de-la-carpeta>
