import time
import yt_dlp as youtube_dl
from models import Menu

def start_handler(bot, message):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(2)
    bot.send_message(message.chat.id, "Welcome to the YouTube video downloader bot. Send me a YouTube video URL and I'll help you download it! \U0001F601")

def help_handler(bot, message, menu):
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(2)
    help_message = "Here's a list of available commands:\n\n" \
                   "/start - Start the bot\n" \
                   "/help - Show this help message\n" \
                   "/info - Show information about the bot\n"
    bot.send_message(message.chat.id, help_message)
    
    
def info_handler(bot, message):
    bot.send_message(message.chat.id, "Reminder to place some info about the bot here")

def default_handler(bot, message):
    url = message.text

    if not url.startswith('http'):
        return

    video_qualities = get_video_qualities(url)

    if not video_qualities:
        bot.send_message(message.chat.id, 'Sorry, this video cannot be downloaded. Please try another one.')
        return

    qualities_menu = Menu.create(video_qualities)
    bot.send_message(message.chat.id, 'Please choose the video quality:', reply_markup=qualities_menu)

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
