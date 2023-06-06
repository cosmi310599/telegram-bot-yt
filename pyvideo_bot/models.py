from telebot.types import ReplyKeyboardMarkup, KeyboardButton

class Menu:
    @staticmethod
    def create(items):
        menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for item in items:
            button = KeyboardButton(item)
            menu.add(button)
        return menu
