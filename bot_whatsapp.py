from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

# 👇 IMPORTAMOS LA LÓGICA DE NEGOCIO
from what import procesar_mensaje

app = Flask(__name__)


@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    try:
        # 1️⃣ Obtener mensaje entrante
        incoming_msg = request.values.get("Body", "")
        incoming_msg = incoming_msg.strip()
        print("Mensaje recibido:", incoming_msg)

        # 2️⃣ Procesar mensaje con la lógica del Excel
        respuesta = procesar_mensaje(incoming_msg)

        # 3️⃣ Construir respuesta Twilio
        resp = MessagingResponse()
        msg = resp.message()

        # 4️⃣ Logo Pacustoms
        msg.media(
            "https://raw.githubusercontent.com/frankunicofrank-source/"
            "bot-whatsapp-render/main/logo_pacustoms.PNG"
        )

        # 5️⃣ Texto de respuesta
        msg.body(respuesta)

        # 6️⃣ DEVOLVER SIEMPRE TwiML
        return str(resp)

    except Exception as e:
        # 🔥 Escudo final: NUNCA se cae el endpoint
        print("ERROR CRÍTICO EN /whatsapp:", e)

        resp = MessagingResponse()
        resp.message(
            "⚠️ Ocurrió un error interno al procesar su solicitud.\n"
            "Por favor intente nuevamente en unos momentos."
        )
        return str(resp)


@app.route("/", methods=["GET"])
def health():
    # Endpoint de salud (Render / debugging)
    return "OK", 200


if __name__ == "__main__":
    # ⚠️ IMPORTANTE PARA RENDER
    app.run(host="0.0.0.0", port=5000)
