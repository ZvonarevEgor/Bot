import requests
from command_class import Command

CITIES = {'кольчугино': '546521', 'москва': '524901', 'владимир': '473247'}
PERIODS = {'погода сейчас': 'weather', 'трое суток с периодом 3 часа': 'forecast',
           'сутки по 3 часа': 'forecast'}


class CommandWeather(Command):
    def __init__(self, keys, description):
        super(CommandWeather, self).__init__(keys, description)

    # Get json response on my request
    @staticmethod
    def get_weather(state):
        city = state[1]
        period = state[3]
        token = '1964414c84dbc3a8d4985dbbccdaa953'
        url = 'http://api.openweathermap.org/data/2.5/' + period
        params = {'id': city, 'units': 'metric', 'lang': 'ru', 'APPID': token}
        r = requests.get(url, params)
        answer = r.json()
        return answer

    # Check that you have correctly entered the city
    @staticmethod
    def test_area(state, k):
        message = ''
        city = state[1]
        if city not in CITIES:
            message += 'Пожалуйста, проверьте, правильно ли введён город и повторите ввод.'
            state.pop(1)
            k.clear_buttons()
            k.add_button('Москва')
            k.add_button('Владимир')
            k.add_button('Кольчугино')
            k.add_button('Выход', color='negative')
            keyboard = k.dump()
        else:
            state[1] = CITIES[city]
            k.clear_buttons()
            k.add_button('Погода сейчас')
            k.add_button('Сутки по 3 часа')
            k.add_button('Трое суток с периодом 3 часа')
            k.add_button('Выход', color='negative')
            keyboard = k.dump()
            message = 'За какой период хотите узнать погоду?\n\n1) Погода сейчас\n2)' \
                      ' Сутки по 3 часа\n3) Трое суток с периодом 3 часа'
        return message, state, keyboard

    # Check that correctly entered the period
    @staticmethod
    def test_period(state, k):
        keyboard = k.dump()
        message = ''
        period = state[2]
        if period not in PERIODS:
            state.pop(2)
            k.clear_buttons()
            k.add_button('Погода сейчас')
            k.add_button('Сутки по 3 часа')
            k.add_button('Трое суток с периодом 3 часа')
            k.add_button('Выход', color='negative')
            keyboard = k.dump()
            message += 'Пожалуйста, проверьте, правильно ли введён период и повторите ввод.'
        else:
            state.append(PERIODS[period])
        return message, state, keyboard

    def make_message(self, answer, state, k):
        k.clear_buttons()
        k.add_button('Работа')
        k.add_button('Википедия')
        k.add_button('Погода')
        k.add_button('Помощь')
        keyboard = k.dump()
        period = state[3]
        message = ''
        if period == 'weather':
            message += self.weather_now(answer)
        elif period == 'forecast':
            if state[2] == 'трое суток с периодом 3 часа':
                message = self.weather_few_days(answer['list'][:25])
            else:
                message += self.weather_few_days(answer['list'][:9])
        state.clear()
        return message, state, keyboard

    # Parse the answer to get the weather now
    @staticmethod
    def weather_now(answer):
        description = answer['weather'][0]['description']
        weather = answer['main']['temp']
        maximum = answer['main']['temp_max']
        minimum = answer['main']['temp_min']
        data = 'Сейчас {}.\nНа улице {} градусов\nТемпература в основном лежит в ' \
               'диапазоне от {} до {} градусов'.format(description, weather, minimum, maximum)
        return data

    # Parse the answer to get the weather for few days
    @staticmethod
    def weather_few_days(answer):
        message = ''
        for period in answer:
            temp = period['main']['temp']
            description = period['weather'][0]['description']
            time = period['dt_txt']
            base = time[:11]
            last_time = time[-8:-6]
            if int(last_time[0]) > 0:
                new_time = int(last_time) + 3
            else:
                if int(last_time[1]) == 9:
                    new_time = 12
                else:
                    new_time = '0{}'.format(int(last_time[1]) + 3)
            if new_time == 24:
                new_time = '0{}'.format(0)
                last_date = time[8:11]
                new_date = int(last_date) + 1
                base = '{}{}{}'.format(time[:8], new_date, ' ')
            changed_time = '{}{}{}'.format(base, new_time, ':00:00')
            message += '{}\nСредняя температура: {}\nПогода: {}\n\n'.format(changed_time, temp, description)
        return message

    # Main function
    def process(self, state, k):
        keyboard = k.dump()
        attachment = ''
        message = ''
        if len(state) == 1:
            message += 'В каком городе смотреть погоду?\n\n1) Москва\n2) Владимир\n3) Кольчугино'
            k.clear_buttons()
            k.add_button('Москва')
            k.add_button('Владимир')
            k.add_button('Кольчугино')
            k.add_button('Выход', color='negative')
            keyboard = k.dump()
        elif len(state) == 2:
            message, state, keyboard = self.test_area(state, k)
        elif len(state) == 3:
            message, state, keyboard = self.test_period(state, k)
        if len(state) == 4:
            answer = self.get_weather(state)
            message, state, keyboard = self.make_message(answer, state, k)
        return message, attachment, state, keyboard
