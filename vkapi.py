import vk

session = vk.Session()
api = vk.API(session, v=5.92)


def send_message(user_id, random_id, token, message, attachment, keyboard):
    api.messages.send(access_token=token, random_id=str(random_id),
                      user_id=str(user_id), message=message,
                      attachment=attachment, keyboard=keyboard)
