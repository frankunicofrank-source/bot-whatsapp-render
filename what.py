import sqlite3
import os
import re

# ================= CONFIG =================
MAX_GUIAS = 10
DB_NAME = "guias.db"
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, DB_NAME)


def conectar_db():
    return sqlite3.connect(DB_PATH)


def buscar_guias(lista_busqueda):
    try:
        conn = conectar_db()
        cursor = conn.cursor()

        placeholders = ",".join("?" * len(lista_busqueda))

        query = f"""
        SELECT GUIA, REFERENCIA, PROCESO, FECHA_ARRIBO, STATUS
        FROM guias
        WHERE GUIA IN ({placeholders})
           OR REFERENCIA IN ({placeholders})
        """

        valores = lista_busqueda + lista_busqueda
        cursor.execute(query, valores)

        filas = cursor.fetchall()
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
        return "⚠️ Error al consultar la base de datos."


def procesar_mensaje(texto):
    texto = texto.strip()

    if not texto:
        return (
            "Reciba un cordial saludo de *Pacustoms*.\n\n"
            "ℹ️ Para consultar el estado, envíe el número de guía o referencia.\n"
            "📌 Ejemplos:\n"
            "72993106554\n"
            "26-068MIA\n"
            "26-070A\n\n"
            "🤝 *Fue un gusto atenderle.*"
        )

    tokens = re.findall(r"[A-Za-z0-9\-]+", texto)

    if not tokens:
        return "ℹ️ No se detectaron guías válidas."

    if len(tokens) > MAX_GUIAS:
        return (
            f"⚠️ Ha enviado *{len(tokens)} valores*.\n"
            f"🔢 El máximo permitido es *{MAX_GUIAS}*."
        )

    tokens_norm = [
        t.replace(".0", "").replace(" ", "").upper().strip()
        for t in tokens
    ]

    cuerpo = buscar_guias(tokens_norm)

    return (
        "Reciba un cordial saludo de *Pacustoms*.\n\n"
        "📋 *El estado de sus guías es el siguiente:*\n\n"
        f"{cuerpo}\n\n"
        "🤝 *Fue un gusto atenderle.*"
    )
