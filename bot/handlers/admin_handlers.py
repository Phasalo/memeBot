from typing import Optional
from aiogram.types import Message

from DB.phrases.phrases import PHRASES_RU
from DB.tables.queries import QueriesTable
from DB.tables.users import UsersTable
from utils import format_string
from bot import decorators
from bot.keyboards import inline_keyboards as ikb
from bot.decorators import available_commands, cmd
from bot.routers import AdminRouter

router = AdminRouter()


@cmd('get_users', router, 'таблица со всем пользователями')         # /get_users
async def _(message: Message):
    await ikb.get_users_by_page(message.from_user.id)


@cmd('getcmds', router, 'список всех доступных команд')             # /getcmds
async def _(message: Message):
    commands_text = "\n".join(
        command.__str__() for command in available_commands
    )
    await message.answer(f"<b>📜 Доступные команды:</b>\n\n{commands_text}")


@cmd('ban', router, 'заблокировать пользователя по ID')             # /ban
@decorators.one_argument_command
async def _(message: Message, user_id):
    if message.from_user.id == int(user_id):
        await message.answer(PHRASES_RU.errors.ban_yourself)
        return
    with UsersTable() as user_db:
        ok = user_db.set_ban_status(user_id, message.from_user.id, True)
        if ok:
            await message.answer(PHRASES_RU.get('success.user_banned', user_id=user_id))
        else:
            await message.answer(PHRASES_RU.errors.db_error)


@cmd('unban', router, 'разблокировать пользователя по ID')          # /unban
async def _(message: Message, user_id):
    pass


@cmd('promote', router, 'повышает уровень доступа пользователя')    # /promote
async def _(message: Message, user_id):
    pass


@cmd('demote', router, 'понижает уровень доступа пользователя')     # /demote
@decorators.one_argument_command
async def _(message: Message, user_id):
    if not user_id:
        await message.answer(PHRASES_RU.errors.wrong_user_id)
        return
    with UsersTable() as users_db:
        ok = users_db.set_admin(user_id, message.from_user.id, False)
        if ok:
            await message.answer(PHRASES_RU.get('success.user_demoted', user_id=user_id))
        else:
            await message.answer(PHRASES_RU.errors.db_error)


@cmd('root', router, 'команда для супер-администратора')            # /root
async def _(message: Message):
    pass


@cmd('query', router, 'последние N запросов пользователя')          # /query
@decorators.one_argument_command
async def cmd_query(message: Message, amount: Optional[int]):
    if not amount:
        amount = 5

    with QueriesTable() as queries_db:
        queries = queries_db.get_last_queries(int(amount))
        if not queries:
            await message.answer('Запросов не было')
            return

        txt = format_string.format_queries_text(
            queries=queries,
            header_template='',
            line_template="{username} <blockquote>{time}</blockquote> <i>{query}</i>\n\n",
            show_username=True
        )

        if txt:
            await message.answer(txt.replace('\t', '\n'), disable_web_page_preview=True)


@cmd('user_query', router, 'запросы пользователя по ID')            # /user_query
@decorators.one_argument_command
async def cmd_user_query(message: Message, user_id_to_find: int):
    await ikb.user_query_by_page(message.from_user.id, user_id_to_find)
