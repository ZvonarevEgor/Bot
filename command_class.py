class Command:
    def __init__(self, keys, description):
        self.keys = keys
        self.description = description

    def info(self):
        message = '"' + self.keys[0].capitalize() + '"' + ' - ' + self.description + '\n'
        return message

    def process(self, state, k):
        pass


class Sessions:
    sessions_dict = {}

    def __init__(self):
        self.sessions_dict = {}

    def clear(self):
        self.sessions_dict = {}

    def state_(self, user_id):
        state = self.sessions_dict[user_id]['args']
        return state

    def state_update(self, user_id, state):
        self.sessions_dict[user_id]['args'] = state
        if self.sessions_dict[user_id]['args'] == []:
            self.clear_session(user_id)

    def add(self, user_id, command, body):
        self.sessions_dict[user_id] = {}
        self.sessions_dict[user_id]['cmd'] = command
        args = self.sessions_dict[user_id]['args'] = []
        args.append(body)

    def update(self, user_id, body):
        self.sessions_dict[user_id]['args'].append(body)

    def this_command(self, user_id):
        command = self.sessions_dict[user_id]['cmd']
        return command

    def clear_session(self, user_id):
        self.sessions_dict.pop(user_id)
