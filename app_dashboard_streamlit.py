"""
AgroTech Extremadura — Dashboard Principal
Conectado a Supabase con datos reales.
Credenciales via st.secrets (nunca hardcodeadas).
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

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
# CSS GLOBAL
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');

:root {
    --green-900: #0d2b1a; --green-800: #14432a; --green-700: #1a5c38;
    --green-600: #1f7a48; --green-500: #27a05e; --green-400: #3dbd76;
    --green-300: #5fd494; --green-100: #d6f5e5;
    --earth-700: #5c3d1e; --earth-500: #8b5e34; --earth-300: #c49a6c;
    --amber-500: #f59e0b; --amber-100: #fef3c7;
    --red-500: #ef4444;   --red-100: #fee2e2;
    --blue-500: #3b82f6;  --blue-100: #dbeafe;
    --border: #d1ead9; --shadow: 0 4px 24px rgba(13,43,26,0.08);
    --shadow-lg: 0 8px 40px rgba(13,43,26,0.14); --radius: 16px; --radius-sm: 10px;
}
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif !important; }
.stApp { background: linear-gradient(135deg, #f0faf4 0%, #e8f5ee 50%, #f5f9f2 100%) fixed; }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--green-900) 0%, var(--green-800) 60%, #0a2010 100%) !important;
    border-right: none !important; box-shadow: 4px 0 30px rgba(0,0,0,0.3) !important;
}
/* Aplicar color claro SOLO a elementos dentro del sidebar */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] a,
section[data-testid="stSidebar"] li,
section[data-testid="stSidebar"] .stRadio,
section[data-testid="stSidebar"] .stMarkdown { color: #d6f5e5 !important; }
section[data-testid="stSidebar"] .stRadio label {
    background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: var(--radius-sm) !important; padding: 10px 16px !important;
    margin: 3px 0 !important; cursor: pointer !important; transition: all 0.2s ease !important;
}
section[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(63,189,118,0.15) !important; border-color: var(--green-400) !important;
}
#MainMenu, footer, header { visibility: hidden; }

/* Asegurar que el botón de colapsar/desplegar sidebar siempre sea visible */
button[kind="header"] { display: flex !important; visibility: visible !important; opacity: 1 !important; }
[data-testid="collapsedControl"] { display: flex !important; visibility: visible !important; color: var(--green-500) !important; background: white !important; border-radius: 0 8px 8px 0 !important; box-shadow: 2px 0 8px rgba(13,43,26,0.15) !important; }
[data-testid="collapsedControl"]:hover { background: var(--green-100) !important; }
.block-container { padding: 1.5rem 2rem !important; max-width: 1400px !important; }

.kpi-card {
    background: white; border-radius: var(--radius); padding: 22px 24px;
    box-shadow: var(--shadow); border: 1px solid var(--border);
    position: relative; overflow: hidden; transition: all 0.3s ease;
}
.kpi-card:hover { box-shadow: var(--shadow-lg); transform: translateY(-3px); }
.kpi-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0;
    height: 4px; border-radius: var(--radius) var(--radius) 0 0;
}
.kpi-green::before { background: linear-gradient(90deg, var(--green-500), var(--green-300)); }
.kpi-amber::before { background: linear-gradient(90deg, var(--amber-500), #fbbf24); }
.kpi-red::before   { background: linear-gradient(90deg, var(--red-500), #f87171); }
.kpi-blue::before  { background: linear-gradient(90deg, var(--blue-500), #60a5fa); }
.kpi-earth::before { background: linear-gradient(90deg, #8b5e34, #c49a6c); }

.kpi-icon  { font-size: 2rem; margin-bottom: 8px; display: block; }
.kpi-value { font-size: 2.2rem; font-weight: 800; color: #0d2b1a; line-height: 1; margin: 4px 0; }
.kpi-label { font-size: 0.78rem; font-weight: 600; color: #7aa98e; text-transform: uppercase; letter-spacing: 0.08em; }
.kpi-sub   { font-size: 0.78rem; color: #7aa98e; margin-top: 6px; }

.badge { display:inline-block; padding:3px 10px; border-radius:20px; font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; }
.badge-green { background:var(--green-100); color:var(--green-700); }
.badge-amber { background:var(--amber-100); color:#b45309; }
.badge-red   { background:var(--red-100);   color:#b91c1c; }
.badge-blue  { background:var(--blue-100);  color:#1d4ed8; }
.badge-earth { background:#fdf4e7; color:var(--earth-700); }
.badge-gray  { background:#f1f5f9; color:#475569; }

.section-header { display:flex; align-items:center; gap:12px; margin-bottom:20px; padding-bottom:14px; border-bottom:2px solid var(--border); }
.section-icon { width:40px; height:40px; background:linear-gradient(135deg,var(--green-500),var(--green-400)); border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:1.1rem; box-shadow:0 4px 12px rgba(39,160,94,0.3); }
.section-title { font-size:1.25rem; font-weight:700; color:#0d2b1a; margin:0; }
.section-sub   { font-size:0.8rem; color:#7aa98e; margin:0; }

.alert-item { display:flex; align-items:flex-start; gap:14px; padding:14px 16px; border-radius:var(--radius-sm); margin-bottom:10px; border-left:4px solid; transition:all 0.2s; }
.alert-item:hover { transform:translateX(4px); }
.alert-critical { background:#fff5f5; border-color:var(--red-500); }
.alert-warning  { background:#fffbeb; border-color:var(--amber-500); }
.alert-info     { background:#eff6ff; border-color:var(--blue-500); }
.alert-ok       { background:#f0fdf4; border-color:var(--green-500); }

.alert-dot { width:10px; height:10px; border-radius:50%; margin-top:5px; flex-shrink:0; }
.dot-red   { background:var(--red-500);   animation: pulse-r 2s infinite; }
.dot-amber { background:var(--amber-500); }
.dot-blue  { background:var(--blue-500);  }
.dot-green { background:var(--green-500); }
@keyframes pulse-r { 0%,100%{box-shadow:0 0 0 0 rgba(239,68,68,0.4)} 50%{box-shadow:0 0 0 6px rgba(239,68,68,0)} }

.alert-title { font-weight:700; font-size:0.88rem; color:#0d2b1a; }
.alert-desc  { font-size:0.8rem; color:#4a7c5f; margin-top:2px; }
.alert-time  { font-size:0.72rem; color:#7aa98e; margin-top:4px; font-family:'DM Mono',monospace; }

.page-hero {
    background: linear-gradient(135deg, var(--green-900) 0%, var(--green-700) 100%);
    border-radius: var(--radius); padding: 28px 32px; margin-bottom: 28px;
    color: white; position: relative; overflow: hidden;
}
.page-hero::after { content:'🌿'; position:absolute; right:30px; top:50%; transform:translateY(-50%); font-size:5rem; opacity:0.15; }
.page-hero h1  { color:white !important; font-size:1.7rem; font-weight:800; margin:0 0 4px; }
.page-hero p   { color:rgba(255,255,255,0.7); margin:0; font-size:0.9rem; }
.page-hero .hero-badge { display:inline-block; background:rgba(255,255,255,0.15); border:1px solid rgba(255,255,255,0.25); border-radius:20px; padding:4px 14px; font-size:0.75rem; font-weight:600; color:white; margin-bottom:10px; }

.mono { font-family:'DM Mono',monospace; }

.data-row { background:white; border-radius:12px; padding:14px 20px; margin-bottom:8px; border:1px solid var(--border); display:flex; align-items:center; gap:16px; box-shadow:0 2px 8px rgba(13,43,26,0.05); transition:all 0.2s; }
.data-row:hover { border-color:var(--green-400); box-shadow:var(--shadow); }

.stButton button { background:linear-gradient(135deg,var(--green-600),var(--green-500)) !important; color:white !important; border:none !important; border-radius:var(--radius-sm) !important; font-weight:600 !important; font-family:'Plus Jakarta Sans',sans-serif !important; box-shadow:0 4px 14px rgba(39,160,94,0.35) !important; transition:all 0.2s !important; }
.stButton button:hover { transform:translateY(-1px) !important; box-shadow:0 6px 20px rgba(39,160,94,0.45) !important; }

.login-wrap { max-width:440px; margin:60px auto; background:white; border-radius:24px; padding:48px 40px; box-shadow:var(--shadow-lg); border:1px solid var(--border); text-align:center; }

/* Labels de filtros visibles en el área principal */
.block-container label, .block-container .stSelectbox label, .block-container .stTextInput label {
    color: #0d2b1a !important; font-weight: 600 !important; font-size: 0.82rem !important;
}
/* Sobreescribir el color oscuro heredado del sidebar para los widgets del main */
.main label { color: #0d2b1a !important; }
.main .stSelectbox > label { color: #0d2b1a !important; }
.main .stTextInput > label { color: #0d2b1a !important; }
[data-testid="stForm"] label { color: #0d2b1a !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CONEXIÓN SUPABASE
# ─────────────────────────────────────────────
@st.cache_resource
def get_supabase():
    try:
        from supabase import create_client
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"❌ Error conectando a Supabase: {e}")
        return None

# ─────────────────────────────────────────────
# CARGA DE DATOS
# ─────────────────────────────────────────────
@st.cache_data(ttl=300)
def load(tabla, order_col=None, desc=True, limit=200):
    sb = get_supabase()
    if not sb:
        return pd.DataFrame()
    try:
        q = sb.table(tabla).select("*")
        if order_col:
            q = q.order(order_col, desc=desc)
        q = q.limit(limit)
        r = q.execute()
        return pd.DataFrame(r.data) if r.data else pd.DataFrame()
    except Exception as e:
        st.warning(f"⚠️ {tabla}: {e}")
        return pd.DataFrame()

# ─────────────────────────────────────────────
# HELPERS UI
# ─────────────────────────────────────────────
def section_header(icon, title, sub=""):
    st.markdown(f"""
    <div class="section-header">
        <div class="section-icon">{icon}</div>
        <div>
            <p class="section-title">{title}</p>
            <p class="section-sub">{sub}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def page_hero(badge, title, subtitle):
    st.markdown(f"""
    <div class="page-hero">
        <span class="hero-badge">{badge}</span>
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)

def kpi_card(col, cls, icon, value, label, sub):
    with col:
        st.markdown(f"""
        <div class="kpi-card {cls}">
            <span class="kpi-icon">{icon}</span>
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Plus Jakarta Sans", color="#0d2b1a"),
    margin=dict(l=0, r=0, t=30, b=0),
    xaxis=dict(showgrid=False, color="#7aa98e"),
    yaxis=dict(gridcolor="#e8f5ee", color="#7aa98e"),
    legend=dict(
        orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
        font=dict(size=12, color="#0d2b1a"),
        bgcolor="rgba(255,255,255,0.85)",
        bordercolor="#d1ead9", borderwidth=1,
    ),
)

