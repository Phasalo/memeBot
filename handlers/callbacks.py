from aiogram import Router, F
from aiogram.types import CallbackQuery
from DB.db_interface import AbstractMovieDB
from config_data.config import config
from keyboards import user_keyboards, main_keyboard
from DB.db_factory import DBFactory
from handlers.callbacks_data import TemplateCallBack

router = Router()

db_instance: AbstractMovieDB = DBFactory.get_db_instance(config)


@router.callback_query(TemplateCallBack.filter())
async def moderate_film_callbacks(callback: CallbackQuery, callback_data: TemplateCallBack):
    pass
