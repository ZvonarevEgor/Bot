import speech_recognition as sr
import requests
import os
from pydub import AudioSegment


r = sr.Recognizer()


def get_audiofile(link):
    url = link.replace('\\', '')
    q = requests.get(url)
    audio = q.content
    with open('test.mp3', 'wb') as file:
        file.write(audio)


def convert_to_wav():
    source = "test.mp3"
    wav_file = "new.wav"
    sound = AudioSegment.from_mp3(source)
    sound.export(wav_file, format="wav")


def speech_to_text():
    with sr.AudioFile("new.wav") as source:
        audio = r.record(source)
        text = r.recognize_google(audio, language='ru-RU')
    return text


def clean_directory():
    os.remove('test.mp3')
    os.remove('new.wav')


def main(data):
    link = data['attachments'][0]["audio_message"]["link_mp3"]
    get_audiofile(link)
    convert_to_wav()
    message = speech_to_text()
    clean_directory()
    return message
