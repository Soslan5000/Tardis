from telebot import TeleBot
from config import TOKEN
from functions import send_menu, send_info, send_terms, send_timetable, send_links, send_review
from admin_funcs import admin_rele_func, change_links_func, change_link_test
from keyboards import exit_btn, redact_links_btn, back_btn
from keyboards import admin_menu_kb
from config import admin_password

bot = TeleBot(TOKEN)


# Раздел меню с командами
@bot.message_handler(commands=['start', 'menu'])
def menu(message):
    send_menu(bot, message)


# Раздел с информацией о школе
@bot.message_handler(commands=['info'])
def info(message):
    send_info(bot, message)


# Раздел с условиями работы
@bot.message_handler(commands=['terms'])
def terms(message):
    send_terms(bot, message)


# Раздел с расписанием
@bot.message_handler(commands=['timetable'])
def timetable(message):
    send_timetable(bot, message)


# Раздел с доступными ссылками
@bot.message_handler(commands=['links'])
def links(message):
    send_links(bot, message)


# Раздел с отзывами
@bot.message_handler(commands=['review'])
def review(message):
    send_review(bot, message)


# Реакция на случайные нажатия на этапе выбора команды или вход в админ-панель
@bot.message_handler(content_types=["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice",
                                    "location", "contact", "new_chat_members", "left_chat_member", "new_chat_title",
                                    "new_chat_photo", "delete_chat_photo", "group_chat_created",
                                    "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                                    "migrate_from_chat_id", "pinned_message"])
def menu(message):
    text = message.text
    chat_id = message.chat.id
    if text == admin_password:  # Вход в админ-панель при правильном пароле
        msg = bot.send_message(chat_id, 'Вы активировали админ-панель', reply_markup=admin_menu_kb)
        if msg is not None:
            bot.register_next_step_handler(msg, admin_rele)
    else:  # Выход в меню при неверном пароле
        send_menu(bot, message)


def admin_rele(message):
    text = message.text
    chat_id = message.chat.id
    if text == exit_btn:  # Выход из админ-панели в главное меню, если была нажата кнопка "Выход"
        send_menu(bot, message)
    elif text == redact_links_btn:  # Переход на редактирования ссылок, если была нажата кнопка "Редактировать раздел links"
        msg = admin_rele_func(bot, message)
        if msg is not None:
            bot.register_next_step_handler(msg, change_links)
    else:
        msg = bot.send_message(chat_id, 'Воспользуйтесь кнопками', reply_markup=admin_menu_kb)
        bot.register_next_step_handler(msg, admin_rele)


########################################################################################################################
def change_links(message):
    """Раздел редактирования ссылок, которые может увидеть пользователь, вызывая команду links
    Если нажата кнопка выхода, то выходим в меню
    Если нажата кнопка назад, возвращаемся в меню админ-панели
    Иначе, список ссылок заменяется на тот, который прописан в сообщении
    Перед тем, как произойдёт замена, формат сообщения проверяется функцией change_link_test(text)
    Если формат сообщения неверный, то бот попросит повторить ввод ссылок"""

    text = message.text
    chat_id = message.chat.id
    if text == exit_btn:
        send_menu(bot, message)
    elif text == back_btn:
        msg = bot.send_message(chat_id, 'Главное меню админ-панели', reply_markup=admin_menu_kb)
        bot.register_next_step_handler(msg, admin_rele)
    else:
        if change_link_test(text):
            msg = change_links_func(bot, message)
            if msg is not None:
                msg = bot.send_message(chat_id, 'Меню админ-панели', reply_markup=admin_menu_kb)
                bot.register_next_step_handler(msg, admin_rele)
        else:
            msg = bot.send_message(chat_id, 'Следует написать список ссылок в нужном формате')
            if msg is not None:
                bot.register_next_step_handler(msg, change_links)
########################################################################################################################


if __name__ == '__main__':
    bot.polling(none_stop=True)
