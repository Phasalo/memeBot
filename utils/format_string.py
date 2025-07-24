import re
from typing import List, Optional
from DB.models import UserModel, QueryModel
from phrases import PHRASES_RU
from DB.models import Pagination


def clear_string(text: str):
    if not text:
        return PHRASES_RU.icon.not_text
    return text.replace('<', '&lt;').replace('>', '&gt;').replace('&', '&amp;')


def find_first_number(input_string):
    match = re.search(r'\d+', input_string)

    if match:
        return int(match.group())
    else:
        return None


def get_query_count_emoji(count: int) -> str:
    for emoji, threshold in PHRASES_RU.icon.query.thresholds.__dict__.items():
        if count > threshold:
            return emoji
    return PHRASES_RU.icon.query.default


def format_user_list(users_info: List[UserModel], pagination: Pagination) -> str:
    txt = [PHRASES_RU.title.users,
           PHRASES_RU.replace('footnote.total', total=pagination.total_items)]

    for user in users_info:
        line_data = {
            'username': f'@{user.username}' if user.username else PHRASES_RU.icon.not_username,
            'user_id': str(user.user_id).ljust(12),
            'query_stat': f'{get_query_count_emoji(user.query_count)} {user.query_count}',
            'registration_date': user.registration_date.strftime("%d.%m.%Y")
        }

        user_line = PHRASES_RU.replace('template.user', **line_data)

        if user.is_banned:
            txt.append(f'<s>{user_line}</s>')
        elif user.is_admin:
            txt.append(f'<b>{user_line}</b>')
        else:
            txt.append(user_line)

    txt.append('<code>.</code>\n' * (pagination.per_page - len(users_info)))

    return ''.join(txt)


def format_queries_text(
        queries: List[QueryModel],
        username: Optional[str] = None,
        user_id: Optional[int] = None,
        footnote_template: str = PHRASES_RU.footnote.user_query,
        line_template: str = PHRASES_RU.template.user_query,
        show_username: bool = False
) -> str:
    """
    Форматирует список запросов в текстовое сообщение.

    Args:
        queries: Список объектов QueryModel
        username: Имя пользователя (если есть)
        user_id: ID пользователя (если username отсутствует)
        footnote_template: Шаблон заголовка с {username} placeholder
        line_template: Шаблон строки запроса с {time} и {query} placeholders
        show_username: Показывать ли имя пользователя в каждой строке

    Returns:
        Отформатированная строка с историей запросов
    """
    username_display = f'@{username}' if username else (str(user_id) if user_id else PHRASES_RU.error.unknown)
    txt = [PHRASES_RU.title.query,
           footnote_template.format(username=username_display)]

    for query in queries:
        line_data = {
            'time': query.query_date.strftime("%d.%m.%Y %H:%M:%S") if query.query_date else PHRASES_RU.error.unknown,
            'query': clear_string(query.query_text),
            'username': f"@{query.user.username}" if show_username and query.user and query.user.username else ""
        }
        txt.append(line_template.format(**line_data))

    return ''.join(txt)
