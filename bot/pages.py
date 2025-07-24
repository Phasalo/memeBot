from aiogram.types import Message, CallbackQuery
from typing import Union, Callable, Any
from math import ceil
from DB.phrases import PHRASES_RU


# async def __make_page(event: Union[Message, CallbackQuery],
#                       title: str,
#                       database: Database,
#                       row_processor: Callable[[Any], str],
#                       page_size: int,
#                       page_number: int):
#     """Генератор страниц"""
#     if isinstance(event, CallbackQuery):
#         await event.answer()
#
#     page = database.get_by_page(page_number, page_size)
#     max_page_number = ceil(database.count() / page_size)
#     msg_text = [title]
#
#     for i, row in enumerate(page):
#         if i < len(page):
#             msg_text.append(row_processor(*row))
#
#     msg_text.append(PHRASES_RU.get('footnote.page', page_number=page_number, max_page_number=max_page_number))
#
#     msg_text = ''.join(msg_text)
#     page_kb = kb.make_page(page_number, max_page_number)
#
#     if isinstance(event, Message):
#         await event.answer(text=msg_text, reply_markup=page_kb)
#     else:
#         await event.message.edit_text(text=msg_text, reply_markup=page_kb)
