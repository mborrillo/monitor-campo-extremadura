import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from supabase import create_client

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="AgroTech Analytics", page_icon="📊", layout="wide")

# 2. ESTILO CSS PARA MÁXIMA LEGIBILIDAD
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    /* Forzar color blanco en textos de métricas y etiquetas */
    div[data-testid="stMetricLabel"] p { font-size: 16px !important; color: #a1a1aa !important; }
    div[data-testid="stMetricValue"] { font-size: 32px !important; color: #00ff9d !important; }
    
    /* Estilo para los títulos de sección */
    .section-title { color: #00ff9d; font-size: 24px; font-weight: bold; margin-top: 20px; margin-bottom: 10px; border-left: 5px solid #00ff9d; padding-left: 15px; }
    
    /* Mejorar la visualización de las tablas */
    .stDataFrame { border: 1px solid #30363d; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. CONEXIÓN A SUPABASE
URL = "https://zzucvsremavkikecsptg.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp6dWN2c3JlbWF2a2lrZWNzcHRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA5ODIzMTUsImV4cCI6MjA4NjU1ODMxNX0.3J-whUICeuP-IgrVJ4J7t7ZpawqVn8arGSboNIZHetw"
supabase = create_client(URL, KEY)

# 4. CARGA DE DATOS (Consumiendo Vistas)
@st.cache_data(ttl=300)
def load_view_data(view_name):
    try:
        # Aquí es donde le decimos que lea la VISTA en lugar de la tabla
        res = supabase.table(view_name).select("*").execute()
        return pd.DataFrame(res.data)
    except Exception as e:
        return pd.DataFrame()

# Intentamos cargar la vista analítica principal
# NOTA: Cambia "v_analitica_precios" por el nombre exacto de tu Vista en Supabase
df = load_view_data("v_mercado_completo") 

if df.empty:
    # Si la vista falla, cargamos la tabla base como respaldo para no romper la app
    df = load_view_data("precios_agricolas")
    st.info("💡 Mostrando tabla base. Para ver analítica avanzada, asegúrate de que la Vista SQL existe.")

try:
    # --- HEADER ESTILO LOVABLE ---
    col_t1, col_t2 = st.columns([3, 1])
    with col_t1:
        st.title("🚜 AgroTech Extremadura")
        st.write("Terminal de Inteligencia de Mercados | Datos en Tiempo Real")
    with col_t2:
        st.metric("ESTADO DEL SISTEMA", "ONLINE", delta="Sincronizado")

    st.markdown("---")

    # --- SIDEBAR FILTROS ---
    with st.sidebar:
        st.header("🔍 Filtros de Análisis")
        if 'sector' in df.columns:
            sectores = st.multiselect("Seleccionar Sectores", df['sector'].unique(), default=df['sector'].unique())
            df_filtrado = df[df['sector'].isin(sectores)]
        else:
            df_filtrado = df
        
        st.markdown("---")
        st.write("**Referencia de Divisa:** 1 EUR = 1.08 USD (Aprox)")

    # --- BLOQUE 1: KPIs DE IMPACTO (Similares a Lovable) ---
    st.markdown('<p class="section-title">📌 Indicadores Clave de Hoy</p>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)

    # Buscamos Trigo y AOVE para los KPIs principales
    def get_val(df, slug, col):
        target = df[df['mapping_slug'] == slug]
        return target.iloc[0][col] if not target.empty else 0

    with c1:
        precio_trigo = get_val(df_filtrado, 'Trigo', 'precio_min')
        var_trigo = get_val(df_filtrado, 'Trigo', 'variacion_p')
        st.metric("TRIGO DURO (Local)", f"{precio_trigo} €/t", f"{var_trigo}%")

    with c2:
        # Supongamos que tu vista tiene 'precio_int' traído de yfinance
        precio_int = get_val(df_filtrado, 'Trigo', 'precio_internacional') if 'precio_internacional' in df.columns else 0
        st.metric("TRIGO (Chicago)", f"{precio_int} $", "CBOT")

    with c3:
        precio_aove = get_val(df_filtrado, 'aceite', 'precio_min')
        st.metric("AOVE (Extremadura)", f"{precio_aove} €/kg", "Lonja")

    with c4:
        st.metric("SITUACIÓN", "OPORTUNIDAD" if precio_trigo < (precio_int*0.9) else "EQUILIBRIO")

    # --- BLOQUE 2: GRÁFICOS ANALÍTICOS ---
    col_g1, col_g2 = st.columns([2, 1])

    with col_g1:
        st.markdown('<p class="section-title">📈 Tendencia Comparativa</p>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_filtrado['fecha'], y=df_filtrado['precio_min'], name="Precio Local", line=dict(color='#00ff9d', width=3)))
        
        if 'precio_internacional' in df_filtrado.columns:
            fig.add_trace(go.Scatter(x=df_filtrado['fecha'], y=df_filtrado['precio_internacional'], name="Mercado Global", line=dict(color='#ff4b4b', dash='dot')))
        
        fig.update_layout(template="plotly_dark", height=400, margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    with col_g2:
        st.markdown('<p class="section-title">📊 Mix de Productos</p>', unsafe_allow_html=True)
        # Un pequeño gráfico de barras con los precios actuales
        top_df = df_filtrado.groupby('producto')['precio_min'].mean().sort_values(ascending=False).head(8)
        st.bar_chart(top_df)

    # --- BLOQUE 3: TABLA DE DATOS CRUDA ---
    st.markdown('<p class="section-title">📋 Detalle Completo de Operaciones</p>', unsafe_allow_html=True)
    st.dataframe(df_filtrado, use_container_width=True)

except Exception as e:
    st.error(f"Hubo un problema al procesar los datos: {e}")
