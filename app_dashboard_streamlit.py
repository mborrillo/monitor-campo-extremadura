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
section[data-testid="stSidebar"] * { color: #d6f5e5 !important; }
section[data-testid="stSidebar"] .stRadio label {
    background: rgba(255,255,255,0.05) !important; border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: var(--radius-sm) !important; padding: 10px 16px !important;
    margin: 3px 0 !important; cursor: pointer !important; transition: all 0.2s ease !important;
}
section[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(63,189,118,0.15) !important; border-color: var(--green-400) !important;
}
#MainMenu, footer, header { visibility: hidden; }
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
    font=dict(family="Plus Jakarta Sans"),
    margin=dict(l=0, r=0, t=0, b=0),
    xaxis=dict(showgrid=False, color="#7aa98e"),
    yaxis=dict(gridcolor="#e8f5ee", color="#7aa98e"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
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
            "🗺️  Mapa de Estaciones",
            "📊  Mercados & Precios",
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

        st.markdown("""
        <div style="position:absolute;bottom:20px;left:0;right:0;text-align:center;font-size:0.68rem;color:rgba(214,245,229,0.3);">
            AgroTech Extremadura v2.0
        </div>
        """, unsafe_allow_html=True)

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
        n_alerta = int(df_ac["alerta_riesgo"].notna().sum())

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
            fig = px.line(df_plot.sort_values("fecha"),
                          x="fecha", y="temp_actual", color="estacion",
                          color_discrete_sequence=COLORS,
                          labels={"fecha": "", "temp_actual": "°C", "estacion": ""})
            fig.update_traces(line=dict(width=2.5))
            fig.update_layout(height=290, **CHART_LAYOUT)
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
# MAPA DE ESTACIONES
# ─────────────────────────────────────────────
def render_mapa():
    page_hero("🗺️ Geolocalización", "Mapa de Estaciones", "Red de monitorización agrometeorológica de Extremadura")

    df = load("v_mapa_operaciones")

    if df.empty or "latitud" not in df.columns:
        st.warning("Sin datos de localización en v_mapa_operaciones")
        return

    col_m, col_d = st.columns([2, 1])

    with col_m:
        section_header("📍", "Estaciones activas", "Coloreadas por tramo energético")

        def color_tramo(t):
            t = str(t or "").lower()
            if "punta" in t: return "#ef4444"
            if "llano" in t: return "#f59e0b"
            return "#27a05e"

        df["_color"] = df["tramo_energia"].apply(color_tramo) if "tramo_energia" in df.columns else "#27a05e"

        try:
            fig = go.Figure()
            for tramo_val in (df["tramo_energia"].unique() if "tramo_energia" in df.columns else ["—"]):
                sub = df[df["tramo_energia"] == tramo_val] if "tramo_energia" in df.columns else df
                fig.add_trace(go.Scattermapbox(
                    lat=sub["latitud"], lon=sub["longitud"],
                    mode="markers+text",
                    marker=dict(size=16, color=sub["_color"], opacity=0.9),
                    text=sub["estacion"].astype(str).str[:10] if "estacion" in sub.columns else "",
                    textposition="top right",
                    textfont=dict(size=10),
                    hovertext=sub.apply(lambda r:
                        f"<b>{r.get('estacion','—')}</b><br>"
                        f"🌡️ {r.get('temp_actual','—')}°C | 💧 {r.get('humedad','—')}%<br>"
                        f"⚡ {r.get('precio_kwh','—')} €/kWh | {r.get('tramo_energia','—')}<br>"
                        f"💧 {r.get('recomendacion_riego','—')}", axis=1),
                    hoverinfo="text",
                    name=str(tramo_val),
                ))
            fig.update_layout(
                mapbox=dict(style="open-street-map",
                            center=dict(lat=df["latitud"].mean(), lon=df["longitud"].mean()),
                            zoom=7),
                height=450, margin=dict(l=0,r=0,t=0,b=0),
                legend=dict(orientation="h", yanchor="top", y=0.01, xanchor="left", x=0.01,
                            bgcolor="rgba(255,255,255,0.9)"),
                paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        except Exception:
            # Fallback
            st.map(df.rename(columns={"latitud": "lat", "longitud": "lon"})[["lat","lon"]], zoom=7)

    with col_d:
        section_header("📋", "Detalle por estación", "Datos actuales")
        for _, row in df.iterrows():
            tramo = str(row.get("tramo_energia", "")).lower()
            b_cls = "badge-red" if "punta" in tramo else ("badge-amber" if "llano" in tramo else "badge-green")
            st.markdown(f"""
            <div class="data-row">
                <div style="flex:1;">
                    <div style="font-weight:700;font-size:0.88rem;color:#0d2b1a;">{row.get('estacion','—')}</div>
                    <div style="font-size:0.75rem;color:#7aa98e;margin-top:3px;">
                        🌡️ {row.get('temp_actual','—')}°C &nbsp;
                        💧 {row.get('humedad','—')}% &nbsp;
                        🌬️ {row.get('viento_vel','—')} km/h
                    </div>
                    <div style="font-size:0.72rem;color:#7aa98e;margin-top:2px;">
                        🌧️ {row.get('precipitacion','—')} mm &nbsp;⚡ {row.get('precio_kwh','—')} €/kWh
                    </div>
                </div>
                <span class="badge {b_cls}">{row.get('tramo_energia','—')}</span>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MERCADOS & PRECIOS
# ─────────────────────────────────────────────
def render_mercados():
    page_hero("📊 Análisis de mercado", "Mercados & Precios", "Precios agrícolas locales vs internacionales — lonja de Extremadura")

    df_p = load("precios_agricolas",       order_col="fecha", limit=300)
    df_c = load("v_comparativa_mercados",  order_col="fecha", limit=100)

    # ── KPIs ──
    if not df_p.empty and "fecha" in df_p.columns:
        df_p["fecha"] = pd.to_datetime(df_p["fecha"])
        ultimo  = df_p["fecha"].max()
        df_hoy  = df_p[df_p["fecha"] == ultimo]
        subidas = int((df_hoy["variacion_p"] > 0).sum()) if "variacion_p" in df_hoy.columns else 0
        bajadas = int((df_hoy["variacion_p"] < 0).sum()) if "variacion_p" in df_hoy.columns else 0
        c1,c2,c3,c4 = st.columns(4)
        kpi_card(c1, "kpi-green", "📅", ultimo.strftime("%d/%m/%y"), "Última cotización", f"{len(df_hoy)} productos")
        kpi_card(c2, "kpi-earth", "🌾", str(len(df_hoy)), "Productos cotizando", "Lonja Extremadura")
        kpi_card(c3, "kpi-green", "📈", str(subidas), "Al alza", "vs día anterior")
        kpi_card(c4, "kpi-red",   "📉", str(bajadas), "A la baja", "vs día anterior")
        st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        section_header("🏷️", "Precios por producto", "Última cotización disponible")
        if not df_p.empty and "precio_max" in df_p.columns:
            df_ult = df_p.sort_values("fecha").groupby("producto").last().reset_index()
            df_ult = df_ult.sort_values("precio_max", ascending=True).tail(15)
            colors_bar = ["#27a05e" if (v or 0) >= 0 else "#ef4444"
                          for v in df_ult.get("variacion_p", [0]*len(df_ult))]
            fig = go.Figure(go.Bar(
                x=df_ult["precio_max"], y=df_ult["producto"],
                orientation="h",
                marker=dict(color=colors_bar, opacity=0.85),
                text=[f"+{v:.1f}%" if (v or 0) > 0 else f"{v:.1f}%"
                      for v in df_ult.get("variacion_p", [0]*len(df_ult))],
                textposition="outside",
                hovertemplate="<b>%{y}</b><br>%{x} €/kg<extra></extra>",
            ))
            layout = {**CHART_LAYOUT}
            layout["xaxis"] = dict(showgrid=True, gridcolor="#e8f5ee", color="#7aa98e", title="€/kg")
            layout["yaxis"] = dict(showgrid=False, color="#0d2b1a")
            fig.update_layout(height=380, **layout)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Sin datos de precios")

    with col2:
        section_header("🌍", "Comparativa local vs internacional", "Diferencial de arbitraje")
        if not df_c.empty:
            df_c["fecha"] = pd.to_datetime(df_c["fecha"])
            df_ult_c = df_c.sort_values("fecha").groupby("producto").last().reset_index()
            for _, row in df_ult_c.iterrows():
                dif   = float(row.get("diferencial_arbitraje", 0) or 0)
                local = float(row.get("precio_local_kg", 0) or 0)
                intl  = float(row.get("precio_internacional_kg", 0) or 0)
                sign  = "+" if dif > 0 else ""
                b_cls = "badge-green" if dif > 0 else "badge-red"
                st.markdown(f"""
                <div class="data-row">
                    <div style="flex:1;">
                        <div style="font-weight:700;font-size:0.88rem;color:#0d2b1a;">{row.get('producto','—')}</div>
                        <div style="font-size:0.75rem;color:#7aa98e;">{row.get('relacion','—')}</div>
                        <div style="font-size:0.75rem;color:#4a7c5f;margin-top:4px;">
                            🏠 <b class="mono">{local:.2f}</b> &nbsp;|&nbsp; 🌍 <b class="mono">{intl:.2f}</b> €/kg
                        </div>
                    </div>
                    <div style="text-align:right;">
                        <span class="badge {b_cls}">{sign}{dif:.2f} €</span>
                        <div style="font-size:0.68rem;color:#7aa98e;margin-top:3px;">diferencial</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Evolución diferencial
            if len(df_c) > 5:
                st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
                section_header("📉", "Evolución diferencial", "Histórico")
                fig2 = go.Figure()
                for prod, color in zip(df_c["producto"].unique()[:4], COLORS):
                    sub = df_c[df_c["producto"] == prod].sort_values("fecha")
                    fig2.add_trace(go.Scatter(
                        x=sub["fecha"], y=sub["diferencial_arbitraje"],
                        name=prod, line=dict(color=color, width=2),
                        mode="lines+markers", marker=dict(size=5),
                    ))
                fig2.update_layout(height=220, **CHART_LAYOUT)
                st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Sin datos de comparativa")

    # ── Tabla completa ──
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    section_header("📋", "Tabla de precios completa", "Filtrable por sector y período")
    if not df_p.empty:
        cf1, cf2, _ = st.columns([1, 1, 2])
        with cf1:
            sectores  = ["Todos"] + sorted(df_p["sector"].dropna().unique().tolist())
            sector_sel = st.selectbox("Sector", sectores)
        with cf2:
            n_dias = st.selectbox("Período (días)", [7, 14, 30, 60, 90], index=1)

        cutoff  = df_p["fecha"].max() - pd.Timedelta(days=n_dias)
        df_tab  = df_p[df_p["fecha"] >= cutoff]
        if sector_sel != "Todos":
            df_tab = df_tab[df_tab["sector"] == sector_sel]
        cols_show = [c for c in ["fecha","sector","producto","variedad","precio_min","precio_max","unidad","variacion_p","fuente"] if c in df_tab.columns]
        st.dataframe(df_tab[cols_show].sort_values("fecha", ascending=False).reset_index(drop=True),
                     use_container_width=True, height=300)

# ─────────────────────────────────────────────
# ALERTAS
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
        elif "Alertas"     in page: render_alertas()
        elif "Configuraci" in page: render_configuracion()
    except Exception as e:
        st.error(f"Error al cargar la sección: {e}")
        st.info("Pulsa '🔄 Recargar datos' en el menú lateral o recarga la página.")

if __name__ == "__main__":
    main()
