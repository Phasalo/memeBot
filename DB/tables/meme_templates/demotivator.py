from collections.abc import Callable
from functools import wraps

from DB.tables.base import BaseTable
from utils.picture_generation.generation_utils.models import DemotivatorStyle, Stroke


def with_user_check(method: Callable):
    @wraps(method)
    def wrapper(self, user_id: int, *args, **kwargs):
        # Проверяем существование пользователя
        self.cursor.execute(f'SELECT 1 FROM {self.__tablename__} WHERE user_id = ?', (user_id,))
        user_exists = self.cursor.fetchone() is not None
        if not user_exists:
            self._create_user_style(user_id)

        return method(self, user_id, *args, **kwargs)

    return wrapper


class DemotivatorTable(BaseTable):
    __tablename__ = 'demotivator'

    def create_table(self):
        query = f'''
        CREATE TABLE IF NOT EXISTS {self.__tablename__} (
            user_id INTEGER NOT NULL,
            background_color TEXT DEFAULT '#000000',
            stroke_color TEXT DEFAULT '#FFFFFF',
            stroke_width INTEGER DEFAULT 4,
            stroke_indent INTEGER DEFAULT 8
        )'''

        self.cursor.execute(query)
        self.conn.commit()
        self._log('CREATE_TABLE')

    def _create_user_style(self, user_id: int):
        def_style = DemotivatorStyle()  # demotivator default style
        self.cursor.execute(f'INSERT INTO {self.__tablename__} (user_id, background_color, stroke_color, stroke_width, stroke_indent) '
                            'VALUES (?, ?, ?, ?, ?)',
                            (user_id, def_style.background_color, def_style.stroke.color, def_style.stroke.width, def_style.stroke_indent))
        self.conn.commit()
        self._log('CREATE_USER_DEMOTIVATOR_STYLE', user_id=user_id)

    @with_user_check
    def get_user_style(self, user_id: int) -> DemotivatorStyle:
        self.cursor.execute(f'SELECT background_color, stroke_color, stroke_width, stroke_indent '
                            f'FROM {self.__tablename__} WHERE user_id = ?', (user_id,))
        result = self.cursor.fetchone()

        return DemotivatorStyle(
            background_color=result['background_color'],
            stroke=Stroke(color=result['stroke_color'], width=result['stroke_width']),
            stroke_indent=result['stroke_indent']
        )

    @with_user_check
    def update_background_color(self, user_id: int, color: str):
        self.cursor.execute(f'UPDATE {self.__tablename__} '
                            'SET background_color = ? WHERE user_id = ?',
                            (color, user_id))
        self.conn.commit()
        self._log('UPDATE_BACKGROUND_COLOR', user_id=user_id, color=color)

    @with_user_check
    def update_stroke_color(self, user_id: int, color: str):
        self.cursor.execute(f'UPDATE {self.__tablename__} '
                            'SET stroke_color = ? WHERE user_id = ?',
                            (color, user_id))
        self.conn.commit()
        self._log('UPDATE_STROKE_COLOR', user_id=user_id, color=color)

    @with_user_check
    def update_stroke_width(self, user_id: int, width: int):
        self.cursor.execute(f'UPDATE {self.__tablename__} '
                            'SET stroke_width = ? WHERE user_id = ?',
                            (width, user_id))
        self.conn.commit()
        self._log('UPDATE_STROKE_WIDTH', user_id=user_id, width=width)

    @with_user_check
    def update_stroke_indent(self, user_id: int, indent: int):
        self.cursor.execute(f'UPDATE {self.__tablename__} '
                            'SET stroke_indent = ? WHERE user_id = ?',
                            (indent, user_id))
        self.conn.commit()
        self._log('UPDATE_STROKE_INDENT', user_id=user_id, indent=indent)
