"""
AgroTech Extremadura — Dashboard Principal
Streamlit app con diseño moderno inspirado en la versión Lovable.
Conexión a Supabase para datos de sensores IoT.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import math

# Supabase — importación opcional (no bloquea si no está instalado)
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

# ─────────────────────────────────────────────
# CONFIGURACIÓN PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AgroTech Extremadura",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CSS GLOBAL — TEMA AGRO PREMIUM
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');

/* ── Variables ── */
:root {
    --green-900: #0d2b1a;
    --green-800: #14432a;
    --green-700: #1a5c38;
    --green-600: #1f7a48;
    --green-500: #27a05e;
    --green-400: #3dbd76;
    --green-300: #5fd494;
    --green-100: #d6f5e5;
    --earth-700: #5c3d1e;
    --earth-500: #8b5e34;
    --earth-300: #c49a6c;
    --amber-500: #f59e0b;
    --amber-100: #fef3c7;
    --red-500: #ef4444;
    --red-100: #fee2e2;
    --blue-500: #3b82f6;
    --blue-100: #dbeafe;
    --bg-dark: #0a1a10;
    --bg-card: #ffffff;
    --text-primary: #0d2b1a;
    --text-secondary: #4a7c5f;
    --text-muted: #7aa98e;
    --border: #d1ead9;
    --shadow: 0 4px 24px rgba(13,43,26,0.08);
    --shadow-lg: 0 8px 40px rgba(13,43,26,0.14);
    --radius: 16px;
    --radius-sm: 10px;
}

/* ── Reset base ── */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* ── Fondo principal ── */
.stApp {
    background: linear-gradient(135deg, #f0faf4 0%, #e8f5ee 50%, #f5f9f2 100%);
    background-attachment: fixed;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--green-900) 0%, var(--green-800) 60%, #0a2010 100%) !important;
    border-right: none !important;
    box-shadow: 4px 0 30px rgba(0,0,0,0.3) !important;
}

section[data-testid="stSidebar"] * {
    color: #d6f5e5 !important;
}

section[data-testid="stSidebar"] .stRadio label {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: var(--radius-sm) !important;
    padding: 10px 16px !important;
    margin: 3px 0 !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    display: flex !important;
    align-items: center !important;
}

section[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(63,189,118,0.15) !important;
    border-color: var(--green-400) !important;
}

section[data-testid="stSidebar"] .stRadio [data-checked="true"] + label,
section[data-testid="stSidebar"] .stRadio input:checked + div {
    background: rgba(39,160,94,0.25) !important;
    border-color: var(--green-400) !important;
}

/* ── Ocultar elementos Streamlit genéricos ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 1.5rem 2rem !important;
    max-width: 1400px !important;
}

/* ── Cards ── */
.card {
    background: var(--bg-card);
    border-radius: var(--radius);
    padding: 24px;
    box-shadow: var(--shadow);
    border: 1px solid var(--border);
    transition: all 0.3s ease;
    height: 100%;
}
.card:hover { box-shadow: var(--shadow-lg); transform: translateY(-2px); }

/* ── KPI Cards ── */
.kpi-card {
    background: white;
    border-radius: var(--radius);
    padding: 22px 24px;
    box-shadow: var(--shadow);
    border: 1px solid var(--border);
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}
.kpi-card:hover { box-shadow: var(--shadow-lg); transform: translateY(-3px); }
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    border-radius: var(--radius) var(--radius) 0 0;
}
.kpi-green::before { background: linear-gradient(90deg, var(--green-500), var(--green-300)); }
.kpi-amber::before { background: linear-gradient(90deg, var(--amber-500), #fbbf24); }
.kpi-red::before   { background: linear-gradient(90deg, var(--red-500), #f87171); }
.kpi-blue::before  { background: linear-gradient(90deg, var(--blue-500), #60a5fa); }

.kpi-icon {
    font-size: 2rem;
    margin-bottom: 8px;
    display: block;
}
.kpi-value {
    font-size: 2.2rem;
    font-weight: 800;
    color: var(--text-primary);
    line-height: 1;
    margin: 4px 0;
}
.kpi-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.kpi-trend {
    font-size: 0.82rem;
    font-weight: 600;
    margin-top: 8px;
    padding: 3px 8px;
    border-radius: 20px;
    display: inline-block;
}
.trend-up   { background: var(--green-100); color: var(--green-700); }
.trend-down { background: var(--red-100);   color: var(--red-500); }
.trend-warn { background: var(--amber-100); color: #b45309; }

/* ── Section header ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
    padding-bottom: 14px;
    border-bottom: 2px solid var(--border);
}
.section-icon {
    width: 40px; height: 40px;
    background: linear-gradient(135deg, var(--green-500), var(--green-400));
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    box-shadow: 0 4px 12px rgba(39,160,94,0.3);
}
.section-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0;
}
.section-sub {
    font-size: 0.8rem;
    color: var(--text-muted);
    margin: 0;
}

/* ── Alert cards ── */
.alert-item {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 14px 16px;
    border-radius: var(--radius-sm);
    margin-bottom: 10px;
    border-left: 4px solid;
    transition: all 0.2s;
}
.alert-item:hover { transform: translateX(4px); }
.alert-critical { background: #fff5f5; border-color: var(--red-500); }
.alert-warning  { background: #fffbeb; border-color: var(--amber-500); }
.alert-info     { background: #eff6ff; border-color: var(--blue-500); }
.alert-ok       { background: #f0fdf4; border-color: var(--green-500); }

.alert-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    margin-top: 5px;
    flex-shrink: 0;
    animation: pulse 2s infinite;
}
.dot-red    { background: var(--red-500); }
.dot-amber  { background: var(--amber-500); animation: none; }
.dot-blue   { background: var(--blue-500); animation: none; }
.dot-green  { background: var(--green-500); animation: none; }

@keyframes pulse {
    0%,100% { box-shadow: 0 0 0 0 rgba(239,68,68,0.4); }
    50%      { box-shadow: 0 0 0 6px rgba(239,68,68,0); }
}

.alert-title   { font-weight: 700; font-size: 0.88rem; color: var(--text-primary); }
.alert-desc    { font-size: 0.8rem;  color: var(--text-secondary); margin-top: 2px; }
.alert-time    { font-size: 0.72rem; color: var(--text-muted); margin-top: 4px; font-family: 'DM Mono', monospace; }

/* ── Badge / pill ── */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.badge-green  { background: var(--green-100);  color: var(--green-700); }
.badge-amber  { background: var(--amber-100);  color: #b45309; }
.badge-red    { background: var(--red-100);    color: #b91c1c; }
.badge-blue   { background: var(--blue-100);   color: #1d4ed8; }
.badge-earth  { background: #fdf4e7; color: var(--earth-700); }

/* ── Sensor table ── */
.sensor-row {
    display: flex;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid var(--border);
    gap: 12px;
}
.sensor-row:last-child { border-bottom: none; }

/* ── Login ── */
.login-wrap {
    max-width: 440px;
    margin: 60px auto;
    background: white;
    border-radius: 24px;
    padding: 48px 40px;
    box-shadow: var(--shadow-lg);
    border: 1px solid var(--border);
    text-align: center;
}
.login-logo   { font-size: 3rem; margin-bottom: 12px; }
.login-title  { font-size: 1.6rem; font-weight: 800; color: var(--text-primary); }
.login-sub    { color: var(--text-muted); font-size: 0.9rem; margin: 8px 0 32px; }

/* ── Streamlit input overrides ── */
.stTextInput input, .stSelectbox select {
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.stTextInput input:focus {
    border-color: var(--green-500) !important;
    box-shadow: 0 0 0 3px rgba(39,160,94,0.15) !important;
}
.stButton button {
    background: linear-gradient(135deg, var(--green-600), var(--green-500)) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 14px rgba(39,160,94,0.35) !important;
}
.stButton button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(39,160,94,0.45) !important;
}

/* ── Parcela mapa card ── */
.parcela-card {
    background: white;
    border-radius: var(--radius-sm);
    padding: 16px;
    border: 1px solid var(--border);
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.2s;
    cursor: pointer;
}
.parcela-card:hover {
    border-color: var(--green-400);
    box-shadow: 0 4px 16px rgba(39,160,94,0.12);
}

/* ── Metric gauge text ── */
.gauge-label {
    text-align: center;
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-top: -10px;
}

/* ── Page title ── */
.page-hero {
    background: linear-gradient(135deg, var(--green-900) 0%, var(--green-700) 100%);
    border-radius: var(--radius);
    padding: 28px 32px;
    margin-bottom: 28px;
    color: white;
    position: relative;
    overflow: hidden;
}
.page-hero::after {
    content: '🌿';
    position: absolute;
    right: 30px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 5rem;
    opacity: 0.15;
}
.page-hero h1 { color: white !important; font-size: 1.7rem; font-weight: 800; margin: 0 0 4px; }
.page-hero p  { color: rgba(255,255,255,0.7); margin: 0; font-size: 0.9rem; }
.page-hero .hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.75rem;
    font-weight: 600;
    color: white;
    margin-bottom: 10px;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: var(--border);
    margin: 20px 0;
}

/* ── Number mono ── */
.mono { font-family: 'DM Mono', monospace; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATOS SIMULADOS (reemplazar con Supabase)
# ─────────────────────────────────────────────
@st.cache_data(ttl=60)
def get_sensor_data():
    """Genera datos de sensores IoT simulados. Reemplazar con consulta a Supabase."""
    random.seed(42)
    now = datetime.now()
    parcelas = ["Parcela Norte", "Parcela Sur", "Parcela Este", "Parcela Oeste", "Invernadero A", "Invernadero B"]
    cultivos = ["Tomate", "Pimiento", "Maíz", "Trigo", "Olivo", "Vid"]
    
    sensores = []
    for i, (p, c) in enumerate(zip(parcelas, cultivos)):
        base_temp = 18 + i * 2
        sensores.append({
            "id": f"SNS-{i+1:03d}",
            "parcela": p,
            "cultivo": c,
            "temperatura": round(base_temp + random.uniform(-3, 5), 1),
            "humedad": round(55 + random.uniform(-20, 30), 1),
            "ph": round(6.5 + random.uniform(-1, 1), 2),
            "nitrogeno": round(80 + random.uniform(-20, 40), 1),
            "luz_solar": round(600 + random.uniform(-200, 300), 0),
            "estado": random.choice(["Óptimo", "Óptimo", "Óptimo", "Atención", "Alerta"]),
            "ultima_lectura": (now - timedelta(minutes=random.randint(1, 30))).strftime("%H:%M"),
            "lat": 39.15 + i * 0.02 + random.uniform(-0.01, 0.01),
            "lon": -6.00 + i * 0.03 + random.uniform(-0.01, 0.01),
            "hectareas": round(3 + random.uniform(1, 8), 1),
        })
    return pd.DataFrame(sensores)

@st.cache_data(ttl=60)
def get_historical_data():
    """Series temporales de temperatura y humedad últimas 24h."""
    random.seed(99)
    now = datetime.now()
    horas = [now - timedelta(hours=i) for i in range(23, -1, -1)]
    data = []
    for h in horas:
        for parcela in ["Parcela Norte", "Parcela Sur", "Invernadero A"]:
            base = 20 if "Invernadero" not in parcela else 25
            data.append({
                "hora": h,
                "parcela": parcela,
                "temperatura": round(base + 4 * math.sin(h.hour * math.pi / 12) + random.uniform(-1.5, 1.5), 1),
                "humedad": round(65 - 10 * math.sin(h.hour * math.pi / 12) + random.uniform(-5, 5), 1),
            })
    return pd.DataFrame(data)

@st.cache_data(ttl=3600)
def get_produccion_data():
    """Datos de producción mensual por cultivo."""
    meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
    return pd.DataFrame({
        "mes": meses,
        "Tomate": [0, 0, 12, 45, 89, 120, 145, 130, 80, 30, 5, 0],
        "Pimiento": [0, 0, 0, 20, 60, 95, 110, 105, 70, 25, 0, 0],
        "Maíz": [0, 0, 0, 5, 25, 55, 90, 110, 95, 40, 10, 0],
        "Trigo": [5, 10, 25, 60, 90, 85, 30, 5, 0, 10, 20, 8],
    })

# ─────────────────────────────────────────────
# LOGIN / AUTENTICACIÓN
# ─────────────────────────────────────────────
def render_login():
    col_l, col_c, col_r = st.columns([1, 1.2, 1])
    with col_c:
        st.markdown("""
        <div class="login-wrap">
            <div class="login-logo">🌿</div>
            <div class="login-title">AgroTech Extremadura</div>
            <div class="login-sub">Plataforma de gestión agrícola inteligente</div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            email = st.text_input("Correo electrónico", placeholder="usuario@agrotech.es")
            password = st.text_input("Contraseña", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("Acceder al Dashboard", use_container_width=True)

            if submitted:
                # ── Demo: cualquier email/pass accede ──
                # Para Supabase real: supabase.auth.sign_in_with_password(...)
                if email and password:
                    st.session_state["logged_in"] = True
                    st.session_state["user_email"] = email
                    st.session_state["user_name"] = email.split("@")[0].capitalize()
                    st.rerun()
                else:
                    st.error("Introduce email y contraseña.")

        st.markdown("""
        <div style="text-align:center; margin-top:16px; font-size:0.78rem; color:#7aa98e;">
        🔒 Demo: cualquier credencial válida da acceso<br>
        Integra Supabase Auth en <code>get_supabase_client()</code>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR NAVEGACIÓN
# ─────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        # Logo
        st.markdown("""
        <div style="text-align:center; padding:20px 0 28px;">
            <div style="font-size:2.5rem;">🌿</div>
            <div style="font-size:1.1rem; font-weight:800; color:#d6f5e5; margin-top:6px;">AgroTech</div>
            <div style="font-size:0.72rem; color:#5fd494; letter-spacing:0.12em; text-transform:uppercase;">Extremadura</div>
        </div>
        <hr style="border:none; border-top:1px solid rgba(255,255,255,0.1); margin-bottom:20px;">
        """, unsafe_allow_html=True)

        nav = st.radio(
            "Navegación",
            ["🏠  Dashboard", "🗺️  Mapa de Parcelas", "📊  Producción & Cultivos", "🔔  Alertas", "⚙️  Configuración"],
            label_visibility="collapsed",
        )

        st.markdown("<hr style='border:none;border-top:1px solid rgba(255,255,255,0.1);margin:20px 0;'>", unsafe_allow_html=True)

        # Info usuario
        user = st.session_state.get("user_name", "Usuario")
        st.markdown(f"""
        <div style="padding:12px 16px; background:rgba(255,255,255,0.07); border-radius:12px; border:1px solid rgba(255,255,255,0.1);">
            <div style="font-size:0.72rem; color:#5fd494; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:6px;">Sesión activa</div>
            <div style="font-weight:700; font-size:0.9rem;">👤 {user}</div>
            <div style="font-size:0.72rem; color:rgba(214,245,229,0.6); margin-top:2px;">{st.session_state.get('user_email','')}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        if st.button("Cerrar sesión", use_container_width=True):
            st.session_state["logged_in"] = False
            st.rerun()

        # Footer sidebar
        st.markdown("""
        <div style="position:absolute; bottom:20px; left:0; right:0; text-align:center; font-size:0.68rem; color:rgba(214,245,229,0.35);">
            AgroTech Extremadura v2.0<br>© 2025 — Todos los derechos reservados
        </div>
        """, unsafe_allow_html=True)

    return nav.split("  ", 1)[-1] if "  " in nav else nav

# ─────────────────────────────────────────────
# PÁGINA: DASHBOARD
# ─────────────────────────────────────────────
def render_dashboard(df):
    st.markdown("""
    <div class="page-hero">
        <span class="hero-badge">🌱 Vista general</span>
        <h1>Dashboard Principal</h1>
        <p>Monitorización en tiempo real de todas las parcelas y sensores IoT</p>
    </div>
    """, unsafe_allow_html=True)

    # ── KPIs ──
    k1, k2, k3, k4 = st.columns(4)
    kpis = [
        ("kpi-green", "🌡️", f"{df['temperatura'].mean():.1f}°C", "Temperatura Media", "↑ +1.2°C vs ayer", "trend-up"),
        ("kpi-blue",  "💧", f"{df['humedad'].mean():.1f}%",    "Humedad Media",      "↓ -3.1% vs ayer",  "trend-down"),
        ("kpi-amber", "⚠️", str(len(df[df['estado']=='Alerta'])), "Alertas Activas",  "1 crítica, 1 media", "trend-warn"),
        ("kpi-green", "📍", str(len(df)),                        "Parcelas Activas",  f"{df['hectareas'].sum():.0f} ha totales", "trend-up"),
    ]
    for col, (cls, icon, val, label, trend, tcls) in zip([k1, k2, k3, k4], kpis):
        with col:
            st.markdown(f"""
            <div class="kpi-card {cls}">
                <span class="kpi-icon">{icon}</span>
                <div class="kpi-value">{val}</div>
                <div class="kpi-label">{label}</div>
                <span class="kpi-trend {tcls}">{trend}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # ── Fila 2: Gráfica temperatura + Estado parcelas ──
    col_chart, col_estado = st.columns([2, 1])

    with col_chart:
        hist = get_historical_data()
        st.markdown("""
        <div class="section-header">
            <div class="section-icon">📈</div>
            <div>
                <p class="section-title">Temperatura últimas 24h</p>
                <p class="section-sub">Por parcela — actualización cada minuto</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        fig = px.line(
            hist, x="hora", y="temperatura", color="parcela",
            color_discrete_map={
                "Parcela Norte": "#27a05e",
                "Parcela Sur": "#f59e0b",
                "Invernadero A": "#3b82f6",
            },
            labels={"hora": "", "temperatura": "°C", "parcela": ""},
        )
        fig.update_layout(
            height=280,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
            xaxis=dict(showgrid=False, color="#7aa98e"),
            yaxis=dict(gridcolor="#e8f5ee", color="#7aa98e"),
            font=dict(family="Plus Jakarta Sans"),
        )
        fig.update_traces(line=dict(width=2.5))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col_estado:
        st.markdown("""
        <div class="section-header">
            <div class="section-icon">🏷️</div>
            <div>
                <p class="section-title">Estado de Parcelas</p>
                <p class="section-sub">Resumen de condiciones</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        estado_counts = df["estado"].value_counts().reset_index()
        estado_counts.columns = ["estado", "count"]
        colors = {"Óptimo": "#27a05e", "Atención": "#f59e0b", "Alerta": "#ef4444"}
        fig2 = go.Figure(data=[go.Pie(
            labels=estado_counts["estado"],
            values=estado_counts["count"],
            hole=0.65,
            marker=dict(colors=[colors.get(e, "#888") for e in estado_counts["estado"]]),
            textinfo="percent+label",
            textfont=dict(family="Plus Jakarta Sans", size=12),
        )])
        fig2.update_layout(
            height=280,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            annotations=[dict(text=f"<b>{len(df)}</b><br>parcelas", x=0.5, y=0.5, showarrow=False, font=dict(size=13, family="Plus Jakarta Sans"))],
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Fila 3: Tabla sensores ──
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">📡</div>
        <div>
            <p class="section-title">Lecturas de Sensores IoT</p>
            <p class="section-sub">Todos los dispositivos activos en tiempo real</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    for _, row in df.iterrows():
        badge_cls = "badge-green" if row["estado"] == "Óptimo" else ("badge-amber" if row["estado"] == "Atención" else "badge-red")
        st.markdown(f"""
        <div style="background:white; border-radius:12px; padding:14px 20px; margin-bottom:8px;
                    border:1px solid #d1ead9; display:flex; align-items:center; gap:16px;
                    box-shadow:0 2px 8px rgba(13,43,26,0.05);">
            <div style="min-width:110px;">
                <div style="font-weight:700;font-size:0.88rem;color:#0d2b1a;">{row['parcela']}</div>
                <div style="font-size:0.72rem;color:#7aa98e;font-family:'DM Mono',monospace;">{row['id']}</div>
            </div>
            <span class="badge badge-earth">{row['cultivo']}</span>
            <div style="flex:1;display:flex;gap:20px;justify-content:center;">
                <span title="Temperatura" style="font-size:0.85rem;color:#0d2b1a;">🌡️ <b class='mono'>{row['temperatura']}°C</b></span>
                <span title="Humedad"     style="font-size:0.85rem;color:#0d2b1a;">💧 <b class='mono'>{row['humedad']}%</b></span>
                <span title="pH"          style="font-size:0.85rem;color:#0d2b1a;">⚗️ pH <b class='mono'>{row['ph']}</b></span>
                <span title="Nitrógeno"   style="font-size:0.85rem;color:#0d2b1a;">🧪 <b class='mono'>{row['nitrogeno']} mg/L</b></span>
            </div>
            <div style="text-align:right;min-width:80px;">
                <span class="badge {badge_cls}">{row['estado']}</span>
                <div style="font-size:0.68rem;color:#7aa98e;margin-top:4px;font-family:'DM Mono',monospace;">🕐 {row['ultima_lectura']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PÁGINA: MAPA DE PARCELAS
# ─────────────────────────────────────────────
def render_mapa(df):
    st.markdown("""
    <div class="page-hero">
        <span class="hero-badge">🗺️ Geolocalización</span>
        <h1>Mapa de Parcelas</h1>
        <p>Ubicación y estado de todas las fincas y sensores IoT</p>
    </div>
    """, unsafe_allow_html=True)

    col_mapa, col_info = st.columns([2, 1])

    with col_mapa:
        st.markdown("""
        <div class="section-header">
            <div class="section-icon">📍</div>
            <div>
                <p class="section-title">Vista satélite de parcelas</p>
                <p class="section-sub">Extremadura — Zona de cultivo principal</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Mapa nativo de Streamlit — no requiere token Mapbox
        map_df = df[["lat", "lon"]].copy()
        map_df.columns = ["lat", "lon"]

        try:
            # Streamlit >= 1.31
            st.map(map_df, latitude="lat", longitude="lon", zoom=12, use_container_width=True)
        except TypeError:
            # Fallback para versiones anteriores
            st.map(map_df, zoom=12)

        # Leyenda de colores debajo del mapa
        st.markdown("""
        <div style="display:flex;gap:16px;margin-top:8px;flex-wrap:wrap;">
            <span style="font-size:0.78rem;color:#4a7c5f;">
                <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#27a05e;margin-right:5px;"></span>Óptimo
            </span>
            <span style="font-size:0.78rem;color:#4a7c5f;">
                <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#f59e0b;margin-right:5px;"></span>Atención
            </span>
            <span style="font-size:0.78rem;color:#4a7c5f;">
                <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#ef4444;margin-right:5px;"></span>Alerta
            </span>
        </div>
        """, unsafe_allow_html=True)

    with col_info:
        st.markdown("""
        <div class="section-header">
            <div class="section-icon">📋</div>
            <div>
                <p class="section-title">Detalle de parcelas</p>
                <p class="section-sub">Selecciona para ver datos</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        for _, row in df.iterrows():
            badge_cls = "badge-green" if row["estado"] == "Óptimo" else ("badge-amber" if row["estado"] == "Atención" else "badge-red")
            st.markdown(f"""
            <div class="parcela-card">
                <div>
                    <div style="font-weight:700;font-size:0.88rem;color:#0d2b1a;">{row['parcela']}</div>
                    <div style="font-size:0.75rem;color:#7aa98e;margin-top:2px;">
                        🌱 {row['cultivo']} &nbsp;|&nbsp; 📐 {row['hectareas']} ha
                    </div>
                    <div style="font-size:0.72rem;color:#7aa98e;font-family:'DM Mono',monospace;margin-top:4px;">
                        🌡️ {row['temperatura']}°C &nbsp; 💧 {row['humedad']}%
                    </div>
                </div>
                <span class="badge {badge_cls}">{row['estado']}</span>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PÁGINA: PRODUCCIÓN & CULTIVOS
# ─────────────────────────────────────────────
def render_produccion(df):
    st.markdown("""
    <div class="page-hero">
        <span class="hero-badge">📊 Análisis</span>
        <h1>Producción & Cultivos</h1>
        <p>Rendimiento por cultivo, análisis de temporada y comparativas anuales</p>
    </div>
    """, unsafe_allow_html=True)

    prod = get_produccion_data()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="section-header">
            <div class="section-icon">📈</div>
            <div>
                <p class="section-title">Producción mensual (Tn)</p>
                <p class="section-sub">Año en curso por cultivo</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        fig = go.Figure()
        colors_prod = {"Tomate": "#27a05e", "Pimiento": "#ef4444", "Maíz": "#f59e0b", "Trigo": "#8b5e34"}
        for cultivo, color in colors_prod.items():
            fig.add_trace(go.Bar(
                x=prod["mes"], y=prod[cultivo],
                name=cultivo,
                marker_color=color,
                opacity=0.85,
            ))
        fig.update_layout(
            barmode="group",
            height=320,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
            xaxis=dict(showgrid=False, color="#7aa98e"),
            yaxis=dict(gridcolor="#e8f5ee", color="#7aa98e", title="Toneladas"),
            font=dict(family="Plus Jakarta Sans"),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col2:
        st.markdown("""
        <div class="section-header">
            <div class="section-icon">🌾</div>
            <div>
                <p class="section-title">Distribución por cultivo</p>
                <p class="section-sub">Producción acumulada anual</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        totales = {c: prod[c].sum() for c in ["Tomate", "Pimiento", "Maíz", "Trigo"]}
        fig3 = go.Figure(data=[go.Pie(
            labels=list(totales.keys()),
            values=list(totales.values()),
            hole=0.55,
            marker=dict(colors=["#27a05e", "#ef4444", "#f59e0b", "#8b5e34"]),
            textinfo="percent+label",
            textfont=dict(family="Plus Jakarta Sans", size=12),
        )])
        fig3.update_layout(
            height=320,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            font=dict(family="Plus Jakarta Sans"),
        )
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Fila: Humedad histórica + Gauges IoT ──
    col3, col4 = st.columns([3, 2])

    with col3:
        st.markdown("""
        <div class="section-header">
            <div class="section-icon">💧</div>
            <div>
                <p class="section-title">Humedad últimas 24h</p>
                <p class="section-sub">Comparativa entre parcelas</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        hist = get_historical_data()
        fig4 = px.area(
            hist, x="hora", y="humedad", color="parcela",
            color_discrete_map={"Parcela Norte": "#27a05e", "Parcela Sur": "#f59e0b", "Invernadero A": "#3b82f6"},
            labels={"hora": "", "humedad": "%", "parcela": ""},
        )
        fig4.update_traces(opacity=0.5)
        fig4.update_layout(
            height=240,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
            xaxis=dict(showgrid=False, color="#7aa98e"),
            yaxis=dict(gridcolor="#e8f5ee", color="#7aa98e"),
            font=dict(family="Plus Jakarta Sans"),
        )
        st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

    with col4:
        st.markdown("""
        <div class="section-header">
            <div class="section-icon">📊</div>
            <div>
                <p class="section-title">Niveles actuales</p>
                <p class="section-sub">Promedios de sensores</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        metrics = [
            ("Temperatura", df['temperatura'].mean(), 0, 50, "°C", "#27a05e"),
            ("Humedad",     df['humedad'].mean(),     0, 100, "%", "#3b82f6"),
            ("pH Suelo",    df['ph'].mean(),           0, 14,  "", "#f59e0b"),
        ]
        for label, val, mn, mx, unit, color in metrics:
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number",
                value=val,
                number=dict(suffix=unit, font=dict(size=20, family="Plus Jakarta Sans", color="#0d2b1a")),
                gauge=dict(
                    axis=dict(range=[mn, mx], tickfont=dict(size=9, color="#7aa98e")),
                    bar=dict(color=color, thickness=0.65),
                    bgcolor="white",
                    borderwidth=0,
                    steps=[dict(range=[mn, mx], color="#f0faf4")],
                    threshold=dict(line=dict(color=color, width=3), thickness=0.85, value=val),
                ),
            ))
            fig_g.update_layout(
                height=110,
                margin=dict(l=10, r=10, t=20, b=5),
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Plus Jakarta Sans"),
            )
            st.markdown(f"<div style='font-size:0.75rem;font-weight:600;color:#7aa98e;text-align:center;text-transform:uppercase;letter-spacing:0.08em;'>{label}</div>", unsafe_allow_html=True)
            st.plotly_chart(fig_g, use_container_width=True, config={"displayModeBar": False})

# ─────────────────────────────────────────────
# PÁGINA: ALERTAS
# ─────────────────────────────────────────────
def render_alertas(df):
    st.markdown("""
    <div class="page-hero">
        <span class="hero-badge">🔔 Notificaciones</span>
        <h1>Centro de Alertas</h1>
        <p>Avisos críticos, advertencias del sistema y notificaciones de sensores IoT</p>
    </div>
    """, unsafe_allow_html=True)

    # Stats de alertas
    c1, c2, c3, c4 = st.columns(4)
    vals = [
        ("kpi-red",   "🚨", "2", "Críticas",   "Requieren acción inmediata"),
        ("kpi-amber", "⚠️", "3", "Advertencias","Revisión recomendada"),
        ("kpi-blue",  "ℹ️", "5", "Informativas","Solo informativas"),
        ("kpi-green", "✅", "12","Resueltas",   "Últimas 24 horas"),
    ]
    for col, (cls, ic, v, l, s) in zip([c1,c2,c3,c4], vals):
        with col:
            st.markdown(f"""
            <div class="kpi-card {cls}">
                <span class="kpi-icon">{ic}</span>
                <div class="kpi-value">{v}</div>
                <div class="kpi-label">{l}</div>
                <div style="font-size:0.75rem;color:#7aa98e;margin-top:6px;">{s}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    col_act, col_hist = st.columns([1, 1])

    alertas = [
        ("critical", "dot-red",   "Temperatura crítica",        "Parcela Sur: 38.5°C supera el umbral máximo (35°C). Cultivo de tomate en riesgo.", "Hace 12 min"),
        ("critical", "dot-red",   "Fallo sensor IoT",           "Sensor SNS-004 sin respuesta desde las 14:32. Verificar conectividad.", "Hace 28 min"),
        ("warning",  "dot-amber", "Humedad baja",               "Invernadero A: 31% de humedad. Umbral mínimo recomendado: 45%.", "Hace 1h 15min"),
        ("warning",  "dot-amber", "Nivel N bajo en suelo",      "Parcela Norte: Nitrógeno en 48 mg/L. Programar fertilización.", "Hace 2h 40min"),
        ("warning",  "dot-amber", "pH fuera de rango",          "Parcela Oeste: pH 7.9 — rango óptimo para vid: 5.5–6.5.", "Hace 3h"),
        ("info",     "dot-blue",  "Riego automático activado",  "Sistema de riego iniciado en Parcela Norte según programación.", "Hace 4h"),
        ("info",     "dot-blue",  "Actualización de firmware",  "Sensores SNS-001, SNS-002 actualizados a v3.4.1 correctamente.", "Hace 6h"),
    ]

    with col_act:
        st.markdown("""
        <div class="section-header">
            <div class="section-icon">🚨</div>
            <div>
                <p class="section-title">Alertas activas</p>
                <p class="section-sub">Ordenadas por prioridad</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        for tipo, dot, titulo, desc, tiempo in alertas:
            cls = f"alert-{tipo if tipo != 'critical' else 'critical'}"
            if tipo == "critical": cls = "alert-critical"
            elif tipo == "warning": cls = "alert-warning"
            else: cls = "alert-info"

            st.markdown(f"""
            <div class="alert-item {cls}">
                <div class="alert-dot {dot}"></div>
                <div style="flex:1">
                    <div class="alert-title">{titulo}</div>
                    <div class="alert-desc">{desc}</div>
                    <div class="alert-time">🕐 {tiempo}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_hist:
        st.markdown("""
        <div class="section-header">
            <div class="section-icon">📅</div>
            <div>
                <p class="section-title">Historial de alertas (7 días)</p>
                <p class="section-sub">Evolución por categoría</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        dias = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        fig_a = go.Figure()
        fig_a.add_trace(go.Bar(x=dias, y=[1, 3, 2, 1, 2, 0, 2], name="Críticas", marker_color="#ef4444"))
        fig_a.add_trace(go.Bar(x=dias, y=[3, 2, 4, 2, 3, 1, 3], name="Advertencias", marker_color="#f59e0b"))
        fig_a.add_trace(go.Bar(x=dias, y=[5, 4, 6, 3, 5, 2, 5], name="Informativas", marker_color="#3b82f6"))
        fig_a.update_layout(
            barmode="stack",
            height=280,
            margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
            xaxis=dict(showgrid=False, color="#7aa98e"),
            yaxis=dict(gridcolor="#e8f5ee", color="#7aa98e"),
            font=dict(family="Plus Jakarta Sans"),
        )
        st.plotly_chart(fig_a, use_container_width=True, config={"displayModeBar": False})

        # Parcelas con más alertas
        st.markdown("""
        <div style="margin-top:16px;">
        <div style="font-size:0.8rem;font-weight:700;color:#4a7c5f;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:10px;">
            📍 Parcelas con más incidencias
        </div>
        """, unsafe_allow_html=True)
        for p, n, cls in [("Parcela Sur", 4, "badge-red"), ("Invernadero A", 3, "badge-amber"), ("Parcela Oeste", 2, "badge-amber"), ("Parcela Norte", 1, "badge-blue")]:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;padding:8px 12px;background:white;border-radius:8px;border:1px solid #d1ead9;margin-bottom:6px;">
                <span style="font-size:0.85rem;font-weight:600;color:#0d2b1a;">{p}</span>
                <span class="badge {cls}">{n} alertas</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PÁGINA: CONFIGURACIÓN
# ─────────────────────────────────────────────
def render_configuracion():
    st.markdown("""
    <div class="page-hero">
        <span class="hero-badge">⚙️ Ajustes</span>
        <h1>Configuración del Sistema</h1>
        <p>Parámetros de conexión Supabase, umbrales de alerta y preferencias</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="section-header">
            <div class="section-icon">🗄️</div>
            <div>
                <p class="section-title">Conexión Supabase</p>
                <p class="section-sub">Configuración de base de datos</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("supabase_config"):
            sb_url = st.text_input("Supabase URL", placeholder="https://xxxx.supabase.co", value=st.session_state.get("sb_url", ""))
            sb_key = st.text_input("API Key (anon)", type="password", placeholder="eyJ...", value=st.session_state.get("sb_key", ""))
            tabla_sensores = st.text_input("Tabla de sensores", value=st.session_state.get("tabla_sensores", "sensor_readings"))

            if st.form_submit_button("💾 Guardar configuración", use_container_width=True):
                st.session_state["sb_url"] = sb_url
                st.session_state["sb_key"] = sb_key
                st.session_state["tabla_sensores"] = tabla_sensores
                st.success("✅ Configuración guardada. Reconectando...")

        st.markdown("""
        <div style="background:#f0faf4;border:1px solid #d1ead9;border-radius:12px;padding:16px;margin-top:12px;">
        <div style="font-size:0.8rem;font-weight:700;color:#1a5c38;margin-bottom:8px;">📝 Cómo integrar Supabase</div>
        <div style="font-size:0.78rem;color:#4a7c5f;line-height:1.7;">
        1. Instala: <code>pip install supabase>=2.11.0</code><br>
        2. En tu código:<br>
        <code>from supabase import create_client</code><br>
        <code>sb = create_client(SB_URL, SB_KEY)</code><br>
        <code>data = sb.table("sensor_readings").select("*").execute()</code><br>
        3. Reemplaza <code>get_sensor_data()</code> con la consulta real.
        </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="section-header">
            <div class="section-icon">🔔</div>
            <div>
                <p class="section-title">Umbrales de Alerta</p>
                <p class="section-sub">Valores límite por parámetro</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.form("umbrales_config"):
            c_a, c_b = st.columns(2)
            with c_a:
                temp_min = st.number_input("Temp. mínima (°C)", value=5.0, step=0.5)
                hum_min  = st.number_input("Humedad mínima (%)", value=40.0, step=1.0)
                ph_min   = st.number_input("pH mínimo", value=5.5, step=0.1)
            with c_b:
                temp_max = st.number_input("Temp. máxima (°C)", value=35.0, step=0.5)
                hum_max  = st.number_input("Humedad máxima (%)", value=90.0, step=1.0)
                ph_max   = st.number_input("pH máximo", value=7.5, step=0.1)

            notif_email = st.text_input("Email de notificaciones", placeholder="admin@finca.es")
            if st.form_submit_button("💾 Guardar umbrales", use_container_width=True):
                st.success("✅ Umbrales actualizados correctamente.")

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="section-header">
        <div class="section-icon">👥</div>
        <div>
            <p class="section-title">Gestión de Usuarios</p>
            <p class="section-sub">Administración de accesos y roles</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    usuarios = [
        ("Carlos Martínez", "carlos@agrotech.es", "Administrador", "badge-green", "Activo"),
        ("María López",     "maria@agrotech.es",  "Técnico",        "badge-blue",  "Activo"),
        ("Pedro García",    "pedro@finca.es",      "Operador",       "badge-earth", "Activo"),
        ("Ana Sánchez",     "ana@finca.es",        "Visualización",  "badge-amber", "Inactivo"),
    ]

    for nombre, email, rol, rol_cls, estado in usuarios:
        est_cls = "badge-green" if estado == "Activo" else "badge-red"
        st.markdown(f"""
        <div style="background:white;border-radius:12px;padding:14px 20px;margin-bottom:8px;
                    border:1px solid #d1ead9;display:flex;align-items:center;gap:16px;box-shadow:0 2px 8px rgba(13,43,26,0.05);">
            <div style="width:38px;height:38px;background:linear-gradient(135deg,#27a05e,#3dbd76);border-radius:50%;
                        display:flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:1rem;flex-shrink:0;">
                {nombre[0]}
            </div>
            <div style="flex:1;">
                <div style="font-weight:700;font-size:0.88rem;color:#0d2b1a;">{nombre}</div>
                <div style="font-size:0.75rem;color:#7aa98e;font-family:'DM Mono',monospace;">{email}</div>
            </div>
            <span class="badge {rol_cls}">{rol}</span>
            <span class="badge {est_cls}">{estado}</span>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAIN — ROUTER
# ─────────────────────────────────────────────
def main():
    # ── Inicializar estado ──
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # ── Login ──
    if not st.session_state["logged_in"]:
        render_login()
        return

    # ── App autenticada ──
    df = get_sensor_data()
    page = render_sidebar()

    if "Dashboard" in page:
        render_dashboard(df)
    elif "Mapa" in page:
        render_mapa(df)
    elif "Producci" in page:
        render_produccion(df)
    elif "Alertas" in page:
        render_alertas(df)
    elif "Configuraci" in page:
        render_configuracion()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Error inesperado: {e}")
        st.info("Recarga la página para intentarlo de nuevo.")
