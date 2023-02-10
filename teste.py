import urllib.parse, requests, json
from unidecode import unidecode

# txt = """Olá colaborador da ALT/goiaba/pudim/laranja/ Telecom ou Interline.\nEste canal de atendimento é apenas para demandas internas.\n\nNossos horários de funcionamento são:\n1 - TI - Helpdesk atua em horário comercial\n2 - GEC - Ativação atua entre 08h00 às 18h00 e plantão entre 18h00 até 21h00 segunda a sexta e 08h00 às 12h00 no sábado\n3 - SUPRIMENTOS - atua em horário comercial\n\n*Selecione o setor que deseja ser atendido:*"""
# txt = urllib.parse.quote(txt, safe='')

# url = "https://uctdemo.bitrix24.com/rest/80/wfq81jxpqz51a4d3/imbot.message.add.json?BOT_ID=460&CLIENT_ID=3w9n1jpfeyz3ec2po8azne3g9ye70eye&DIALOG_ID=80&MESSAGE=" + txt

# r = requests.get("https://wdapi.com.br/placas/EEM1207/df493696b2cdd0fc424aab9728c87988")

# r = urllib.parse.unquote(r.content)
# r = json.loads(r)
# print(r)
baseUrl = "http://127.0.0.1:5002"


# def searchUser(msg, rest):
#     msg = msg.split('(')
#     msg = msg[1].split(')')
#     name = msg[0]
#     request = requests.get(f"{rest}user.search.json?NAME={name}")
#     request = urllib.parse.unquote(request.content)
#     request = json.loads(request)
#     return request['result'][0]['ID']

# r = searchUser('=== Outgoing message, author: Bitrix24 (Lucas Linhares) ===\n\n (goiaba)((()sz)', 'https://uctdemo.bitrix24.com/rest/80/epssi2msr79jf3ee/')
# print(r)


# def getVar(client_id, chat_id, var, count = False):
#     data = {
#             "WHERE":{
#             "client_id": client_id,
#             "chat_id": chat_id,
#             "var": var
#         }
#     }
#     request = requests.post(f"{baseUrl}/getVar", json=data)
#     r = urllib.parse.unquote(request.content)

#     return r if count == False else len(r)


# print(getVar('rkzl1smrnve2j8riv0rykd5l1qjnf063', '19697', 'Nome'))