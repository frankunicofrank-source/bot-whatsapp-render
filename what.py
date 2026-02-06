import pandas as pd
import os
import re

# ================= CONFIGURACIÓN =================
MAX_GUIAS = 10
EXCEL_NAME = "ESTATUS DIARIO NUEVO.xlsx"
COLUMNAS_REQUERIDAS = {
    "GUIA", "REFERENCIA", "PROCESO", "FECHA DE ARRIBO", "STATUS"
}
# ================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, EXCEL_NAME)


# ---------- CARGA SEGURA DEL EXCEL ----------
def cargar_excel():
    try:
        if not os.path.exists(EXCEL_PATH):
            return None, f"❌ No se encontró el archivo *{EXCEL_NAME}*."

        df = pd.read_excel(EXCEL_PATH)

        # Validar columnas
        faltantes = COLUMNAS_REQUERIDAS - set(df.columns)
        if faltantes:
            return None, f"❌ Faltan columnas en el Excel: {', '.join(faltantes)}"

        # Normalización fuerte (CLAVE)
        def normalizar(valor):
            return (
                str(valor)
                .replace(".0", "")
                .replace(" ", "")
                .upper()
                .strip()
            )

        df["GUIA"] = df["GUIA"].apply(normalizar)
        df["REFERENCIA"] = df["REFERENCIA"].apply(normalizar)

        return df, None

    except Exception:
        return None, (
            "⚠️ Ocurrió un error al consultar la información.\n"
            "Por favor intente nuevamente en unos momentos."
        )


# ---------- BÚSQUEDA ----------
def buscar_guias(df, lista_busqueda):
    try:
        resultados = df[
            df["GUIA"].isin(lista_busqueda) |
            df["REFERENCIA"].isin(lista_busqueda)
        ]

        if resultados.empty:
            return "❌ No se encontró información para las guías o referencias enviadas."

        # Ordenar de forma segura
        resultados = resultados.copy()
        resultados["FECHA DE ARRIBO"] = resultados["FECHA DE ARRIBO"].astype(str)
        resultados = resultados.sort_values(
            by="FECHA DE ARRIBO", errors="ignore"
        )

        mensajes = []
        for _, f in resultados.iterrows():
            mensajes.append(
                f"📦 *Guía:* {f['GUIA']}\n"
                f"🔖 *Referencia:* {f['REFERENCIA']}\n"
                f"⚙️ *Proceso:* {f['PROCESO']}\n"
                f"📅 *Arribo:* {f['FECHA DE ARRIBO']}\n"
                f"📌 *Estado:* {f['STATUS']}"
            )

        return "\n\n".join(mensajes)

    except Exception:
        return "⚠️ Error interno al procesar la información."


# ---------- PROCESAMIENTO PRINCIPAL ----------
def procesar_mensaje(texto):
    try:
        texto = texto.strip()

        if not texto:
            return (
                "Reciba un cordial saludo de *Pacustoms*.\n\n"
                "ℹ️ Para consultar el estado, envíe el número de guía o referencia.\n"
                "📌 Ejemplos:\n"
                "72993106554\n"
                "26-068 MIA\n"
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

        # Normalizar lo que envía el usuario
        tokens_norm = [
            t.replace(".0", "").replace(" ", "").upper().strip()
            for t in tokens
        ]

        df, error = cargar_excel()
        if error:
            return error

        cuerpo = buscar_guias(df, tokens_norm)

        if cuerpo.startswith("❌") or cuerpo.startswith("⚠️"):
            return cuerpo

        return (
            "Reciba un cordial saludo de *Pacustoms*.\n\n"
            "📋 *El estado de sus guías es el siguiente:*\n\n"
            f"{cuerpo}\n\n"
            "🤝 *Fue un gusto atenderle.*"
        )

    except Exception:
        return (
            "⚠️ Ocurrió un error inesperado.\n"
            "Por favor intente nuevamente."
        )


# ---------- PRUEBA LOCAL ----------
if __name__ == "__main__":
    while True:
        msg = input("Mensaje: ")
        print(procesar_mensaje(msg))
