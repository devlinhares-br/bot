from urllib.parse import quote
import requests, urllib.parse, json

baseUrl = "http://127.0.0.1:5002"

def messageAdd(msg, dialog_id, **kwargs):
    if(not(('BOT_ID' in kwargs) and ('CLIENT_ID' in kwargs) and ('REST' in kwargs))):
        return 'Não autorizado!'
    msg = quote(msg)
    request = requests.get(f"{kwargs['REST']}imbot.message.add.json?BOT_ID={kwargs['BOT_ID']}&CLIENT_ID={kwargs['CLIENT_ID']}&DIALOG_ID={dialog_id}&MESSAGE={msg}")
    return request.content

def chatTransfer(chat_id, id, line = False, extranet = 'N', **kwargs):
    if((not(('BOT_ID' in kwargs) and ('CLIENT_ID' in kwargs) and ('REST' in kwargs))) or extranet == 'N'):
        return 'Não autorizado!'
    t = "QUEUE_ID" if (line == True) else "TRANSFER_ID"
    request = requests.get(f"{kwargs['REST']}imopenlines.operator.transfer.json?BOT_ID={kwargs['BOT_ID']}&CLIENT_ID={kwargs['CLIENT_ID']}&CHAT_ID={chat_id}&{t}={id}")
    return request.content

def searchUser(msg, rest):
    msg = msg.split('(')
    msg = msg[1].split(')')
    name = msg[0]
    request = requests.get(f"{rest}user.search.json?NAME={name}")
    request = urllib.parse.unquote(request.content)
    request = json.loads(request)
    return request['result'][0]['ID']

def chatLeave(chat_id, **kwargs):
    if(not(('BOT_ID' in kwargs) and ('CLIENT_ID' in kwargs) and ('REST' in kwargs))):
        return 'Não autorizado!'
    request = requests.get(f"{kwargs['REST']}imbot.chat.leave.json?BOT_ID={kwargs['BOT_ID']}&CLIENT_ID={kwargs['CLIENT_ID']}&CHAT_ID={chat_id}")
    return request.content

def updateTitle(chat_id, title, **kwargs):
    if(not(('BOT_ID' in kwargs) and ('CLIENT_ID' in kwargs) and ('REST' in kwargs))):
        return 'Não autorizado!'
    request = requests.get(f"{kwargs['REST']}imbot.chat.updateTitle.json?BOT_ID={kwargs['BOT_ID']}&CLIENT_ID={kwargs['CLIENT_ID']}&CHAT_ID={chat_id}&TITLE={title}")
    return request.content

# RED, GREEN, MINT, LIGHT_BLUE, DARK_BLUE, PURPLE, AQUA, PINK, LIME, BROWN, AZURE, KHAKI, SAND, MARENGO, GRAY, GRAPHITE
def creatChat(users=[], title="Chat gerado por automação", color="GREEN", **kwargs):
    if(not(('BOT_ID' in kwargs) and ('CLIENT_ID' in kwargs) and ('REST' in kwargs))):
        return 'Não autorizado!'
    title = quote(title)
    request = requests.get(f"{kwargs['REST']}imbot.chat.add.json?BOT_ID={kwargs['BOT_ID']}&CLIENT_ID={kwargs['CLIENT_ID']}&COLOR={color}&TITLE={title}&USERS={users}")
    return request.content


def getChat(chat_id, domain, count = False):
    data = {
        "SELECT": ["BOT_ID", "DIALOG_ID", "CHAT_ID", "LAST_BLOCK", "msgEnviada"],
        "WHERE":{
            "CHAT_ID": chat_id,
            "DOMAIN": domain
        }
    }
    request = requests.post(f"{baseUrl}/select", json=data)
    r = request.content
    r = urllib.parse.unquote(r)
    r = json.loads(r)
    return r if count == False else len(r)

def setConversa(bot_id, client_id, dialog_id, chat_id, domain):
    data = {
    "COLUMNS":["BOT_ID", "CLIENT_ID", "DIALOG_ID", "CHAT_ID", "DOMAIN", "LAST_BLOCK"],
    "VALUES": [ bot_id, client_id, dialog_id, chat_id, domain, "INI0"]
    }
    request = requests.post(f"{baseUrl}/insert", json=data)
    r = urllib.parse.unquote(request.content)
    return r

