import os, sys
from flask import Flask, request
from utils import wit_response
from pymessenger import Bot
from googletrans import Translator

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAAKWxAuARyABAF9eLDIITaLUTg85uZBEEBCG0de1xiQnGvsWMhOv153nSaJfwPVe3ZBvbyp9mxzdxH8gfP9dtcopmJ3lfJueLYeiGlab8ZCMcXTZBiPRWaBDiNsMlroawBafpE3xjnUZB32nzZBkNdXrXUuYVPSZBhT9vKVPoOFhgZDZD"
VERIFY_TOKEN = 'TestingTheTokenByUmerQaisar'
bot = Bot(PAGE_ACCESS_TOKEN)
translator = Translator()

@app.route('/', methods=['GET'])
def verify():
    # Webhook verification
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    log(data)

    if data['object'] == 'page':
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                # IDs
                sender_id = messaging_event['sender']['id']
                recipient_id = messaging_event['recipient']['id']

                if messaging_event.get('message'):
                    # Extracting text message
                    if 'text' in messaging_event['message']:
                        messaging_text = messaging_event['message']['text']
                    else:
                        messaging_text = 'no text'

                    response = None

                    entity, value = wit_response(messaging_text)
                    if entity == 'newstype':
                        response = "Ok, I will send you the {} news".format(str(value))
                    elif entity == 'location':
                        response = "Ok, so you live in {0}. I'll send you top headlines from {0}".format(str(value))
                        t= translator.translate(response)
                        detect = translator.detect(messaging_text)
                        if detect.lang == 'en':
                            t= translator.translate(response,dest='en') 
                            response = t.text
                        if detect.lang == 'it':
                            t= translator.translate(response,dest='it') 
                            response = t.text
                        if detect.lang == 'es':
                            t= translator.translate(response,dest='es')
                            response = t.text
                        if detect.lang == 'fr':
                                t= translator.translate(response,dest='es')
                                response = t.text
                        else:
                            response = "Sorry I didn't understand your laguage"        
                    if response == None:
                        response = "I have no idea what you are saying!"
                    bot.send_text_message(sender_id, response)

    return "ok", 200


def log(message):
    print(message)
    sys.stdout.flush()


if __name__ == "__main__":
    app.run(debug=True)