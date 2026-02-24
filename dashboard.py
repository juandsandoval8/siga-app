import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import database as db

COLORES_ESTADO = {
    "En formación":  "#3B82F6",
    "En búsqueda":   "#F59E0B",
    "Contratado":    "#10B981",
    "En pasantía":   "#8B5CF6",
    "Finalizado":    "#6B7280",
    "Retirado":      "#EF4444",
}
COLORES_RIESGO = {"Verde": "#10B981", "Amarillo": "#F59E0B", "Rojo": "#EF4444"}

def show():
    st.markdown("""
    <div class='page-header'>
        <h1>🏠 Dashboard Ejecutivo</h1>
        <p>Indicadores en tiempo real · Gestión de Aprendices SENA</p>
    </div>
    """, unsafe_allow_html=True)

    stats = db.get_stats()

    # ── KPIs ──────────────────────────────────────────────────────────────────
    c1,c2,c3,c4,c5 = st.columns(5)
    kpis = [
        (c1, stats["total"],       "Total Aprendices",    "Registrados en el sistema"),
        (c2, stats["contratados"], "Contratados",         "✅ Con contrato activo"),
        (c3, stats["pasantia"],    "En Pasantía",         "🔄 Etapa productiva"),
        (c4, stats["busqueda"],    "En Búsqueda",         "🔍 Sin empresa aún"),
        (c5, stats["empresas"],    "Empresas Aliadas",    "🏢 Registradas"),
    ]
    for col, val, lbl, delta in kpis:
        with col:
            st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-num'>{val}</div>
                <div class='kpi-lbl'>{lbl}</div>
                <div class='kpi-delta'>{delta}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Alertas de riesgo ─────────────────────────────────────────────────────
    if stats["riesgo_rojo"] > 0:
        st.error(f"⚠️ **{stats['riesgo_rojo']} aprendiz(ces) en RIESGO ALTO** — Requieren atención inmediata. Ve al módulo de Aprendices y filtra por Riesgo Rojo.")

    # ── Gráficos ──────────────────────────────────────────────────────────────
    col_a, col_b = st.columns([3,2])

    with col_a:
        st.markdown("#### 📊 Distribución por Estado")
        if stats["por_estado"]:
            df_e = pd.DataFrame(stats["por_estado"], columns=["Estado","Cantidad"])
            fig = px.bar(
                df_e, x="Estado", y="Cantidad",
                color="Estado",
                color_discrete_map=COLORES_ESTADO,
                text="Cantidad"
            )
            fig.update_layout(
                showlegend=False, plot_bgcolor="white", paper_bgcolor="white",
                font_family="Sora", margin=dict(t=10,b=10,l=10,r=10),
                xaxis_title="", yaxis_title="Aprendices"
            )
            fig.update_traces(textposition="outside", marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("#### 🚦 Semáforo de Riesgo")
        if stats["por_riesgo"]:
            df_r = pd.DataFrame(stats["por_riesgo"], columns=["Riesgo","Cantidad"])
            fig2 = px.pie(
                df_r, values="Cantidad", names="Riesgo",
                color="Riesgo",
                color_discrete_map=COLORES_RIESGO,
                hole=0.55
            )
            fig2.update_layout(
                font_family="Sora", paper_bgcolor="white",
                margin=dict(t=10,b=10,l=10,r=10),
                legend=dict(orientation="h", yanchor="bottom", y=-0.2)
            )
            fig2.update_traces(textinfo="percent+label")
            st.plotly_chart(fig2, use_container_width=True)

    # ── Por regional ──────────────────────────────────────────────────────────
    if stats["por_regional"]:
        st.markdown("#### 🗺️ Aprendices por Regional")
        df_reg = pd.DataFrame(stats["por_regional"], columns=["Regional","Cantidad"])
        fig3 = px.bar(
            df_reg.sort_values("Cantidad", ascending=True),
            x="Cantidad", y="Regional", orientation="h",
            color_discrete_sequence=["#0A2540"], text="Cantidad"
        )
        fig3.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            font_family="Sora", margin=dict(t=10,b=10,l=10,r=10),
            xaxis_title="Cantidad", yaxis_title=""
        )
        fig3.update_traces(textposition="outside", marker_line_width=0)
        st.plotly_chart(fig3, use_container_width=True)

    # ── Resumen documentos ────────────────────────────────────────────────────
    st.markdown("---")
    col_x, col_y = st.columns(2)
    with col_x:
        st.markdown(f"""
        <div class='kpi-card' style='text-align:left; border-left-color: #8B5CF6;'>
            <div style='font-size:1.1rem;font-weight:700;color:#0A2540;'>📄 Documentos subidos</div>
            <div class='kpi-num' style='color:#8B5CF6;margin-top:8px;'>{stats["documentos"]}</div>
        </div>
        """, unsafe_allow_html=True)
    with col_y:
        pct = round(stats["contratados"] / stats["total"] * 100) if stats["total"] > 0 else 0
        st.markdown(f"""
        <div class='kpi-card' style='text-align:left; border-left-color: #FF6B35;'>
            <div style='font-size:1.1rem;font-weight:700;color:#0A2540;'>📈 Tasa de vinculación</div>
            <div class='kpi-num' style='color:#FF6B35;margin-top:8px;'>{pct}%</div>
            <div class='kpi-delta'>Contratados / Total aprendices</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><div style='text-align:center;opacity:.4;font-size:.75rem;'>🔄 Actualiza la página (F5) para ver cambios en tiempo real</div>", unsafe_allow_html=True)
