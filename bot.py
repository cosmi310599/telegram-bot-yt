import telebot
import yt_dlp as youtube_dl
import os
import time
import emoji
import requests


BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


menu = telebot.types.ReplyKeyboardMarkup()
menu.row('/start', '/info', '/help')



@bot.message_handler(commands=['start', 'hello', 'Start', 'Hello'])
def start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(2)
    bot.send_message(message.chat.id, "Welcome to the YouTube video downloader bot. Send me a YouTube video URL and I'll help you download it! \U0001F601")


@bot.message_handler(commands=['help','Help'])
def help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(2)
    # help_message = "Here's a list of available commands:\n\n" \
    #                "/start - Start the bot\n" \
    #                "/help - Show this help message\n" \
    #                "/info - Show information about the bot\n"
    # bot.send_message(message.chat.id, help_message)
    bot.send_message(message.chat.id, "In the section above you will be able to see the available commands: ", reply_markup=menu)


@bot.message_handler(commands=['info','Info'])
def info(message):
    bot.send_message(message.chat.id, "Reminder to place some info about the bot here")

# @bot.message_handler(commands=['clear', 'Clear'])
# def clear_chat_history(message):
#     try:
#        pass
#     except Exception as e:
#         bot.send_message(message.cat.id, f"An error ocurred: {e}")
#         return False 
    

# @bot.message_handler(func=lambda message: True)
# def handle_message(message):
#     bot.send_message(message.chat.id, "I'm sorry, I didn't understand that command. Use the /help command to see a list of available commands.")


# def get_video_qualities(video_url):


def get_video_qualities(video_url):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'forceurl': True,
        'simulate': True,
        'no_warnings': True,
        'youtube_include_dash_manifest': False,
        'youtube_include_hls_manifest': False,
        'listformats': True
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        formats = info_dict.get('formats', None)

    if not formats:
        return []

    qualities = []
    for f in formats:
        if f.get('ext') == 'mp4' and f.get('vcodec') != 'none':
            quality = f.get('format_note', 'unknown')
            if quality not in qualities:
                qualities.append(quality)

    return qualities


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    
    ydl_opts = {
        'quiet': False,
        'simulate': False,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'outtmpl': '%(title)s.%(ext)s'
    }


    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url)
            video_path = ydl.prepare_filename(info_dict)
            video = open(video_path, 'rb')
            bot.send_video(message.chat.id, video)
            video.close()
            
        except Exception as e:
            bot.send_message(message.chat.id, f"An error occurred: {e}")
            


bot.polling()
