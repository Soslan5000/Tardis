from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton


def create_kb_for_links(path=r'texsts\Ссылки.txt'):
    keyboard_for_links = InlineKeyboardMarkup()
    with open(path, 'r', encoding='utf-8') as f:
        for row in f:
            text, url = row.split('___')
            btn = InlineKeyboardButton(text=text, url=url)
            keyboard_for_links.row(btn)
    return keyboard_for_links
