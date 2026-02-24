import streamlit as st
import pandas as pd
import io
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import database as db

ESTADOS     = ["En formación","En búsqueda","Contratado","En pasantía","Finalizado","Retirado"]
VINCULACION = ["Contrato aprendizaje","Pasantía","Proyecto productivo",""]
RIESGOS     = ["Verde","Amarillo","Rojo"]
REGIONALES  = ["Bogotá","Medellín","Cali","Barranquilla","Bucaramanga","Manizales","Pereira","Otra"]

BADGE_RIESGO = {
    "Verde":    "badge badge-verde",
    "Amarillo": "badge badge-amarillo",
    "Rojo":     "badge badge-rojo",
}
BADGE_ESTADO = {
    "Contratado":   "badge badge-verde",
    "En pasantía":  "badge badge-azul",
    "En formación": "badge badge-azul",
    "En búsqueda":  "badge badge-amarillo",
    "Finalizado":   "badge",
    "Retirado":     "badge badge-rojo",
}

def form_aprendiz(prefill=None, key_prefix="new"):
    p = prefill or {}
    with st.container():
        c1,c2 = st.columns(2)
        nombre   = c1.text_input("Nombre completo *",     value=p.get("nombre",""),    key=f"{key_prefix}_nombre")
        doc      = c2.text_input("Documento de identidad",value=p.get("documento",""), key=f"{key_prefix}_doc")

        c3,c4,c5 = st.columns(3)
        programa = c3.text_input("Programa de formación", value=p.get("programa",""),  key=f"{key_prefix}_prog")
        ficha    = c4.text_input("Ficha",                 value=p.get("ficha",""),     key=f"{key_prefix}_ficha")
        regional = c5.selectbox("Regional",               REGIONALES,
                                index=REGIONALES.index(p["regional"]) if p.get("regional") in REGIONALES else 0,
                                key=f"{key_prefix}_reg")

        c6,c7,c8 = st.columns(3)
        estado   = c6.selectbox("Estado",ESTADOS,
                                index=ESTADOS.index(p["estado"]) if p.get("estado") in ESTADOS else 0,
                                key=f"{key_prefix}_estado")
        vinc     = c7.selectbox("Tipo vinculación", VINCULACION,
                                index=VINCULACION.index(p["vinculacion"]) if p.get("vinculacion") in VINCULACION else 0,
                                key=f"{key_prefix}_vinc")
        riesgo   = c8.selectbox("Nivel de riesgo", RIESGOS,
                                index=RIESGOS.index(p["riesgo"]) if p.get("riesgo") in RIESGOS else 0,
                                key=f"{key_prefix}_riesgo")

        c9,c10 = st.columns(2)
        empresa    = c9.text_input("Empresa",    value=p.get("empresa",""),    key=f"{key_prefix}_empresa")
        instructor = c10.text_input("Instructor",value=p.get("instructor",""),key=f"{key_prefix}_inst")

        c11,c12 = st.columns(2)
        fi = c11.text_input("Fecha inicio (YYYY-MM-DD)", value=p.get("fecha_inicio",""), key=f"{key_prefix}_fi")
        ff = c12.text_input("Fecha fin   (YYYY-MM-DD)", value=p.get("fecha_fin",""),     key=f"{key_prefix}_ff")

        obs = st.text_area("Observaciones", value=p.get("observaciones",""), height=80, key=f"{key_prefix}_obs")

    return dict(nombre=nombre, documento=doc, programa=programa, ficha=ficha,
                regional=regional, estado=estado, vinculacion=vinc, riesgo=riesgo,
                empresa=empresa, instructor=instructor,
                fecha_inicio=fi, fecha_fin=ff, observaciones=obs)

