from telepot import Bot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from resources.stt import Speech_to_Text
from resources.tts import Text_to_Speech
from telepot.loop import MessageLoop
from tempfile import mkstemp
from pprint import pprint
from io import BytesIO

import subprocess
import telepot
import wave
import time
import sys
import os


class TelegramInterface:

    def __init__(self, token, luna):
        self.token = token
        self.luna = luna

        self.stt = Speech_to_Text([])

        self.bot = telepot.Bot(token)
        self.bot.getMe()

        self.messages = []

    def say(self, text, uid, conv_id):
        try:
            user = self.luna.local_storage['LUNA_telegram_id_to_name_table'][uid]
        except:
            user = uid
        self.luna.Log.write('ACTION', '--{}--@{} (Telegram): {}'.format(self.luna.system_name.upper(), user, text),
                            conv_id=conv_id, show=True)
        self.bot.sendMessage(uid, text, parse_mode='HTML')

    def sendAudio(self, audio_file, uid, conv_id):
        _, voice_filename = mkstemp(prefix='voice-', suffix='.wav')
        _, converted_audio_filename = mkstemp(prefix='converted-audio-', suffix='.oga')
        wavformat = audio_file['format']
        wav = audio_file['file']
        with wave.open(voice_filename, 'wb') as file:
            file.setnchannels(wavformat['channels'])
            file.setframerate(wavformat['rate'])
            file.setsampwidth(2)
            file.writeframes(wav)
        cmd = ['/usr/bin/ffmpeg',
               '-y',
               '-loglevel', 'panic',
               '-i', voice_filename,
               '-acodec', 'libopus',
               converted_audio_filename]
        subprocess.call(cmd, shell=False)
        self.bot.sendAudio(uid, open(converted_audio_filename, 'rb'))
        os.remove(converted_audio_filename)
        os.remove(voice_filename)

    def send_video(self, video, uid, supports_streaming=True):
        self.bot.sendVideo(uid, video, supports_streaming=supports_streaming)

    def send_file(self, file, uid):
        document = open(file)
        self.bot.sendDocument(uid, document)

    def start(self):
        def on_chat_message(msg):
            content_type, chat_type, chat_id = telepot.glance(msg)
            if content_type == 'text':
                msg['content_type'] = 'text'

            elif content_type == 'voice':
                msg['content_type'] = 'voice'
                _, voice_filename = mkstemp(prefix='voice-', suffix='.oga')
                _, converted_audio_filename = mkstemp(prefix='converted-audio-', suffix='.wav')
                self.bot.download_file(msg['voice']['file_id'], voice_filename)
                cmd = ['/usr/bin/ffmpeg',
                       '-y',
                       '-loglevel', 'panic',
                       '-i', voice_filename,
                       '-codec:a', 'pcm_s16le',
                       converted_audio_filename]
                subprocess.call(cmd, shell=False)
                msg['text'] = self.stt.recognize(converted_audio_filename)
                with open(voice_filename, 'rb') as file:
                    msg['content'] = file.read()
                # self.bot.sendMessage(chat_id, msg['text'])
                os.remove(converted_audio_filename)
                os.remove(voice_filename)

            elif content_type == 'photo':
                msg['content_type'] = 'photo'
                file = BytesIO()
                self.bot.download_file(msg['photo'][-1]['file_id'], file)
                file.seek(0)
                msg['content'] = file.read()
            else:
                msg['content_type'] = content_type
            # Auf jeden Fall einen 'text' ergänzen (der bei manchen content_types einfach caption heißt)
            try:
                text = msg['text']
            except KeyError:
                try:
                    msg['text'] = msg['caption']
                except KeyError:
                    msg['text'] = 'TIMEOUT_OR_INVALID'
            self.messages.append(msg)

        def on_callback_query(msg):
            msg['text'] = msg['data']
            msg['content_type'] = 'callback_query'
            self.messages.append(msg)

        MessageLoop(self.bot, {'chat': on_chat_message, 'callback_query': on_callback_query}).run_as_thread()


def main():
    tgi = TelegramInterface()
    tgi.start()
    while True:
        if len(tgi.messages) > 0:
            print(tgi.messages[0])
            del tgi.messages[0]
        time.sleep(1)


if __name__ == "__main__":
    main()