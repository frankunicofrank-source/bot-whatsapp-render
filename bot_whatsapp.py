from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

# 👇 IMPORTAMOS LA LÓGICA
from what import procesar_mensaje

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "").strip()
    print("Mensaje recibido:", incoming_msg)

    # 👇 AQUÍ ESTÁ LA CLAVE
    respuesta = procesar_mensaje(incoming_msg)

    resp = MessagingResponse()
    msg = resp.message()
    msg.body(respuesta)

    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
