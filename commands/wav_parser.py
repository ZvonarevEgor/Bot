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


def main(data):
    link = data['attachments'][0]["audio_message"]["link_mp3"]
    get_audiofile(link)
    convert_to_wav()
    message = speech_to_text()
    clean_directory()
    return message
