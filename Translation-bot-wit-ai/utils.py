from wit import Wit
from googletrans import Translator
translator = Translator()
wit_access_token = "B6HJ7THTYDETNSQK5Y5NPWIK6XLNIXNP"
client = Wit(access_token=wit_access_token)

def wit_response(message_text):
    t = translator.translate(message_text)
    resp = client.message(t.text)
	
    entity = None
    value = None

    try:
        entity = list(resp['entities'])[0]
        value = resp['entities'][entity][0]['value']
    except:
        pass

    return (entity, value)