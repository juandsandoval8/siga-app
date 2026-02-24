import streamlit as st
import pandas as pd
import io
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import database as db

SECTORES     = ["Tecnología","Financiero","Logística","Salud","Educación","Construcción","Manufactura","Publicidad","Comercio","Otro"]
CUMPLIMIENTO = ["Alto","Medio","Bajo"]

BADGE_CUMPL = {
    "Alto":  "badge badge-verde",
    "Medio": "badge badge-amarillo",
    "Bajo":  "badge badge-rojo",
}

def form_empresa(prefill=None, key_prefix="ne"):
    p = prefill or {}
    c1,c2 = st.columns(2)
    nombre = c1.text_input("Nombre empresa *",    value=p.get("nombre",""),  key=f"{key_prefix}_nom")
    nit    = c2.text_input("NIT",                 value=p.get("nit",""),     key=f"{key_prefix}_nit")

    c3,c4 = st.columns(2)
    sector = c3.selectbox("Sector", SECTORES,
                          index=SECTORES.index(p["sector"]) if p.get("sector") in SECTORES else 0,
                          key=f"{key_prefix}_sec")
    ciudad = c4.text_input("Ciudad",             value=p.get("ciudad",""),  key=f"{key_prefix}_ciu")

    c5,c6,c7 = st.columns(3)
    contacto = c5.text_input("Contacto",         value=p.get("contacto",""),  key=f"{key_prefix}_con")
    telefono = c6.text_input("Teléfono",         value=p.get("telefono",""),  key=f"{key_prefix}_tel")
    email    = c7.text_input("Email",            value=p.get("email",""),     key=f"{key_prefix}_eml")

    c8, _ = st.columns(2)
    cumpl  = c8.selectbox("Nivel de cumplimiento", CUMPLIMIENTO,
                           index=CUMPLIMIENTO.index(p["nivel_cumplimiento"]) if p.get("nivel_cumplimiento") in CUMPLIMIENTO else 0,
                           key=f"{key_prefix}_cumpl")
    obs    = st.text_area("Observaciones", value=p.get("observaciones",""), height=70, key=f"{key_prefix}_obs")

    return dict(nombre=nombre, nit=nit, sector=sector, ciudad=ciudad,
                contacto=contacto, telefono=telefono, email=email,
                nivel_cumplimiento=cumpl, observaciones=obs)

def show():
    st.markdown("""
    <div class='page-header'>
        <h1>🏢 Empresas Aliadas</h1>
        <p>Gestión de empresas vinculadas a la formación de aprendices</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📋 Listado de empresas", "➕ Registrar empresa"])

    with tab1:
        buscar = st.text_input("🔎 Buscar empresa (nombre / NIT / sector)")
        datos  = db.get_empresas(buscar=buscar if buscar else None)
        st.markdown(f"**{len(datos)} empresas registradas**")

        if datos:
            for row in datos:
                with st.container():
                    c1,c2,c3,c4,c5,c6 = st.columns([3,2,2,2,2,2])
                    c1.markdown(f"**{row['nombre']}**<br><small style='color:#64748b;'>{row['nit'] or 'Sin NIT'} · {row['sector']}</small>", unsafe_allow_html=True)
                    c2.caption(row["ciudad"] or "—")
                    badge_c = BADGE_CUMPL.get(row['nivel_cumplimiento'], 'badge')
                    c3.markdown(f"<span class='{badge_c}'>{row['nivel_cumplimiento']}</span>", unsafe_allow_html=True)
                    c4.caption(f"📞 {row['telefono'] or '—'}")
                    c5.caption(row["email"] or "—")

                    with c6:
                        if st.button("✏️ Editar", key=f"eedit_{row['id']}"):
                            st.session_state[f"emp_editando_{row['id']}"] = True
                        if st.button("🗑️ Borrar", key=f"edel_{row['id']}"):
                            db.delete_empresa(row["id"])
                            st.success("Empresa eliminada.")
                            st.rerun()

                    if st.session_state.get(f"emp_editando_{row['id']}"):
                        with st.form(key=f"form_emp_edit_{row['id']}"):
                            st.markdown("**Editar empresa**")
                            nuevo = form_empresa(prefill=row, key_prefix=f"ee{row['id']}")
                            cs,cc = st.columns(2)
                            if cs.form_submit_button("💾 Guardar", type="primary"):
                                db.save_empresa(nuevo, empresa_id=row["id"])
                                st.session_state[f"emp_editando_{row['id']}"] = False
                                st.success("✅ Empresa actualizada.")
                                st.rerun()
                            if cc.form_submit_button("Cancelar"):
                                st.session_state[f"emp_editando_{row['id']}"] = False
                                st.rerun()

                    # Aprendices vinculados a esta empresa
                    aps = db.get_aprendices({"buscar": row["nombre"]})
                    if aps:
                        with st.expander(f"👤 {len(aps)} aprendiz(ces) vinculado(s)"):
                            for a in aps:
                                st.caption(f"• {a['nombre']} — {a['estado']} — {a['programa']}")

                st.markdown("<hr style='margin:6px 0;border-color:#f0f0f0;'>", unsafe_allow_html=True)

            # Exportar
            st.markdown("---")
            df_export = pd.DataFrame(datos).drop(columns=["id","created_at"], errors="ignore")
            buf = io.BytesIO()
            df_export.to_excel(buf, index=False)
            st.download_button(
                "⬇️ Exportar a Excel",
                data=buf.getvalue(),
                file_name="empresas_siga.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("No se encontraron empresas.")

    with tab2:
        with st.form("form_nueva_empresa"):
            st.markdown("**Datos de la nueva empresa**")
            nuevo = form_empresa(key_prefix="new_emp")
            if st.form_submit_button("✅ Registrar empresa", type="primary"):
                if not nuevo["nombre"]:
                    st.error("El nombre es obligatorio.")
                else:
                    try:
                        db.save_empresa(nuevo)
                        st.success(f"✅ Empresa **{nuevo['nombre']}** registrada.")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Error: {e}")
