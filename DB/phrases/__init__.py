from json import load as json_load
from os.path import dirname
from typing import Any, Dict
from random import choice
import re


class Phrases:
    """Класс для представления"""
    def __init__(self, dictionary: Dict[str, Any]):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                setattr(self, key, Phrases(value))
            else:
                setattr(self, key, value)

    def __getattribute__(self, name: str):
        value = object.__getattribute__(self, name)

        if isinstance(value, list):
            return choice(value)
        return value

    def __getattr__(self, name: str):
        raise AttributeError(f'<b>Фраза «{name}» не найдена</b>')

    def __repr__(self):
        return str(self.__dict__)

    def replace(self, phrase_name: str, **replacements: Any) -> str:
        """
        Получает фразу с заменой плейсхолдеров

        :param phrase_name: Название фразы (например 'success.user_banned')
        :param replacements: Параметры для замены (например user_id=123)
        :return: Готовая фраза с подставленными значениями
        """
        parts = phrase_name.split('.')
        current = self

        try:
            for part in parts:
                current = getattr(current, part)
        except AttributeError:
            raise AttributeError(f'Фраза "{phrase_name}" не найдена')

        if isinstance(current, list):
            phrase = choice(current)
        else:
            phrase = current

        # Заменяем все плейсхолдеры вида {key}
        for key, value in replacements.items():
            pattern = re.compile(r'\{\s*' + re.escape(key) + r'\s*\}')
            phrase = pattern.sub(str(value), phrase)

        return phrase


def __load_phrases(phrases_path: str) -> Phrases:
    with open(phrases_path, 'r', encoding='utf-8') as file:
        phrases_dict = json_load(file)
    return Phrases(phrases_dict)


PHRASES_RU = __load_phrases(f'{dirname(__file__)}/phrases_ru.json')
