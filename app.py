import streamlit as st

st.set_page_config(
    page_title="SIGA – Sistema Integral de Gestión del Aprendiz",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Estilos globales ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&family=DM+Mono:wght@400;500&display=swap');

:root {
    --verde:   #00C896;
    --azul:    #0A2540;
    --acento:  #FF6B35;
    --gris:    #F4F7FA;
    --texto:   #1A1A2E;
    --borde:   #E2E8F0;
}

* { font-family: 'Sora', sans-serif !important; }

/* Fondo general */
.stApp { background: var(--gris); }
[data-testid="stSidebar"] {
    background: var(--azul) !important;
    border-right: 3px solid var(--verde);
}
[data-testid="stSidebar"] * { color: #fff !important; }

/* Botones sidebar activos */
[data-testid="stSidebar"] .stRadio label:hover { color: var(--verde) !important; }

/* Ocultar header por defecto */
#MainMenu, footer, header { visibility: hidden; }

/* Tarjetas KPI */
.kpi-card {
    background: white;
    border-radius: 16px;
    padding: 24px 20px;
    text-align: center;
    border-left: 5px solid var(--verde);
    box-shadow: 0 2px 16px rgba(0,0,0,.06);
    transition: transform .2s;
}
.kpi-card:hover { transform: translateY(-3px); }
.kpi-num  { font-size: 2.6rem; font-weight: 800; color: var(--azul); line-height:1; }
.kpi-lbl  { font-size: .82rem; color: #64748b; margin-top: 6px; font-weight: 600; text-transform: uppercase; letter-spacing: .06em; }
.kpi-delta{ font-size: .78rem; color: var(--verde); font-weight: 600; }

/* Header de página */
.page-header {
    background: linear-gradient(135deg, var(--azul) 0%, #163a6b 100%);
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 28px;
    color: white;
}
.page-header h1 { font-size: 1.8rem; font-weight: 800; margin: 0; color: white; }
.page-header p  { margin: 6px 0 0; opacity: .75; font-size: .95rem; }

/* Tablas */
.stDataFrame { border-radius: 12px; overflow: hidden; }

/* Semáforo */
.badge {
    display:inline-block; padding:3px 12px; border-radius:20px;
    font-size:.78rem; font-weight:700; text-transform:uppercase; letter-spacing:.05em;
}
.badge-verde  { background:#D1FAE5; color:#065F46; }
.badge-amarillo{ background:#FEF3C7; color:#92400E; }
.badge-rojo   { background:#FEE2E2; color:#991B1B; }
.badge-azul   { background:#DBEAFE; color:#1E40AF; }

/* Formularios */
.form-card {
    background: white; border-radius: 16px; padding: 28px;
    box-shadow: 0 2px 16px rgba(0,0,0,.06); margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ── Navegación ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:20px 0 30px;text-align:center;'>
        <div style='font-size:2.4rem;'>🎓</div>
        <div style='font-size:1.1rem;font-weight:800;margin-top:8px;'>SIGA</div>
        <div style='font-size:.72rem;opacity:.6;margin-top:2px;'>Sistema Integral de Gestión<br>del Aprendiz</div>
    </div>
    """, unsafe_allow_html=True)

    pagina = st.radio(
        "",
        ["🏠  Dashboard", "👤  Aprendices", "🏢  Empresas", "📄  Documentos"],
        label_visibility="collapsed"
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='opacity:.4;font-size:.72rem;padding:0 8px;'>v1.0 · SENA Colombia</div>", unsafe_allow_html=True)

# ── Importar páginas ──────────────────────────────────────────────────────────
if   "Dashboard"   in pagina: from pages import dashboard;   dashboard.show()
elif "Aprendices"  in pagina: from pages import aprendices;  aprendices.show()
elif "Empresas"    in pagina: from pages import empresas;     empresas.show()
elif "Documentos"  in pagina: from pages import documentos;   documentos.show()