def show():
    st.markdown("""
    <div class='page-header'>
        <h1>👤 Base Maestra de Aprendices</h1>
        <p>Registro, consulta y seguimiento de aprendices SENA</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📋 Listado y gestión", "➕ Registrar nuevo aprendiz"])

    # ── Tab 1: Listado ────────────────────────────────────────────────────────
    with tab1:
        with st.expander("🔍 Filtros", expanded=True):
            fc1,fc2,fc3,fc4 = st.columns(4)
            f_estado   = fc1.selectbox("Estado",   ["Todos"]+ESTADOS,   key="f_est")
            f_regional = fc2.selectbox("Regional", ["Todos"]+REGIONALES, key="f_reg")
            f_riesgo   = fc3.selectbox("Riesgo",   ["Todos"]+RIESGOS,   key="f_rie")
            f_buscar   = fc4.text_input("🔎 Buscar (nombre / doc / programa)", key="f_bus")

        filtros = dict(estado=f_estado, regional=f_regional, riesgo=f_riesgo, buscar=f_buscar)
        datos   = db.get_aprendices(filtros)

        st.markdown(f"**{len(datos)} aprendices encontrados**")

        if datos:
            # Tabla visual simplificada
            for row in datos:
                with st.container():
                    c1,c2,c3,c4,c5,c6 = st.columns([3,2,2,2,2,2])
                    c1.markdown(f"**{row['nombre']}**<br><small style='color:#64748b;'>{row['documento']} · {row['programa']}</small>", unsafe_allow_html=True)
                    badge_e = BADGE_ESTADO.get(row['estado'], 'badge')
                    c2.markdown(f"<span class='{badge_e}'>{row['estado']}</span>", unsafe_allow_html=True)
                    badge_r = BADGE_RIESGO.get(row['riesgo'], 'badge')
                    c3.markdown(f"<span class='{badge_r}'>{row['riesgo']}</span>", unsafe_allow_html=True)
                    c5.caption(row["empresa"] or "Sin empresa")

                    with c6:
                        if st.button("✏️ Editar", key=f"edit_{row['id']}"):
                            st.session_state[f"editando_{row['id']}"] = True
                        if st.button("🗑️ Borrar", key=f"del_{row['id']}"):
                            db.delete_aprendiz(row["id"])
                            st.success("Aprendiz eliminado.")
                            st.rerun()

                    # Formulario de edición inline
                    if st.session_state.get(f"editando_{row['id']}"):
                        with st.form(key=f"form_edit_{row['id']}"):
                            st.markdown("**Editar aprendiz**")
                            nuevo = form_aprendiz(prefill=row, key_prefix=f"e{row['id']}")
                            cs, cc = st.columns(2)
                            if cs.form_submit_button("💾 Guardar cambios", type="primary"):
                                db.save_aprendiz(nuevo, aprendiz_id=row["id"])
                                st.session_state[f"editando_{row['id']}"] = False
                                st.success("✅ Aprendiz actualizado.")
                                st.rerun()
                            if cc.form_submit_button("Cancelar"):
                                st.session_state[f"editando_{row['id']}"] = False
                                st.rerun()

                st.markdown("<hr style='margin:6px 0;border-color:#f0f0f0;'>", unsafe_allow_html=True)

            # Exportar
            st.markdown("---")
            df_export = pd.DataFrame(datos).drop(columns=["id","created_at"], errors="ignore")
            buf = io.BytesIO()
            df_export.to_excel(buf, index=False)
            st.download_button(
                "⬇️ Exportar a Excel",
                data=buf.getvalue(),
                file_name="aprendices_siga.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("No se encontraron aprendices con los filtros seleccionados.")

    # ── Tab 2: Nuevo aprendiz ─────────────────────────────────────────────────
    with tab2:
        with st.form("form_nuevo_aprendiz"):
            st.markdown("**Datos del nuevo aprendiz**")
            nuevo = form_aprendiz(key_prefix="new")
            if st.form_submit_button("✅ Registrar aprendiz", type="primary"):
                if not nuevo["nombre"]:
                    st.error("El nombre es obligatorio.")
                else:
                    try:
                        db.save_aprendiz(nuevo)
                        st.success(f"✅ Aprendiz **{nuevo['nombre']}** registrado exitosamente.")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Error al guardar: {e}")

    # ── Importar desde Excel ──────────────────────────────────────────────────
    with st.expander("📥 Importar desde Excel / CSV"):
        st.markdown("""
        **Formato requerido del archivo:**
        Columnas: `nombre, documento, programa, ficha, regional, estado, empresa, vinculacion, fecha_inicio, fecha_fin, instructor, riesgo, observaciones`
        """)
        archivo = st.file_uploader("Sube tu Excel o CSV", type=["xlsx","csv"], key="import_ap")
        if archivo:
            try:
                if archivo.name.endswith(".csv"):
                    df_imp = pd.read_csv(archivo)
                else:
                    df_imp = pd.read_excel(archivo)
                st.dataframe(df_imp.head(), use_container_width=True)
                if st.button("📤 Importar todos los registros"):
                    ok = 0
                    for _, row in df_imp.iterrows():
                        try:
                            db.save_aprendiz({
                                "nombre":       str(row.get("nombre","")),
                                "documento":    str(row.get("documento","")),
                                "programa":     str(row.get("programa","")),
                                "ficha":        str(row.get("ficha","")),
                                "regional":     str(row.get("regional","")),
                                "estado":       str(row.get("estado","En formación")),
                                "empresa":      str(row.get("empresa","")),
                                "vinculacion":  str(row.get("vinculacion","")),
                                "fecha_inicio": str(row.get("fecha_inicio","")),
                                "fecha_fin":    str(row.get("fecha_fin","")),
                                "instructor":   str(row.get("instructor","")),
                                "riesgo":       str(row.get("riesgo","Verde")),
                                "observaciones":str(row.get("observaciones","")),
                            })
                            ok += 1
                        except: pass
                    st.success(f"✅ {ok} registros importados.")
                    st.rerun()
            except Exception as e:
                st.error(f"Error leyendo archivo: {e}")
