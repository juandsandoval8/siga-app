"""
database.py – Capa de datos SIGA
Usa Supabase si hay credenciales configuradas; si no, usa SQLite local (para desarrollo).
"""
import os, sqlite3, json, datetime
from pathlib import Path
import streamlit as st

# ── Detectar modo ─────────────────────────────────────────────────────────────
USE_SUPABASE = (
    "SUPABASE_URL" in st.secrets and "SUPABASE_KEY" in st.secrets
) if hasattr(st, "secrets") else False

DB_PATH = Path(__file__).parent / "siga_local.db"

# ── SQLite local ──────────────────────────────────────────────────────────────
def get_conn():
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS aprendices (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre      TEXT NOT NULL,
        documento   TEXT UNIQUE,
        programa    TEXT,
        ficha       TEXT,
        regional    TEXT,
        estado      TEXT DEFAULT 'En formación',
        empresa     TEXT,
        vinculacion TEXT,
        fecha_inicio TEXT,
        fecha_fin    TEXT,
        instructor   TEXT,
        riesgo       TEXT DEFAULT 'Verde',
        observaciones TEXT,
        created_at   TEXT DEFAULT (datetime('now'))
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS empresas (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre      TEXT NOT NULL,
        nit         TEXT UNIQUE,
        sector      TEXT,
        ciudad      TEXT,
        contacto    TEXT,
        telefono    TEXT,
        email       TEXT,
        nivel_cumplimiento TEXT DEFAULT 'Alto',
        observaciones TEXT,
        created_at  TEXT DEFAULT (datetime('now'))
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS documentos (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre       TEXT NOT NULL,
        tipo         TEXT,
        aprendiz_id  INTEGER,
        empresa_id   INTEGER,
        filename     TEXT,
        filedata     BLOB,
        fecha_subida TEXT DEFAULT (datetime('now')),
        observaciones TEXT
    )""")

    # Datos demo si las tablas están vacías
    if c.execute("SELECT COUNT(*) FROM aprendices").fetchone()[0] == 0:
        demo_aprendices = [
            ("María López", "1001234567", "Análisis y Desarrollo de Software", "2850123", "Bogotá", "Contratado", "TechCorp SAS", "Contrato aprendizaje", "2024-01-15", "2024-07-15", "Carlos Pérez", "Verde", "Buen desempeño"),
            ("Juan Rodríguez", "1007654321", "Contabilidad y Finanzas", "2850456", "Medellín", "En pasantía", "Banco Popular", "Pasantía", "2024-02-01", "2024-08-01", "Ana García", "Amarillo", "Pendiente documentación"),
            ("Andrea Martínez", "1009876543", "Gestión Logística", "2850789", "Cali", "En formación", "", "", "", "", "Luis Herrera", "Verde", ""),
            ("Carlos Gómez", "1002345678", "Diseño Gráfico", "2851012", "Bogotá", "En búsqueda", "", "", "", "", "María Torres", "Rojo", "Sin empresa asignada hace 3 meses"),
            ("Sofía Restrepo", "1008765432", "Mercadeo", "2851345", "Barranquilla", "Finalizado", "PubliGroup", "Contrato aprendizaje", "2023-06-01", "2023-12-01", "Pedro Díaz", "Verde", "Certificado exitoso"),
        ]
        c.executemany("""INSERT INTO aprendices
            (nombre,documento,programa,ficha,regional,estado,empresa,vinculacion,
             fecha_inicio,fecha_fin,instructor,riesgo,observaciones)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", demo_aprendices)

    if c.execute("SELECT COUNT(*) FROM empresas").fetchone()[0] == 0:
        demo_empresas = [
            ("TechCorp SAS", "900123456-1", "Tecnología", "Bogotá", "Sandra Ruiz", "3001234567", "sruz@techcorp.co", "Alto", "Excelente empresa aliada"),
            ("Banco Popular", "860034313-7", "Financiero", "Medellín", "Roberto Mora", "3107654321", "rmora@bancopopular.co", "Alto", ""),
            ("PubliGroup", "900654321-2", "Publicidad", "Barranquilla", "Claudia Vega", "3209876543", "cvega@puligroup.co", "Medio", "Revisar contrato"),
            ("LogisTrans", "900111222-3", "Logística", "Cali", "Fernando Ríos", "3154321098", "frios@logistrans.co", "Alto", ""),
        ]
        c.executemany("""INSERT INTO empresas
            (nombre,nit,sector,ciudad,contacto,telefono,email,nivel_cumplimiento,observaciones)
            VALUES (?,?,?,?,?,?,?,?,?)""", demo_empresas)

    conn.commit()
    conn.close()

# ── API de acceso a datos ─────────────────────────────────────────────────────

def get_aprendices(filtros=None):
    conn = get_conn()
    q = "SELECT * FROM aprendices WHERE 1=1"
    params = []
    if filtros:
        if filtros.get("estado") and filtros["estado"] != "Todos":
            q += " AND estado=?"; params.append(filtros["estado"])
        if filtros.get("regional") and filtros["regional"] != "Todos":
            q += " AND regional=?"; params.append(filtros["regional"])
        if filtros.get("riesgo") and filtros["riesgo"] != "Todos":
            q += " AND riesgo=?"; params.append(filtros["riesgo"])
        if filtros.get("buscar"):
            q += " AND (nombre LIKE ? OR documento LIKE ? OR programa LIKE ?)"
            t = f"%{filtros['buscar']}%"
            params += [t, t, t]
    q += " ORDER BY created_at DESC"
    rows = conn.execute(q, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def save_aprendiz(data, aprendiz_id=None):
    conn = get_conn()
    if aprendiz_id:
        conn.execute("""UPDATE aprendices SET
            nombre=?,documento=?,programa=?,ficha=?,regional=?,estado=?,
            empresa=?,vinculacion=?,fecha_inicio=?,fecha_fin=?,instructor=?,
            riesgo=?,observaciones=? WHERE id=?""",
            (data["nombre"],data["documento"],data["programa"],data["ficha"],
             data["regional"],data["estado"],data["empresa"],data["vinculacion"],
             data["fecha_inicio"],data["fecha_fin"],data["instructor"],
             data["riesgo"],data["observaciones"],aprendiz_id))
    else:
        conn.execute("""INSERT INTO aprendices
            (nombre,documento,programa,ficha,regional,estado,empresa,vinculacion,
             fecha_inicio,fecha_fin,instructor,riesgo,observaciones)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (data["nombre"],data["documento"],data["programa"],data["ficha"],
             data["regional"],data["estado"],data["empresa"],data["vinculacion"],
             data["fecha_inicio"],data["fecha_fin"],data["instructor"],
             data["riesgo"],data["observaciones"]))
    conn.commit(); conn.close()

def delete_aprendiz(aprendiz_id):
    conn = get_conn()
    conn.execute("DELETE FROM aprendices WHERE id=?", (aprendiz_id,))
    conn.commit(); conn.close()

def get_empresas(buscar=None):
    conn = get_conn()
    q = "SELECT * FROM empresas WHERE 1=1"
    params = []
    if buscar:
        q += " AND (nombre LIKE ? OR nit LIKE ? OR sector LIKE ?)"
        t = f"%{buscar}%"; params += [t,t,t]
    q += " ORDER BY nombre"
    rows = conn.execute(q, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def save_empresa(data, empresa_id=None):
    conn = get_conn()
    if empresa_id:
        conn.execute("""UPDATE empresas SET
            nombre=?,nit=?,sector=?,ciudad=?,contacto=?,telefono=?,email=?,
            nivel_cumplimiento=?,observaciones=? WHERE id=?""",
            (data["nombre"],data["nit"],data["sector"],data["ciudad"],
             data["contacto"],data["telefono"],data["email"],
             data["nivel_cumplimiento"],data["observaciones"],empresa_id))
    else:
        conn.execute("""INSERT INTO empresas
            (nombre,nit,sector,ciudad,contacto,telefono,email,nivel_cumplimiento,observaciones)
            VALUES (?,?,?,?,?,?,?,?,?)""",
            (data["nombre"],data["nit"],data["sector"],data["ciudad"],
             data["contacto"],data["telefono"],data["email"],
             data["nivel_cumplimiento"],data["observaciones"]))
    conn.commit(); conn.close()

def delete_empresa(empresa_id):
    conn = get_conn()
    conn.execute("DELETE FROM empresas WHERE id=?", (empresa_id,))
    conn.commit(); conn.close()

def save_documento(nombre, tipo, filedata, filename, aprendiz_id=None, empresa_id=None, obs=""):
    conn = get_conn()
    conn.execute("""INSERT INTO documentos
        (nombre,tipo,filedata,filename,aprendiz_id,empresa_id,observaciones)
        VALUES (?,?,?,?,?,?,?)""",
        (nombre, tipo, filedata, filename, aprendiz_id, empresa_id, obs))
    conn.commit(); conn.close()

def get_documentos(aprendiz_id=None, empresa_id=None, tipo=None):
    conn = get_conn()
    q = "SELECT id,nombre,tipo,filename,fecha_subida,aprendiz_id,empresa_id,observaciones FROM documentos WHERE 1=1"
    params = []
    if aprendiz_id: q += " AND aprendiz_id=?"; params.append(aprendiz_id)
    if empresa_id:  q += " AND empresa_id=?";  params.append(empresa_id)
    if tipo and tipo != "Todos": q += " AND tipo=?"; params.append(tipo)
    q += " ORDER BY fecha_subida DESC"
    rows = conn.execute(q, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_documento_blob(doc_id):
    conn = get_conn()
    row = conn.execute("SELECT filedata,filename FROM documentos WHERE id=?", (doc_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_stats():
    conn = get_conn()
    stats = {}
    stats["total"]      = conn.execute("SELECT COUNT(*) FROM aprendices").fetchone()[0]
    stats["contratados"]= conn.execute("SELECT COUNT(*) FROM aprendices WHERE estado='Contratado'").fetchone()[0]
    stats["pasantia"]   = conn.execute("SELECT COUNT(*) FROM aprendices WHERE estado='En pasantía'").fetchone()[0]
    stats["busqueda"]   = conn.execute("SELECT COUNT(*) FROM aprendices WHERE estado='En búsqueda'").fetchone()[0]
    stats["riesgo_rojo"]= conn.execute("SELECT COUNT(*) FROM aprendices WHERE riesgo='Rojo'").fetchone()[0]
    stats["empresas"]   = conn.execute("SELECT COUNT(*) FROM empresas").fetchone()[0]
    stats["documentos"] = conn.execute("SELECT COUNT(*) FROM documentos").fetchone()[0]
    stats["por_estado"] = conn.execute(
        "SELECT estado, COUNT(*) as cnt FROM aprendices GROUP BY estado").fetchall()
    stats["por_regional"]= conn.execute(
        "SELECT regional, COUNT(*) as cnt FROM aprendices WHERE regional!='' GROUP BY regional").fetchall()
    stats["por_riesgo"] = conn.execute(
        "SELECT riesgo, COUNT(*) as cnt FROM aprendices GROUP BY riesgo").fetchall()
    conn.close()
    return stats

# Inicializar al importar
init_db()
