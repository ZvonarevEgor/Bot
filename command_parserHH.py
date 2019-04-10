import requests
import json
from bs4 import BeautifulSoup
from command_class import Command


class CommandParserHH(Command):
    def __init__(self, keys, description):
        super(CommandParserHH, self).__init__(keys, description)

    # Get a list with information from all the pages
    def get_all_pages(self, area, period, experience, text):
        list_pages = []
        i = 0

        while True:
            url = 'https://api.hh.ru/vacancies'
            parametres = {'text': text, 'area': area, 'experience': experience,
                          'premium': 'True', 'order_by': 'relevance',
                          'period': period, 'page': i}
            r = requests.get(url, parametres)
            i_list = r.json()
            list_pages.append(i_list)
            pages_count = i_list['pages']
            if i == pages_count - 1:
                return list_pages
                break
            i += 1

    # Making 1 list only with vacancies
    def general_list_pages(self, list_pages):
        general_list = []
        for dict_ in list_pages:
            for vacancy in dict_['items']:
                general_list.append(vacancy)
        return general_list

    # Bring the necessary information - list with str information
    def sort_information(self, general_list):
        filtered_vacancies = []

        for vacancy in general_list:
            name_of_vac = vacancy['name']
            company = vacancy['employer']['name']
            url = vacancy['alternate_url']
            # Some keys can be nontype
            sal_from, sal_to, sal_cur = self.get_salary(vacancy)
            requir = vacancy['snippet'].get('requirement',
                                            'Требования не указаны')

            if sal_from == '_' and sal_to == ('_'):
                main_str = '{} \n- Зарплата не указана. \n- {} \n- {}\n{}\
                                 \n\n'.format(name_of_vac, company, requir, url)
            else:
                main_str = '{} \n- {} \n- от {} до {} {}\n- {} \n{}\
                \n\n'.format(name_of_vac, company, sal_from, sal_to,
                             sal_cur, requir, url)

            general_str = BeautifulSoup(main_str, "lxml").text
            filtered_vacancies.append(general_str)
        return filtered_vacancies

    # Some of the values of salary can be None
    def get_salary(self, vacancy):
        salary_key = vacancy.get('salary', 'none')
        if salary_key == 'none':
            sal_from, sal_to, sal_cur = '_', '_', '_'
        else:
            salary_value = vacancy['salary']
            if salary_value is None:
                sal_from, sal_to, sal_cur = '_', '_', '_'
            else:
                sal_from = vacancy['salary'].get('from', '_')
                sal_to = vacancy['salary'].get('to', '_')
                sal_cur = vacancy['salary'].get('currency', '_')
        return sal_from, sal_to, sal_cur

    def upgrade_args(self, filtered_vacancies, state):
        state.append(filtered_vacancies)
        return state

    # Form a message with vacancies to the user
    def make_message(self, state, k):
        all_vacancies = state[0][0]
        state[0][1] = state[0][1] + 1
        views = state[0][1]
        rest_pages = all_vacancies//3 + 1
        message = 'Всего вакансий найдено: ' + str(all_vacancies) + '\n'

        if len(state[5]) <= 3:
            message += 'Страница ' + str(views) + ' из ' + str(rest_pages) + '\n\n'
            for vacancy in state[5]:
                message += vacancy
            state.clear()
            k.clear_buttons()
            k.add_button('Работа')
            k.add_button('Википедия')
            k.add_button('Помощь')
            keyboard = k.dump()
        else:
            message += 'Страница ' + str(views) + ' из ' + str(rest_pages) + '\n\n'
            for vacancy in state[5][:3]:
                message += vacancy
            state[5] = state[5][3:]
            keyboard = k.dump()
            message += 'Для следующей страницы, напиши мне любой символ/слово.'

        return message, state, keyboard

    # Checking how the search area is entered
    def test_area(self, state, k):
        k.clear_buttons()
        k.add_button('3')
        k.add_button('7')
        k.add_button('14')
        k.add_button('Выход', color='negative')
        keyboard = k.dump()
        message = 'За какой период искать вакансии? (цифрой от 1 до 30)' \
                  '\nК примеру 3 = вакансии выложены в течение 3х суток.'
        if state[1] == 'москва' or state[1] == '1':
            state.pop(1)
            state.append('1')
        elif state[1] == 'санкт-петербург' or state[1] == '2':
            state.pop(1)
            state.append('2')
        elif state[1] == 'нижний новгород' or state[1] == '3':
            state.pop(1)
            state.append('66')
        elif state[1] == 'владимир' or state[1] == '4':
            state.pop(1)
            state.append('23')
        else:
            state.pop(1)
            k.clear_buttons()
            k.add_button('Москва')
            k.add_button('Санкт-Петербург')
            k.add_button('Нижний Новгород')
            k.add_button('Владимир')
            keyboard = k.dump()
            message = 'Пожалуйста, вводи город без ошибок.'
        return message, state, keyboard

    # Checking how the search period is entered
    def test_period(self, state, k):
        message = 'Какой опыт? \n\n1) Нет опыта\n' \
                  '2) От 1 года до 3х\n3) От 3х до 6ти лет'
        k.clear_buttons()
        k.add_button('3')
        k.add_button('7')
        k.add_button('14')
        k.add_button('Выход', color='negative')
        keyboard = k.dump()
        try:
            period = state[2]
            period = int(period)
            if period > 30 or period < 1:
                message = 'Пожалуйста, введи период числом от 1 до 30.'
                state.pop(2)
            else:
                k.clear_buttons()
                k.add_button('Нет опыта')
                k.add_button('От 1 года до 3х')
                k.add_button('От 3х до 6ти лет')
                k.add_button('Выход', color='negative')
                keyboard = k.dump()
                pass
        except:
            state.pop(2)
            message = 'Пожалуйста, введи период числом от 1 до 30.'
        return message, state, keyboard

    # Check, as introduced experience
    def test_exp(self, state, k):
        k.clear_buttons()
        k.add_button('Выход', color='negative')
        keyboard = k.dump()
        message = 'Что ищем?'
        if state[3] == 'нет опыта' or state[3] == '1':
            state.pop(3)
            state.append('noExperience')
        elif state[3] == 'от 1 года до 3х' or state[3] == '2':
            state.pop(3)
            state.append('between1And3')
        elif state[3] == 'от 3х до 6ти лет' or state[3] == '3':
            state.pop(3)
            state.append('between3And6')
        else:
            state.pop(3)
            message = 'Пожалуйста, убедись, что ошибок нет и повторите ввод.'
            k.clear_buttons()
            k.add_button('Нет опыта')
            k.add_button('От 1 года до 3х')
            k.add_button('От 3х до 6ти лет')
            k.add_button('Выход', color='negative')
            keyboard = k.dump()
        return message, state, keyboard

    # Depending on the current session, I ask the right things
    def test_msgs(self, state, k):
        if len(state) == 1:
            k.clear_buttons()
            k.add_button('Москва')
            k.add_button('Санкт-Петербург')
            k.add_button('Нижний Новгород')
            k.add_button('Владимир')
            keyboard = k.dump()
            message = 'В каком городе ищем вакансии?\n\n'
            message += '1) Москва\n2) Санкт-Петербург\n3) Нижний Новгород\n' \
                       '4) Владимир'
        elif len(state) == 2:
            message, state, keyboard = self.test_area(state, k)
        elif len(state) == 3:
            message, state, keyboard = self.test_period(state, k)
        elif len(state) == 4:
            message, state, keyboard = self.test_exp(state, k)
        return message, state, keyboard

    # A function of the interaction with the bot
    def process(self, state, k):
        attachment = ''
        if len(state) < 5:
            message, state, keyboard = self.test_msgs(state, k)
        if len(state) == 5:
            list_pages = self.get_all_pages(*state[1:])
            general_list = self.general_list_pages(list_pages)
            filtered_vacancies = self.sort_information(general_list)
            state = self.upgrade_args(filtered_vacancies, state)
            state[0] = []
            state[0].append(len(state[5]))
            state[0].append(0)
        if len(state) >= 6:
            k.clear_buttons()
            k.add_button('Ещё')
            k.add_button('Выход', color='negative')
            keyboard = k.dump()
            message, state, keyboard = self.make_message(state, k)
        return message, attachment, state, keyboard
