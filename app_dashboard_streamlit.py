import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from supabase import create_client

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="AgroTech Extremadura", page_icon="🟢", layout="wide")

# 2. ESTILO VISUAL: PALETA EXTREMADURA (Verde, Blanco, Negro)
st.markdown("""
    <style>
    /* Fondo principal Negro Carbón */
    .main { background-color: #0b0d0f; color: #ffffff; }
    
    /* Títulos en Verde Extremadura */
    h1, h2, h3, .section-title { 
        color: #009739 !important; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Tarjetas de Métricas */
    div[data-testid="stMetric"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    /* Texto de métricas: Blanco y Verde */
    div[data-testid="stMetricLabel"] p { color: #ffffff !important; font-size: 18px !important; font-weight: bold !important; }
    div[data-testid="stMetricValue"] { color: #009739 !important; font-size: 34px !important; }

    /* Estilo de la tabla para que sea legible */
    .stDataFrame div { font-size: 18px !important; }
    
    /* Ajuste del sidebar */
    .css-1d391kg { background-color: #161b22; }
    </style>
    """, unsafe_allow_html=True)

# 3. CONEXIÓN (Mantenemos tus credenciales)
URL = "https://zzucvsremavkikecsptg.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp6dWN2c3JlbWF2a2lrZWNzcHRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA5ODIzMTUsImV4cCI6MjA4NjU1ODMxNX0.3J-whUICeuP-IgrVJ4J7t7ZpawqVn8arGSboNIZHetw"
supabase = create_client(URL, KEY)

@st.cache_data(ttl=300)
def load_data():
    try:
        # Cargamos los precios agrícolas y mercados internacionales
        res = supabase.table("precios_agricolas").select("*").execute()
        df = pd.DataFrame(res.data)
        # Convertir fecha a datetime para que el gráfico no sea un caos
        df['fecha'] = pd.to_datetime(df['fecha'])
        return df
    except:
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # --- SIDEBAR: FILTRO MEJORADO ---
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/1/13/Escudo_de_Extremadura.svg", width=100)
        st.header("Panel de Control")
        
        # Selector multiselect: por defecto todos
        todos_sectores = df['sector'].unique().tolist()
        sectores_sel = st.multiselect(
            "Filtrar Sectores:", 
            options=todos_sectores, 
            default=todos_sectores,
            help="Escribe para buscar o selecciona de la lista"
        )
        
        df_filtrado = df[df['sector'].isin(sectores_sel)].sort_values(by='fecha', ascending=False)

    # --- HEADER ---
    st.title("🟢 AgroTech Extremadura: Inteligencia de Mercados")
    st.write(f"Última actualización: {df['fecha'].max().strftime('%d/%m/%Y')}")
    st.markdown("---")

    # --- BLOQUE 1: KPIs ---
    c1, c2, c3 = st.columns(3)
    
    # Lógica para sacar precios actuales (ejemplo con Trigo)
    trigo_data = df_filtrado[df_filtrado['mapping_slug'] == 'Trigo']
    if not trigo_data.empty:
        actual = trigo_data.iloc[0]
        with c1:
            st.metric("TRIGO DURO (Local)", f"{actual['precio_min']} €/kg", f"{actual['variacion_p']}%")
        with c2:
            # Aquí podrías cruzar con la tabla de mercados internacionales si la tienes cargada
            st.metric("REFERENCIA CHICAGO", "0.27 $", "-1.2%", delta_color="inverse")
        with c3:
            st.metric("DIFERENCIAL (GAP)", "0.03 €", "Oportunidad")

    # --- BLOQUE 2: GRÁFICO DE TENDENCIA (LIMPIO) ---
    st.subheader("📈 Evolución de Precios y Correlación")
    
    # Agrupamos por fecha para evitar que las líneas se crucen raro
    df_chart = df_filtrado.groupby(['fecha', 'producto'])['precio_min'].mean().reset_index()
    
    fig = go.Figure()
    for prod in df_chart['producto'].unique()[:5]: # Mostramos los top 5 para no saturar
        p_data = df_chart[df_chart['producto'] == prod]
        fig.add_trace(go.Scatter(
            x=p_data['fecha'], 
            y=p_data['precio_min'], 
            name=prod,
            mode='lines+markers',
            line=dict(width=3),
            marker=dict(size=6)
        ))

    fig.update_layout(
        template="plotly_dark",
        hovermode="x unified",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=False),
        yaxis=dict(title="Precio (€/unidad)", gridcolor="#30363d")
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- BLOQUE 3: TABLA DETALLADA (GRANDE Y LEGIBLE) ---
    st.subheader("📋 Datos Históricos Detallados")
    
    # Formateamos la tabla para que sea más bonita
    df_display = df_filtrado[['fecha', 'sector', 'producto', 'variedad', 'precio_min', 'precio_max', 'unidad']].copy()
    df_display['fecha'] = df_display['fecha'].dt.strftime('%d/%m/%Y')
    
    st.dataframe(
        df_display, 
        use_container_width=True, 
        height=500 # Aumentamos la altura para que se vea mucho dato
    )

else:
    st.error("No se han podido cargar los datos de Supabase.")
