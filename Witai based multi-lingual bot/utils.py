import os
from wit import Wit
from googletrans import Translator
translator = Translator()
wit_access_token = os.getenv("WIT_ACCESS_TOKEN")
client = Wit(access_token=wit_access_token) if wit_access_token else None

def wit_response(message_text):
    if client is None:
        raise RuntimeError("Missing required env var: WIT_ACCESS_TOKEN")
    t = translator.translate(message_text)
    resp = client.message(t.text)
	
    entity = None
    value = None

    try:
        entity = list(resp['entities'])[0]
        value = resp['entities'][entity][0]['value']
    except Exception:
        pass

    return (entity, value)
