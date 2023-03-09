from flask import Flask, request, Response, json
from bot_functions import getBot, strToList
import urllib.parse, bot

app = Flask(__name__)

# bot
@app.route("/bot", methods=['POST'])
def index():
    data = request.get_data(as_text=True)
    data = urllib.parse.unquote(data)
    data = urllib.parse.parse_qs(data)

    if(str(data['event']) == "['ONIMBOTMESSAGEADD']" and data['data[PARAMS][FROM_USER_ID]'] == data['data[USER][ID]'] ):
        with open('log.log', 'w') as arquivo:
            arquivo.write(f'{data}\n')
        data = parseDict(data)
        bot.bot(data)

    return '200'

def parseDict(data=dict()):
    
    data = remove(data)
    id = getBot(data['auth[application_token]'])
    if id == '-1': return 'Não autorizado!'
    else: id = strToList(id)
    try:
        data = {
        'event': data['event'],
        'data':{
            'BOT': {
                'BOT_ID': data[f'data[BOT][{id[1]}][BOT_ID]']
            },
            'PARAMS':{
                'FROM_USER_ID': data['data[PARAMS][FROM_USER_ID]'],
                'TO_USER_ID': data['data[PARAMS][TO_USER_ID]'],
                'MESSAGE': data['data[PARAMS][MESSAGE]'],
                'AUTHOR_ID': data['data[PARAMS][AUTHOR_ID]'],
                'CHAT_ID': data['data[PARAMS][CHAT_ID]'],
                'DIALOG_ID': data['data[PARAMS][DIALOG_ID]']
            },
            'USER':{
                'ID': data['data[USER][ID]'],
                'NAME': data['data[USER][NAME]'],
                'IS_EXTRANET': data['data[USER][IS_EXTRANET]']
            }
        },
        'auth':{
                'domain': data['auth[domain]'],
                'token': data['auth[application_token]']
            }
    }
    except Exception as e:
        return gera_response(400, "retunr", "Erro ao gerar o dicionário.\nConteudo faltando.")
    return data

def remove(data = {}):
    for key in data:
        data[key] = str(data[key]).replace("'","")
        data[key] = str(data[key]).replace("]","")
        data[key] = str(data[key]).replace("[","")
    return data

def gera_response(status, nome_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_conteudo] = conteudo
    if mensagem:
        body["msg"] = mensagem
    
    return Response(json.dumps(body), status, mimetype="application/json")

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=12120)
