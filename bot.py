import json
import bot_functions

def bot(dados = {}):

    auth = bot_functions.getBot(str(dados['auth']['token']))
    if auth:
        auth = bot_functions.strToList(auth)
    else: 
        return 'Não autorizado!'
    if('=== Outgoing message, author:' in dados['data']["PARAMS"]["MESSAGE"]):
        id = bot_functions.searchUser(msg = dados['data']["PARAMS"]["MESSAGE"], rest = auth[2])
        bot_functions.chatTransfer(chat_id = dados['data']['PARAMS']['CHAT_ID'], id = id, line = False, extranet = dados['data']['USER']["IS_EXTRANET"], BOT_ID = auth[1], CLIENT_ID = auth[0], REST = auth[2])
        bot_functions.chatLeave(chat_id=dados['data']['PARAMS']['CHAT_ID'], BOT_ID=auth[1], CLIENT_ID=auth[0], REST=auth[2])
        return '200'
    
    if dados['data']['USER']['IS_EXTRANET'] != 'Y':
        bot_functions.chatLeave(chat_id=dados['data']['PARAMS']['CHAT_ID'], BOT_ID=auth[1], CLIENT_ID=auth[0], REST=auth[2])

    conversa = bot_functions.getChat(dados['data']["PARAMS"]["CHAT_ID"], dados["auth"]["domain"], count = True)
    if conversa == 0:
        bot_functions.setConversa(bot_id = auth[1], client_id=auth[0], dialog_id=dados['data']['PARAMS']['DIALOG_ID'], chat_id=dados['data']['PARAMS']['CHAT_ID'], domain=dados['auth']['domain'])
    conversa = bot_functions.getChat(dados['data']["PARAMS"]["CHAT_ID"], dados["auth"]["domain"])
    chat = bot_functions.getBlock(conversa[0][3], auth[0])
    if chat == -1: return '404'
    chat = json.dumps(chat)
    chat = json.loads(chat)

    if('next' in chat and 'G' not in chat['id'] and 'R' not in chat['id'] and 'M' not in chat['id']):
        chat = bot_functions.getBlock(chat['next'],auth[0])
        chat = json.dumps(chat)
        chat = json.loads(chat)

        bot_functions.updateLastBlock(bloco=chat['id'], bot_id=auth[1], client_id=auth[0], chat_id=dados['data']['PARAMS']['CHAT_ID'])
        conversa = bot_functions.getChat(dados['data']["PARAMS"]["CHAT_ID"], dados["auth"]["domain"])
        chat = bot_functions.getBlock(conversa[0][3], auth[0])
        if chat == -1: return '404'
        chat = json.dumps(chat)
        chat = json.loads(chat)
        bot_functions.updateLastBlock(bloco=chat['id'], bot_id=auth[1], client_id=auth[0], chat_id=dados['data']['PARAMS']['CHAT_ID'])
    
    if('G' in chat['id']):
        while True:
            if 'G' not in chat['id']:
                break
            if(conversa[0][4] == 0):
                
                
                if(bot_functions.getVar(client_id = auth[0], chat_id = dados['data']['PARAMS']['CHAT_ID'], var = chat['var'], count = True) == 0):
                    bot_functions.messageAdd(msg=chat['mensagem'], dialog_id=dados['data']['PARAMS']['DIALOG_ID'], BOT_ID=auth[1], CLIENT_ID=auth[0], REST=auth[2])
                    bot_functions.updateMsgEnviada(msgEnviada=1, bot_id=auth[1], client_id=auth[0], chat_id=dados['data']['PARAMS']['CHAT_ID'])
                    return '200'
                else:
                    chat = bot_functions.getBlock(chat['next'],auth[0])
                    bot_functions.updateLastBlock(bloco=chat['id'], bot_id=auth[1], client_id=auth[0], chat_id=dados['data']['PARAMS']['CHAT_ID'])
                    chat = json.dumps(chat)
                    chat = json.loads(chat)
                    bot_functions.updateMsgEnviada(msgEnviada=0, bot_id=auth[1], client_id=auth[0], chat_id=dados['data']['PARAMS']['CHAT_ID'])
                    conversa = bot_functions.getChat(dados['data']["PARAMS"]["CHAT_ID"], dados["auth"]["domain"])
            else:
                if('not_guard_var' not in chat):
                    bot_functions.insertVar(client_id = auth[0], chat_id = dados['data']['PARAMS']['CHAT_ID'],  var = chat['var'], valor = dados['data']['PARAMS']['MESSAGE'])
                chat = bot_functions.getBlock(chat['next'],auth[0])
                bot_functions.updateLastBlock(bloco=chat['id'], bot_id=auth[1], client_id=auth[0], chat_id=dados['data']['PARAMS']['CHAT_ID'])
                chat = json.dumps(chat)
                chat = json.loads(chat)
                bot_functions.updateMsgEnviada(msgEnviada=0, bot_id=auth[1], client_id=auth[0], chat_id=dados['data']['PARAMS']['CHAT_ID'])
                conversa = bot_functions.getChat(dados['data']["PARAMS"]["CHAT_ID"], dados["auth"]["domain"])

    if('R' in chat):
        data = []
        for i in range(len(chat['var'])):
            data.append(bot_functions.getVar(client_id=auth[0], chat_id=dados['data']['PARAMS']['CHAT_ID'], var = chat['var'][i], count = False))
        bot_functions.requisicao(r=chat['request'], data=[], client_id=auth[0], chat_id=dados['data']['PARAMS']['CHAT_ID'])
        bot_functions.updateLastBlock(bloco=chat['next'], bot_id=auth[1], client_id=auth[0], chat_id=dados['data']['PARAMS']['CHAT_ID'])
        chat = bot_functions.getBlock(chat['next'],auth[0])
        chat = json.dumps(chat)
        chat = json.loads(chat)
        
    if('BL' in chat):
        fields = {
            "NAME": dados['data']['USER']['NAME'],

        }
        bot_functions.creat_lead(dialog_id=dados['data']['PARAMS']['DIALOG_ID'], BOT_ID=auth[1], CLIENT_ID=auth[0], REST=auth[2], FIELDS=fields)
        bot_functions.updateLastBlock(bloco=chat['op'][str(item + 1)], bot_id=auth[1], client_id=auth[0], chat_id=dados['data']['PARAMS']['CHAT_ID'])
        conversa = bot_functions.getChat(dados['data']["PARAMS"]["CHAT_ID"], dados["auth"]["domain"])
        chat = bot_functions.getBlock(conversa[0][3], auth[0])
        bot(dados = dados)
        


    if('mensagem' in chat and chat['id'] == str(conversa[0][3]) and conversa[0][4] == 0 and 'M' not in chat['id'] and 'G' not in chat['id']):       
        nome = bot_functions.getVar(client_id = auth[0], chat_id = dados['data']['PARAMS']['CHAT_ID'], var = "Nome")
        msg = bot_functions.varInMessage(str(chat['mensagem']), str(nome), 'nome')
        bot_functions.messageAdd(msg=msg, dialog_id=dados['data']['PARAMS']['DIALOG_ID'], BOT_ID=auth[1], CLIENT_ID=auth[0], REST=auth[2])
        bot_functions.updateMsgEnviada(msgEnviada=1, bot_id=auth[1], client_id=auth[0], chat_id=dados['data']['PARAMS']['CHAT_ID'])

    if('op' in chat and conversa[0][4] == 1):
        try:
            if(dados['data']['PARAMS']['MESSAGE'] not in chat['op']):
                bot_functions.messageAdd(msg="Opção invalida!", dialog_id=dados['data']['PARAMS']['DIALOG_ID'], BOT_ID=auth[1], CLIENT_ID=auth[0], REST=auth[2])
                nome = bot_functions.getVar(client_id = auth[0], chat_id = dados['data']['PARAMS']['CHAT_ID'], var = "Nome")
                msg = bot_functions.varInMessage(str(chat['mensagem']), str(nome), 'nome')
                bot_functions.messageAdd(msg=msg, dialog_id=dados['data']['PARAMS']['DIALOG_ID'], BOT_ID=auth[1], CLIENT_ID=auth[0], REST=auth[2])
                return "404"   
            for item in range(len(chat['op'])):
                if ((item + 1) == int(dados['data']['PARAMS']['MESSAGE'])) and conversa[0][3] == chat['id']:  
                    bot_functions.updateLastBlock(bloco=chat['op'][str(item + 1)], bot_id=auth[1], client_id=auth[0], chat_id=dados['data']['PARAMS']['CHAT_ID'])
                    conversa = bot_functions.getChat(dados['data']["PARAMS"]["CHAT_ID"], dados["auth"]["domain"])
                    chat = bot_functions.getBlock(conversa[0][3], auth[0])
                    if chat == -1: return '404'
                    chat = json.dumps(chat)
                    chat = json.loads(chat)
                    nome = bot_functions.getVar(client_id = auth[0], chat_id = dados['data']['PARAMS']['CHAT_ID'], var = "Nome")
                    msg = bot_functions.varInMessage(str(chat['mensagem']), str(nome), 'nome')
                    bot_functions.messageAdd(msg=msg, dialog_id=dados['data']['PARAMS']['DIALOG_ID'], BOT_ID=auth[1], CLIENT_ID=auth[0], REST=auth[2])
                    break
        except:
            bot_functions.messageAdd(msg="Opção invalida!", dialog_id=dados['data']['PARAMS']['DIALOG_ID'], BOT_ID=auth[1], CLIENT_ID=auth[0], REST=auth[2])
            nome = bot_functions.getVar(client_id = auth[0], chat_id = dados['data']['PARAMS']['CHAT_ID'], var = "Nome")
            msg = bot_functions.varInMessage(str(chat['mensagem']), str(nome), 'nome')
            bot_functions.messageAdd(msg=msg, dialog_id=dados['data']['PARAMS']['DIALOG_ID'], BOT_ID=auth[1], CLIENT_ID=auth[0], REST=auth[2])
            return "404"

    if('M' in chat['id']):
        while True:
            if 'M' not in chat['id']: break
            if('next' not in chat): break
            chat = bot_functions.getBlock(chat['next'],auth[0])
            chat = json.dumps(chat)
            chat = json.loads(chat)
            nome = bot_functions.getVar(client_id = auth[0], chat_id = dados['data']['PARAMS']['CHAT_ID'], var = "Nome")
            msg = bot_functions.varInMessage(str(chat['mensagem']), str(nome), 'nome')
            bot_functions.messageAdd(msg=str(chat['mensagem']), dialog_id=dados['data']['PARAMS']['DIALOG_ID'], BOT_ID=auth[1], CLIENT_ID=auth[0], REST=auth[2])
            bot_functions.updateLastBlock(bloco=chat['id'], bot_id=auth[1], client_id=auth[0], chat_id=dados['data']['PARAMS']['CHAT_ID'])
            conversa = bot_functions.getChat(dados['data']["PARAMS"]["CHAT_ID"], dados["auth"]["domain"])
            chat = bot_functions.getBlock(conversa[0][3], auth[0])
            if chat == -1: return '404'
            chat = json.dumps(chat)
            chat = json.loads(chat)
            bot_functions.updateMsgEnviada(msgEnviada=0, bot_id=auth[1], client_id=auth[0], chat_id=dados['data']['PARAMS']['CHAT_ID'])
            if('END' in chat):
                if(chat['END'] ==  True):
                    bot_functions.deleteConversa(bot_id=auth[1], client_id=auth[0], chat_id=dados['data']['PARAMS']['CHAT_ID'])

    if('T' in chat['id']):
        nome = bot_functions.getVar(client_id = auth[0], chat_id = dados['data']['PARAMS']['CHAT_ID'], var = "Nome")
        bot_functions.updateTitle(chat_id=dados['data']['PARAMS']['CHAT_ID'], title=f"{nome}", BOT_ID=auth[1], CLIENT_ID=auth[0], REST=auth[2])
        bot_functions.chatTransfer(chat_id=dados['data']['PARAMS']['CHAT_ID'], id=chat['transfer'], line=chat['line'], extranet=dados['data']['USER']["IS_EXTRANET"], BOT_ID=auth[1], CLIENT_ID=auth[0], REST=auth[2])
        bot_functions.updateLastBlock(bloco=chat['id'], bot_id=auth[1], client_id=auth[0], chat_id=dados['data']['PARAMS']['CHAT_ID'])
        bot_functions.updateMsgEnviada(msgEnviada=0, bot_id=auth[1], client_id=auth[0], chat_id=dados['data']['PARAMS']['CHAT_ID'])

    
    if('END' in chat):
        if(chat['END'] == True):
            bot_functions.deleteConversa(bot_id=auth[1], client_id=auth[0], chat_id=dados['data']['PARAMS']['CHAT_ID'])

    return '200'
