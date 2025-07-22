from aiogram.filters.callback_data import CallbackData


class CutMessageCallBack(CallbackData, prefix="cut"):
    action: int
    user_id: int = 0
    page: int = 1
