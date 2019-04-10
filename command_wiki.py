import wikipedia
from command_class import Command


class Wiki(Command):
    def __init__(self, keys, description):
        super(Wiki, self).__init__(keys, description)

    def get_answer(self, text):
        wikipedia.set_lang('RU')
        answer = wikipedia.summary(text)
        return answer

    def process(self, state, k):
        attachment = ''
        if len(state) == 1:
            message = 'Что ищем в википедии?'
            k.clear_buttons()
            k.add_button('Выход', color='negative')
            keyboard = k.dump()
        else:
            try:
                text = str(state[1])
                message = self.get_answer(text)
                state.clear()
                k.clear_buttons()
                k.add_button('Работа')
                k.add_button('Википедия')
                k.add_button('Помощь')
                keyboard = k.dump()
            except:
                message = 'Слишком экзотический вопрос. Что ищем?'
                state.pop(1)
                k.clear_buttons()
                k.add_button('Выход', color='negative')
                keyboard = k.dump()
        return message, attachment, state, keyboard