COLORS = ["#27a05e", "#f59e0b", "#3b82f6", "#ef4444", "#8b5e34", "#a855f7"]

# ─────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────
def render_login():
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown("""
        <div class="login-wrap">
            <div style="font-size:3rem">🌿</div>
            <div style="font-size:1.6rem;font-weight:800;color:#0d2b1a;">AgroTech Extremadura</div>
            <div style="color:#7aa98e;font-size:0.9rem;margin:8px 0 32px;">Monitor del Campo Extremeño</div>
        </div>
        """, unsafe_allow_html=True)
        with st.form("login_form"):
            email    = st.text_input("Correo electrónico", placeholder="usuario@agrotech.es")
            password = st.text_input("Contraseña", type="password", placeholder="••••••••")
            if st.form_submit_button("Acceder al Dashboard", use_container_width=True):
                if email and password:
                    # Acceso directo: cualquier email+contraseña da acceso al dashboard.
                    # Para auth real con Supabase, activa el bloque comentado más abajo.
                    st.session_state.update({
                        "logged_in": True,
                        "user_email": email,
                        "user_name": email.split("@")[0].capitalize(),
                    })
                    st.rerun()
                    # ── Auth real Supabase (descomentar cuando tengas usuarios en Supabase Auth) ──
                    # try:
                    #     sb = get_supabase()
                    #     res = sb.auth.sign_in_with_password({"email": email, "password": password})
                    #     st.session_state.update({
                    #         "logged_in": True,
                    #         "user_email": res.user.email,
                    #         "user_name": res.user.email.split("@")[0].capitalize(),
                    #     })
                    #     st.rerun()
                    # except Exception as e:
                    #     st.error(f"Credenciales incorrectas: {e}")
                else:
                    st.error("Introduce email y contraseña.")

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center;padding:20px 0 28px;">
            <div style="font-size:2.5rem;">🌿</div>
            <div style="font-size:1.1rem;font-weight:800;color:#d6f5e5;margin-top:6px;">AgroTech</div>
            <div style="font-size:0.72rem;color:#5fd494;letter-spacing:0.12em;text-transform:uppercase;">Monitor del Campo</div>
        </div>
        <hr style="border:none;border-top:1px solid rgba(255,255,255,0.1);margin-bottom:20px;">
        """, unsafe_allow_html=True)

        nav = st.radio("nav", [
            "🏠  Dashboard",
            "🗺️  Mapa de Operaciones",
            "📊  Monitor de Mercados",
            "🌐  Monitor de Productos",
            "🔔  Alertas",
            "⚙️  Configuración",
        ], label_visibility="collapsed")

        st.markdown("<hr style='border:none;border-top:1px solid rgba(255,255,255,0.1);margin:20px 0;'>", unsafe_allow_html=True)

        user = st.session_state.get("user_name", "Usuario")
        st.markdown(f"""
        <div style="padding:12px 16px;background:rgba(255,255,255,0.07);border-radius:12px;border:1px solid rgba(255,255,255,0.1);">
            <div style="font-size:0.72rem;color:#5fd494;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:6px;">Sesión activa</div>
            <div style="font-weight:700;font-size:0.9rem;">👤 {user}</div>
            <div style="font-size:0.72rem;color:rgba(214,245,229,0.6);margin-top:2px;">{st.session_state.get('user_email','')}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        if st.button("🔄 Recargar datos", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        if st.button("Cerrar sesión", use_container_width=True):
            st.session_state["logged_in"] = False
            st.rerun()



    return nav.split("  ", 1)[-1]

# ─────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────
def render_dashboard():
    page_hero("🌱 Vista general", "Dashboard Principal", "Estado actual del campo extremeño — datos en tiempo real")

    df_mapa  = load("v_mapa_operaciones")
    df_salud = load("v_salud_sectores")
    df_clima = load("datos_clima", order_col="fecha", limit=100)

    # ── KPIs ──
    c1, c2, c3, c4, c5 = st.columns(5)

    if not df_mapa.empty:
        temp   = df_mapa["temp_actual"].mean()        if "temp_actual"    in df_mapa else None
        hum    = df_mapa["humedad"].mean()             if "humedad"        in df_mapa else None
        kwh    = df_mapa["precio_kwh"].mean()          if "precio_kwh"     in df_mapa else None
        tramo  = df_mapa["tramo_energia"].mode()[0]    if "tramo_energia"  in df_mapa else "—"
    else:
        temp = hum = kwh = None
        tramo = "—"

    df_ac    = load("v_alertas_clima_extrema", order_col="fecha")
    n_alerta = 0
    if not df_ac.empty and "alerta_riesgo" in df_ac.columns:
        # Solo contar alertas reales, excluyendo valores vacíos/normales
        n_alerta = int(df_ac["alerta_riesgo"].dropna().apply(
            lambda x: str(x).strip().lower() not in ["", "none", "nan", "sin alerta", "normal", "sin alarma"]
        ).sum())

    kpi_card(c1, "kpi-green", "🌡️",
             f"{temp:.1f}°C" if temp is not None else "—",
             "Temperatura media", f"{len(df_mapa)} estaciones")
    kpi_card(c2, "kpi-blue", "💧",
             f"{hum:.0f}%" if hum is not None else "—",
             "Humedad media", "Promedio campo")
    kpi_card(c3, "kpi-amber", "⚡",
             f"{kwh:.3f}€" if kwh is not None else "—",
             "Precio kWh", tramo)
    kpi_card(c4, "kpi-red" if n_alerta > 0 else "kpi-green", "⚠️",
             str(n_alerta), "Alertas clima", "Activas")

    if not df_salud.empty and "estado_mercado" in df_salud.columns:
        al_alza = int(df_salud["estado_mercado"].str.contains("alza|sube|bueno", case=False, na=False).sum())
        kpi_card(c5, "kpi-earth", "🌾", f"{al_alza}/{len(df_salud)}", "Sectores al alza", "Estado mercado")
    else:
        kpi_card(c5, "kpi-earth", "🌾", "—", "Sectores", "Sin datos")

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # ── Temperatura histórica + Salud sectores ──
    col_g, col_s = st.columns([2, 1])

    with col_g:
        section_header("📈", "Temperatura por estación", "datos_clima — últimos 30 días")
        if not df_clima.empty and "fecha" in df_clima.columns and "temp_actual" in df_clima.columns:
            df_plot = df_clima.copy()
            df_plot["fecha"] = pd.to_datetime(df_plot["fecha"])
            # Agrupar por semana y estación para mejor legibilidad
            df_plot["semana"] = df_plot["fecha"].dt.to_period("W").apply(lambda x: x.start_time)
            df_avg = df_plot.groupby(["semana", "estacion"])["temp_actual"].agg(["mean", "min", "max"]).reset_index()
            df_avg.columns = ["semana", "estacion", "temp_media", "temp_min", "temp_max"]
            
            estaciones = df_avg["estacion"].unique()
            fig = go.Figure()
            for i, est in enumerate(estaciones[:6]):
                sub = df_avg[df_avg["estacion"] == est].sort_values("semana")
                color = COLORS[i % len(COLORS)]
                # Área entre min y max
                fig.add_trace(go.Scatter(
                    x=list(sub["semana"]) + list(sub["semana"])[::-1],
                    y=list(sub["temp_max"]) + list(sub["temp_min"])[::-1],
                    fill="toself",
                    fillcolor=f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.12)",
                    line=dict(width=0), showlegend=False, hoverinfo="skip",
                ))
                # Línea media
                fig.add_trace(go.Scatter(
                    x=sub["semana"], y=sub["temp_media"],
                    name=est, line=dict(color=color, width=2.5),
                    mode="lines+markers", marker=dict(size=6),
                    hovertemplate=f"<b>{est}</b><br>Semana: %{{x|%d/%m}}<br>Media: %{{y:.1f}}°C<extra></extra>",
                ))
            layout_t = {**CHART_LAYOUT}
            layout_t["yaxis"] = dict(gridcolor="#e8f5ee", color="#7aa98e", title="°C")
            layout_t["xaxis"] = dict(showgrid=False, color="#7aa98e", tickformat="%d/%m")
            fig.update_layout(height=290, **layout_t)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Sin datos de temperatura histórica")

    with col_s:
        section_header("🏷️", "Salud de Sectores", "Estado actual del mercado")
        if not df_salud.empty:
            for _, row in df_salud.iterrows():
                estado = str(row.get("estado_mercado", "")).lower()
                if any(x in estado for x in ["alza", "bueno", "sube"]):
                    b_cls, dot = "badge-green", "🟢"
                elif any(x in estado for x in ["baja", "baj", "mal"]):
                    b_cls, dot = "badge-red", "🔴"
                else:
                    b_cls, dot = "badge-amber", "🟡"
                var  = float(row.get("variacion_media_sector", 0) or 0)
                sign = "+" if var > 0 else ""
                st.markdown(f"""
                <div class="data-row" style="padding:12px 16px;">
                    <span style="font-size:1.1rem;">{dot}</span>
                    <div style="flex:1;">
                        <div style="font-weight:700;font-size:0.88rem;color:#0d2b1a;">{row.get('sector','—')}</div>
                        <div style="font-size:0.75rem;color:#7aa98e;">
                            {row.get('num_productos','—')} productos ·
                            ↑{row.get('productos_al_alza',0)} ↓{row.get('productos_a_la_baja',0)}
                        </div>
                    </div>
                    <span class="badge {b_cls}">{sign}{var:.1f}%</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Sin datos de sectores")

    # ── Recomendaciones ──
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    section_header("💡", "Recomendaciones operativas", "v_mapa_operaciones — estaciones activas")
    if not df_mapa.empty:
        cols = st.columns(min(len(df_mapa), 3))
        for i, (_, row) in enumerate(df_mapa.head(3).iterrows()):
            with cols[i]:
                st.markdown(f"""
                <div style="background:white;border-radius:14px;padding:18px 20px;border:1px solid var(--border);box-shadow:var(--shadow);height:100%;">
                    <div style="font-weight:800;font-size:0.95rem;color:#0d2b1a;margin-bottom:12px;">📍 {row.get('estacion','—')}</div>
                    <div style="font-size:0.8rem;color:#4a7c5f;margin-bottom:8px;">
                        <span style="font-weight:600;">💧 Riego:</span><br>{row.get('recomendacion_riego','Sin datos')}
                    </div>
                    <div style="font-size:0.8rem;color:#4a7c5f;margin-bottom:8px;">
                        <span style="font-weight:600;">🌿 Tratamiento:</span><br>{row.get('recomendacion_tratamiento','Sin datos')}
                    </div>
                    <div style="font-size:0.78rem;color:#7aa98e;margin-top:10px;border-top:1px solid var(--border);padding-top:8px;">
                        ☀️ {row.get('luz_estado','—')} &nbsp;|&nbsp;
                        🌬️ {row.get('viento_vel','—')} km/h &nbsp;|&nbsp;
                        🌡️ {row.get('temp_actual','—')}°C
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Sin datos de estaciones")

# ─────────────────────────────────────────────
# MAPA DE OPERACIONES
# ─────────────────────────────────────────────
def render_mapa():
    page_hero("🗺️ Geolocalización", "Mapa de Operaciones", "Visualización geográfica de las estaciones")

    df = load("v_mapa_operaciones")

    if df.empty or "latitud" not in df.columns:
        st.warning("Sin datos de localización en v_mapa_operaciones")
        return

    # ── Filtros en la parte superior ──
    f1, f2, f3 = st.columns([1, 1, 2])
    with f1:
        # Filtro por tratamiento
        tratamiento_opts = ["Todos"]
        if "recomendacion_tratamiento" in df.columns:
            vals = df["recomendacion_tratamiento"].dropna().unique().tolist()
            tratamiento_opts += sorted(vals)
        filtro_trat = st.selectbox("Tratamiento", tratamiento_opts)
    with f2:
        # Filtro por riego
        riego_opts = ["Todos"]
        if "recomendacion_riego" in df.columns:
            vals = df["recomendacion_riego"].dropna().unique().tolist()
            riego_opts += sorted(vals)
        filtro_riego = st.selectbox("Riego", riego_opts)
    with f3:
        buscar = st.text_input("🔍 Buscar estación", placeholder="Nombre de estación...")

    # Aplicar filtros
    df_filtered = df.copy()
    if filtro_trat != "Todos" and "recomendacion_tratamiento" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["recomendacion_tratamiento"] == filtro_trat]
    if filtro_riego != "Todos" and "recomendacion_riego" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["recomendacion_riego"] == filtro_riego]
    if buscar and "estacion" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["estacion"].str.contains(buscar, case=False, na=False)]

    # ── Leyenda de estados ──
    st.markdown("""
    <div style="display:flex;align-items:center;gap:20px;margin:8px 0 16px;padding:10px 16px;background:white;border-radius:10px;border:1px solid var(--border);">
        <span style="display:flex;align-items:center;gap:6px;font-size:0.82rem;font-weight:600;color:#0d2b1a;">
            <span style="width:12px;height:12px;border-radius:50%;background:#27a05e;display:inline-block;"></span> Óptimo
        </span>
        <span style="display:flex;align-items:center;gap:6px;font-size:0.82rem;font-weight:600;color:#0d2b1a;">
            <span style="width:12px;height:12px;border-radius:50%;background:#f59e0b;display:inline-block;"></span> Precaución
        </span>
        <span style="display:flex;align-items:center;gap:6px;font-size:0.82rem;font-weight:600;color:#0d2b1a;">
            <span style="width:12px;height:12px;border-radius:50%;background:#ef4444;display:inline-block;"></span> Crítico
        </span>
    </div>
    """, unsafe_allow_html=True)

    def color_estado(row):
        """Color según recomendacion_tratamiento: verde=óptimo, amarillo=precaución, rojo=crítico"""
        trat = str(row.get("recomendacion_tratamiento", "") or "").lower()
        # Palabras clave para crítico (rojo)
        if any(x in trat for x in ["crític", "peligro", "no tratar", "prohibido", "suspender"]):
            return "#ef4444"
        # Palabras clave para precaución (amarillo)
        if any(x in trat for x in ["precaución", "precaucion", "esperar", "vigilar", "atención", "atencion", "llano", "discrecional"]):
            return "#f59e0b"
        # Por defecto óptimo (verde)
        return "#27a05e"

    if not df_filtered.empty:
        df_filtered = df_filtered.copy()
        df_filtered["_color"] = df_filtered.apply(color_estado, axis=1)

    # ── Calcular zoom y centro dinámicos según el filtro ──
    def calc_zoom_center(dff, df_base):
        """Calcula zoom y centro: si hay filtro activo hace zoom sobre la selección"""
        if dff.empty:
            lat_c = df_base["latitud"].mean() if not df_base.empty else 38.9
            lon_c = df_base["longitud"].mean() if not df_base.empty else -6.3
            return lat_c, lon_c, 7
        lat_c = dff["latitud"].mean()
        lon_c = dff["longitud"].mean()
        if len(dff) == 1:
            return lat_c, lon_c, 11
        lat_range = dff["latitud"].max() - dff["latitud"].min()
        lon_range = dff["longitud"].max() - dff["longitud"].min()
        max_range = max(lat_range, lon_range)
        if max_range < 0.1:   zoom = 11
        elif max_range < 0.3: zoom = 10
        elif max_range < 0.8: zoom = 9
        elif max_range < 1.5: zoom = 8
        elif max_range < 3.0: zoom = 7
        else:                  zoom = 6
        return lat_c, lon_c, zoom

    center_lat, center_lon, zoom_level = calc_zoom_center(df_filtered, df)

    # ── Mapa a pantalla completa ──
    try:
        fig = go.Figure()
        color_groups = {
            "#27a05e": "Óptimo",
            "#f59e0b": "Precaución",
            "#ef4444": "Crítico",
        }
        for hex_color, label in color_groups.items():
            sub = df_filtered[df_filtered["_color"] == hex_color] if not df_filtered.empty else pd.DataFrame()
            if sub.empty:
                continue
            hover_texts = sub.apply(lambda r:
                f"<b>{r.get('estacion','—')}</b><br>"
                f"🌬️ Viento: {r.get('viento_vel','—')} km/h<br>"
                f"🌧️ Precipitación: {r.get('precipitacion','—')} mm<br>"
                f"🌡️ Temp. actual: {r.get('temp_actual','—')} °C<br>"
                f"💧 Humedad: {r.get('humedad','—')}%<br>"
                f"<b>Tratamiento:</b> {r.get('recomendacion_tratamiento','—')}<br>"
                f"<b>Riego:</b> {r.get('recomendacion_riego','—')}<br>"
                f"Estado luz: {r.get('luz_estado','—')}", axis=1).tolist()
            fig.add_trace(go.Scattermapbox(
                lat=sub["latitud"].tolist(),
                lon=sub["longitud"].tolist(),
                mode="markers",
                marker=go.scattermapbox.Marker(size=16, color=hex_color, opacity=1.0),
                text=hover_texts,
                hoverinfo="text",
                name=label,
            ))
        fig.update_layout(
            mapbox=dict(
                style="open-street-map",
                center=dict(lat=center_lat, lon=center_lon),
                zoom=zoom_level,
            ),
            height=540, margin=dict(l=0, r=0, t=0, b=0),
            legend=dict(
                orientation="h", yanchor="top", y=0.01, xanchor="left", x=0.01,
                bgcolor="rgba(255,255,255,0.92)", font=dict(size=13, color="#0d2b1a"),
                bordercolor="#d1ead9", borderwidth=1,
            ),
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    except Exception as e:
        st.warning(f"No se pudo cargar el mapa: {e}")
        if not df_filtered.empty and "latitud" in df_filtered.columns:
            st.map(df_filtered.rename(columns={"latitud": "lat", "longitud": "lon"})[["lat","lon"]], zoom=7)

    # ── Tabla resumida debajo del mapa ──
    if not df_filtered.empty:
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        section_header("📋", "Estaciones filtradas", f"{len(df_filtered)} estaciones")
        cols_show = [c for c in ["estacion", "temp_actual", "humedad", "viento_vel", "precipitacion",
                                  "recomendacion_tratamiento", "recomendacion_riego", "luz_estado"] if c in df_filtered.columns]
        st.dataframe(df_filtered[cols_show].reset_index(drop=True), use_container_width=True, height=260)

# ─────────────────────────────────────────────
# MONITOR DE MERCADOS
# ─────────────────────────────────────────────
def render_mercados():
    page_hero("📊 Análisis de mercado", "Monitor de Mercados", "Comparativa de precios locales vs internacionales")

    df_p = load("precios_agricolas",       order_col="fecha", limit=300)
    df_c = load("v_comparativa_mercados",  order_col="fecha", limit=100)

    # ── Filtros en la parte superior ──
    f1, f2 = st.columns([1, 2])
    with f1:
        sector_opts = ["Todos"]
        if not df_p.empty and "sector" in df_p.columns:
            sector_opts += sorted(df_p["sector"].dropna().unique().tolist())
        filtro_sector = st.selectbox("Sector", sector_opts)
    with f2:
        buscar_prod = st.text_input("🔍 Buscar mercado", placeholder="Nombre del mercado o producto...")

    # ── KPIs ──
    # Calcular Al Alza / A la Baja desde v_comparativa_mercados (diferencial_arbitraje)
    n_emparejados = 0
    al_alza_merc = 0
    a_la_baja_merc = 0
    ultimo = None

    if not df_p.empty and "fecha" in df_p.columns:
        df_p["fecha"] = pd.to_datetime(df_p["fecha"])
        ultimo = df_p["fecha"].max()

    if not df_c.empty:
        df_c["fecha"] = pd.to_datetime(df_c["fecha"])
        df_ult_c_kpi = df_c.sort_values("fecha").groupby("producto").last().reset_index()
        n_emparejados = len(df_ult_c_kpi)
        if "diferencial_arbitraje" in df_ult_c_kpi.columns:
            al_alza_merc   = int((df_ult_c_kpi["diferencial_arbitraje"].fillna(0) > 0).sum())
            a_la_baja_merc = int((df_ult_c_kpi["diferencial_arbitraje"].fillna(0) < 0).sum())

    c1, c2, c3, c4 = st.columns(4)
    kpi_card(c1, "kpi-green", "📅",
             ultimo.strftime("%d/%m/%y") if ultimo is not None else "—",
             "Última cotización",
             f"{len(df_p[df_p['fecha'] == ultimo]) if ultimo is not None and not df_p.empty else 0} productos")
    kpi_card(c2, "kpi-earth", "🔗", str(n_emparejados), "Mercados Emparejados", "Local vs Internacional")
    kpi_card(c3, "kpi-green", "📈", str(al_alza_merc),  "Al alza",   "Diferencial positivo")
    kpi_card(c4, "kpi-red",   "📉", str(a_la_baja_merc), "A la baja", "Diferencial negativo")
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── Dataset filtrado compartido (afecta gráfico Y tabla) ──
    df_vis = pd.DataFrame()
    if not df_c.empty:
        df_vis = df_c.sort_values("fecha").groupby("producto").last().reset_index()
        if buscar_prod:
            df_vis = df_vis[df_vis["producto"].str.contains(buscar_prod, case=False, na=False)]
        if filtro_sector != "Todos" and "sector" in df_vis.columns:
            df_vis = df_vis[df_vis["sector"] == filtro_sector]

    # ── Gráfico comparativo Precio Local vs Internacional ──
    section_header("📊", "Precios: Local vs Internacional (€/kg)", "Comparativa por producto — filtros aplicados")

    if not df_vis.empty and "precio_local_kg" in df_vis.columns:
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            name="Precio Local",
            x=df_vis["producto"],
            y=df_vis["precio_local_kg"],
            marker_color="#27a05e",
            opacity=0.9,
            hovertemplate="<b>%{x}</b><br>Local: %{y:.2f} €/kg<extra></extra>",
        ))
        fig_bar.add_trace(go.Bar(
            name="Precio Internacional",
            x=df_vis["producto"],
            y=df_vis["precio_internacional_kg"],
            marker_color="#2d2d2d",
            opacity=0.85,
            hovertemplate="<b>%{x}</b><br>Internacional: %{y:.2f} €/kg<extra></extra>",
        ))
        layout_bar = {**CHART_LAYOUT}
        layout_bar["barmode"] = "group"
        layout_bar["xaxis"] = dict(showgrid=False, color="#0d2b1a", tickfont=dict(color="#0d2b1a", size=11))
        layout_bar["yaxis"] = dict(gridcolor="#e8f5ee", color="#7aa98e", title="€/kg")
        layout_bar["legend"] = dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
            font=dict(size=12, color="#0d2b1a"),
            bgcolor="rgba(255,255,255,0.85)", bordercolor="#d1ead9", borderwidth=1,
        )
        fig_bar.update_layout(height=320, **layout_bar)
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
    elif df_vis.empty:
        st.info("No hay datos que coincidan con los filtros aplicados")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Tabla "Precios del Día" ──
    fecha_str_header = ultimo.strftime('%Y-%m-%d') if ultimo is not None else '—'
    section_header("🗓️", "Precios del Día", f"Última actualización: {fecha_str_header}")

    if not df_vis.empty:
        # Botón exportar
        cols_export = [c for c in ["producto", "precio_local_kg", "precio_internacional_kg",
                                    "diferencial_arbitraje", "sector", "relacion", "fecha"] if c in df_vis.columns]
        csv_data = df_vis[cols_export].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Exportar tabla CSV",
            data=csv_data,
            file_name=f"monitor_mercados_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            key="export_mercados",
        )
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

        # Cabecera tabla
        st.markdown("""
        <div style="display:grid;grid-template-columns:2fr 1.5fr 1.5fr 1.5fr 1fr;gap:8px;
                    padding:10px 20px;background:#f0faf4;border-radius:10px 10px 0 0;
                    border:1px solid var(--border);border-bottom:2px solid var(--border);margin-bottom:2px;">
            <span style="font-size:0.75rem;font-weight:700;color:#0d2b1a;text-transform:uppercase;letter-spacing:0.06em;">Producto</span>
            <span style="font-size:0.75rem;font-weight:700;color:#0d2b1a;text-transform:uppercase;letter-spacing:0.06em;">Local (€/kg)</span>
            <span style="font-size:0.75rem;font-weight:700;color:#0d2b1a;text-transform:uppercase;letter-spacing:0.06em;">Internacional (€/kg)</span>
            <span style="font-size:0.75rem;font-weight:700;color:#0d2b1a;text-transform:uppercase;letter-spacing:0.06em;">Diferencial</span>
            <span style="font-size:0.75rem;font-weight:700;color:#0d2b1a;text-transform:uppercase;letter-spacing:0.06em;">Tendencia</span>
        </div>
        """, unsafe_allow_html=True)

        for _, row in df_vis.iterrows():
            dif   = float(row.get("diferencial_arbitraje", 0) or 0)
            local = float(row.get("precio_local_kg", 0) or 0)
            intl  = float(row.get("precio_internacional_kg", 0) or 0)
            sign  = "+" if dif > 0 else ""
            b_bg  = "#dcfce7" if dif > 0 else "#fee2e2"
            b_col = "#15803d" if dif > 0 else "#b91c1c"
            if dif > 0:
                tend_svg = """<svg width="22" height="16" viewBox="0 0 22 16"><polyline points="2,13 8,7 13,10 20,3" fill="none" stroke="#27a05e" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><polyline points="15,3 20,3 20,8" fill="none" stroke="#27a05e" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>"""
            elif dif < 0:
                tend_svg = """<svg width="22" height="16" viewBox="0 0 22 16"><polyline points="2,3 8,9 13,6 20,13" fill="none" stroke="#ef4444" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><polyline points="15,13 20,13 20,8" fill="none" stroke="#ef4444" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>"""
            else:
                tend_svg = """<svg width="22" height="16" viewBox="0 0 22 16"><polyline points="2,8 20,8" fill="none" stroke="#f59e0b" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>"""

            st.markdown(f"""
            <div style="display:grid;grid-template-columns:2fr 1.5fr 1.5fr 1.5fr 1fr;gap:8px;
                        align-items:center;padding:14px 20px;background:white;
                        border:1px solid var(--border);border-top:none;margin-bottom:0;
                        transition:background 0.15s;">
                <span style="font-weight:600;font-size:0.9rem;color:#0d2b1a;">{row.get('producto','—')}</span>
                <span style="font-family:'DM Mono',monospace;font-size:0.88rem;color:#1a5c38;">{local:.2f} €/kg</span>
                <span style="font-family:'DM Mono',monospace;font-size:0.88rem;color:#475569;">{intl:.2f} €/kg</span>
                <span style="display:inline-flex;align-items:center;">
                    <span style="background:{b_bg};color:{b_col};font-weight:700;font-size:0.82rem;
                                 padding:4px 12px;border-radius:20px;font-family:'DM Mono',monospace;">
                        {sign}{dif:.2f} €/kg
                    </span>
                </span>
                <span>{tend_svg}</span>
            </div>
            """, unsafe_allow_html=True)

    elif not df_p.empty:
        df_tab = df_p.copy()
        if buscar_prod:
            df_tab = df_tab[df_tab["producto"].str.contains(buscar_prod, case=False, na=False)]
        if filtro_sector != "Todos" and "sector" in df_tab.columns:
            df_tab = df_tab[df_tab["sector"] == filtro_sector]
        cols_show = [c for c in ["fecha","sector","producto","precio_min","precio_max","unidad","variacion_p"] if c in df_tab.columns]
        st.download_button("⬇️ Exportar CSV", df_tab[cols_show].to_csv(index=False).encode("utf-8"),
                           f"mercados_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv", key="export_merc_fb")
        st.dataframe(df_tab[cols_show].sort_values("fecha", ascending=False).reset_index(drop=True),
                     use_container_width=True, height=300)
    else:
        st.info("Sin datos de mercados disponibles")

