import copy


class Keyboard_cls():
    keyboard_ex = {"one_time": None, "buttons": [[]]}
    button_ex = {
        "action": {
          "type": "text",
          "label": ""
        },
        "color": ""
    }

    def __init__(self):
        self.keyboard = copy.deepcopy(self.keyboard_ex)

    def add_button(self, text, color='default'):
        if len(self.keyboard['buttons']) == 1:
            if len(self.keyboard['buttons'][0]) < 2:
                index = 0
            else:
                self.keyboard['buttons'].append([])
                index = 1
        else:
            index = 1
        button = copy.deepcopy(self.button_ex)
        button['action']['label'] = text
        button['color'] = color
        self.keyboard['buttons'][index].append(button)

    def clear_buttons(self):
        self.keyboard = copy.deepcopy(self.keyboard_ex)

    def dump(self):
        return self.keyboard
