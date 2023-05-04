from messages import except_msg
from keyboards import except_kb
from config import exception_channel_id


def excepted(func):
    def wrapper(bot, message):
        try:
            msg = func(bot, message)
            return msg
        except Exception as e:
            bot.send_message(exception_channel_id, e)
            bot.reply_to(message, except_msg, reply_markup=except_kb)

    return wrapper


def except_link_func(func):
    def wrapper(bot, message):
        try:
            msg = func(bot, message, path=r'texsts\Ссылки.txt')
            return msg
        except Exception as e:
            bot.send_message(exception_channel_id, e)
            bot.reply_to(message, except_msg, reply_markup=except_kb)

    return wrapper
