from flask import Flask, request
import settings
import services

app = Flask(__name__)

@app.route('/bienvenido', methods=['GET'])
def bienvenido():
    return 'Hola mundo, este es una prueba de Adrian'

@app.route('/webhook', methods=['GET'])
def token_verify():
    try:
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if token == settings.token and challeng != None:
            return challenge
        else:
            return 'token incorrecto', 403
    except Exception as e:
        return e,403


@app.route('/webhook', methods=['POST'])
def recive_messages():
    try:
        body = request.get_json()
        entry = body['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        message = value['messages'][0]
        number = message['from']
        messageId = message['id']
        contacts = value['contacts'][0]
        name = contacts['profile']['name']
        text = services.get_wpp_message(message)
        
        services.chatbot_admin(text, number, messageId, name)
        
        return 'Enviado'
    except Exception as e:
        return 'No enviado' + str[e]

if __name__ == '__main__':
    app.run()
