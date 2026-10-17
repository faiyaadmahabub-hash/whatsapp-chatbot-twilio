from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.form.get("Body").lower()
    resp = MessagingResponse()
    msg = resp.message()

    if "hello" in incoming_msg:
        msg.body("Hello! I am your WhatsApp bot.")
    elif "help" in incoming_msg:
        msg.body("Available commands:\n- hello\n- info\n- bye")
    elif "info" in incoming_msg:
        msg.body("This is a simple WhatsApp chatbot built from scratch.")
    elif "bye" in incoming_msg:
        msg.body("Goodbye.")
    else:
        msg.body("Command not recognized. Type 'help'.")

    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
