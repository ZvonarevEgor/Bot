from flask import Flask, request, json
from messageHandler import *
# -*- coding: utf-8 -*-

token = 'token'
confirmation_token = 'conf_token'

command_list = [CommandParserHH(['работа', 'hh', 'head', 'hunter', 'парсер',
                                 'вакансии'], 'найду вакансии на HeadHunter'),
                Wiki(['википедия', 'вики'], 'найду в википедии \
                                                   интересующий тебя вопрос'),
                CommandWeather(['погода'], 'подскажу, какая погода сейчас или будет потом'),
                CommandStatHH(['анализ it'], 'проанализирую, какие скилы необходимо иметь для '
                                             'определенной IT специальности')]

handler = Handler(command_list)

app = Flask(__name__)


@app.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return confirmation_token
    elif data['type'] == 'message_new':
        handler.handle(data['object'], token)
        return "ok"
