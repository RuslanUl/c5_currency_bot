import telebot
import traceback

from config import *
from extensions import APIException, Convertor

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Приветствую!\nЧтобы начать работу введите команду боту в следующем формате: \n <имя валюты>' \
           '<в какую валюту преревести><количество валюты>\nУвидеть список всех доступных валют: /values\n' \
           'Пример:\nдоллар рубль 100'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def value(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = "\n".join((text, key,))
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split()
    try:
        if len(values) != 3:
            raise APIException("Неверное количество параметров!")

        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)


bot.polling()
