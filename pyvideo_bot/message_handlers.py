import time
import yt_dlp as youtube_dl
from models import Menu
from concurrent.futures import ThreadPoolExecutor
from yt_dlp import YoutubeDL
from bot import executor, download_queues


# Creating a ThreadPoolExecutor instance for handling video download tasks
executor = ThreadPoolExecutor(max_workers=5)


def start_handler(bot, message):
    """
    Handle /start command.
    """
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(2)
    bot.send_message(message.chat.id, "Welcome to the YouTube video downloader bot. Send me a YouTube video URL and I'll help you download it! \U0001F601")


def help_handler(bot, message, menu):
    """
    Handle /help command.
    """
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(2)
    help_message = "Here's a list of available commands:\n\n" \
                   "/start - Start the bot\n" \
                   "/help - Show this help message\n" \
                   "/info - Show information about the bot\n"
    bot.send_message(message.chat.id, help_message)


def info_handler(bot, message):
    """
    Handle /info command.
    """
    bot.send_message(message.chat.id, "Reminder to place some info about the bot here")


def default_handler(bot, message):
    """
    Handle all other messages that are not commands.
    """
    url = message.text

    if not url.startswith('http'):
        return

    video_qualities = get_video_qualities(url)

    if not video_qualities:
        bot.send_message(message.chat.id, 'Sorry, this video cannot be downloaded. Please try another one.')
        return

    qualities_menu = Menu.create(video_qualities)
    bot.send_message(message.chat.id, 'Please choose the video quality:', reply_markup=qualities_menu)

    bot.register_next_step_handler(message, handle_quality_choice, url, video_qualities)


def handle_quality_choice(bot, message, url, qualities):
    """
    Handle the user's choice of video quality.
    """
    chosen_quality = message.text

    if chosen_quality not in qualities:
        bot.send_message(message.chat.id, 'Invalid choice. Please choose a valid video quality.')
        bot.register_next_step_handler(message, handle_quality_choice, url, qualities)
    else:
        bot.send_message(message.chat.id, f'Downloading video in {chosen_quality} quality...')

        future = executor.submit(download_video, bot, message, url, chosen_quality)
        future.add_done_callback(lambda f: bot.send_message(message.chat.id, 'Download complete!'))


def get_video_qualities(video_url):
    """
    Get available video qualities from a YouTube video.
    """
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
            quality = f.get('format_note')
            if quality and quality not in qualities:
                qualities.append(quality)

    return qualities


def download_video(bot, message, url, quality):
    """
    Download a video using the provided url and quality.
    """
    bot.send_chat_action(message.chat.id, 'upload_video')
    options = {
        'format': quality,
        'outtmpl': 'downloads/%(title)s.%(ext)s'
    }

    try:
        with YoutubeDL(options) as ydl:
            ydl.download([url])
    except Exception as e:
        bot.send_message(message.chat.id, "An error occurred while downloading the video.")
        print(f"An error occurred: {e}")


def handle_quality_choice(bot, message, url, qualities):
    """
    Handle the choice of video quality for download.

    Parameters
    ----------
    bot : telebot.TeleBot
        The bot instance.
    message : telebot.types.Message
        The message instance.
    url : str
        The YouTube video URL.
    qualities : list
        The list of available video qualities.

    Returns
    -------
    None
    """
    chosen_quality = message.text

    if chosen_quality not in qualities:
        bot.send_message(message.chat.id, 'Invalid choice. Please choose a valid video quality.')
        bot.register_next_step_handler(message, handle_quality_choice, url, qualities)
    else:
        bot.send_message(message.chat.id, f'Downloading video in {chosen_quality} quality...')

        # Submit the download job to the executor
        future = executor.submit(download_video, bot, message, url, chosen_quality)
        
        # Store the future in the download queue
        download_queues[message.chat.id] = future

        # Add a callback to inform the user when the download is complete
        future.add_done_callback(lambda f: bot.send_message(message.chat.id, 'Download complete!'))

        # Add another callback to remove the job from the queue when it's done
        future.add_done_callback(lambda f: download_queues.pop(message.chat.id, None))