# ─────────────────────────────────────────────
# MONITOR DE PRODUCTOS INTERNACIONALES
# ─────────────────────────────────────────────
def render_monitor_productos():
    page_hero("🌐 Mercados Internacionales", "Monitor de Productos", "Seguimiento de precios internacionales por categoría")

    df = load("v_monitor_productos", order_col="fecha", limit=500)

    # ── Filtros ──
    f1, f2, f3 = st.columns([1, 1, 2])
    with f1:
        cat_opts = ["Todas"]
        if not df.empty and "categoria" in df.columns:
            cat_opts += sorted(df["categoria"].dropna().unique().tolist())
        filtro_cat = st.selectbox("Categoría", cat_opts)
    with f2:
        tend_opts = ["Todas"]
        if not df.empty and "tendencia" in df.columns:
            tend_opts += sorted(df["tendencia"].dropna().unique().tolist())
        filtro_tend = st.selectbox("Tendencia", tend_opts)
    with f3:
        buscar_prod = st.text_input("🔍 Buscar producto", placeholder="Nombre del producto...")

    # ── KPIs ──
    ultimo_prod = None
    n_productos_int = 0
    n_alza = 0
    n_baja = 0

    if not df.empty:
        if "fecha" in df.columns:
            df["fecha"] = pd.to_datetime(df["fecha"])
            ultimo_prod = df["fecha"].max()
        if "producto" in df.columns:
            n_productos_int = df["producto"].nunique()
        if "tendencia" in df.columns:
            tend_lower = df.groupby("producto")["fecha"].idxmax().map(lambda i: str(df.loc[i, "tendencia"]).lower() if i in df.index else "")
            n_alza = int((tend_lower.str.contains("alza|sube|alcista|up|positiv", na=False)).sum())
            n_baja = int((tend_lower.str.contains("baja|baj|bajista|down|negativ", na=False)).sum())

    c1, c2, c3, c4 = st.columns(4)
    kpi_card(c1, "kpi-green", "📅",
             ultimo_prod.strftime("%d/%m/%y") if ultimo_prod is not None else "—",
             "Última cotización", "Fecha más reciente")
    kpi_card(c2, "kpi-blue",  "🌐", str(n_productos_int), "Productos Internacionales", "En seguimiento")
    kpi_card(c3, "kpi-green", "📈", str(n_alza),  "En Alza",  "Tendencia positiva")
    kpi_card(c4, "kpi-red",   "📉", str(n_baja),  "En Baja",  "Tendencia negativa")
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ── Aplicar filtros al dataframe ──
    df_f = df.copy()
    if filtro_cat != "Todas" and "categoria" in df_f.columns:
        df_f = df_f[df_f["categoria"] == filtro_cat]
    if filtro_tend != "Todas" and "tendencia" in df_f.columns:
        df_f = df_f[df_f["tendencia"] == filtro_tend]
    if buscar_prod and "producto" in df_f.columns:
        df_f = df_f[df_f["producto"].str.contains(buscar_prod, case=False, na=False)]

    # ── Gráfico Timeline — variación de precios por categoría ──
    section_header("📈", "Variación de Precios por Categoría", "Evolución del precio_cierre por fecha y categoría — filtros aplicados")

    if not df_f.empty and "fecha" in df_f.columns and "precio_cierre" in df_f.columns and "categoria" in df_f.columns:
        df_chart = df_f.copy()
        df_chart["precio_cierre"] = pd.to_numeric(df_chart["precio_cierre"], errors="coerce")
        df_chart = df_chart.dropna(subset=["precio_cierre", "fecha"])
        df_chart = df_chart.sort_values("fecha")

        # Media de precio_cierre por fecha+categoría (sin agrupar en periodos, fecha exacta)
        df_grouped = (
            df_chart.groupby(["fecha", "categoria"])["precio_cierre"]
            .mean().reset_index()
        )

        categorias = df_grouped["categoria"].dropna().unique()
        palette = ["#27a05e", "#f59e0b", "#3b82f6", "#ef4444", "#8b5e34", "#a855f7", "#0ea5e9", "#f97316"]
        fig = go.Figure()

        for i, cat in enumerate(categorias):
            sub = df_grouped[df_grouped["categoria"] == cat].sort_values("fecha")
            color = palette[i % len(palette)]
            r_c, g_c, b_c = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
            fig.add_trace(go.Scatter(
                x=sub["fecha"],
                y=sub["precio_cierre"],
                name=str(cat),
                line=dict(color=color, width=2.2),
                mode="lines+markers",
                marker=dict(size=5, color=color),
                hovertemplate=(
                    f"<b>{cat}</b><br>"
                    "%{x|%d/%m/%Y}<br>"
                    "Precio: <b>%{y:.4f}</b><extra></extra>"
                ),
            ))

        layout_t = {**CHART_LAYOUT}
        layout_t["xaxis"] = dict(
            showgrid=True, gridcolor="#e8f5ee",
            color="#0d2b1a", tickfont=dict(color="#0d2b1a", size=11),
            tickformat="%d/%m/%y", title="",
        )
        layout_t["yaxis"] = dict(
            gridcolor="#e8f5ee", color="#0d2b1a",
            tickfont=dict(color="#0d2b1a", size=11),
            title="Precio cierre",
        )
        layout_t["legend"] = dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
            font=dict(size=12, color="#0d2b1a"),
            bgcolor="rgba(255,255,255,0.9)", bordercolor="#d1ead9", borderwidth=1,
        )
        layout_t["hovermode"] = "x unified"
        layout_t["margin"] = dict(l=0, r=0, t=50, b=0)
        fig.update_layout(height=380, **layout_t)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    elif df_f.empty:
        st.info("No hay datos que coincidan con los filtros aplicados")
    else:
        st.info("Sin datos suficientes para el gráfico de evolución")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Tabla: Evolución de Productos Internacionales ──
    fecha_header = ultimo_prod.strftime("%Y-%m-%d") if ultimo_prod is not None else "—"
    section_header("📋", "Evolución de Productos Internacionales", f"Última actualización: {fecha_header}")

    if not df_f.empty:
        cols_tabla = [c for c in ["fecha", "producto", "precio_cierre", "moneda", "var_precio", "categoria", "tendencia"]
                      if c in df_f.columns]

        # Botón exportar
        csv_data = df_f[cols_tabla].sort_values("fecha", ascending=False).to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Exportar tabla CSV",
            data=csv_data,
            file_name=f"monitor_productos_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            key="export_productos",
        )
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

        # Cabecera de tabla personalizada
        col_widths = "1.2fr " + " ".join(["1.4fr"] * (len(cols_tabla) - 1))
        col_labels = {
            "fecha": "Fecha", "producto": "Producto", "precio_cierre": "Precio Cierre",
            "moneda": "Moneda", "var_precio": "Var. Precio", "categoria": "Categoría", "tendencia": "Tendencia",
        }
        header_html = "".join([
            f'<span style="font-size:0.75rem;font-weight:700;color:#0d2b1a;text-transform:uppercase;letter-spacing:0.06em;">{col_labels.get(c, c)}</span>'
            for c in cols_tabla
        ])
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:{col_widths};gap:8px;
                    padding:10px 20px;background:#f0faf4;border-radius:10px 10px 0 0;
                    border:1px solid var(--border);border-bottom:2px solid var(--border);margin-bottom:2px;">
            {header_html}
        </div>
        """, unsafe_allow_html=True)

        df_tabla = df_f[cols_tabla].sort_values("fecha", ascending=False).head(100).reset_index(drop=True)

        for _, row in df_tabla.iterrows():
            tend_val = str(row.get("tendencia", "") or "").lower()
            var_val  = row.get("var_precio", None)

            if any(x in tend_val for x in ["alza", "sube", "alcista", "up", "positiv"]):
                tend_bg, tend_col, tend_svg = "#dcfce7", "#15803d", \
                    '<svg width="18" height="14" viewBox="0 0 22 16"><polyline points="2,13 8,7 13,10 20,3" fill="none" stroke="#27a05e" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><polyline points="15,3 20,3 20,8" fill="none" stroke="#27a05e" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
            elif any(x in tend_val for x in ["baja", "bajista", "down", "negativ"]):
                tend_bg, tend_col, tend_svg = "#fee2e2", "#b91c1c", \
                    '<svg width="18" height="14" viewBox="0 0 22 16"><polyline points="2,3 8,9 13,6 20,13" fill="none" stroke="#ef4444" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><polyline points="15,13 20,13 20,8" fill="none" stroke="#ef4444" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
            else:
                tend_bg, tend_col, tend_svg = "#fef3c7", "#b45309", \
                    '<svg width="18" height="14" viewBox="0 0 22 16"><line x1="2" y1="8" x2="20" y2="8" stroke="#f59e0b" stroke-width="2.2" stroke-linecap="round"/></svg>'

            try:
                var_f = float(var_val) if var_val is not None else None
                var_str = (f"+{var_f:.2f}%" if var_f > 0 else f"{var_f:.2f}%") if var_f is not None else "—"
                var_color = "#15803d" if (var_f or 0) > 0 else ("#b91c1c" if (var_f or 0) < 0 else "#475569")
            except Exception:
                var_str, var_color = str(var_val or "—"), "#475569"

            try:
                precio_f = float(row.get("precio_cierre", 0) or 0)
                precio_str = f"{precio_f:.4f}"
            except Exception:
                precio_str = str(row.get("precio_cierre", "—"))

            fecha_v = row.get("fecha", "")
            try:
                fecha_str = pd.to_datetime(fecha_v).strftime("%d/%m/%Y")
            except Exception:
                fecha_str = str(fecha_v)

            cells = []
            for c in cols_tabla:
                if c == "fecha":
                    cells.append(f'<span style="font-family:\'DM Mono\',monospace;font-size:0.8rem;color:#7aa98e;">{fecha_str}</span>')
                elif c == "producto":
                    cells.append(f'<span style="font-weight:600;font-size:0.88rem;color:#0d2b1a;">{row.get("producto","—")}</span>')
                elif c == "precio_cierre":
                    cells.append(f'<span style="font-family:\'DM Mono\',monospace;font-size:0.88rem;color:#1a5c38;font-weight:600;">{precio_str}</span>')
                elif c == "moneda":
                    cells.append(f'<span style="font-size:0.82rem;color:#475569;font-weight:500;">{row.get("moneda","—")}</span>')
                elif c == "var_precio":
                    cells.append(f'<span style="font-family:\'DM Mono\',monospace;font-size:0.85rem;font-weight:700;color:{var_color};">{var_str}</span>')
                elif c == "categoria":
                    cells.append(f'<span style="font-size:0.82rem;color:#1a5c38;background:#f0faf4;padding:2px 8px;border-radius:6px;font-weight:600;">{row.get("categoria","—")}</span>')
                elif c == "tendencia":
                    cells.append(f'<span style="display:inline-flex;align-items:center;gap:6px;background:{tend_bg};color:{tend_col};font-weight:700;font-size:0.78rem;padding:3px 10px;border-radius:20px;">{tend_svg} {str(row.get("tendencia","—")).upper()}</span>')

            cells_html = "".join([f"<span>{cell}</span>" for cell in cells])
            st.markdown(f"""
            <div style="display:grid;grid-template-columns:{col_widths};gap:8px;
                        align-items:center;padding:12px 20px;background:white;
                        border:1px solid var(--border);border-top:none;
                        transition:background 0.15s;">
                {cells_html}
            </div>
            """, unsafe_allow_html=True)

        if len(df_f) > 100:
            st.caption(f"Mostrando los 100 registros más recientes de {len(df_f)} totales.")
    else:
        st.info("Sin datos disponibles con los filtros seleccionados")


# ─────────────────────────────────────────────
# ─────────────────────────────────────────────
def render_alertas():
    page_hero("🔔 Notificaciones", "Centro de Alertas", "Clima extremo y energía — actualizados automáticamente")

    df_clima = load("v_alertas_clima_extrema", order_col="fecha")
    df_energ = load("v_alertas_energia",       order_col="fecha")

    c1, c2, c3, c4 = st.columns(4)
    n_cl = int(df_clima["alerta_riesgo"].notna().sum()) if not df_clima.empty and "alerta_riesgo" in df_clima.columns else 0
    n_en = int(df_energ["estado_costo"].str.contains("caro|alto|punta", case=False, na=False).sum()) if not df_energ.empty and "estado_costo" in df_energ.columns else 0

    kpi_card(c1, "kpi-red"   if n_cl > 0 else "kpi-green", "🌩️", str(n_cl), "Alertas clima",   "Temperatura extrema")
    kpi_card(c2, "kpi-amber" if n_en > 0 else "kpi-green", "⚡", str(n_en), "Alertas energía", "kWh elevado")
    kpi_card(c3, "kpi-blue", "📋", str(len(df_clima)), "Registros clima",   "Disponibles")
    kpi_card(c4, "kpi-blue", "🕐", str(len(df_energ)), "Registros energía", "Disponibles")

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    col_cl, col_en = st.columns(2)

    with col_cl:
        section_header("🌩️", "Alertas de Clima Extremo", "v_alertas_clima_extrema")
        if not df_clima.empty:
            df_c = df_clima.copy()
            df_c["fecha"] = pd.to_datetime(df_c["fecha"])
            df_c = df_c.sort_values("fecha", ascending=False)
            for _, row in df_c.head(10).iterrows():
                alerta = str(row.get("alerta_riesgo", "") or "")
                alerta_l = alerta.lower()
                if not alerta or alerta_l in ["none", "nan", ""]:
                    dot, cls = "dot-green", "alert-ok"
                    alerta = "Sin alerta"
                elif any(x in alerta_l for x in ["alta", "extremo", "peligro", "rojo"]):
                    dot, cls = "dot-red", "alert-critical"
                else:
                    dot, cls = "dot-amber", "alert-warning"
                fecha_str = row["fecha"].strftime("%d/%m/%Y") if hasattr(row["fecha"], "strftime") else str(row["fecha"])
                st.markdown(f"""
                <div class="alert-item {cls}">
                    <div class="alert-dot {dot}"></div>
                    <div style="flex:1">
                        <div class="alert-title">{row.get('estacion','—')}</div>
                        <div class="alert-desc">🌡️ Máx: <b>{row.get('temp_max','—')}°C</b> | Mín: <b>{row.get('temp_min','—')}°C</b></div>
                        <div class="alert-desc" style="margin-top:3px;">{alerta}</div>
                        <div class="alert-time">📅 {fecha_str}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Gráfica temp max/min
            if len(df_c) > 3:
                df_plot = df_c.sort_values("fecha").tail(30)
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=df_plot["fecha"], y=df_plot["temp_max"],
                    name="Máx", line=dict(color="#ef4444", width=2), fill="tonexty"))
                fig.add_trace(go.Scatter(x=df_plot["fecha"], y=df_plot["temp_min"],
                    name="Mín", line=dict(color="#3b82f6", width=2)))
                fig.update_layout(height=200, **CHART_LAYOUT)
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Sin alertas de clima disponibles")

    with col_en:
        section_header("⚡", "Alertas de Energía", "v_alertas_energia — precio €/kWh por tramo")
        if not df_energ.empty:
            df_e = df_energ.copy()
            df_e["fecha"] = pd.to_datetime(df_e["fecha"])
            df_e = df_e.sort_values(["fecha", "hora"], ascending=False)
            for _, row in df_e.head(10).iterrows():
                estado = str(row.get("estado_costo", "") or "").lower()
                if any(x in estado for x in ["caro", "alto", "punta"]):
                    dot, cls = "dot-red", "alert-critical"
                elif any(x in estado for x in ["medio", "llano"]):
                    dot, cls = "dot-amber", "alert-warning"
                else:
                    dot, cls = "dot-green", "alert-ok"
                vs_med = float(row.get("vs_media", 0) or 0)
                sign   = "+" if vs_med > 0 else ""
                fecha_str = row["fecha"].strftime("%d/%m/%Y") if hasattr(row["fecha"], "strftime") else str(row["fecha"])
                st.markdown(f"""
                <div class="alert-item {cls}">
                    <div class="alert-dot {dot}"></div>
                    <div style="flex:1">
                        <div class="alert-title">Hora {row.get('hora','—')}:00 — {row.get('tramo','—')}</div>
                        <div class="alert-desc">⚡ <b class="mono">{row.get('precio_kwh','—')} €/kWh</b> &nbsp;| vs media: <b>{sign}{vs_med:.3f} €</b></div>
                        <div class="alert-desc">{row.get('estado_costo','—')}</div>
                        <div class="alert-time">📅 {fecha_str}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Gráfica precio por hora (último día)
            df_ult_dia = df_e[df_e["fecha"] == df_e["fecha"].max()].sort_values("hora")
            if not df_ult_dia.empty and "hora" in df_ult_dia.columns:
                colores_h = df_ult_dia["tramo"].apply(lambda t:
                    "#ef4444" if "punta" in str(t).lower()
                    else "#f59e0b" if "llano" in str(t).lower()
                    else "#27a05e"
                ) if "tramo" in df_ult_dia.columns else ["#27a05e"] * len(df_ult_dia)
                fig2 = go.Figure(go.Bar(
                    x=df_ult_dia["hora"], y=df_ult_dia["precio_kwh"],
                    marker_color=colores_h, opacity=0.85,
                    hovertemplate="Hora %{x}:00<br>%{y} €/kWh<extra></extra>",
                ))
                layout2 = {**CHART_LAYOUT}
                layout2["xaxis"] = dict(showgrid=False, color="#7aa98e", title="Hora del día")
                layout2["yaxis"] = dict(gridcolor="#e8f5ee", color="#7aa98e", title="€/kWh")
                fig2.update_layout(height=200, **layout2)
                st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Sin alertas de energía disponibles")

# ─────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────
def render_configuracion():
    page_hero("⚙️ Ajustes", "Configuración del Sistema", "Secrets de Supabase, AEMET y diagnóstico de conexiones")

    col1, col2 = st.columns(2)

    with col1:
        section_header("🔐", "Estado de conexiones", "Verificación en tiempo real")

        # Test Supabase
        try:
            sb = get_supabase()
            sb.table("datos_clima").select("id").limit(1).execute()
            st.markdown("""<div class="alert-item alert-ok">
                <div class="alert-dot dot-green"></div>
                <div><div class="alert-title">✅ Supabase conectado</div>
                <div class="alert-desc">Lectura de tablas OK</div></div></div>""", unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f"""<div class="alert-item alert-critical">
                <div class="alert-dot dot-red"></div>
                <div><div class="alert-title">❌ Supabase no conectado</div>
                <div class="alert-desc">{str(e)[:120]}</div></div></div>""", unsafe_allow_html=True)

        # Test AEMET
        try:
            ak = st.secrets["AEMET_KEY"]
            st.markdown("""<div class="alert-item alert-ok">
                <div class="alert-dot dot-green"></div>
                <div><div class="alert-title">✅ AEMET configurado</div>
                <div class="alert-desc">API key presente en secrets</div></div></div>""", unsafe_allow_html=True)
        except Exception:
            st.markdown("""<div class="alert-item alert-warning">
                <div class="alert-dot dot-amber"></div>
                <div><div class="alert-title">⚠️ AEMET no configurado</div>
                <div class="alert-desc">Añade AEMET_KEY en Streamlit Secrets</div></div></div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        section_header("📖", "Cómo configurar secrets", "")
        st.markdown("""
        <div style="background:#f0faf4;border:1px solid #d1ead9;border-radius:12px;padding:16px 20px;font-size:0.82rem;color:#1a5c38;line-height:1.9;">
        <b>1.</b> En Streamlit Cloud → tu app → <b>Settings → Secrets</b><br>
        <b>2.</b> Pega el siguiente bloque (reemplaza las claves):
        </div>
        """, unsafe_allow_html=True)
        st.code(
            'SUPABASE_URL = "https://zzucvsremavkikecsptg.supabase.co"\n'
            'SUPABASE_KEY = "tu_clave_supabase"\n'
            'AEMET_KEY    = "tu_clave_aemet"',
            language="toml"
        )
        st.warning("⚠️ Nunca pongas las claves directamente en el código Python. Los Secrets de Streamlit Cloud son cifrados y nunca se suben a GitHub.")

    with col2:
        section_header("📊", "Tablas y vistas disponibles", "Estado de cada fuente de datos")

        tablas = [
            ("datos_clima",             "🌤️", "Meteorología histórica",     "13 cols"),
            ("datos_energia",           "⚡", "Precios energía eléctrica",  "7 cols"),
            ("precios_agricolas",       "🌾", "Precios lonja",              "14 cols"),
            ("mercados_internacionales","🌍", "Mercados internacionales",   "9 cols"),
            ("mapeo_productos",         "🗂️", "Catálogo productos",        "4 cols"),
            ("v_mapa_operaciones",      "📍", "Vista mapa estaciones",      "12 cols"),
            ("v_salud_sectores",        "💚", "Vista salud sectores",       "6 cols"),
            ("v_alertas_clima_extrema", "🌩️", "Vista alertas clima",       "5 cols"),
            ("v_alertas_energia",       "⚡", "Vista alertas energía",      "6 cols"),
            ("v_comparativa_mercados",  "📊", "Vista comparativa",          "6 cols"),
        ]
        sb = get_supabase()
        for tabla, icon, desc, cols_info in tablas:
            n, color = "—", "#ef4444"
            if sb:
                try:
                    r = sb.table(tabla).select("*", count="exact").limit(1).execute()
                    n = str(r.count) if r.count is not None else "✓"
                    color = "#27a05e"
                except:
                    n, color = "err", "#f59e0b"
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;padding:9px 14px;background:white;
                        border-radius:10px;border:1px solid var(--border);margin-bottom:6px;">
                <span>{icon}</span>
                <div style="flex:1;">
                    <div style="font-weight:600;font-size:0.82rem;color:#0d2b1a;font-family:'DM Mono',monospace;">{tabla}</div>
                    <div style="font-size:0.72rem;color:#7aa98e;">{desc} · {cols_info}</div>
                </div>
                <span style="font-family:'DM Mono',monospace;font-size:0.85rem;font-weight:700;color:{color};">{n}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        if st.button("🔄 Limpiar caché y reconectar", use_container_width=True):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.success("Caché limpiada. Reconectando...")
            st.rerun()

# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        render_login()
        return

    page = render_sidebar()

    try:
        if   "Dashboard"   in page: render_dashboard()
        elif "Mapa"        in page: render_mapa()
        elif "Mercados"    in page: render_mercados()
        elif "Productos"   in page: render_monitor_productos()
        elif "Alertas"     in page: render_alertas()
        elif "Configuraci" in page: render_configuracion()
    except Exception as e:
        st.error(f"Error al cargar la sección: {e}")
        st.info("Pulsa '🔄 Recargar datos' en el menú lateral o recarga la página.")

if __name__ == "__main__":
    main()
