from telebot.types import ReplyKeyboardMarkup

menu_btn = '/menu'
info_btn = '/info'
terms_btn = '/terms'
timetable_btn = '/timetable'
links_btn = '/links'
review_btn = '/review'
back_to_the_menu_btn = 'Вернуться в меню'
exit_btn = 'Выход'
redact_links_btn = 'Редактировать раздел links'
back_btn = 'Назад'

menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
menu_kb.row(menu_btn, info_btn, terms_btn)
menu_kb.row(timetable_btn, links_btn, review_btn)

info_kb = ReplyKeyboardMarkup(resize_keyboard=True)
info_kb.row(back_to_the_menu_btn)

terms_kb = ReplyKeyboardMarkup(resize_keyboard=True)
terms_kb.row(back_to_the_menu_btn)

timetable_kb = ReplyKeyboardMarkup(resize_keyboard=True)
timetable_kb.row(back_to_the_menu_btn)

links_kb = ReplyKeyboardMarkup(resize_keyboard=True)
links_kb.row(back_to_the_menu_btn)

review_kb = ReplyKeyboardMarkup(resize_keyboard=True)
review_kb.row(back_to_the_menu_btn)

except_kb = ReplyKeyboardMarkup(resize_keyboard=True)
except_kb.row(back_to_the_menu_btn)

admin_menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
admin_menu_kb.row(exit_btn)
admin_menu_kb.row(redact_links_btn)

exit_kb = ReplyKeyboardMarkup(resize_keyboard=True)
exit_kb.row(exit_btn)

exit_back_kb = ReplyKeyboardMarkup(resize_keyboard=True)
exit_back_kb.row(exit_btn)
exit_back_kb.row(back_btn)
