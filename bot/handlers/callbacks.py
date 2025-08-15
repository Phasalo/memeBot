import logging
import os
from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile
from aiogram.utils.chat_action import ChatActionSender

from DB.models import UserModel
from DB.tables.queries import QueriesTable
from DB.tables.users import UsersTable
from bot.bot_utils.models import PageCallBack, GenerateCallBack, SetsCallBack, ModeCallBack, ColorCallBack
from bot.handlers.default import settings_handler
from bot.keyboards import inline as ikb
from bot import pages
from config import bot
from config.const import MemeModes, SettingsAction, ColorFields
from phrases import PHRASES_RU
from utils.image_generation import mem_generator

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(PageCallBack.filter())
async def cut_message_distributor(callback: CallbackQuery, callback_data: PageCallBack):
    type_of_event = callback_data.type_of_event
    page = callback_data.page
    user_id = callback_data.user_id
    await callback.answer()
    if type_of_event == 1:
        await pages.get_users(callback.from_user.id, page, callback.message.message_id)
    elif type_of_event == 2:
        await pages.user_query(callback.from_user.id, user_id, page, callback.message.message_id)
    elif type_of_event == -1:
        pass


async def _user_mode(user_loc: UserModel, callback: CallbackQuery):
    current_mode_name = PHRASES_RU.replace('answer.current_mode', mode=MemeModes.get_name(user_loc.mode))
    try:
        await callback.message.edit_text(current_mode_name, reply_markup=ikb.get_mode_keyboard(user_loc.mode))
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            pass
        else:
            raise


async def _color_mode(callback: CallbackQuery, user: UserModel, action: SettingsAction):
    text_part, color = {
        SettingsAction.UPPER_TEXT: ("верхнего текста", user.upper_color),
        SettingsAction.BOTTOM_TEXT: ("нижнего текста", user.bottom_color),
        SettingsAction.UPPER_STROKE: ("контура верхнего текста", user.upper_stroke_color),
        SettingsAction.BOTTOM_STROKE: ("контура нижнего текста", user.bottom_stroke_color),
    }[action]

    message_text = PHRASES_RU.replace('answer.choose_color', text_part=text_part)
    try:
        await callback.message.edit_text(message_text, reply_markup=ikb.get_color_keyboard(color, action))
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            pass
        else:
            raise


@router.callback_query(SetsCallBack.filter())
async def settings_button_distributor(callback: CallbackQuery, callback_data: SetsCallBack, user_row: UserModel):
    async def _text_case(user: UserModel):
        await callback.message.edit_text(f'Сейчас стоят {"<b>БАЛЬШИЕ БУКАВЫ</b>" if user.giant_text else "<i>маленькие буковки</i>"}',
                                         reply_markup=ikb.get_case_keyboard(user.giant_text))

    action = callback_data.action
    if user_row is None:
        await callback.message.answer('Произошла ошибка!')
        logger.error(
            'Cannot check user setting. The \'user_row\' '
            f'key was not found in the middleware data. user_id={callback.from_user.id}'
        )
        return

    match action:
        case SettingsAction.SETTINGS:
            await settings_handler(callback.message, user_row, True)

        case SettingsAction.USER_MODE:
            await _user_mode(user_row, callback)

        case SettingsAction.UPPER_TEXT | SettingsAction.BOTTOM_TEXT | SettingsAction.UPPER_STROKE | SettingsAction.BOTTOM_STROKE:
            await _color_mode(callback, user_row, action)

        case SettingsAction.TEXTCASE:
            await _text_case(user_row)

        case SettingsAction.SET_GIANT_CASE | SettingsAction.SET_SMALL_CASE:
            with UsersTable() as db:
                db.change_text_case(callback.from_user.id, True if action == SettingsAction.SET_GIANT_CASE else False)
                user_row.giant_text = action == SettingsAction.SET_GIANT_CASE
                await _text_case(user_row)


@router.callback_query(ModeCallBack.filter())
async def mode_distributor(callback: CallbackQuery, callback_data: ModeCallBack):
    with UsersTable() as db:
        db.change_mode(callback.from_user.id, callback_data.mode)
        user = db.get_user(callback.from_user.id)
        await _user_mode(user, callback)


@router.callback_query(ColorCallBack.filter())
async def color_distributor(callback: CallbackQuery, callback_data: ColorCallBack):
    color = callback_data.color
    action = callback_data.action

    field_mapping = {
        SettingsAction.UPPER_TEXT: ColorFields.UPPER,
        SettingsAction.BOTTOM_TEXT: ColorFields.BOTTOM,
        SettingsAction.UPPER_STROKE: ColorFields.UPPER_STROKE,
        SettingsAction.BOTTOM_STROKE: ColorFields.BOTTOM_STROKE
    }

    with UsersTable() as db:
        if field := field_mapping.get(action):
            db.change_color(callback.from_user.id, color, field)
        user = db.get_user(callback.from_user.id)

    await _color_mode(callback, user, action)


@router.callback_query(GenerateCallBack.filter())
async def regenerate_button_distributor(callback: CallbackQuery, callback_data: GenerateCallBack, user_row: UserModel):
    async with ChatActionSender(bot=bot, chat_id=callback.from_user.id, action='upload_photo'):
        query_id = callback_data.query_id
        with QueriesTable() as db:
            query = db.get_query(query_id)
            meme_txt = query.query_text.strip().split('\n')[:3]
            meme_txt[0] = meme_txt[0].replace('/', '').replace("\\", '')
            meme_path = await mem_generator.create_meme(None, *meme_txt,
                                                        mode=user_row.mode,
                                                        upper_color=user_row.upper_color,
                                                        bottom_color=user_row.bottom_color,
                                                        upper_stroke_color=user_row.upper_stroke_color,
                                                        bottom_stroke_color=user_row.bottom_stroke_color,
                                                        stroke_width=user_row.stroke_width,
                                                        giant_text=user_row.giant_text)
            await callback.message.edit_media(media=InputMediaPhoto(media=FSInputFile(meme_path)),
                                              reply_markup=ikb.get_photo_inline_keyboard(query_id))
            os.remove(meme_path)
