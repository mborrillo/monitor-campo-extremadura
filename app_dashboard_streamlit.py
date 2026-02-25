import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from supabase import create_client

# 1. CONFIGURACIÓN DE PÁGINA (Lo primero siempre)
st.set_page_config(page_title="AgroTech Analytics", page_icon="📊", layout="wide")

# 2. ESTILO CSS PERSONALIZADO (Para arreglar la legibilidad)
st.markdown("""
    <style>
    /* Fondo y fuente general */
    .main { background-color: #0e1117; color: #ffffff; }
    
    /* Estilo para las tarjetas de métricas */
    div[data-testid="stMetricValue"] { font-size: 28px; font-weight: bold; color: #00ff9d !important; }
    div[data-testid="stMetricDelta"] { font-size: 16px; }
    
    /* Títulos y textos */
    h1, h2, h3 { color: #00ff9d !important; font-family: 'Inter', sans-serif; }
    .stText { font-size: 18px !important; color: #e0e0e0; }
    
    /* Contenedores blancos para tablas para que se lean bien */
    .stDataFrame { background-color: #ffffff; border-radius: 10px; padding: 5px; }
    </style>
    """, unsafe_allow_html=True)

# 3. CONEXIÓN (Asegúrate de tener tus keys aquí)
URL = "https://zzucvsremavkikecsptg.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp6dWN2c3JlbWF2a2lrZWNzcHRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA5ODIzMTUsImV4cCI6MjA4NjU1ODMxNX0.3J-whUICeuP-IgrVJ4J7t7ZpawqVn8arGSboNIZHetw" # Usa la 'anon public' que encontramos antes
client = create_client(URL, KEY)

# 4. LÓGICA DE DATOS
@st.cache_data(ttl=600)
def load_data():
    # Traemos la vista comparativa que cruza Lonja e Internacional
    res = client.table("v_comparativa_mercados").select("*").execute()
    df = pd.DataFrame(res.data)
    return df

try:
    df = load_data()
    
    # --- HEADER ---
    st.title("🚜 AgroTech: Terminal Analítica de Extremadura")
    st.markdown("---")

    # --- FILTROS EN SIDEBAR ---
    st.sidebar.header("Configuración de Análisis")
    sector = st.sidebar.multiselect("Sector", df['sector'].unique(), default=df['sector'].unique())
    df_filtrado = df[df['sector'].isin(sector)]

    # --- BLOQUE 1: MÉTRICAS CLAVE (KPIs) ---
    st.subheader("📌 Indicadores de Referencia")
    col1, col2, col3, col4 = st.columns(4)
    
    # Ejemplo con un producto específico (Trigo)
    trigo = df_filtrado[df_filtrado['mapping_slug'] == 'Trigo'].iloc[0] if not df_filtrado[df_filtrado['mapping_slug'] == 'Trigo'].empty else None
    
    if trigo is not None:
        with col1:
            st.metric("TRIGO (Lonja)", f"{trigo['precio_med_lonja']} €", f"{trigo['variacion_lonja']}%")
        with col2:
            st.metric("TRIGO (Chicago)", f"{trigo['precio_internacional']} $", f"{trigo['variacion_int']}%")
        with col3:
            # Cálculo de brecha (Gap)
            gap = round(trigo['precio_med_lonja'] - (trigo['precio_internacional'] * 0.92), 3) # Conversión aprox a €
            st.metric("DIFERENCIAL (Gap)", f"{gap} €", "Arbitraje")
        with col4:
            st.metric("ESTADO DEL MERCADO", "🔴 Bajista" if trigo['variacion_int'] < 0 else "🟢 Alcista")

    st.markdown("---")

    # --- BLOQUE 2: GRÁFICO COMPARATIVO ---
    st.subheader("📈 Correlación: Lonja de Extremadura vs. Internacional")
    
    fig = go.Figure()
    # Precio Local
    fig.add_trace(go.Scatter(x=df_filtrado['fecha'], y=df_filtrado['precio_med_lonja'], name="Precio Extremadura (€)", line=dict(color='#00ff9d', width=4)))
    # Precio Internacional (Normalizado o en eje secundario)
    fig.add_trace(go.Scatter(x=df_filtrado['fecha'], y=df_filtrado['precio_internacional'], name="Precio Global ($)", line=dict(color='#ff4b4b', dash='dot')))
    
    fig.update_layout(template="plotly_dark", hovermode="x unified", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

    # --- BLOQUE 3: TABLA DETALLADA ---
    st.subheader("📋 Desglose de Operaciones")
    st.dataframe(df_filtrado[['fecha', 'producto', 'precio_med_lonja', 'precio_internacional', 'variacion_lonja', 'sector']], use_container_width=True)

except Exception as e:
    st.error(f"Esperando datos de Supabase... {e}")
