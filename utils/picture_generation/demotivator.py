from typing import Optional
from PIL import Image, ImageDraw, ImageFont
from config.const import TEMP_DIR
from utils.picture_generation.generation_utils.calculations import unique_name, fit_font_width, text_height, textbbox_points
from utils.picture_generation.generation_utils.models import Text, DemotivatorStyle, Point
from assets.fonts import FONT_TIMES

FOOTNOTE_TEXT = 'phasalopedia.ru'
FOOTNOTE_FONT = ImageFont.truetype(FONT_TIMES, 25)


def create_demotivator(image_path: str,
                       mem_style: DemotivatorStyle,
                       top_text: Optional[Text] = None,
                       bottom_text: Optional[Text] = None,
                       width_mem_side: int = 1000,
                       margin: int = 50,
                       image_indent: int = 50,
                       text_margin: int = 150,
                       interlignage: int = 25) -> str:
    image_paste = Image.open(image_path).convert('RGB')

    width_img_container = width_mem_side - (2 * margin)
    ratio = image_paste.height / image_paste.width
    image_paste = image_paste.resize((width_img_container, round(width_img_container * ratio)), Image.LANCZOS)

    width_text_container = width_mem_side - (2 * text_margin)
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

    img_height = margin + image_paste.height
    if top_text:
        img_height += top_height
    if bottom_text:
        img_height += bottom_height
    if top_text and bottom_text:
        img_height += interlignage
    if top_text or bottom_text:
        img_height += image_indent
    img_height += margin

    image = Image.new('RGB', (width_mem_side, img_height), mem_style.background_color)
    canvas = ImageDraw.Draw(image)

    canvas.rectangle(
        (margin - mem_style.stroke_indent,
         margin - mem_style.stroke_indent,
         margin + image_paste.width + mem_style.stroke_indent,
         margin + image_paste.height + mem_style.stroke_indent),
        fill=mem_style.background_color,
        outline=mem_style.stroke.color,
        width=mem_style.stroke.width,
    )

    image.paste(image_paste, (margin, margin))

    footnote_top_left, footnote_bottom_right = textbbox_points(
        canvas,
        (image_paste.width + margin, image_paste.height + margin),
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
        (image_paste.width + margin,
         image_paste.height + margin),
        FOOTNOTE_TEXT,
        font=FOOTNOTE_FONT,
        fill=mem_style.stroke.color,
        anchor='rt'
    )

    center_x = image.width // 2
    top_point = Point(center_x, margin + image_paste.height + image_indent)
    if top_text and bottom_text:
        bottom_point = Point(center_x, top_point.y + top_height + interlignage)
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

    save_path = TEMP_DIR / unique_name(prefix='demotivator', extension='.png')
    image.save(save_path, format='PNG')
    return save_path
