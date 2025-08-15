from pathlib import Path
from enum import Enum
from types import MappingProxyType
from typing import Dict, Set

BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / 'assets'
TEMP_DIR = BASE_DIR / 'temp'
IMAGE_DIR = ASSETS_DIR / 'images'
FONTS_DIR = ASSETS_DIR / 'fonts'

USERS_PER_PAGE = 15
QUERIES_PER_PAGE = 6


class MemeModes:
    """Класс для работы с режимами пользователя"""
    IN = 'in'  # Мемас
    DE = 'de'  # Демотиватор
    BO = 'bo'  # Чтиво
    FC = 'fc'  # Факты

    IN_NAME = 'Мемас'
    DE_NAME = 'Демотиватор'
    BO_NAME = 'Чтиво'
    FC_NAME = 'Факты'

    _MODES_NAMES: Dict[str, str] = {
        IN: IN_NAME,
        DE: DE_NAME,
        BO: BO_NAME,
        FC: FC_NAME
    }

    @classmethod
    def all_modes(cls) -> Dict[str, str]: return cls._MODES_NAMES.copy()

    @classmethod
    def get_name(cls, mode_code: str) -> str:
        """Получить название по коду режима"""
        return cls._MODES_NAMES.get(mode_code, 'Неизвестный режим')

    @classmethod
    def get_all_codes(cls) -> Set[str]:
        """Получить все коды режимов"""
        return set(cls._MODES_NAMES.keys())

    @classmethod
    def is_valid_mode(cls, mode_code: str) -> bool:
        """Проверить, что код режима допустим"""
        return mode_code in cls._MODES_NAMES


class ColorFields:
    UPPER = 'upper_color'
    BOTTOM = 'bottom_color'
    UPPER_STROKE = 'upper_stroke_color'
    BOTTOM_STROKE = 'bottom_stroke_color'

    @classmethod
    def all_fields(cls):
        return {cls.UPPER, cls.BOTTOM, cls.UPPER_STROKE, cls.BOTTOM_STROKE}


class SettingsAction(Enum):
    SETTINGS = 'settings'
    USER_MODE = 'user_mode'
    UPPER_TEXT = 'upper_text'
    BOTTOM_TEXT = 'bottom_text'
    UPPER_STROKE = 'upper_stroke'
    BOTTOM_STROKE = 'bottom_stroke'
    TEXTCASE = 'textcase'
    SET_SMALL_CASE = 'small_case'
    SET_GIANT_CASE = 'giant_case'


class UserColors:
    """Класс для работы с пользовательскими цветами"""
    NIGER = '#000000'
    PURPLE_PIZZA = '#FF00FF'
    EGGPLANT = '#800080'
    MENSTRUAL = '#FF0000'
    BABY_SURPRISE = '#800000'
    PEE_PEE = '#FFFF00'
    VOMIT = '#808000'
    VERDEPOM = '#00FF00'
    INDIAN = '#008000'
    THRUSH_EGGS = '#00FFFF'
    CHUROK_BIRD = '#008080'
    CONFIDENCE = '#0000FF'
    NAVY_UNIFORM = '#000080'
    SNOW_WHITE = '#FFFFFF'

    _COLORS_DATA: Dict[str, str] = {
        'Нигер': NIGER,
        'Пурпурная пицца': PURPLE_PIZZA,
        'Баклажанный': EGGPLANT,
        'Месячные': MENSTRUAL,
        'Детская неожиданность': BABY_SURPRISE,
        'Пись-пись': PEE_PEE,
        'Рвота': VOMIT,
        'Вердепомовый': VERDEPOM,
        'Индийский': INDIAN,
        'Яйца странствующего дрозда': THRUSH_EGGS,
        'Окраска птицы чюрок': CHUROK_BIRD,
        'Цвет уверенности': CONFIDENCE,
        'Форма морских офицеров': NAVY_UNIFORM,
        'Белоснежка': SNOW_WHITE,
    }

    @classmethod
    def get_color_name_by_hash(cls, color_hash: str) -> str:
        """Получить название цвета по hex-коду"""
        for name, color_data in cls._COLORS_DATA.items():
            if color_data.lower() == color_hash.lower():
                return name
        return color_hash

    @classmethod
    def get_all_color_codes(cls) -> Set[str]:
        """Получить все числовые коды цветов"""
        return set(cls._COLORS_DATA.values())

    @classmethod
    def get_all_colors(cls) -> MappingProxyType[str, str]:
        """Получить все цвета с их кодами"""
        return MappingProxyType(cls._COLORS_DATA)
