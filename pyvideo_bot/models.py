import queue
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

class DownloadQueue:
    def __init__(self):
        self.q = queue.Queue()

    def add(self, item):
        self.q.put(item)

    def get(self):
        return self.q.get()

    def is_empty(self):
        return self.q.empty()

    def size(self):
        return self.q.qsize()

class Menu:
    @staticmethod
    def create(items):
        menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for item in items:
            button = KeyboardButton(item)
            menu.add(button)
        return menu
