from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

# 👇 IMPORTAMOS LA LÓGICA
from what import procesar_mensaje

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "").strip()
    print("Mensaje recibido:", incoming_msg)

    respuesta = procesar_mensaje(incoming_msg)

    resp = MessagingResponse()
    msg = resp.message()

    # Texto del bot (NO se toca)
    msg.body(respuesta)

    # Logo (NO se toca)
    msg.media(
        "https://raw.githubusercontent.com/frankunicofrank-source/"
        "bot-whatsapp-render/main/logo_pacustoms.PNG"
    )

    # ✅ NUEVO: imagen del oso AL FINAL
    msg.media(
        "https://raw.githubusercontent.com/frankunicofrank-source/"
        "bot-whatsapp-render/main/cierre_pacustoms.png"
    )

    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
