from aiogram import Router
from aiogram.types import CallbackQuery
from bot.keyboards import inline_keyboards as ikb
from bot.models import CutMessageCallBack

router = Router()


@router.callback_query(CutMessageCallBack.filter())
async def cut_message_distributor(callback: CallbackQuery, callback_data: CutMessageCallBack):
    action = callback_data.action
    page = callback_data.page
    user_id = callback_data.user_id
    if action == 1:
        await ikb.get_users_by_page(callback.from_user.id, page, callback.message.message_id)
    elif action == 2:
        await ikb.user_query_by_page(callback.from_user.id, user_id, page, callback.message.message_id)
    elif action == -1:
        await callback.answer()
