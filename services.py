import requests
import settings
import json

def get_wpp_message(message):
    if type not in message:
        text = 'mensaje no reconocido'
    
    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    
    return text

def send_wpp_message(data):
    try:
        whatsapp_token = settings.whatsapp_token
        whatsapp_url = settings.whatsapp_url
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + whatsapp_token}
        response = requests.post(whatsapp_url, 
                                headers = headers, 
                                data = data)
        if response.status_code == 200:
            return 'mensaje enviado', 200
        else:
            return 'error al enviar el mensaje', response.status_code
    except Exception as e:
        return e, 403

def text_message(number, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",    
            "recipient_type": "individual",
            "to": number,
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data

def replyButton_message(number, options, body, footer, sedd, messageId):
    buttons = []
    
    for i, option in enumerate(options):
        buttons.append(
            {
                "type" : "reply",
                "reply" : {
                    "id" : sedd + "_btn_" + str(i+1),
                    "text" : option
                }
            }
        )
    
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer  
                },
                "action": {
                    "buttons": buttons,
                }
            }
        }
    )

    return data

def listReply_message(number, options, body, footer, sedd, messageId):
    rows = []
    
    for i, option in enumerate(options):
        rows.append(
            {
                "type" : "reply",
                "reply" : {
                    "id" : sedd + "_row_" + str(i+1),
                    "title" : option,
                    "description" : ""
                }
            }
        )
    
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver opciones",
                    "sections": [
                        {
                            "title": "Secciones",
                            "rows": rows
                        },
                    ]
                }
            }
        }
    )

    return data

def chatbot_admin(text, number, messageId, name):
    text = text.lower() #mensaje que envio al usuario
    list = []
    
    data = text_message(number, "Hola mundo, este mensaje se envio desde Python")
    send_wpp_message(data)
