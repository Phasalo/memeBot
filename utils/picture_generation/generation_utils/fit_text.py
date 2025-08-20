from typing import Tuple, Optional, List
from PIL import ImageFont
from utils.picture_generation.generation_utils.calculations import (font_to_width,
                                                                    font_width,
                                                                    SizeLike,
                                                                    size_like_to_tuple)
from utils.picture_generation.generation_utils.models import Font


def _crop_text(text: str, font: ImageFont.FreeTypeFont,
               max_width: int, suffix: str = '') -> str:
    low_width, high_width = 0, len(text)
    cropped_text = ''

    while low_width <= high_width:
        cursor = (low_width + high_width) // 2
        candidate = text[:cursor] + suffix
        if font_width(candidate, font) <= max_width:
            cropped_text = candidate
            low_width = cursor + 1
        else:
            high_width = cursor - 1

    return cropped_text


def crop_text(text: str, block_width: int,
              font_path: str, min_font_size: int,
              overflow_suffix: str = '...') -> Tuple[str, int]:
    font_size = font_to_width(text, block_width, font_path)
    if font_size >= min_font_size:
        return text, font_size

    font = ImageFont.truetype(font_path, min_font_size)
    cropped_text = _crop_text(text, font, block_width, overflow_suffix)

    return cropped_text, min_font_size


def wrap_word(word: str, font: ImageFont.FreeTypeFont,
              max_width: int, warp_suffix: str = '-') -> List[str]:
    parts = []
    cursor = 0

    while cursor < len(word):
        chunk = _crop_text(word[cursor:], font, max_width)

        if not chunk:
            return ['']

        if cursor + len(chunk) < len(word):
            chunk_suffix = chunk + warp_suffix
        else:
            chunk_suffix = chunk

        cursor += len(chunk)
        parts.append(chunk_suffix)

    return parts


def wrap_text(text: str, font: Font, block_size: SizeLike,
              max_strings: Optional[int] = None,
              overflow_suffix: str = '...',
              warp_suffix: str = '-') -> List[str]:
    if not text.strip():
        return ['']

    max_width, max_height = size_like_to_tuple(block_size)

    if max_strings is None:
        max_strings = int(max_height / font.line_height)

    strings: List[str] = []
    current_string: List[str] = []
    current_width: int = 0
    space_width = font_width(' ', font.true_type)

    def wrap():
        nonlocal current_string, current_width
        if current_string:
            strings.append(" ".join(current_string))
        current_string, current_width = [], 0

    for word in text.split():
        word_width = font_width(word, font.true_type)
        extra_space = space_width if current_string else 0

        if word_width > max_width:
            for part in wrap_word(word, font.true_type, max_width, warp_suffix):
                part_width = font_width(part, font.true_type)
                extra_space_part = space_width if current_string else 0
                if current_width + part_width + extra_space_part <= max_width:
                    current_string.append(part)
                    current_width += part_width + extra_space_part
                else:
                    wrap()
                    current_string.append(part)
                    current_width = part_width
        elif current_width + word_width + extra_space <= max_width:
            current_string.append(word)
            current_width += word_width + extra_space
        else:
            wrap()
            current_string.append(word)
            current_width = word_width

        if len(strings) >= max_strings:
            last_line = strings[-1].rstrip()
            if len(last_line) > len(overflow_suffix):
                strings[-1] = last_line[:-len(overflow_suffix)] + overflow_suffix
            else:
                strings[-1] = overflow_suffix
            return strings

    if current_string:
        strings.append(' '.join(current_string))

    return strings
