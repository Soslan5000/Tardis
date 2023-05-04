from messages import *
from keyboards import menu_kb, info_kb, terms_kb, timetable_kb, links_kb, review_kb
from decorators import excepted
import time
from inline_keyboards import create_kb_for_links

conv_time = lambda x: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(x))


@excepted
def send_menu(bot, message):
    bot.send_message(message.chat.id, menu_msg, reply_markup=menu_kb)


@excepted
def send_info(bot, message):
    bot.send_message(message.chat.id, info_msg, reply_markup=info_kb)


@excepted
def send_terms(bot, message):
    bot.send_message(message.chat.id, terms_msg, reply_markup=terms_kb)


@excepted
def send_timetable(bot, message):
    bot.send_message(message.chat.id, timetable_msg, reply_markup=timetable_kb)


@excepted
def send_links(bot, message):
    inl_links_kb = create_kb_for_links()
    bot.send_message(message.chat.id, links_msg, reply_markup=inl_links_kb)
    bot.send_message(message.chat.id, 'Для возврата нажмите "В меню"', reply_markup=links_kb)


@excepted
def send_review(bot, message):
    bot.send_message(message.chat.id, review_msg, reply_markup=review_kb)
