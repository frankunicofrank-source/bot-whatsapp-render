import pandas as pd
import re
from datetime import datetime

# ================= CONFIGURACIÓN =================
MAX_GUIAS = 10
# ================================================

# Excel SIEMPRE actualizado desde OneDrive
EXCEL_URL = "https://pacustomsec-my.sharepoint.com/:x:/g/personal/tababela_pacustoms_com_ec/IQCXWyChYgg-Q5ncYOYtPLMgAXClPOYykl8T-ihNYgbei5Y/download"

df = pd.read_excel(EXCEL_URL)

# ---------- UTILIDADES ----------
def saludo():
    hora = datetime.now().hour
    if 5 <= hora < 12:
        return "🌅 Buenos días"
    elif 12 <= hora < 19:
        return "☀️ Buenas tardes"
    else:
        return "🌙 Buenas noches"

# ---------- LÓGICA PRINCIPAL ----------
def buscar_guias(lista_guias):
    resultados = df[df["GUIA"].isin(lista_guias)]

    if resultados.empty:
        return "❌ No se encontró información para las guías enviadas."

    resultados = resultados.sort_values(by="FECHA DE ARRIBO")

    mensajes = []
    for _, f in resultados.iterrows():
        mensajes.append(
            f"📦 *Guía:* {f['GUIA']}\n"
            f"⚙️ *Proceso:* {f['PROCESO']}\n"
            f"📅 *Arribo:* {f['FECHA DE ARRIBO']}\n"
            f"📌 *Estado:* {f['STATUS']}"
        )

    return "\n\n".join(mensajes)

def procesar_mensaje(texto):
    numeros = re.findall(r"\d+", texto)

    if not numeros:
        return (
            f"{saludo()} 👋\n\n"
            "ℹ️ Para consultar el estado, envía el número de guía.\n"
            "📌 Ejemplo:\n"
            "72993106554\n"
            "o varias guías separadas por espacios."
        )

    if len(numeros) > MAX_GUIAS:
        return (
            f"⚠️ Has enviado *{len(numeros)} guías*.\n"
            f"🔢 El máximo permitido es *{MAX_GUIAS}* por mensaje."
        )

    numeros = list(map(int, numeros))
    cuerpo = buscar_guias(numeros)

    return (
        f"{saludo()} 👋\n\n"
        "📋 *Con gusto, el estado de tus guías es el siguiente:*\n\n"
        f"{cuerpo}\n\n"
        "✅ *Quedamos atentos a cualquier otra consulta.*"
    )

# ---------- MODO PRUEBA LOCAL ----------
if __name__ == "__main__":
    mensaje = input("Mensaje: ")
    print(procesar_mensaje(mensaje))
