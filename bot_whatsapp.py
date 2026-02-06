from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

# 👇 IMPORTAMOS LA LÓGICA
from what import procesar_mensaje

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "").strip()
    print("Mensaje recibido:", incoming_msg)

    # Texto generado desde what.py (NO se toca)
    respuesta = procesar_mensaje(incoming_msg)

    resp = MessagingResponse()
    msg = resp.message()

    # 1️⃣ TEXTO (siempre primero)
    msg.body(respuesta)

    # 2️⃣ IMAGEN DE CIERRE (OSO) — SIEMPRE ABAJO
    msg.media(
        "https://raw.githubusercontent.com/frankunicofrank-source/"
        "bot-whatsapp-render/main/cierre_pacustoms.png"
    )

    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
