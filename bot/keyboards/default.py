from aiogram.utils.keyboard import ReplyKeyboardMarkup as KMarkup
from aiogram.utils.keyboard import KeyboardButton as KButton

from config.const import MemeModes
from phrases import PHRASES_RU


def __make_placeholder_appeal() -> str:
    return PHRASES_RU.placeholder_appeal


meme_button: KButton = KButton(text=MemeModes.IN_NAME)
demotivator_button: KButton = KButton(text=MemeModes.DE_NAME)
book_button: KButton = KButton(text=MemeModes.BO_NAME)
settings_button: KButton = KButton(text=PHRASES_RU.button.settings)

basic_keyboard: KMarkup = KMarkup(
    keyboard=[
        [meme_button, demotivator_button],
        [book_button, settings_button]],
    resize_keyboard=True)
