import os

from aiogram import F
from aiogram.utils.chat_action import ChatActionSender

from DB.models import UserModel, QueryModel
from DB.tables.queries import QueriesTable
from DB.tables.users import UsersTable
from bot.keyboards import default as kb, inline as ikb
from bot.handlers.admin import command_getcmds
from aiogram.types import Message, FSInputFile, InputMediaPhoto
from bot.bot_utils.routers import UserRouter, BaseRouter
from config import config, bot
from config.const import MemeModes, UserColors, IMAGE_DIR, TEMP_DIR
from phrases import PHRASES_RU
from utils.image_generation import mem_generator

router = UserRouter()


@router.command('start', 'запустить бота')  # /start
async def _(message: Message):
    await message.answer(PHRASES_RU.commands.start, reply_markup=kb.basic_keyboard)


@router.command('help', 'как пользоваться ботом')  # /help
async def _(message: Message):
    await message.answer(PHRASES_RU.commands.help, reply_markup=kb.basic_keyboard)


@router.command('about', 'о разработчиках')  # /about
async def _(message: Message):
    await message.answer(PHRASES_RU.commands.about, disable_web_page_preview=True, reply_markup=kb.basic_keyboard)


@router.command(('commands', 'cmds'), 'список всех команд (это сообщение)')  # /commands /cmds
async def _(message: Message):
    commands_text = '\n'.join(str(command) for command in BaseRouter.available_commands if not command.is_admin)
    await message.answer(PHRASES_RU.title.commands + commands_text, reply_markup=kb.basic_keyboard)


@router.command('example', 'примеры созданных мемасов')  # /example
async def example_command(message: Message):
    async with ChatActionSender(bot=bot, chat_id=message.from_user.id, action='upload_photo'):
        photo1 = InputMediaPhoto(media=FSInputFile(IMAGE_DIR / 'example1.jpg'))
        photo2 = InputMediaPhoto(media=FSInputFile(IMAGE_DIR / 'example2.jpg'))
        photo3 = InputMediaPhoto(media=FSInputFile(IMAGE_DIR / 'example3.jpg'))

        await bot.send_media_group(media=[photo1, photo2, photo3], chat_id=message.chat.id)


@router.command('meme', 'мемас с случайным городом России')  # /meme
async def _(message: Message, user_row: UserModel):
    await send_meme(message, user=user_row, mode=MemeModes.IN, city_meme=True)


@router.command('deme', 'демотиватор с случайным городом России')  # /deme
async def create_demo_command(message: Message, user_row: UserModel):
    await send_meme(message, user=user_row, mode=MemeModes.DE, city_meme=True)


@router.message(F.text == config.tg_bot.password)
async def _(message: Message):
    with UsersTable() as users_db:
        if users_db.set_admin(message.from_user.id, message.from_user.id):
            await message.delete()
            await message.answer(PHRASES_RU.success.promoted)
            await command_getcmds(message)
        else:
            await message.answer(PHRASES_RU.error.db, reply_markup=kb.basic_keyboard)


@router.message(F.text == PHRASES_RU.button.settings)
async def settings_handler(message: Message, user_row: UserModel, edit=False):
    #                                        ^^^^^^^^^^^^^^^^^^^^
    #                                        <-- anti phasalo -->

    txt = ('<b>Твои текущие настройки</b>\n\n'
           f'Режим: <i><b>{MemeModes.get_name(user_row.mode)}</b></i>\n'
           f'Цвет верхнего текста: <i><u>{UserColors.get_color_name_by_hash(user_row.upper_color)}</u></i>\n'
           f'Цвет нижнего текста: <i><u>{UserColors.get_color_name_by_hash(user_row.bottom_color)}</u></i>\n'
           f'Контур верхнего текста: <i><u>{UserColors.get_color_name_by_hash(user_row.upper_stroke_color)}</u></i>\n'
           f'Контур нижнего текста: <i><u>{UserColors.get_color_name_by_hash(user_row.bottom_stroke_color)}</u></i>\n'
           f'Регистр текста: <i>{"<b>БАЛЬШИЕ БУКАВЫ</b>" if user_row.giant_text else "маленькие буковки"}</i>\n')
    if edit:
        await message.edit_text(txt, reply_markup=ikb.get_keyboard())
    else:
        await message.answer(txt, reply_markup=ikb.get_keyboard())


@router.message(F.text == MemeModes.DE_NAME)
async def set_demotivator(message: Message):
    with UsersTable() as db:
        db.change_mode(message.from_user.id, MemeModes.DE)
    await message.answer(PHRASES_RU.replace('answer.mode_changed', mode=MemeModes.DE_NAME.lower()), reply_markup=kb.basic_keyboard)


@router.message(F.text == MemeModes.IN_NAME)
async def set_meme(message: Message):
    with UsersTable() as db:
        db.change_mode(message.from_user.id, MemeModes.IN)
    await message.answer(PHRASES_RU.replace('answer.mode_changed', mode=MemeModes.IN_NAME.lower()), reply_markup=kb.basic_keyboard)


@router.message(F.text == MemeModes.BO_NAME)
async def set_book(message: Message, ):
    with UsersTable() as db:
        db.change_mode(message.from_user.id, MemeModes.BO)
    await message.answer(PHRASES_RU.replace('answer.mode_changed', mode=MemeModes.BO_NAME.lower()), reply_markup=kb.basic_keyboard)


async def send_meme(message: Message, user: UserModel, mode=None, city_meme=False):
    async with ChatActionSender(bot=bot, chat_id=message.from_user.id, action='upload_photo'):
        try:
            if message.text is None and message.caption is None:
                await message.answer(PHRASES_RU.answer.no_caption)
                return
            meme_txt = message.text if message.text else message.caption
            with QueriesTable() as queries_db:
                query = queries_db.add_query(QueryModel(user.user_id, meme_txt))
            meme_txt = meme_txt.strip().split('\n')[:3]
            meme_txt[0] = meme_txt[0].replace('/', '').replace("\\", '')
            photo_path = None
            if city_meme:
                meme_txt = [None, None, None]
            if message.photo:
                photo_path = str(TEMP_DIR / f'photo{user.user_id}-{query.query_id}.jpg')
                await bot.download_file((await bot.get_file(message.photo[-1].file_id)).file_path, photo_path)

            meme_path = await mem_generator.create_meme(photo_path, *meme_txt,
                                                        mode=mode if mode else user.mode,
                                                        upper_color=user.upper_color,
                                                        bottom_color=user.bottom_color,
                                                        upper_stroke_color=user.upper_stroke_color,
                                                        bottom_stroke_color=user.bottom_stroke_color,
                                                        stroke_width=user.stroke_width,
                                                        giant_text=user.giant_text)

            keyboard = kb.basic_keyboard if (city_meme or message.photo) else ikb.get_photo_inline_keyboard(query.query_id)
            await message.answer_photo(photo=FSInputFile(meme_path), reply_markup=keyboard)
            os.remove(meme_path)
        except Exception:
            await message.answer(PHRASES_RU.error.smth_went_wrong, reply_markup=kb.basic_keyboard)
            raise


@router.message(F.content_type.in_({'text', 'photo'}))
async def general_send_meme(message: Message, user_row: UserModel):
    await send_meme(message, user_row)


@router.message()
async def _(message: Message):
    await message.answer(text=PHRASES_RU.answer.unknown, reply_markup=kb.basic_keyboard)
