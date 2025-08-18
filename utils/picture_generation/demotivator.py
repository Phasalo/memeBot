from typing import Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
from config.const import TEMP_DIR
from utils.picture_generation.generation_utils.calculations import unique_name, fit_font_width, text_height, \
    textbbox_points, size_minside
from utils.picture_generation.generation_utils.models import Text, DemotivatorStyle, Point, Size
from assets.fonts import FONT_TIMES
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip

FOOTNOTE_TEXT = 'phasalopedia.ru'
FOOTNOTE_FONT = ImageFont.truetype(FONT_TIMES, 25)

WIDTH_MEM_SIDE: int = 700
MARGIN: int = 50
IMAGE_INDENT: int = 50
TEXT_MARGIN: int = 150
INTERLIGNAGE: int = 25


def create_demotivator_image(image_path: str,
                             mem_style: DemotivatorStyle,
                             top_text: Optional[Text] = None,
                             bottom_text: Optional[Text] = None) -> str:
    frame_image = Image.open(image_path).convert('RGB')
    width_img_container = WIDTH_MEM_SIDE - (2 * MARGIN)
    ratio = frame_image.height / frame_image.width
    size = (width_img_container, round(width_img_container * ratio))
    frame_image = frame_image.resize(size, Image.LANCZOS)

    image_path = _create_demotivator(Size(*size), mem_style, top_text, bottom_text)
    image = Image.open(image_path).convert('RGBA')

    image.paste(frame_image, (MARGIN, MARGIN))

    save_path = TEMP_DIR / unique_name(prefix='image_demotivator', extension='.png')
    image.save(save_path, format='PNG')
    return save_path


def create_demotivator_video(video_path: str,
                             mem_style: DemotivatorStyle,
                             top_text: Optional[Text] = None,
                             bottom_text: Optional[Text] = None) -> str:
    video = VideoFileClip(video_path)
    width_img_container = WIDTH_MEM_SIDE - (2 * MARGIN)
    video_width, video_height = video.size
    ratio = video_height / video_width
    size = (width_img_container, round(width_img_container * ratio))
    video = video.resized(size)

    frame_image_path = _create_demotivator(Size(*size), mem_style, top_text, bottom_text)
    frame_image = ImageClip(frame_image_path).with_duration(video.duration)

    video = video.with_position((MARGIN, MARGIN))
    video = CompositeVideoClip([frame_image, video])

    save_path = TEMP_DIR / unique_name(prefix='video_demotivator', extension='.mp4')
    video.write_videofile(save_path)
    return save_path


def _create_demotivator(image_size: Size,
                        mem_style: DemotivatorStyle,
                        top_text: Optional[Text] = None,
                        bottom_text: Optional[Text] = None) -> str:
    width_text_container = WIDTH_MEM_SIDE - (2 * TEXT_MARGIN)

    top_font = None
    bottom_font = None
    top_height = None
    bottom_height = None
    top_font_size = None
    bottom_font_size = None

    if top_text:
        top_font_size = fit_font_width(top_text.text, width_text_container, top_text.font)
    if bottom_text:
        bottom_font_size = fit_font_width(bottom_text.text, width_text_container, bottom_text.font)

    if top_text and bottom_text:
        top_font_size = min(top_font_size, bottom_font_size * 2)
        bottom_font_size = top_font_size // 2

    if top_text:
        top_font = ImageFont.truetype(top_text.font, top_font_size)
        top_height = text_height(top_text.text, top_font)

    if bottom_text:
        bottom_font = ImageFont.truetype(bottom_text.font, bottom_font_size)
        bottom_height = text_height(bottom_text.text, bottom_font)

    image_height = MARGIN + image_size.height
    if top_text:
        image_height += top_height
    if bottom_text:
        image_height += bottom_height
    if top_text and bottom_text:
        image_height += INTERLIGNAGE
    if top_text or bottom_text:
        image_height += IMAGE_INDENT
    image_height += MARGIN

    image = Image.new('RGB', (WIDTH_MEM_SIDE, image_height), mem_style.background_color)
    canvas = ImageDraw.Draw(image)

    canvas.rectangle(
        (MARGIN - mem_style.stroke_indent,
         MARGIN - mem_style.stroke_indent,
         MARGIN + image_size.width + mem_style.stroke_indent,
         MARGIN + image_size.height + mem_style.stroke_indent),
        fill=mem_style.background_color,
        outline=mem_style.stroke.color,
        width=mem_style.stroke.width,
    )

    footnote_top_left, footnote_bottom_right = textbbox_points(
        canvas,
        (image_size.width + MARGIN, image_size.height + MARGIN),
        FOOTNOTE_TEXT,
        FOOTNOTE_FONT,
        anchor='rt'
    )

    canvas.rectangle(
        (footnote_top_left.x - mem_style.stroke_indent // 2,
         footnote_top_left.y,
         footnote_bottom_right.x + mem_style.stroke_indent // 2,
         footnote_bottom_right.y),
        fill=mem_style.background_color
    )

    canvas.text(
        (image_size.width + MARGIN,
         image_size.height + MARGIN),
        FOOTNOTE_TEXT,
        font=FOOTNOTE_FONT,
        fill=mem_style.stroke.color,
        anchor='rt'
    )

    center_x = image.width // 2
    top_point = Point(center_x, MARGIN + image_size.height + IMAGE_INDENT)
    if top_text and bottom_text:
        bottom_point = Point(center_x, top_point.y + top_height + INTERLIGNAGE)
    else:
        bottom_point = top_point

    if top_text:
        canvas.text(
            top_point.tuple,
            top_text.text,
            font=top_font,
            fill=top_text.color,
            anchor='mt'
        )

    if bottom_text:
        canvas.text(
            bottom_point.tuple,
            bottom_text.text,
            font=bottom_font,
            fill=bottom_text.color,
            anchor='mt'
        )

    save_path = TEMP_DIR / unique_name(prefix='raw_demotivator', extension='.png')
    image.save(save_path, format='PNG')
    return save_path


if __name__ == '__main__':
    from assets.fonts import FONT_TIMES, FONT_ARIAL

    create_demotivator_video(video_path=r'L:\maxim\PythonProjects\memeBot\temp\ast\fam.mp4',
                             mem_style=DemotivatorStyle(),
                             top_text=Text(text='Опа, а это видео', font=FONT_TIMES),
                             bottom_text=Text(text='Опа, а это видео', font=FONT_ARIAL))

    create_demotivator_image(image_path=r'L:\maxim\PythonProjects\memeBot\temp\ast\dog2.jpg',
                             mem_style=DemotivatorStyle(),
                             top_text=Text(text='Опа, а это видео', font=FONT_TIMES),
                             bottom_text=Text(text='Опа, а это видео', font=FONT_ARIAL))
