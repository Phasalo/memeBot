from aiogram.filters.callback_data import CallbackData


class TemplateCallBack(CallbackData, prefix="template"):
    action: int
    user_id: int = 0
    page: int = 1
