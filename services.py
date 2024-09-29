import requests
import settings
import json

def get_wpp_message(message):
    print(message)
    if 'type' not in message:
        text = 'Mensaje no reconocido'
        return text
    
    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = "Mensaje no reconocido"
    
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
                    "title" : option
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
                "id" : sedd + "_row_" + str(i+1),
                "title" : option,
                "description" : ""
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

def document_message(number, url, caption, filename):
    data = json.dumps(
        {
            "messagin_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document" : {
                "url": url,
                "caption": caption,
                "filename": filename
            }
        }
    )
    return data

def sticker_message(number, sticker_id):
    data = json.dumps(
        {
            "messagin_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "sticker",
            "sticker": {
                "id": sticker_id
            }
        }
    )
    return data

def get_media_id(media_name, media_type):
    media_id = ""
    if media_type == "sticker":
        media_id = sett.stickers.get(media_name, None)
    if media_type == "image":
        media_id = sett.images.get(media_name, None)
    elif media_type == "video":
        media_id = sett.videos.get(media_name, None)
    elif media_type == "audio":
        media_id = sett.audios.get(media_name, None)
    return media_id

def reply_reaction(number, messageId, emoji):
    data = json.dumps(
        {
            "message_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji,  
            }
        }
    )
    return data

def reply_text(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context":{
                "message_id": messageId,
            },
            "type": "text",
            "text": {
                "body": text,
            }
        }
    )
    return data

def mark_as_read(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": messageId
        }
    )
    return data

def chatbot_admin(text, number, messageId, name):
    text = text.lower() #mensaje que envio al usuario
    list = []
    print(text)
    if "hola" in text:
        body = "Hola, Adrian no está disponible en este momento. Puedes dejar un mensaje y se lo haré llegar."
        footer = "Alma"
        options =   ["📝 Dejar mensaje","🕟 Disponibilidad","📆 Agendar cita"] 

        replyButtonData = replyButton_message(number, options, body, footer, "sed1", messageId)
        replyReaction = reply_reaction(number, messageId, "🫡")
        list.append(replyReaction)
        list.append(replyButtonData)
        
    for item in list:
        send_wpp_message(item)
    