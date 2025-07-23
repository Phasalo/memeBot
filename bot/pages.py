from aiogram.types import Message, CallbackQuery
from typing import Union, Callable, Any
from math import ceil


async def __init_page(event: Union[Message, CallbackQuery]):
    if isinstance(event, CallbackQuery):
        await event.answer()


def make_page_counter(page_number: int, max_page_number: int) -> str:
    return f'\n<i>Страница {page_number} из {max_page_number}</i>'


def calculate_page_number(quantity_items: int, page_size: int) -> int:
    return ceil(quantity_items / page_size)


async def make_page(event: Union[Message, CallbackQuery],
                    database: Database,
                    string_processor: Callable[[Any], str],
                    page_size: int,
                    page_number: int):
    """Генератор страниц"""
    if isinstance(event, CallbackQuery):
        await event.answer()

    page = database.get_by_page(page_number, page_size)
    max_page_number = calculate_page_number(database.count(), page_size)
    msg_text = [phrases['title']['users']]

    for i, row in enumerate(page):
        if i < len(page):
            msg_text.append(string_processor(*row))

    msg_text.append(make_page_counter(page_number, max_page_number))

    msg_text = ''.join(msg_text)
    page_kb = kb.make_page(page_number, max_page_number)

    if isinstance(event, Message):
        await event.answer(text=msg_text, reply_markup=page_kb)
    else:
        await event.message.edit_text(text=msg_text, reply_markup=page_kb)