def getBlock(idBlcok, client_id = ""):
    data = {
        "id_bloco": idBlcok,
        "client_id": client_id
    }
    request = requests.post(f"{baseUrl}/getBlock", json=data)
    if request == -1: return '-1'
    r = urllib.parse.unquote(request.content)
    r = json.loads(r)
    return r

def getAction(block = {}):
    if('next' in block):
        action = getBlock(block['start'])
        getAction(action)
    
    pass

def updateLastBlock(bloco, bot_id, client_id, chat_id):
    data = {
        "UPDATE":
        {
            "LAST_BLOCK": bloco
        },
        "WHERE":
        {
            "BOT_ID": bot_id,
            "CLIENT_ID": client_id,
            "CHAT_ID": chat_id
        }
    }
    request = requests.post(f"{baseUrl}/update", json=data)
    r = urllib.parse.unquote(request.content)
    return r

def updateMsgEnviada(msgEnviada, bot_id, client_id, chat_id):
    data = {
        "UPDATE":
        {
            "msgEnviada": msgEnviada
        },
        "WHERE":
        {
            "BOT_ID": bot_id,
            "CLIENT_ID": client_id,
            "CHAT_ID": chat_id
        }
    }
    request = requests.post(f"{baseUrl}/update", json=data)
    r = urllib.parse.unquote(request.content)
    r = json.loads(r)
    return r

def getBot(client_id):
    data = {
            "client_id": f"{client_id}"
        }

    request = requests.post(f"{baseUrl}/getBot", json=data)
    try:
        r = urllib.parse.unquote(request.content)
    except Exception as err:
        return False
    return r

def insertVar(client_id, chat_id, var, valor):
    data = {
    "COLUMNS":["client_id", "chat_id", "var", "valor"],
    "VALUES": [client_id, chat_id, var, valor]
    }
    request = requests.post(f"{baseUrl}/insertVar", json=data)
    r = urllib.parse.unquote(request.content)
    return r

def getVar(client_id, chat_id, var, count = False):
    data = {
            "WHERE":{
            "client_id": client_id,
            "chat_id": chat_id,
            "var": var
        }
    }
    request = requests.post(f"{baseUrl}/getVar", json=data)
    r = urllib.parse.unquote(request.content)
    return r if count == False else len(r)

def strToList(data = ""):
    data = data.replace("\n","")
    data = data.replace(" ","")
    data = data.replace("[","")
    data = data.replace("]","")
    data = data.replace("'","")
    data = data.replace("\"","")
    data = data.split(",")
    return data

def varInMessage(msg="", var="", varName = ''):
    txt = f"<{varName}>"
    return msg.replace(txt,str(var))

def deleteConversa(bot_id, client_id, chat_id):
    data = {
        "WHERE":
        {
            "BOT_ID": bot_id,
            "CLIENT_ID": client_id,
            "CHAT_ID": chat_id
        }
    }
    request = requests.post(f"{baseUrl}/delete", json=data)
    r = urllib.parse.unquote(request.content)
    r = json.loads(r)
    return r

def editNameUser(idUser, name, **kwargs):
    if(not(('CLIENT_ID' in kwargs) and ('REST' in kwargs))):
        return 'Não autorizado!'
    msg = quote(msg)
    request = requests.get(f"{kwargs['REST']}user.update.json?ID={idUser}&CLIENT_ID={kwargs['CLIENT_ID']}&NAME={name}")
    return request.content


def requisicao(r="", data=[], **kwargs):
    for i in range(len(data)):
        r = varInMessage(msg=r, var= f'<{data[i]}>', varName = f'<{data[i]}>')
    r = requests.get(r)
    r = urllib.parse.unquote(r.content)
    r = json.loads(r)
    try:
        for i in range(len(data)):
            p = data[i]
            insertVar(kwargs['client_id'], kwargs['chat_id'], p, r[p])
    except KeyError:
        return "Key error"
    except:
        return 'Algo deu errado'
    return '200'

def search_by_field(**kwargs):
    if not (('BOT_ID' in kwargs) and ('CLIENT_ID' in kwargs)):
        pass
    
def creat_lead(dialog_id, fields = {}, **kwargs):
    if not (('BOT_ID' in kwargs) and ('CLIENT_ID' in kwargs)):
        return 0
    params = urllib.parse.urlencode(kwargs)
    request = requests.get(f"{kwargs['REST']}crm.lead.add.json?{params}&DIALOG_ID={dialog_id}")
    return request.content