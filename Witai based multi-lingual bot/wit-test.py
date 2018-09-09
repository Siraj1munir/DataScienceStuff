import os, sys
from flask import Flask, request
from utils import wit_response
from pymessenger import Bot
from googletrans import Translator

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "Your FB Page Token"
VERIFY_TOKEN = 'Any String Just for verfication'
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
#simply get response from wit.ai                     
                    entity, value = wit_response(messaging_text)
#Define your entities in your wit.ai application
                    if entity == 'User-defined entity':
                        response = "(Note: this is sample response)Ok, I we will send you the {} What ever you demanded for".format(str(value))
                    elif entity == 'Another wit.ai entity':
                        response = "(Note: this is sample response)Ok, I we will send you the {} What ever you demanded for".format(str(value))
# Simply detect your response and translate into any language (Read doc of googletrans for language support)
                        sentence = translator.translate(response)
                        detect = translator.detect(messaging_text)
                        if detect.lang == 'en':
                            sentence= translator.translate(response,dest='en') 
                            response = sentence.text
            
# If got nothing
                    if response == None:
                        response = "Sorry didn't got your language"
                    bot.send_text_message(sender_id, response)

    return "ok", 200


def log(message):
    print(message)
    sys.stdout.flush()


if __name__ == "__main__":
    app.run(debug=True)
