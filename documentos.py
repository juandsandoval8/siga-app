import streamlit as st
import pandas as pd
import io, base64
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import database as db

TIPOS_DOC = ["Todos","Contrato","Acta de seguimiento","Certificación","Comunicación","Informe final","Foto / imagen","Otro"]
TIPOS_SUBIR = ["Contrato","Acta de seguimiento","Certificación","Comunicación","Informe final","Foto / imagen","Otro"]

def get_ext_icon(filename):
    if not filename: return "📄"
    ext = filename.split(".")[-1].lower()
    return {"pdf":"📕","xlsx":"📗","xls":"📗","csv":"📊","png":"🖼️","jpg":"🖼️","jpeg":"🖼️",
            "doc":"📘","docx":"📘","ppt":"📙","pptx":"📙"}.get(ext,"📄")

def show():
    st.markdown("""
    <div class='page-header'>
        <h1>📄 Control Documental</h1>
        <p>Sube, organiza y descarga contratos, actas, certificaciones e imágenes</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📂 Documentos guardados", "⬆️ Subir nuevo documento"])

    # ── Tab 1: Ver documentos ─────────────────────────────────────────────────
    with tab1:
        fc1,fc2 = st.columns(2)
        f_tipo = fc1.selectbox("Filtrar por tipo", TIPOS_DOC, key="dt")

        documentos = db.get_documentos(tipo=f_tipo if f_tipo != "Todos" else None)

        if not documentos:
            st.info("No hay documentos aún. Usa la pestaña **Subir nuevo documento** para agregar.")
        else:
            st.markdown(f"**{len(documentos)} documento(s)**")
            st.markdown("<br>", unsafe_allow_html=True)

            for doc in documentos:
                with st.container():
                    c1,c2,c3,c4,c5 = st.columns([1,4,2,2,2])

                    ico = get_ext_icon(doc["filename"])
                    c1.markdown(f"<div style='font-size:2rem;text-align:center;padding-top:4px;'>{ico}</div>", unsafe_allow_html=True)
                    c2.markdown(f"**{doc['nombre']}**<br><small style='color:#64748b;'>{doc['tipo']} · {doc['filename']}</small>", unsafe_allow_html=True)
                    c3.caption(f"📅 {doc['fecha_subida'][:10] if doc['fecha_subida'] else '—'}")
                    c4.caption(doc["observaciones"] or "—")

                    with c5:
                        blob = db.get_documento_blob(doc["id"])
                        if blob and blob["filedata"]:
                            ext = blob["filename"].split(".")[-1].lower() if blob["filename"] else "bin"
                            mime_map = {
                                "pdf":"application/pdf","xlsx":"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                "xls":"application/vnd.ms-excel","csv":"text/csv",
                                "png":"image/png","jpg":"image/jpeg","jpeg":"image/jpeg",
                                "doc":"application/msword","docx":"application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            }
                            mime = mime_map.get(ext, "application/octet-stream")
                            st.download_button(
                                "⬇️ Descargar",
                                data=bytes(blob["filedata"]),
                                file_name=blob["filename"],
                                mime=mime,
                                key=f"dl_{doc['id']}"
                            )

                    # Vista previa de imágenes
                    if doc["filename"] and doc["filename"].split(".")[-1].lower() in ["png","jpg","jpeg"]:
                        blob = db.get_documento_blob(doc["id"])
                        if blob and blob["filedata"]:
                            with st.expander("🖼️ Ver imagen"):
                                st.image(bytes(blob["filedata"]), caption=doc["nombre"], use_container_width=True)

                st.markdown("<hr style='margin:6px 0;border-color:#f0f0f0;'>", unsafe_allow_html=True)

        # Resumen por tipo
        if documentos:
            st.markdown("---")
            st.markdown("#### 📊 Resumen por tipo")
            df_tipos = pd.DataFrame(documentos).groupby("tipo").size().reset_index(name="Cantidad")
            df_tipos.columns = ["Tipo","Cantidad"]
            st.dataframe(df_tipos, use_container_width=True, hide_index=True)

    # ── Tab 2: Subir documento ────────────────────────────────────────────────
    with tab2:
        with st.form("form_subir_doc"):
            st.markdown("**Datos del documento**")

            c1,c2 = st.columns(2)
            nombre_doc = c1.text_input("Nombre del documento *", placeholder="Ej: Contrato aprendizaje - María López")
            tipo_doc   = c2.selectbox("Tipo de documento", TIPOS_SUBIR)

            # Asociar a aprendiz o empresa
            c3,c4 = st.columns(2)
            aprendices = db.get_aprendices()
            opciones_ap = ["— Sin aprendiz —"] + [f"{a['nombre']} ({a['documento']})" for a in aprendices]
            sel_ap = c3.selectbox("Aprendiz relacionado", opciones_ap)

            empresas = db.get_empresas()
            opciones_emp = ["— Sin empresa —"] + [e["nombre"] for e in empresas]
            sel_emp = c4.selectbox("Empresa relacionada", opciones_emp)

            obs_doc = st.text_area("Observaciones / descripción", height=70)

            archivo_sub = st.file_uploader(
                "📎 Selecciona el archivo",
                type=["pdf","xlsx","xls","csv","png","jpg","jpeg","doc","docx","ppt","pptx"],
                help="Formatos permitidos: PDF, Excel, CSV, imágenes, Word, PowerPoint"
            )

            if st.form_submit_button("⬆️ Guardar documento", type="primary"):
                if not nombre_doc:
                    st.error("El nombre del documento es obligatorio.")
                elif not archivo_sub:
                    st.error("Selecciona un archivo para subir.")
                else:
                    # Resolver IDs
                    aprendiz_id = None
                    if sel_ap != "— Sin aprendiz —":
                        idx = opciones_ap.index(sel_ap) - 1
                        aprendiz_id = aprendices[idx]["id"]

                    empresa_id = None
                    if sel_emp != "— Sin empresa —":
                        idx = opciones_emp.index(sel_emp) - 1
                        empresa_id = empresas[idx]["id"]

                    filedata = archivo_sub.read()
                    db.save_documento(
                        nombre   = nombre_doc,
                        tipo     = tipo_doc,
                        filedata = filedata,
                        filename = archivo_sub.name,
                        aprendiz_id = aprendiz_id,
                        empresa_id  = empresa_id,
                        obs      = obs_doc
                    )
                    st.success(f"✅ Documento **{nombre_doc}** guardado correctamente ({len(filedata)/1024:.1f} KB).")
                    st.balloons()

        st.markdown("---")
        st.markdown("""
        <div style='background:#EFF6FF;border-left:4px solid #3B82F6;border-radius:8px;padding:14px 18px;font-size:.88rem;'>
        <b>📌 Formatos soportados:</b> PDF, Excel (.xlsx, .xls), CSV, imágenes (PNG, JPG), Word, PowerPoint<br>
        <b>💡 Consejo:</b> Nombra los documentos de forma clara incluyendo el nombre del aprendiz o empresa y la fecha.
        </div>
        """, unsafe_allow_html=True)
