from typing import Tuple, List, Optional
import numpy as np
from PIL import Image, ImageDraw
from utils.picture_generation.generation_utils.calculations import decoding_color
from utils.picture_generation.generation_utils.models import Point, TextStyle


def fit_crop(image: Image.Image, width: int = 1000, height: int = 1000) -> Image.Image:
    w, h = image.size
    scale = max(width / w, height / h)
    new_w, new_h = int(w * scale), int(h * scale)
    image = image.resize((new_w, new_h), Image.LANCZOS)

    left = (new_w - width) // 2
    top = (new_h - height) // 2
    right = left + width
    bottom = top + height

    return image.crop((left, top, right, bottom))


def draw_multiline_text(canvas: ImageDraw.Draw,
                        text_list: List[str],
                        text_style: TextStyle,
                        start_point: Point,
                        shift_y: Optional[int] = None,
                        multiplier_shift: Optional[float] = None,
                        anchor: str = 'ms') -> None:
    if shift_y is None:
        shift_y = text_style.line_height

    if multiplier_shift is None:
        multiplier_shift = 1

    string_y = start_point.y
    for string in text_list:
        canvas.text(
            (start_point.x, string_y),
            string,
            font=text_style.font.true_type,
            fill=text_style.color,
            stroke_width=text_style.stroke.width,
            stroke_fill=text_style.stroke.color,
            anchor=anchor
        )
        string_y += int(shift_y * multiplier_shift)


def draw_round_gradient(width: int, height: int,
                        inner_color: str,
                        outer_color: str,
                        center: Tuple[int, int] = None) -> Image.Image:
    inner = np.array(decoding_color(inner_color), dtype=np.float32)
    outer = np.array(decoding_color(outer_color), dtype=np.float32)

    cx, cy = center or (width // 2, height // 2)

    y, x = np.ogrid[:height, :width]
    dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2)
    max_dist = np.sqrt(max(cx, width - cx) ** 2 + max(cy, height - cy) ** 2)
    t = np.clip(dist / max_dist, 0, 1)[..., None]
    img_array = (inner * (1 - t) + outer * t).astype(np.uint8)

    return Image.fromarray(img_array, mode="RGBA")


def draw_antialiased_polygon(polygon: List[Tuple[int, int]], fill: str,
                             scale: int = 4, padding: int = 10) -> Tuple[Image.Image, Point]:
    xs, ys = zip(*polygon)
    x0, y0, x1, y1 = min(xs), min(ys), max(xs), max(ys)
    width, height = x1 - x0, y1 - y0

    polygon_shifted = [(x - x0 + padding, y - y0 + padding) for x, y in polygon]

    image = Image.new('RGBA', ((width + 2 * padding) * scale, (height + 2 * padding) * scale), (0, 0, 0, 0))
    canvas = ImageDraw.Draw(image)

    polygon_scaled = [(x * scale, y * scale) for x, y in polygon_shifted]
    canvas.polygon(polygon_scaled, fill=fill)

    return image.resize((width + 2 * padding, height + 2 * padding), resample=Image.LANCZOS), Point(x0, y0)
