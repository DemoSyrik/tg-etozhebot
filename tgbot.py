# -*- coding: utf-8 -*-
import json
import telegram
import time
import random
from urllib.request import urlopen
import threading
from tguser import get_user_by_id, TGUser, add_user, remove_user, get_all

__author__ = 'Semyon'

token = '130239822:AAFGuwrEqaXxkPZ_vowX5a3yf-_hXEEUJg4'
beer_sticker_id = 'BQADAgAD_QADns4LAAHbXk6lTJ0R5QI'

photos = ['AgADAgADK6kxG2CJvgNdswd7pploZjZehCoABKs4QZTv6iZwp1sBAAEC',
          'AgADAgADLKkxG2CJvgONCC9tEOCpTptqhCoABK9LKb4c1dHJrV0BAAEC',
          'AgADAgADLakxG2CJvgMbWQ3oQ6dR2xBEhCoABMTY6EiEZpbOcFkBAAEC',
          'AgADAgADLqkxG2CJvgM7un4Cs_YKaouFhCoABBOfX3NSkqo0Iv8AAgI',
          'AgADAgADL6kxG2CJvgMGXfHwLUPVGKCMhCoABEgKlaK6GMhn1v8AAgI',
          'AgADAgADMKkxG2CJvgMAAfxkyZQ_xZJUYoQqAATHCpVfztkmh09cAQABAg']

gay_bar = 'BQADAgAD2wADYIm-A48BNeqWFZNyAg'

bot = telegram.Bot(token=token)

is_streaming = False

class BotThread(threading.Thread):
    def run(self):
        if bot.getMe():
            print("Bot start success")

        def get_tguser(user):
            return get_user_by_id(user.id)

        last_id = 0
        while True:
            updates = bot.getUpdates(offset=last_id)
            update_quantity = len(updates)
            if update_quantity > 0:
                print("Received " + str(update_quantity) + " updates")
                last_id = updates[-1].update_id + 1
                try:
                    for update in updates:
                        message = update.message
                        chat_id = message.chat_id
                        user = message.from_user
                        text = message.text
                        if text:
                            if text == "/subscribe":
                                tguser = get_tguser(user)
                                if not tguser:
                                    tguser = add_user(user.id, user.username)
                                    message_to_send = "Спасибо за подписку, " + user.username
                                    bot.sendMessage(chat_id=chat_id, text=message_to_send)
                                    bot.sendSticker(chat_id=chat_id, sticker=beer_sticker_id)
                                    bot.sendAudio(chat_id=chat_id, audio=gay_bar, title="GayBar", performer="E6", duration=140)
                                else:
                                    message_to_send = "Выгуляй свои $5 где-нибудь в другом месте"
                                    bot.sendMessage(chat_id=chat_id, text=message_to_send)
                            elif text == "/unsubscribe":
                                tguser = get_tguser(user)
                                if not tguser:
                                    message_to_send = "Чтобы отписаться, надо сначала подписаться"
                                    bot.sendMessage(chat_id=chat_id, text=message_to_send)
                                else:
                                    remove_user(tguser)
                                    message_to_send = tguser.username + " has been timed out"
                                    bot.sendMessage(chat_id=chat_id, text=message_to_send)
                            elif text == "/vk":
                                bot.sendMessage(chat_id=chat_id, text="https://vk.com/mad_streams")
                            elif text == "/etz":
                                bot.sendMessage(chat_id=chat_id, text="http://www.twitch.tv/etozhezanuda")
                            elif text == "/subcam":
                                bot.sendPhoto(chat_id=chat_id, photo=random.choice(photos))
                            elif text == "/up":
                                txt = "Стрим идёт, алё! Заходи: http://www.twitch.tv/etozhemad" if is_streaming else "Сейчас стрима нет"
                                bot.sendMessage(chat_id=chat_id, text=txt)
                except Exception as e:
                    print(e)
            else:
                pass
                # print("No updates")
            time.sleep(1)
        print("Logging you off, Shepard")


class EtmInfoThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.last_stream_id = -1
        self.cur_delay = 30  # в секундах

    def run(self):
        global is_streaming

        while True:
            # url = 'https://api.twitch.tv/kraken/streams/etozhemad'
            url = 'https://api.twitch.tv/kraken/streams/welovegames'
            info = json.loads(urlopen(url, timeout=15).read().decode('utf-8'))
            stream = info['stream']
            if stream is not None:
                is_streaming = True
                print("Streaming!")
                stream_id = stream['_id']
                if self.last_stream_id != stream_id:
                    self.last_stream_id = stream_id
                    self.cur_delay = 60 * 10  # начинаем чекать раз в 10 минут
                    channel = stream['channel']
                    channel_status = channel['status']  # то что в шапке
                    game = stream['game']
                    msg = "Мэд завёл стрим! Игра - " + game + ". Название стрима - " + channel_status + ". Заходи: http://www.twitch.tv/etozhemad"
                    subs = get_all()
                    if len(subs) > 0:
                        for sub in subs:
                            tgid = sub.tgid
                            bot.sendMessage(chat_id=tgid, text=msg)
            else:
                is_streaming = False
                self.cur_delay = 30  # снова чекаем раз в 30 секунд
            time.sleep(self.cur_delay)


def start():
    bot_thread = BotThread()
    bot_thread.start()
    etminfo_thread = EtmInfoThread()
    etminfo_thread.start()


if __name__ == "__main__":
    start()
