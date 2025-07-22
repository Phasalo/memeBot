from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

button_1: KeyboardButton = KeyboardButton(text='Кнопка 1')
button_2: KeyboardButton = KeyboardButton(text='Кнопка 2')

keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[button_1], [button_2]],
    resize_keyboard=True,
    one_time_keyboard=False)
