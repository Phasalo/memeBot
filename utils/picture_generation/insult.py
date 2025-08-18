import os
from random import choice, shuffle
from typing import Optional, Tuple

from PIL import Image, ImageDraw, ImageFont
from config.const import TEMP_DIR
from utils.picture_generation.generation_utils.calculations import (unique_name,
                                                                    fit_font_width,
                                                                    text_height, size_minside)
from utils.picture_generation.generation_utils.models import Text, Point, Stroke
from assets.fonts import FONT_IMPACT
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
MARGIN: int = 50
DEFAULT_FONT_SIZE: int = 100


def create_insult_image(image_path: str,
                        top_text: Optional[Text] = None,
                        bottom_text: Optional[Text] = None,
                        is_square: bool = True,
                        with_cropped_top_text: bool = False,
                        with_cropped_bottom_text: bool = False) -> str:
    image = Image.open(image_path).convert('RGBA')
    size = (MIN_SIDE, MIN_SIDE) if is_square else size_minside(image.size, MIN_SIDE)
    image = image.resize(size, Image.LANCZOS)

    frame_image_path = _create_insult(size, top_text, bottom_text, with_cropped_top_text, with_cropped_bottom_text)
    frame_image = Image.open(frame_image_path).convert('RGBA')

    image = Image.alpha_composite(image, frame_image)

    save_path = TEMP_DIR / unique_name(prefix='image_insult', extension='.png')
    image.save(save_path, format='PNG')
    os.remove(frame_image_path)
    return save_path


def create_insult_video(video_path: str,
                        top_text: Optional[Text] = None,
                        bottom_text: Optional[Text] = None,
                        is_square: bool = True,
                        with_cropped_top_text: bool = False,
                        with_cropped_bottom_text: bool = False) -> str:
    video = VideoFileClip(video_path)
    size = (MIN_SIDE, MIN_SIDE) if is_square else size_minside(video.size, MIN_SIDE)
    video = video.resized(size)

    frame_image_path = _create_insult(size, top_text, bottom_text, with_cropped_top_text, with_cropped_bottom_text)
    frame_image = ImageClip(frame_image_path).with_duration(video.duration)

    video = CompositeVideoClip([video, frame_image])

    save_path = TEMP_DIR / unique_name(prefix='video_insult', extension='.mp4')
    video.write_videofile(save_path)
    os.remove(frame_image_path)
    return save_path


def _create_insult(image_size: Tuple[int, int],
                   top_text: Optional[Text] = None,
                   bottom_text: Optional[Text] = None,
                   with_cropped_top_text: bool = False,
                   with_cropped_bottom_text: bool = False) -> str:
    image = Image.new("RGBA", image_size, (0, 0, 0, 0))
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

    width_text_container = image.width - (2 * MARGIN)
    top_font_size = fit_font_width(top_text.text, width_text_container, top_text.font) \
        if top_text else DEFAULT_FONT_SIZE
    bottom_font_size = fit_font_width(bottom_text.text, width_text_container, bottom_text.font) \
        if bottom_text else DEFAULT_FONT_SIZE

    font_size = min(DEFAULT_FONT_SIZE, top_font_size, bottom_font_size)

    top_font = ImageFont.truetype(top_text.font, font_size) if top_text else None
    bottom_font = ImageFont.truetype(bottom_text.font, font_size) if bottom_text else None

    center_x = image.width // 2
    top_height = text_height(top_text.text, top_font) if top_text else 0
    bottom_height = text_height(bottom_text.text, bottom_font) if bottom_text else 0

    if with_cropped_top_text:
        top_point = Point(center_x, -top_height // 2)
    else:
        top_point = Point(center_x, MARGIN)
    if with_cropped_bottom_text:
        bottom_point = Point(center_x, image.height - bottom_height // 2)
    else:
        bottom_point = Point(center_x, image.height - MARGIN - bottom_height)

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

    save_path = TEMP_DIR / unique_name(prefix='raw_insult', extension='.png')
    image.save(save_path, format='PNG')
    return save_path


if __name__ == '__main__':
    from assets.fonts import FONT_IMPACT

    create_insult_video(video_path=r'L:\maxim\PythonProjects\memeBot\temp\ast\fam.mp4',
                        top_text=Text(text='Опа, а это видео', font=FONT_IMPACT),
                        bottom_text=Text(text='Опа, а это видео', font=FONT_IMPACT))

    create_insult_image(image_path=r'L:\maxim\PythonProjects\memeBot\temp\ast\dog2.jpg',
                        top_text=Text(text='Опа, а это видео', font=FONT_IMPACT),
                        bottom_text=Text(text='Опа, а это видео', font=FONT_IMPACT))
