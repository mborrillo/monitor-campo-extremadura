import streamlit as st
from supabase import create_client
import pandas as pd
import plotly.express as px

# 1. Configuración de página
st.set_page_config(page_title="AgroTech Extremadura", layout="wide")

# 2. Credenciales (Verifica que no haya espacios extra en las comillas)
SUPABASE_URL = "https://zzucvsremavkikecsptg.supabase.co"
SUPABASE_KEY = "sb_secret_wfduZo57SIwf3rs1MI13DA_pI5NI6HG"

@st.cache_resource
def get_client():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

client = get_client()

st.title("🚜 Monitor AgroTech Extremadura")

# 3. Función de carga con diagnóstico
def load_data():
    try:
        # Intentamos traer los datos de la vista
        res = client.table("v_comparativa_mercados").select("*").execute()
        if not res.data:
            st.warning("La vista SQL 'v_comparativa_mercados' está vacía.")
            return pd.DataFrame()
        return pd.DataFrame(res.data)
    except Exception as e:
        st.error(f"Error cargando datos: {e}")
        return pd.DataFrame()

df = load_data()

# 4. Mostrar contenido si hay datos
if not df.empty:
    st.success(f"Conexión exitosa. Mostrando {len(df)} productos.")
    
    # Debug: Mostrar nombres de columnas reales por si acaso
    # st.write("Columnas detectadas:", df.columns.tolist())

    # Creamos las columnas para los KPIs
    m1, m2, m3 = st.columns(3)
    m1.metric("Productos", len(df))
    
    # Verificamos si las columnas existen antes de usarlas para evitar el "Oh No"
    col_precio = 'precio_local_kg' if 'precio_local_kg' in df.columns else df.columns[2]
    
    st.divider()
    
    # Tabla simple
    st.subheader("Datos de Mercado")
    st.dataframe(df, use_container_width=True)

    # Gráfico condicional
    if 'diferencial_arbitraje' in df.columns:
        fig = px.bar(df, x='producto', y='diferencial_arbitraje', 
                     title="Diferencial de Mercado",
                     color_discrete_sequence=['#2ecc71'])
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Esperando datos de Supabase... Si este mensaje persiste, revisa que la Vista SQL funcione en el panel de Supabase.")
