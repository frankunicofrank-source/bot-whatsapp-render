from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from what import procesar_mensaje

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "").strip()
    print("Mensaje recibido:", incoming_msg)

    respuesta = procesar_mensaje(incoming_msg)

    resp = MessagingResponse()

    # 1️⃣ MENSAJE PRINCIPAL (SIEMPRE PRIMERO)
    principal = resp.message()
    principal.media(
        "https://raw.githubusercontent.com/frankunicofrank-source/"
        "bot-whatsapp-render/main/logo_pacustoms.PNG"
    )
    principal.body(respuesta)

    # 2️⃣ MENSAJE DE CIERRE (SIEMPRE DESPUÉS)
    cierre = resp.message()
    cierre.media(
        "https://raw.githubusercontent.com/frankunicofrank-source/"
        "bot-whatsapp-render/main/cierre_pacustoms.png"
    )

    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
