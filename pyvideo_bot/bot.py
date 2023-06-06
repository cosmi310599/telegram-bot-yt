import os
import time
import telebot

from message_handlers import start_handler, help_handler, info_handler, default_handler
import emoji 

from models import DownloadQueue

download_queue = DownloadQueue()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

menu = telebot.types.ReplyKeyboardMarkup()
menu.row("/start \U000025B6", "/info \U00002139", "/help \U00002754")

@bot.message_handler(commands=['start', 'hello', 'Start', 'Hello'])
def start(message):
    start_handler(bot, message)

@bot.message_handler(commands=['help','Help'])
def help(message):
    help_handler(bot, message, menu)

@bot.message_handler(commands=['info','Info'])
def info(message):
    info_handler(bot, message)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    default_handler(bot, message)


if __name__ == '__main__':
    bot.polling()
