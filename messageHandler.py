import vkapi
import json
from command_class import Command, Sessions
from command_parserHH import *
from class_keyboard import KeyboardCls
from command_wiki import Wiki
from command_weather import CommandWeather
from command_stat import CommandStatHH

k = KeyboardCls()


class Handler:
    def __init__(self, command_list):
        self.sessions = Sessions()
        self.commands = command_list

    def handle(self, data, token):
        k.clear_buttons()
        k.add_button('Работа')
        k.add_button('Википедия')
        k.add_button('Помощь')
        keyboard = k.dump()
        attachment = ''
        body = data['text'].lower()
        user_id = data["from_id"]
        random_id = data["random_id"]

        if user_id in self.sessions.sessions_dict:
            if body.split(' ')[0] == 'выход':
                self.sessions.clear_session(user_id)
                message = 'Сессия завершена.'
            else:
                command = self.sessions.this_command(user_id)
                self.sessions.update(user_id, body)
                process = command.process(self.sessions.state_(user_id), k)
                message, attachment, state, keyboard = process
                self.sessions.state_update(user_id, state)
        else:
            if body.split(' ')[0] == 'помощь':
                message = 'Полный список ключевых слов для каждой из команд\
                           можете посмотреть в закреплённом сообщении на стене\
                           сообщества' + '\n\n'
                message += '\n'.join([x.info() for x in self.commands])
            elif body.split(' ')[0] == 'выход':
                message = 'Нет незавершенной сессии.'
            else:
                message = 'Прости, не понимаю тебя. Напиши "помощь", чтобы \
                           узнать мои команды.'
                for command in self.commands:
                    if body.split(' ')[0] in command.keys:
                        self.sessions.add(user_id, command, body)
                        process = command.process(self.sessions.state_(user_id), k)
                        message, attachment, state, keyboard = process
                        self.sessions.state_update(user_id, state)

        keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
        keyboard = str(keyboard.decode('utf-8'))
        vkapi.send_message(user_id, random_id, token, message,
                           attachment, keyboard)
