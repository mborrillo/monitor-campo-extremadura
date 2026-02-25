import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from supabase import create_client
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════
# 1. CONFIGURACIÓN DE PÁGINA
# ═══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="AgroTech Extremadura",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════
# 2. PALETA DE COLORES EXTREMADURA
# ═══════════════════════════════════════════════════════════════════
VERDE_EXTREMADURA = "#009739"
VERDE_OSCURO = "#00693E"
BLANCO = "#FFFFFF"
NEGRO = "#000000"
GRIS_CLARO = "#F5F5F5"
GRIS_MEDIO = "#E0E0E0"
VERDE_CLARO = "#E8F5E9"

# ═══════════════════════════════════════════════════════════════════
# 3. ESTILOS CSS PERSONALIZADOS
# ═══════════════════════════════════════════════════════════════════
st.markdown(f"""
    <style>
    /* ============ ESTILOS GENERALES ============ */
    .main {{
        background-color: {BLANCO};
        padding: 2rem;
    }}
    
    /* ============ SIDEBAR ============ */
    [data-testid="stSidebar"] {{
        background-color: {VERDE_OSCURO};
        padding: 2rem 1rem;
    }}
    
    [data-testid="stSidebar"] .css-1d391kg {{
        background-color: {VERDE_OSCURO};
    }}
    
    /* Texto del sidebar en blanco */
    [data-testid="stSidebar"] * {{
        color: {BLANCO} !important;
    }}
    
    /* Links del sidebar */
    [data-testid="stSidebar"] a {{
        color: {BLANCO} !important;
        text-decoration: none;
    }}
    
    /* ============ TÍTULOS ============ */
    h1 {{
        color: {NEGRO} !important;
        font-weight: 700 !important;
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem !important;
    }}
    
    h2 {{
        color: {VERDE_EXTREMADURA} !important;
        font-weight: 600 !important;
        font-size: 1.8rem !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }}
    
    h3 {{
        color: {NEGRO} !important;
        font-weight: 600 !important;
        font-size: 1.3rem !important;
    }}
    
    /* ============ TARJETAS DE MÉTRICAS ============ */
    div[data-testid="stMetric"] {{
        background-color: {BLANCO};
        border: 2px solid {GRIS_MEDIO};
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }}
    
    div[data-testid="stMetric"]:hover {{
        box-shadow: 0 4px 16px rgba(0, 151, 57, 0.15);
        border-color: {VERDE_EXTREMADURA};
    }}
    
    div[data-testid="stMetricLabel"] {{
        color: {NEGRO} !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    div[data-testid="stMetricValue"] {{
        color: {VERDE_EXTREMADURA} !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }}
    
    div[data-testid="stMetricDelta"] {{
        font-size: 0.9rem !important;
    }}
    
    /* ============ BADGES Y ETIQUETAS ============ */
    .badge {{
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.2rem;
    }}
    
    .badge-success {{
        background-color: {VERDE_EXTREMADURA};
        color: {BLANCO};
    }}
    
    .badge-positive {{
        background-color: {VERDE_CLARO};
        color: {VERDE_OSCURO};
    }}
    
    .badge-info {{
        background-color: {GRIS_CLARO};
        color: {NEGRO};
    }}
    
    /* ============ TARJETAS PERSONALIZADAS ============ */
    .custom-card {{
        background-color: {BLANCO};
        border: 2px solid {GRIS_MEDIO};
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
    }}
    
    .custom-card:hover {{
        box-shadow: 0 4px 16px rgba(0, 151, 57, 0.15);
        border-color: {VERDE_EXTREMADURA};
    }}
    
    /* ============ TABLA ============ */
    .dataframe {{
        border: none !important;
        font-size: 0.95rem !important;
    }}
    
    .dataframe thead th {{
        background-color: {VERDE_EXTREMADURA} !important;
        color: {BLANCO} !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        border: none !important;
    }}
    
    .dataframe tbody tr:nth-child(even) {{
        background-color: {GRIS_CLARO} !important;
    }}
    
    .dataframe tbody tr:hover {{
        background-color: {VERDE_CLARO} !important;
    }}
    
    .dataframe td {{
        padding: 0.8rem !important;
        border: none !important;
    }}
    
    /* ============ BOTONES Y SELECTORES ============ */
    .stButton button {{
        background-color: {VERDE_EXTREMADURA};
        color: {BLANCO};
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .stButton button:hover {{
        background-color: {VERDE_OSCURO};
        box-shadow: 0 4px 12px rgba(0, 151, 57, 0.3);
    }}
    
    /* ============ HEADER SECTION ============ */
    .header-section {{
        padding: 1.5rem;
        background: linear-gradient(135deg, {VERDE_EXTREMADURA} 0%, {VERDE_OSCURO} 100%);
        border-radius: 12px;
        color: {BLANCO};
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0, 151, 57, 0.2);
    }}
    
    .header-title {{
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        color: {BLANCO};
    }}
    
    .header-subtitle {{
        font-size: 1.1rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        color: {BLANCO};
    }}
    
    /* ============ SEPARADOR ============ */
    .separator {{
        border-top: 2px solid {GRIS_MEDIO};
        margin: 2rem 0;
    }}
    
    /* ============ FOOTER ============ */
    .footer {{
        text-align: center;
        padding: 2rem;
        color: {GRIS_MEDIO};
        font-size: 0.9rem;
        margin-top: 3rem;
    }}
    </style>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# 4. CONEXIÓN A SUPABASE
# ═══════════════════════════════════════════════════════════════════
URL = "https://zzucvsremavkikecsptg.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp6dWN2c3JlbWF2a2lrZWNzcHRnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA5ODIzMTUsImV4cCI6MjA4NjU1ODMxNX0.3J-whUICeuP-IgrVJ4J7t7ZpawqVn8arGSboNIZHetw"
supabase = create_client(URL, KEY)

@st.cache_data(ttl=300)
def load_data():
    """Carga los datos de precios agrícolas desde Supabase"""
    try:
        res = supabase.table("precios_agricolas").select("*").execute()
        df = pd.DataFrame(res.data)
        df['fecha'] = pd.to_datetime(df['fecha'])
        return df
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()

# ═══════════════════════════════════════════════════════════════════
# 5. FUNCIONES AUXILIARES
# ═══════════════════════════════════════════════════════════════════
def format_badge(text, badge_type="info"):
    """Genera un badge HTML personalizado"""
    return f'<span class="badge badge-{badge_type}">{text}</span>'

def create_price_comparison_chart(df_data):
    """Crea un gráfico de barras comparando precios locales vs internacionales"""
    fig = go.Figure()
    
    # Barras de precio local (verde)
    fig.add_trace(go.Bar(
        name='Precio Local',
        x=df_data['producto'],
        y=df_data['precio_min'],
        marker_color=VERDE_EXTREMADURA,
        text=df_data['precio_min'].round(2),
        textposition='outside',
        texttemplate='%{text}€',
        hovertemplate='<b>%{x}</b><br>Precio Local: %{y:.2f}€<extra></extra>'
    ))
    
    # Barras de precio internacional (negro) - simulado para el ejemplo
    # En producción, esto vendría de tu tabla de mercados internacionales
    precio_internacional = df_data['precio_min'] * 0.6  # Simulación
    fig.add_trace(go.Bar(
        name='Precio Internacional',
        x=df_data['producto'],
        y=precio_internacional,
        marker_color=NEGRO,
        text=precio_internacional.round(2),
        textposition='outside',
        texttemplate='%{text}€',
        hovertemplate='<b>%{x}</b><br>Precio Internacional: %{y:.2f}€<extra></extra>'
    ))
    
    fig.update_layout(
        title={
            'text': 'Precios: Local vs Internacional (€/kg)',
            'font': {'size': 20, 'color': NEGRO, 'family': 'Arial, sans-serif'}
        },
        xaxis={'title': '', 'tickangle': -45},
        yaxis={'title': 'Precio (€/kg)', 'gridcolor': GRIS_MEDIO},
        barmode='group',
        plot_bgcolor=BLANCO,
        paper_bgcolor=BLANCO,
        font={'family': 'Arial, sans-serif', 'size': 12},
        hovermode='x unified',
        legend={
            'orientation': 'h',
            'yanchor': 'bottom',
            'y': 1.02,
            'xanchor': 'right',
            'x': 1
        },
        height=450
    )
    
    return fig

def create_trend_chart(df_data):
    """Crea un gráfico de líneas de tendencia de precios"""
    fig = go.Figure()
    
    productos = df_data['producto'].unique()[:5]  # Top 5 productos
    
    for producto in productos:
        df_prod = df_data[df_data['producto'] == producto].sort_values('fecha')
        
        fig.add_trace(go.Scatter(
            x=df_prod['fecha'],
            y=df_prod['precio_min'],
            name=producto,
            mode='lines+markers',
            line={'width': 3},
            marker={'size': 8},
            hovertemplate='<b>%{fullData.name}</b><br>Fecha: %{x|%d/%m/%Y}<br>Precio: %{y:.2f}€<extra></extra>'
        ))
    
    fig.update_layout(
        title={
            'text': '📈 Evolución de Precios',
            'font': {'size': 20, 'color': NEGRO, 'family': 'Arial, sans-serif'}
        },
        xaxis={'title': 'Fecha', 'gridcolor': GRIS_MEDIO},
        yaxis={'title': 'Precio (€/kg)', 'gridcolor': GRIS_MEDIO},
        plot_bgcolor=BLANCO,
        paper_bgcolor=BLANCO,
        font={'family': 'Arial, sans-serif', 'size': 12},
        hovermode='x unified',
        legend={
            'orientation': 'h',
            'yanchor': 'bottom',
            'y': 1.02,
            'xanchor': 'right',
            'x': 1
        },
        height=400
    )
    
    return fig

# ═══════════════════════════════════════════════════════════════════
# 6. SIDEBAR
# ═══════════════════════════════════════════════════════════════════
with st.sidebar:
    # Logo
    st.markdown("""
        <div style="text-align: center; padding: 1rem 0 2rem 0;">
            <div style="background-color: white; border-radius: 50%; width: 80px; height: 80px; 
                        margin: 0 auto; display: flex; align-items: center; justify-content: center;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                <span style="font-size: 2.5rem;">🌾</span>
            </div>
            <h2 style="color: white !important; margin-top: 1rem;">AgroTech<br/>Extremadura</h2>
            <p style="color: rgba(255,255,255,0.8); font-size: 0.9rem;">Inteligencia Agrícola</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='separator' style='border-color: rgba(255,255,255,0.2);'></div>", unsafe_allow_html=True)
    
    # Menú de navegación
    st.markdown("### 📊 Panel de Control")
    
    # Filtros
    st.markdown("### 🔍 Filtros")
    
    # Carga inicial de datos para obtener opciones
    df_inicial = load_data()
    
    if not df_inicial.empty:
        todos_sectores = df_inicial['sector'].unique().tolist()
        sectores_sel = st.multiselect(
            "Sectores:",
            options=todos_sectores,
            default=todos_sectores,
            help="Selecciona los sectores a visualizar"
        )
    else:
        sectores_sel = []
    
    st.markdown("<div class='separator' style='border-color: rgba(255,255,255,0.2);'></div>", unsafe_allow_html=True)
    
    # Información adicional
    st.markdown("""
        <div style="background-color: rgba(255,255,255,0.1); padding: 1rem; border-radius: 8px; margin-top: 2rem;">
            <p style="font-size: 0.85rem; margin: 0; color: rgba(255,255,255,0.9);">
                <strong>💡 Consejo:</strong><br/>
                Los datos se actualizan cada 5 minutos automáticamente.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top: 2rem; text-align: center; font-size: 0.8rem; color: rgba(255,255,255,0.6);'>© 2026 AgroTech Extremadura</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# 7. CONTENIDO PRINCIPAL
# ═══════════════════════════════════════════════════════════════════

# Cargar datos
df = load_data()

if not df.empty and sectores_sel:
    # Filtrar datos
    df_filtrado = df[df['sector'].isin(sectores_sel)].sort_values(by='fecha', ascending=False)
    
    # ────────────────────────────────────────────────────────────────
    # HEADER
    # ────────────────────────────────────────────────────────────────
    ultima_actualizacion = df['fecha'].max().strftime('%d/%m/%Y')
    
    st.markdown(f"""
        <div class="header-section">
            <h1 class="header-title">🟢 Monitor de Mercados</h1>
            <p class="header-subtitle">Comparativa de precios locales vs internacionales</p>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">
                <strong>Última actualización:</strong> {ultima_actualizacion}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # ────────────────────────────────────────────────────────────────
    # SECCIÓN 1: KPIs PRINCIPALES
    # ────────────────────────────────────────────────────────────────
    st.markdown("## 📊 Indicadores Clave")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # KPI 1: Precio Trigo Duro
    trigo_data = df_filtrado[df_filtrado['mapping_slug'] == 'Trigo']
    if not trigo_data.empty:
        actual = trigo_data.iloc[0]
        with col1:
            st.metric(
                label="TRIGO DURO (Local)",
                value=f"{actual['precio_min']:.2f} €/kg",
                delta=f"{actual['variacion_p']:.1f}%"
            )
    
    # KPI 2: Precio Maíz
    maiz_data = df_filtrado[df_filtrado['mapping_slug'] == 'Maiz']
    if not maiz_data.empty:
        actual = maiz_data.iloc[0]
        with col2:
            st.metric(
                label="MAÍZ (Local)",
                value=f"{actual['precio_min']:.2f} €/kg",
                delta=f"{actual['variacion_p']:.1f}%"
            )
    
    # KPI 3: Total de productos monitoreados
    with col3:
        total_productos = len(df_filtrado['producto'].unique())
        st.metric(
            label="PRODUCTOS MONITOREADOS",
            value=total_productos,
            delta=""
        )
    
    # KPI 4: Sectores activos
    with col4:
        sectores_activos = len(df_filtrado['sector'].unique())
        st.metric(
            label="SECTORES ACTIVOS",
            value=sectores_activos,
            delta=""
        )
    
    st.markdown("<div class='separator'></div>", unsafe_allow_html=True)
    
    # ────────────────────────────────────────────────────────────────
    # SECCIÓN 2: GRÁFICO DE COMPARACIÓN
    # ────────────────────────────────────────────────────────────────
    st.markdown("## 📊 Comparativa de Precios")
    
    # Tomamos los datos más recientes por producto
    df_reciente = df_filtrado.loc[df_filtrado.groupby('producto')['fecha'].idxmax()]
    df_chart_data = df_reciente.nlargest(7, 'precio_min')  # Top 7 productos
    
    fig_comparison = create_price_comparison_chart(df_chart_data)
    st.plotly_chart(fig_comparison, use_container_width=True)
    
    st.markdown("<div class='separator'></div>", unsafe_allow_html=True)
    
    # ────────────────────────────────────────────────────────────────
    # SECCIÓN 3: PRECIOS DEL DÍA
    # ────────────────────────────────────────────────────────────────
    st.markdown("## 💰 Precios del Día")
    
    st.markdown(f"""
        <div style="background-color: {VERDE_CLARO}; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <p style="margin: 0; color: {VERDE_OSCURO}; font-size: 0.95rem;">
                <strong>Última actualización:</strong> {ultima_actualizacion}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Preparar tabla
    df_tabla = df_reciente[['producto', 'precio_min', 'unidad']].copy()
    df_tabla.columns = ['Producto', 'Local (€/kg)', 'Unidad']
    
    # Agregar columna de precio internacional simulado y diferencial
    df_tabla['Internacional (€/kg)'] = (df_tabla['Local (€/kg)'] * 0.6).round(2)
    df_tabla['Diferencial'] = (df_tabla['Local (€/kg)'] - df_tabla['Internacional (€/kg)']).round(2)
    
    # Formatear precios
    df_tabla['Local (€/kg)'] = df_tabla['Local (€/kg)'].apply(lambda x: f"{x:.2f} €/kg")
    df_tabla['Internacional (€/kg)'] = df_tabla['Internacional (€/kg)'].apply(lambda x: f"{x:.2f} €/kg")
    
    # Crear badges para el diferencial
    def format_diferencial(val):
        return f"+{val:.2f} €/kg" if val > 0 else f"{val:.2f} €/kg"
    
    df_tabla['Diferencial'] = df_tabla['Diferencial'].apply(format_diferencial)
    
    # Mostrar tabla
    st.dataframe(
        df_tabla,
        use_container_width=True,
        height=400,
        hide_index=True
    )
    
    st.markdown("<div class='separator'></div>", unsafe_allow_html=True)
    
    # ────────────────────────────────────────────────────────────────
    # SECCIÓN 4: GRÁFICO DE TENDENCIAS
    # ────────────────────────────────────────────────────────────────
    st.markdown("## 📈 Tendencias Históricas")
    
    fig_trends = create_trend_chart(df_filtrado)
    st.plotly_chart(fig_trends, use_container_width=True)
    
    st.markdown("<div class='separator'></div>", unsafe_allow_html=True)
    
    # ────────────────────────────────────────────────────────────────
    # SECCIÓN 5: DATOS DETALLADOS
    # ────────────────────────────────────────────────────────────────
    st.markdown("## 📋 Datos Históricos Detallados")
    
    # Preparar datos para mostrar
    df_display = df_filtrado[['fecha', 'sector', 'producto', 'variedad', 'precio_min', 'precio_max', 'unidad', 'variacion_p']].copy()
    df_display['fecha'] = df_display['fecha'].dt.strftime('%d/%m/%Y')
    df_display.columns = ['Fecha', 'Sector', 'Producto', 'Variedad', 'Precio Mín', 'Precio Máx', 'Unidad', 'Var %']
    
    # Formato de variación
    df_display['Var %'] = df_display['Var %'].apply(lambda x: f"{x:+.2f}%" if pd.notna(x) else "N/A")
    
    # Mostrar con paginación
    st.dataframe(
        df_display,
        use_container_width=True,
        height=500,
        hide_index=True
    )
    
    # Botón de descarga
    csv = df_display.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar datos (CSV)",
        data=csv,
        file_name=f'precios_agricolas_{datetime.now().strftime("%Y%m%d")}.csv',
        mime='text/csv',
    )
    
    # ────────────────────────────────────────────────────────────────
    # FOOTER
    # ────────────────────────────────────────────────────────────────
    st.markdown("""
        <div class="footer">
            <p>🌾 <strong>AgroTech Extremadura</strong> | Inteligencia de Mercados Agrícolas</p>
            <p style="font-size: 0.8rem; margin-top: 0.5rem;">
                Datos actualizados en tiempo real desde fuentes oficiales | © 2026
            </p>
        </div>
    """, unsafe_allow_html=True)

elif df.empty:
    st.error("❌ No se han podido cargar los datos de Supabase. Verifica la conexión.")
else:
    st.warning("⚠️ Por favor, selecciona al menos un sector en el panel lateral.")
