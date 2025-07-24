from typing import Optional
from aiogram.types import Message

from phrases import PHRASES_RU
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
    commands_text = "\n".join(command.__str__() for command in available_commands)
    await message.answer(PHRASES_RU.title.commands + commands_text)


@cmd('ban', router, 'заблокировать пользователя по ID')             # /ban
@decorators.user_id_argument_command
async def _(message: Message, user_id):
    if message.from_user.id == int(user_id):
        await message.answer(PHRASES_RU.error.ban_yourself)
        return
    with UsersTable() as user_db:
        if user_db.set_ban_status(user_id, message.from_user.id, True):
            await message.answer(PHRASES_RU.replace('success.banned', user_id=user_id))
        else:
            await message.answer(PHRASES_RU.error.db)


@cmd('unban', router, 'разблокировать пользователя по ID')          # /unban
@decorators.user_id_argument_command
async def _(message: Message, user_id):
    pass


@cmd('promote', router, 'повышает уровень доступа пользователя')    # /promote
@decorators.user_id_argument_command
async def _(message: Message, user_id):
    pass


@cmd('demote', router, 'понижает уровень доступа пользователя')     # /demote
@decorators.user_id_argument_command
async def _(message: Message, user_id):
    with UsersTable() as users_db:
        if users_db.set_admin(user_id, message.from_user.id, False):
            await message.answer(PHRASES_RU.replace('success.demoted', user_id=user_id))
        else:
            await message.answer(PHRASES_RU.error.db)


@cmd('query', router, 'последние N запросов')          # /query
@decorators.digit_argument_command
async def cmd_query(message: Message, amount: Optional[int]):
    amount = 5 if not amount else amount

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
@decorators.user_id_argument_command
async def cmd_user_query(message: Message, user_id: int):
    await ikb.user_query_by_page(message.from_user.id, user_id)
