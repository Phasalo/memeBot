import uuid
from datetime import datetime
from typing import Tuple
from PIL import ImageFont, ImageDraw, Image
from utils.picture_generation.generation_utils.models import Point


def size_minside(size: Tuple[int, int], min_side: int) -> Tuple[int, int]:
    width, height = size
    scale = min_side / min(width, height)
    return int(width * scale), int(height * scale)


def fit_font_width(text: str, width: int, font_path: str) -> int:
    test_size = 100
    font = ImageFont.truetype(font_path, test_size, encoding='UTF-8')

    text_width = font.getbbox(text)[2]
    scale = width / text_width

    return int(test_size * scale)


def fit_font_height(text: str, height: int, font_path: str) -> int:
    test_size = 100
    font = ImageFont.truetype(font_path, test_size, encoding='UTF-8')

    text_height = font.getbbox(text)[3] - font.getbbox(text)[1]
    scale = height / text_height

    return int(test_size * scale)


def shortened_text_by_font(text: str, width: int,
                           font_path: str, min_font_size: int,
                           text_overflow: str = "...") -> Tuple[str, int]:
    font_size = fit_font_width(text, width, font_path)

    if font_size >= min_font_size:
        return text

    approx_len = max(0, int(len(text) * font_size / min_font_size))
    short_text = text[:approx_len]

    if len(short_text) < len(text):
        short_text = short_text.rstrip() + text_overflow

    return short_text, font_size


def wrap_text_to_fit_width(text: str, width: int, font_path: str, min_font_size: int):
    font_size = fit_font_width(text, width, font_path)

    # Если размер шрифта меньше минимального, переносим на новые строки
    if font_size < min_font_size:
        font_size = min_font_size
        words = text.split()
        lines = []
        current_line = ""
        font = ImageFont.truetype(font_path, font_size, encoding='UTF-8')

        for word in words:
            test_line = (current_line + " " + word).strip()
            line_width = font.getbbox(test_line)[2]
            if line_width <= width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return font_size, lines

    return font_size, [text]


def text_height(text: str, font: ImageFont.FreeTypeFont) -> int:
    bbox = ImageDraw.Draw(Image.new('RGB', (1, 1))).textbbox((0, 0), text, font=font)
    return bbox[3] - bbox[1]


def unique_name(prefix: str = 'photo', extension: str = '.png') -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:16]
    return f"{prefix}_{timestamp}_{unique_id}{extension}"


def decoding_color(color: str) -> Tuple[int, int, int, int]:
    color = color.lstrip('#')
    if len(color) == 6:
        r, g, b = int(color[:2], 16), int(color[2:4], 16), int(color[4:], 16)
        a = 255
    elif len(color) == 8:
        r, g, b, a = int(color[:2], 16), int(color[2:4], 16), int(color[4:6], 16), int(color[6:], 16)
    else:
        raise ValueError("Invalid color format")
    return r, g, b, a


def textbbox_points(canvas: ImageDraw.ImageDraw,
                    pos: Tuple[int, int],
                    text: str,
                    font: ImageFont.FreeTypeFont,
                    anchor: str = "lt") -> Tuple[Point, Point]:
    x1, y1, x2, y2 = canvas.textbbox(pos, text, font=font, anchor=anchor)
    return Point(x1, y1), Point(x2, y2)
