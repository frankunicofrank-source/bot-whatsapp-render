from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from what import procesar_mensaje
from twilio.rest import Client
import os
import threading
import time

app = Flask(__name__)

ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
FROM_WHATSAPP = "whatsapp:+XXXXXXXXXXX"  # tu número Twilio

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def enviar_oso_async(to_number):
    time.sleep(1.5)  # garantiza orden
    client.messages.create(
        from_=FROM_WHATSAPP,
        to=to_number,
        media_url="https://raw.githubusercontent.com/frankunicofrank-source/bot-whatsapp-render/main/cierre_pacustoms.png"
    )

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "").strip()
    from_number = request.values.get("From")

    respuesta = procesar_mensaje(incoming_msg)

    # Respuesta principal
    resp = MessagingResponse()
    msg = resp.message()
    msg.media(
        "https://raw.githubusercontent.com/frankunicofrank-source/bot-whatsapp-render/main/logo_pacustoms.PNG"
    )
    msg.body(respuesta)

    # Enviar oso después, fuera del webhook
    threading.Thread(target=enviar_oso_async, args=(from_number,)).start()

    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
