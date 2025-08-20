import os
from random import choice, shuffle
from typing import Optional
from PIL import Image, ImageDraw
from utils.picture_generation.generation_utils.calculations import (font_to_width,
                                                                    scale_to_min_side)
from utils.picture_generation.generation_utils.fit_text import wrap_text
from utils.picture_generation.generation_utils.models import (Point,
                                                              Size,
                                                              TextStyle,
                                                              InsultStyle,
                                                              DefaultTextStyle)
from utils.picture_generation.generation_utils.processing import draw_multiline_text
from utils.picture_generation.generation_utils.save import save_media
from utils.string_formatter.word_declension import decline_word
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip


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
    town_name = take_from_db()  # TODO ПОДВИЗАТЬ ЗАБОР ГОРОДА ИЗ БД
    return f"Жители {decline_word(town_name, 'Р')}"


MIN_SIDE: int = 700
MARGIN: int = 35
MAX_FONT_SIZE: int = MIN_SIDE // 10
MIN_FONT_SIZE: int = 40


def create_insult_image(image_path: str,
                        top_text: Optional[str] = None,
                        top_style: Optional[TextStyle] = None,
                        bottom_text: Optional[str] = None,
                        bottom_style: Optional[TextStyle] = None,
                        image_style: InsultStyle = InsultStyle()) -> str:
    image = Image.open(image_path).convert('RGBA')
    size = Size(MIN_SIDE, MIN_SIDE) if image_style.is_square else scale_to_min_side(image.size, MIN_SIDE)
    image = image.resize(size.as_tuple, Image.LANCZOS)

    frame_image_path = _create_insult(size, top_text, top_style, bottom_text, bottom_style, image_style)
    frame_image = Image.open(frame_image_path).convert('RGBA')

    image = Image.alpha_composite(image, frame_image)
    os.remove(frame_image_path)

    return save_media(image, prefix='insult')


def create_insult_video(video_path: str,
                        top_text: Optional[str] = None,
                        top_style: Optional[TextStyle] = None,
                        bottom_text: Optional[str] = None,
                        bottom_style: Optional[TextStyle] = None,
                        image_style: InsultStyle = InsultStyle()) -> str:
    video = VideoFileClip(video_path)
    size = Size(MIN_SIDE, MIN_SIDE) if image_style.is_square else scale_to_min_side(video.size, MIN_SIDE)
    video = video.resized(size.as_tuple)

    frame_image_path = _create_insult(size, top_text, top_style, bottom_text, bottom_style, image_style)
    frame_image = ImageClip(frame_image_path).with_duration(video.duration)

    video = CompositeVideoClip([video, frame_image])
    os.remove(frame_image_path)

    return save_media(video, prefix='insult')


def _create_insult(image_size: Size,
                   top_text: Optional[str] = None,
                   top_style: Optional[TextStyle] = None,
                   bottom_text: Optional[str] = None,
                   bottom_style: Optional[TextStyle] = None,
                   image_style: InsultStyle = InsultStyle()) -> str:
    # Дефолтными значениями (Оскорбление города)
    top_text = random_insult() if top_text is None else top_text
    top_style = DefaultTextStyle() if top_style is None else top_style
    bottom_text = random_town_resident() if bottom_text is None else bottom_text
    bottom_style = DefaultTextStyle() if bottom_style is None else bottom_style

    image = Image.new("RGBA", image_size, (0, 0, 0, 0))
    canvas = ImageDraw.Draw(image, 'RGBA')

    # Размера шрифта style.font.point_size
    width_text_block = image_size.width - (2 * MARGIN)

    top_style.font.point_size = MAX_FONT_SIZE
    bottom_style.font.point_size = MAX_FONT_SIZE

    if top_text is not None:
        top_style.font.point_size = font_to_width(top_text, width_text_block, top_style.font.path)
    if bottom_text is not None:
        bottom_style.font.point_size = font_to_width(bottom_text, width_text_block, bottom_style.font.path)

    font_size = min(top_style.font.point_size, bottom_style.font.point_size)
    font_size = max(MIN_FONT_SIZE, min(MAX_FONT_SIZE, font_size))

    top_style.font.point_size = bottom_style.font.point_size = font_size

    # Стартовые точки для текста
    if image_style.crop_top_text:
        top_point = Point(image_size.center_point.x, top_style.ascent // 2)
    else:
        top_point = Point(image_size.center_point.x, MARGIN + top_style.ascent)
    if image_style.crop_bottom_text:
        bottom_point = Point(image_size.center_point.x,
                             image_size.height + bottom_style.line_height)
    else:
        bottom_point = Point(image_size.center_point.x,
                             image_size.height - MARGIN - bottom_style.descent)

    height_text_block = image_size.height - (2 * MARGIN)
    if top_text and bottom_text:
        height_text_block //= 2

    if top_text:
        top_text_list = wrap_text(top_text, top_style.font, Size(width_text_block, height_text_block))
        draw_multiline_text(canvas, top_text_list, top_style, top_point)

    if bottom_text:
        bottom_text_list = wrap_text(bottom_text, bottom_style.font, Size(width_text_block, height_text_block))
        bottom_text_list.reverse()
        draw_multiline_text(canvas, bottom_text_list, bottom_style, bottom_point,
                            multiplier_shift=-1)

    return save_media(image, prefix='raw_insult')


if __name__ == '__main__':
    from assets.fonts import FONT_IMPACT, LOREM_IPSUM, FONT_TIMES

    # create_insult_video(video_path=r'L:\maxim\PythonProjects\memeBot\temp\ast\fam.mp4',
    #                     top_text=Text(text='Опа, а это видео', font=FONT_IMPACT),
    #                     bottom_text=Text(text='Опа, а это видео', font=FONT_IMPACT),
    #                     is_square=True,
    #                     with_cropped_top_text=False,
    #                     with_cropped_bottom_text=True
    #                     )

    create_insult_image(image_path=r'L:\maxim\PythonProjects\memeBot\temp\ast\dog2.jpg',
                        top_text=Text(
                            text='Я люблю собак, они дарят мне счастье, любовь и приятно',
                            font=FONT_TIMES),
                        bottom_text=Text(text='слизывают сперму',
                                         font=FONT_TIMES),
                        is_square=False,
                        with_cropped_top_text=False,
                        with_cropped_bottom_text=False
                        )
