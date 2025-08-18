from random import choice, shuffle
from typing import Optional, Tuple

from PIL import Image, ImageDraw, ImageFont
from config.const import TEMP_DIR
from utils.picture.picture_utils.calculations import (unique_name,
                                                      fit_font_width,
                                                      text_height)
from utils.picture.picture_utils.models import Text, Point, Stroke
from utils.picture.picture_utils.processing import minside_resize
from assets.fonts import FONT_IMPACT
from utils.string_formatter.word_declension import decline_word

INSULTS = [
    [
        'там', ''
    ],
    [
        'нахуй',
        'чтоли', 'чтоль',
        'пиздец', 'ебать',
        'блять', ''
    ],
    [
        'совсем', 'абсолютно', 'совершенно', ''
    ],
    [
        'ёбнулись', 'ёбнутые',
        'охуели', 'охуевшие',
        'охренели', 'охреневшие',
        'ахуели', 'ахуевшие',
        'ахренели', 'ахреневшие',
        'офигели', 'офигевшие',
        'прихуели', 'прихуевшие',
        'прихренели', 'прихреневшие',
        'прифигели', 'прифигевшие',
        'очешуели', 'очешуевшие',
        'долбанулись', 'долбанутые',
        'конченые',
        'долбоёбы',
        'дауны',
    ]
]


def random_insult() -> str:
    insults = [choice(i) for i in INSULTS]
    insults = [i for i in insults if i.strip()]
    shuffle(insults)

    return f'Вы {" ".join(insults)}?'


def random_town_resident() -> str:
    town_name = await take_from_db()  # TODO ПОДВИЗАТЬ ЗАБОР ГОРОДА ИЗ БД
    return f"Жители {await decline_word(town_name, 'Р')}"


def create_insult(image_path: str,
                  top_text: Optional[Text] = None,
                  bottom_text: Optional[Text] = None,
                  with_cropped_texts: Tuple[int, int] = (False, False),
                  mem_min_side: int = 1000,
                  margin: int = 50,
                  default_font_size: int = 100) -> str:
    image = minside_resize(Image.open(image_path).convert('RGB'), mem_min_side)
    canvas = ImageDraw.Draw(image, 'RGBA')

    if not (top_text or bottom_text):
        top_text = Text(text=random_insult(),
                        font=FONT_IMPACT,
                        color='#FFFFFF',
                        stroke=Stroke(color='#000000', width=3))

        bottom_text = Text(text=random_town_resident(),
                           font=FONT_IMPACT,
                           color='#FFFFFF',
                           stroke=Stroke(color='#000000', width=3))

    width_text_container = image.width - (2 * margin)
    top_font_size = fit_font_width(top_text.text, width_text_container, top_text.font) \
        if top_text else default_font_size
    bottom_font_size = fit_font_width(bottom_text.text, width_text_container, bottom_text.font) \
        if bottom_text else default_font_size

    font_size = min(default_font_size, top_font_size, bottom_font_size)

    top_font = ImageFont.truetype(top_text.font, font_size) if top_text else None
    bottom_font = ImageFont.truetype(bottom_text.font, font_size) if bottom_text else None

    center_x = image.width // 2
    top_height = text_height(top_text.text, top_font) if top_text else 0
    bottom_height = text_height(bottom_text.text, bottom_font) if bottom_text else 0

    if with_cropped_texts[0]:
        top_point = Point(center_x, -top_height // 2)
    else:
        top_point = Point(center_x, margin)
    if with_cropped_texts[1]:
        bottom_point = Point(center_x, image.height - bottom_height // 2)
    else:
        bottom_point = Point(center_x, image.height - margin - bottom_height)

    if top_text:
        canvas.text(
            top_point.tuple,
            top_text.text,
            font=top_font,
            fill=top_text.color,
            stroke_width=top_text.stroke.width,
            stroke_fill=top_text.stroke.color,
            anchor="mt"
        )
    if bottom_text:
        canvas.text(
            bottom_point.tuple,
            bottom_text.text,
            font=bottom_font,
            fill=bottom_text.color,
            stroke_width=bottom_text.stroke.width,
            stroke_fill=bottom_text.stroke.color,
            anchor="mt"
        )

    save_path = TEMP_DIR / unique_name(prefix='insult', extension='.png')
    image.save(save_path, format='PNG')
    return save_path
