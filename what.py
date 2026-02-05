import pandas as pd
import os
import re

# ================= CONFIGURACIÓN =================
MAX_GUIAS = 10
EXCEL_NAME = "ESTATUS DIARIO NUEVO.xlsx"
# ================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, EXCEL_NAME)

df = pd.read_excel(EXCEL_PATH)

# Convertir columnas a texto para evitar errores
df["GUIA"] = df["GUIA"].astype(str).str.strip()
df["REFERENCIA"] = df["REFERENCIA"].astype(str).str.strip()

# ---------- LÓGICA PRINCIPAL ----------
def buscar_guias(lista_busqueda):
    resultados = df[
        df["GUIA"].isin(lista_busqueda) |
        df["REFERENCIA"].isin(lista_busqueda)
    ]

    if resultados.empty:
        return "❌ No se encontró información para las guías o referencias enviadas."

    resultados = resultados.sort_values(by="FECHA DE ARRIBO")

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

def procesar_mensaje(texto):
    # Detectar palabras, números, guiones y letras
    tokens = re.findall(r"[A-Za-z0-9\-]+(?:\s?[A-Za-z]+)?", texto)

    if not tokens:
        return (
            "Reciba un cordial saludo de *Pacustoms*.\n\n"
            "ℹ️ Para consultar el estado, envía el número de guía o referencia.\n"
            "📌 Ejemplos:\n"
            "72993106554\n"
            "26-068 MIA\n"
            "26-070A\n\n"
            "🤝 *Fue un gusto atenderte.*"
        )

    if len(tokens) > MAX_GUIAS:
        return (
            f"⚠️ Has enviado *{len(tokens)} valores*.\n"
            f"🔢 El máximo permitido es *{MAX_GUIAS}* por mensaje."
        )

    tokens = [t.strip() for t in tokens]
    cuerpo = buscar_guias(tokens)

    return (
        "Reciba un cordial saludo de *Pacustoms*.\n\n"
        "📋 *El estado de sus guías es el siguiente:*\n\n"
        f"{cuerpo}\n\n"
        "🤝 *Fue un gusto atenderte.*"
    )

# ---------- MODO PRUEBA LOCAL ----------
if __name__ == "__main__":
    print("Escribe el mensaje (una o varias líneas).")
    print("Cuando termines presiona ENTER, luego CTRL+Z y ENTER:\n")

    lineas = []
    while True:
        try:
            lineas.append(input())
        except EOFError:
            break

    mensaje = " ".join(lineas)
    print("\n" + procesar_mensaje(mensaje))
