from keyboards import admin_menu_kb, exit_back_kb
from decorators import except_link_func, excepted


@excepted
def admin_rele_func(bot, message):
    """Функция, вызывающаяся в момент редактирования ссылок"""

    preview_links_func(bot, message)
    msg = bot.send_message(message.chat.id, 'Внесите изменения', reply_markup=exit_back_kb)
    return msg


@except_link_func
def preview_links_func(bot, message, path=r'texsts\Ссылки.txt'):
    """Функция, выводящая список ссылок на внешние источники в боте"""

    with open(path, 'r', encoding='utf-8') as f:
        links = ''.join(f.readlines())
        bot.send_message(message.chat.id, links, disable_web_page_preview=True)


@except_link_func
def change_links_func(bot, message, path=r'texsts\Ссылки.txt'):
    """Принимает параметр message со списком ссылок и вставляет эти ссылки вместо старых"""

    with open(path, 'w', encoding='utf-8') as f:
        f.write(message.text)
    msg = bot.send_message(message.chat.id, 'Изменения сохранены', reply_markup=admin_menu_kb)
    return msg


def change_link_test(text):
    """Принимает на вход текст с ссылками на внешние источники и проверяет, соответствует ли он формату
    <текст1>___<ссылка1>
    <текст2>___<ссылка2>
    и т.д."""

    text = text.split('\n')  # Разбиваем текст на строки
    for row in text:  # Проходимся в тексте по каждой строчке
        if row.count('___') != 1 or row.count('_') != 3 or len(row.split('___')) != 2 or row.split('___')[-1] == '':  # Проверяем на корректность введённые ссылки
            return False
    return True
