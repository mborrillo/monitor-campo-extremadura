import streamlit as st
from supabase import create_client
import pandas as pd
import plotly.express as px

# 1. Configuración Visual Estilo "Lovable" (Limpio y profesional)
st.set_page_config(
    page_title="AgroTech Extremadura",
    page_icon="🚜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilo CSS para tarjetas blancas y fuentes claras
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #1a1a1a; }
    .stDataFrame { border: 1px solid #f0f0f0; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. Credenciales Directas (Para pruebas de conexión)
SUPABASE_URL = "https://zzucvsremavkikecsptg.supabase.co"
SUPABASE_KEY = "sb_secret_wfduZo57SIwf3rs1MI13DA_pI5NI6HG"

@st.cache_resource
def get_supabase_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = get_supabase_client()

# 3. Función para cargar datos de la Vista SQL
def load_market_data():
    try:
        # Consultamos tu vista inteligente
        response = supabase.table("v_comparativa_mercados").select("*").execute()
        return pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"Error de conexión con Supabase: {e}")
        return pd.DataFrame()

# --- INTERFAZ DEL DASHBOARD ---

st.title("🚜 AgroTech Extremadura")
st.markdown("### Inteligencia de Mercados y Arbitraje")
st.write("Datos actualizados desde Lonja de Extremadura y Mercados Internacionales (Chicago/NY).")

# Carga de datos
df = load_market_data()

if not df.empty:
    # 4. KPIs Principales (Tarjetas de métricas)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Mercados Analizados", len(df))
    with col2:
        # Buscamos el mejor diferencial positivo
        mejor_op = df.sort_values(by='diferencial_arbitraje', ascending=False).iloc[0]
        st.metric("Mejor Oportunidad", mejor_op['producto'], f"{mejor_op['diferencial_arbitraje']} €/kg")
    with col3:
        st.metric("Estado Clima", "Estable", "AEMET")
    with col4:
        st.metric("Energía (Media)", "0.12 €/kWh", "Estable")

    st.divider()

    # 5. Tabla de Inteligencia de Mercados
    st.subheader("📊 Monitor de Arbitraje Local vs Internacional")
    
    # Renombramos columnas para que se vean bonitas en la web
    df_show = df.rename(columns={
        'producto': 'Producto',
        'precio_local_kg': 'Precio Extremadura (€/kg)',
        'precio_internacional_kg': 'Ref. Internacional (€/kg)',
        'diferencial_arbitraje': 'Diferencial (€/kg)',
        'relacion': 'Vínculo'
    })
    
    st.dataframe(df_show, use_container_width=True, hide_index=True)

    # 6. Gráfico Visual de Diferenciales
    st.subheader("📈 Análisis de Brecha de Precios")
    fig = px.bar(df, 
                 x='producto', 
                 y='diferencial_arbitraje',
                 labels={'diferencial_arbitraje': 'Diferencial (€/kg)', 'producto': 'Producto'},
                 color='diferencial_arbitraje',
                 color_continuous_scale='RdYlGn', # Verde para positivo, rojo para negativo
                 template='plotly_white')
    
    st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("No se pudieron cargar datos. Verifica que la vista 'v_comparativa_mercados' tenga datos en Supabase.")

st.sidebar.info("Dashboard v1.0 - Conexión Directa")
