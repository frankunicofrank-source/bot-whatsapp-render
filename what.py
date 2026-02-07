import sqlite3
import re
import os

# ================= CONFIGURACIÓN =================
MAX_GUIAS = 10
DB_NAME = "guias.db"
TABLA = "guias"
# ================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, DB_NAME)


# ---------- NORMALIZACIÓN ÚNICA ----------
def normalizar(valor: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", str(valor).upper())


# ---------- CONSULTA A SQLITE (NORMALIZADA) ----------
def consultar_guias(lista_busqueda):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        placeholders = ",".join(["?"] * len(lista_busqueda))

        # Normalizamos GUIA y REFERENCIA en SQL igual que en Python
        normalizacion_sql = """
        UPPER(
            REPLACE(
                REPLACE(
                    REPLACE(
                        REPLACE({campo}, ' ', ''),
                    '-', ''),
                '.', ''),
            '/', '')
        )
        """

        query = f"""
        SELECT
            GUIA,
            REFERENCIA,
            PROCESO,
            "FECHA DE ARRIBO",
            STATUS
        FROM {TABLA}
        WHERE {normalizacion_sql.format(campo='GUIA')} IN ({placeholders})
           OR {normalizacion_sql.format(campo='REFERENCIA')} IN ({placeholders})
        ORDER BY "FECHA DE ARRIBO"
        """

        cur.execute(query, lista_busqueda + lista_busqueda)
        filas = cur.fetchall()
        conn.close()

        if not filas:
            return "❌ No se encontró información para las guías o referencias enviadas."

        mensajes = []
        for g, r, p, f, s in filas:
            mensajes.append(
                f"📦 *Guía:* {g}\n"
                f"🔖 *Referencia:* {r}\n"
                f"⚙️ *Proceso:* {p}\n"
                f"📅 *Arribo:* {f}\n"
                f"📌 *Estado:* {s}"
            )

        return "\n\n".join(mensajes)

    except Exception as e:
        print("ERROR SQLITE:", e)
        return "⚠️ Error al consultar la base de datos."


# ---------- PROCESAMIENTO DEL MENSAJE ----------
def procesar_mensaje(texto):
    texto = texto.strip()

    if not texto:
        return (
            "Reciba un cordial saludo de *Pacustoms*.\n\n"
            "ℹ️ Para consultar el estado, envíe el número de guía o referencia.\n"
            "📌 Ejemplos:\n"
            "26-089 MIA\n"
            "26 089 mia\n"
            "26089MIA\n\n"
            "🤝 *Fue un gusto atenderle.*"
        )

    tokens = re.findall(r"[A-Za-z0-9\-\.\s/]+", texto)

    if not tokens:
        return "ℹ️ No se detectaron guías válidas."

    if len(tokens) > MAX_GUIAS:
        return (
            f"⚠️ Ha enviado *{len(tokens)} valores*.\n"
            f"🔢 El máximo permitido es *{MAX_GUIAS}*."
        )

    tokens_norm = [normalizar(t) for t in tokens]

    cuerpo = consultar_guias(tokens_norm)

    if cuerpo.startswith("❌") or cuerpo.startswith("⚠️"):
        return cuerpo

    return (
        "Reciba un cordial saludo de *Pacustoms*.\n\n"
        "📋 *El estado de sus guías es el siguiente:*\n\n"
        f"{cuerpo}\n\n"
        "🤝 *Fue un gusto atenderle.*"
    )
