import uuid
from datetime import datetime
from typing import Tuple, Union
from PIL import ImageFont
from utils.picture_generation.generation_utils.models import Size, Area, Font

TEST_TEXT_SIZE = 100
SizeLike = Union[Tuple[int, int], Size, Area]


def size_like_to_tuple(size_like: SizeLike) -> Tuple[int, int]:
    if isinstance(size_like, tuple):
        return size_like
    else:
        return size_like.width, size_like.height


def scale_to_width(size: SizeLike, new_width: int) -> Size:
    width, height = size_like_to_tuple(size)
    scale = new_width / width
    return Size(int(width * scale), int(height * scale))


def scale_to_height(size: SizeLike, new_height: int) -> Size:
    width, height = size_like_to_tuple(size)
    scale = new_height / height
    return Size(int(width * scale), int(height * scale))


def scale_to_min_side(size: SizeLike, min_side: int) -> Size:
    width, height = size_like_to_tuple(size)
    scale = min_side / min(width, height)
    return Size(int(width * scale), int(height * scale))


def font_width(text: str, font: ImageFont.FreeTypeFont,) -> int:
    return font.getlength(text)


def font_to_width(text: str, block_width: int, font_path: str) -> int:
    font = ImageFont.truetype(font_path, TEST_TEXT_SIZE, encoding='UTF-8')

    text_width = font_width(text, font)
    scale = block_width / text_width

    return int(TEST_TEXT_SIZE * scale)


def font_to_height(block_height: int, font_path: str) -> int:
    font = ImageFont.truetype(font_path, TEST_TEXT_SIZE, encoding='UTF-8')

    text_height = font_height(font)
    scale = block_height / text_height

    return int(TEST_TEXT_SIZE * scale)


def font_to_block(text: str, block: SizeLike, font_path: str) -> int:
    font = ImageFont.truetype(font_path, TEST_TEXT_SIZE, encoding='UTF-8')

    text_width, text_height = font_width(text, font), font_height(font)
    width, height = size_like_to_tuple(block)

    scale = max(width / text_width, height / text_height)

    return int(TEST_TEXT_SIZE * scale)


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
