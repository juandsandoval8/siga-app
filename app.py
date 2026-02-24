import streamlit as st
import importlib, sys, os

st.set_page_config(
    page_title="SIGA – Sistema Integral de Gestión del Aprendiz",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Estilos globales ──────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700;800&display=swap');
:root { --verde:#00C896; --azul:#0A2540; --gris:#F4F7FA; }
* { font-family: 'Sora', sans-serif !important; }
.stApp { background: var(--gris); }
[data-testid="stSidebar"] { background: var(--azul) !important; border-right: 3px solid var(--verde); }
[data-testid="stSidebar"] * { color: #fff !important; }
#MainMenu, footer, header { visibility: hidden; }
.kpi-card { background:white; border-radius:16px; padding:24px 20px; text-align:center; border-left:5px solid var(--verde); box-shadow:0 2px 16px rgba(0,0,0,.06); }
.kpi-num  { font-size:2.6rem; font-weight:800; color:var(--azul); line-height:1; }
.kpi-lbl  { font-size:.82rem; color:#64748b; margin-top:6px; font-weight:600; text-transform:uppercase; letter-spacing:.06em; }
.kpi-delta{ font-size:.78rem; color:var(--verde); font-weight:600; }
.page-header { background:linear-gradient(135deg,var(--azul) 0%,#163a6b 100%); border-radius:16px; padding:28px 32px; margin-bottom:28px; }
.page-header h1 { font-size:1.8rem; font-weight:800; margin:0; color:white; }
.page-header p  { margin:6px 0 0; opacity:.75; font-size:.95rem; color:white; }
.badge { display:inline-block; padding:3px 12px; border-radius:20px; font-size:.78rem; font-weight:700; text-transform:uppercase; }
.badge-verde   { background:#D1FAE5; color:#065F46; }
.badge-amarillo{ background:#FEF3C7; color:#92400E; }
.badge-rojo    { background:#FEE2E2; color:#991B1B; }
.badge-azul    { background:#DBEAFE; color:#1E40AF; }
</style>
""", unsafe_allow_html=True)

# ── Rutas para importar módulos de pages/ ─────────────────────────────────────
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.join(BASE_DIR, "pages")
for d in [BASE_DIR, PAGES_DIR]:
    if d not in sys.path:
        sys.path.insert(0, d)

# ── Navegación lateral ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:20px 0 30px;text-align:center;'>
        <div style='font-size:2.4rem;'>🎓</div>
        <div style='font-size:1.1rem;font-weight:800;margin-top:8px;'>SIGA</div>
        <div style='font-size:.72rem;opacity:.6;margin-top:2px;'>Sistema Integral de Gestión<br>del Aprendiz</div>
    </div>
    """, unsafe_allow_html=True)

    pagina = st.radio(
        "Navegación",
        ["🏠  Dashboard", "👤  Aprendices", "🏢  Empresas", "📄  Documentos"],
        label_visibility="collapsed"
    )
    st.markdown("<div style='opacity:.4;font-size:.72rem;padding:8px;'>v1.0 · SENA Colombia</div>", unsafe_allow_html=True)

# ── Cargar la página seleccionada ─────────────────────────────────────────────
if "Dashboard" in pagina:
    import dashboard; importlib.reload(dashboard); dashboard.show()
elif "Aprendices" in pagina:
    import aprendices; importlib.reload(aprendices); aprendices.show()
elif "Empresas" in pagina:
    import empresas; importlib.reload(empresas); empresas.show()
elif "Documentos" in pagina:
    import documentos; importlib.reload(documentos); documentos.show()
