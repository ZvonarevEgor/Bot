import speech_recognition as sr
import requests
import os
from pydub import AudioSegment

SOURCE = "test.mp3"
WAV_FILE = "new.wav"


r = sr.Recognizer()


def get_audiofile(link):
    url = link.replace('\\', '')
    q = requests.get(url)
    audio = q.content
    with open(SOURCE, 'wb') as wb:
        wb.write(audio)


def convert_to_wav():
    sound = AudioSegment.from_mp3(SOURCE)
    sound.export(WAV_FILE, format="wav")


def speech_to_text():
    with sr.AudioFile(WAV_FILE) as src:
        audio = r.record(src)
        text = r.recognize_google(audio, language='ru-RU')
    return text


def clean_directory():
    os.remove(SOURCE)
    os.remove(WAV_FILE)


def get_links(data):
    links = []
    if len(data['attachments']) > 0:
        for attachment in data['attachments']:
            links.append(attachment["audio_message"]["link_mp3"])
    if len(data["fwd_messages"]) > 0:
        for forward in data["fwd_messages"]:
            if "fwd_messages" in forward:
                if len(forward["fwd_messages"]) > 0:
                    for fwd in forward["fwd_messages"]:
                        if len(fwd['attachments']) > 0:
                            for attachment in fwd['attachments']:
                                links.append(attachment["audio_message"]["link_mp3"])
                else:
                    if len(forward['attachments']) > 0:
                        for attachment in forward['attachments']:
                            links.append(attachment["audio_message"]["link_mp3"])
            else:
                if len(forward['attachments']) > 0:
                    for attachment in forward['attachments']:
                        links.append(attachment["audio_message"]["link_mp3"])
    return links


def main(data):
    try:
        links = get_links(data)
    except:
        message = 'Упс, ошибка. Возможно, присутствует множественное пересылание сообщений. ' \
                  'Пожалуйста, не пересылайте сообщение более 2х раз.'
        return message
    try:
        message = ''
        for link in links:
            get_audiofile(link)
            convert_to_wav()
            message += '{}\n\n'.format(speech_to_text())
            clean_directory()
    except:
        message = 'Ой, ошибка. Возможно, запись пуста или является композицией.'

    return message
