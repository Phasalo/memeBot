from random import shuffle
from typing import Optional, cast, Callable
from PIL import ImageDraw, Image, ImageFont, ImageEnhance, ImageFilter
import numpy as np
from config.const import TEMP_DIR
from utils.picture.picture_utils.calculations import fit_font_width, unique_name
from utils.picture.picture_utils.models import Text


MAX_RANDOM_STEPS = 10


def random_steps():
    return np.random.randint(1, MAX_RANDOM_STEPS)


def perlin_noise(h, w, scale=20):
    y = np.linspace(0, np.pi * 4, h)
    x = np.linspace(0, np.pi * 4, w)
    yy, xx = np.meshgrid(y, x, indexing="ij")
    noise = (
        np.sin(xx / scale) +
        np.cos(yy / scale) +
        np.sin((xx + yy) / (scale * 0.5))
    )
    noise = (noise - noise.min()) / (noise.max() - noise.min())
    return noise.astype(np.uint8)


def psychedelic_distortion(image: Image.Image) -> Image.Image:
    arr = np.array(cast(np.ndarray, image)).astype(np.float32)
    h, w, _ = arr.shape

    y_indices, x_indices = np.meshgrid(np.arange(h), np.arange(w), indexing="ij")

    # --- RGB сдвиги ---
    for i in range(arr.shape[0]):
        arr[i, :, 0] = np.roll(arr[i, :, 0], int(random_steps() * np.sin(i / random_steps())))
        arr[i, :, 2] = np.roll(arr[i, :, 2],
                               int(random_steps() * np.cos(i / random_steps())))  # синий канал горизонтально

    for j in range(arr.shape[1]):
        arr[:, j, 1] = np.roll(arr[:, j, 1], int(random_steps() * np.sin(j / random_steps())))  # зелёный вертикально
        arr[:, j, 2] = np.roll(arr[:, j, 2], int(random_steps() * np.cos(j / random_steps())))  # синий вертикально

    # Цветовой глитч (перемешивание каналов) исправлено
    for i in range(h):
        shift = np.random.randint(-5, 5)
        arr[i, :, 0] = np.roll(arr[i, :, 0], shift)  # красный канал по строкам

    for j in range(w):
        shift = np.random.randint(-5, 5)
        arr[:, j, 1] = np.roll(arr[:, j, 1], shift)  # зелёный канал по столбцам

    for i in range(h):
        shift = np.random.randint(-5, 5)
        arr[i, :, 2] = np.roll(arr[i, :, 2], shift)  # синий канал по строкам

    # --- Цветовой шум ---
    color_noise = (np.random.rand(h, w, 3) - 0.5) * 50
    arr = np.clip(arr + color_noise, 0, 255)

    # --- Синусоидальные волны ---
    wave_y = random_steps() * np.sin(x_indices / random_steps())
    wave_x = random_steps() * np.sin(y_indices / random_steps())
    new_y = (y_indices + wave_y + wave_x).astype(int) % h
    new_x = (x_indices + wave_x + wave_y).astype(int) % w
    arr = arr[new_y, new_x]

    # --- Шумовая деформация ---
    noise = perlin_noise(h, w, scale=100)
    disp_y = (noise * 100).astype(int)
    disp_x = (noise * 100).astype(int)
    new_y = (y_indices + disp_y) % h
    new_x = (x_indices + disp_x) % w
    arr = arr[new_y, new_x]

    # --- Глитч-линии горизонтальные и вертикальные ---
    for _ in range(random_steps()):
        # горизонтальные
        y = np.random.randint(0, h)
        height = np.random.randint(1, 5)
        shift = np.random.randint(-50, 50)
        arr[y:y+height] = np.roll(arr[y:y+height], shift, axis=1)
        # вертикальные
        x = np.random.randint(0, w)
        width = np.random.randint(1, 5)
        shift = np.random.randint(-50, 50)
        arr[:, x:x+width] = np.roll(arr[:, x:x+width], shift, axis=0)

    # --- Глитч-линии горизонтальные и вертикальные (ИНВЕРТИРУЕМ) ---
    FADE_FACTOR = 0.6
    for _ in range(random_steps()):
        # горизонтальные линии
        y = np.random.randint(0, h)
        height = np.random.randint(1, 20)
        shift = np.random.randint(-50, 50)
        arr[y:y + height] = np.roll(arr[y:y + height], shift, axis=1)
        arr[y:y + height] = 255 - arr[y:y + height]  # инвертируем цвета
        arr[y:y + height] = (arr[y:y + height] * FADE_FACTOR).astype(np.uint8)  # приглушаем

        # вертикальные линии
        x = np.random.randint(0, w)
        width = np.random.randint(1, 5)
        shift = np.random.randint(-50, 50)
        arr[:, x:x + width] = np.roll(arr[:, x:x + width], shift, axis=0)
        arr[:, x:x + width] = 255 - arr[:, x:x + width]  # инвертируем цвета
        arr[:, x:x + width] = (arr[:, x:x + width] * FADE_FACTOR).astype(np.uint8)  # приглушаем

    # --- Мозаичные блоки ---
    for _ in range(random_steps()):
        block_size = min(h, w) // 2
        y = np.random.randint(0, h - block_size)
        x = np.random.randint(0, w - block_size)
        arr[y:y+block_size, x:x+block_size] = np.roll(
            arr[y:y+block_size, x:x+block_size],
            np.random.randint(-20, 20),
            axis=1
        )

    # --- Спиральные искажения ---
    cy, cx = h // 2, w // 2
    yy = y_indices - cy
    xx = x_indices - cx
    angle = np.arctan2(yy, xx) + 0.1 * np.sin(np.sqrt(xx**2 + yy**2) / 2)
    radius = np.sqrt(xx**2 + yy**2)
    new_x = (cx + radius * np.cos(angle)).astype(int) % w
    new_y = (cy + radius * np.sin(angle)).astype(int) % h
    arr = arr[new_y, new_x]

    # for _ in range(20):
    #     block_size = np.random.randint(100, 101)
    #     y = np.random.randint(0, h - block_size)
    #     x = np.random.randint(0, w - block_size)
    #
    #     block = arr[y:y + block_size, x:x + block_size]
    #
    #     # средний цвет блока
    #     avg_color = block.mean(axis=(0, 1), keepdims=True)
    #
    #     # заменяем все пиксели блока на средний цвет
    #     arr[y:y + block_size, x:x + block_size] = avg_color.astype(np.uint8)

    return Image.fromarray(arr.astype(np.uint8))


# ===== БАЗА =====

def apply_effect_with_mask(pixels: np.ndarray,
                           effect_fn: Callable[[np.ndarray], np.ndarray],
                           mask: np.ndarray,) -> np.ndarray:
    assert mask.shape == pixels.shape[:2], "Mask shape must match image (H, W)"

    modified = effect_fn(pixels.copy())
    out = pixels.copy()

    # там где mask==1 — берём из модифицированной версии
    out[mask == 1] = modified[mask == 1]
    return out


# ===== МАСКИ =====

def mask_rectangle(pixels: np.ndarray, x: int, y: int, w: int, h: int) -> np.ndarray:
    """Прямоугольная маска."""
    H, W = pixels.shape[:2]
    mask = np.zeros((H, W), dtype=np.uint8)
    mask[y:y + h, x:x + w] = 1
    return mask


def mask_stripe(pixels: np.ndarray, orientation: str = "horizontal", start: int = 0, thickness: int = 10) -> np.ndarray:
    """Полоска: горизонтальная или вертикальная."""
    H, W = pixels.shape[:2]
    mask = np.zeros((H, W), dtype=np.uint8)
    if orientation == "horizontal":
        mask[start:start + thickness, :] = 1
    else:
        mask[:, start:start + thickness] = 1
    return mask


def mask_function(pixels: np.ndarray, func: Callable[[np.ndarray], np.ndarray], axis: str = "x") -> np.ndarray:
    """
    Маска по математической функции.
    func принимает массив координат и возвращает булев массив.
    """
    H, W = pixels.shape[:2]
    mask = np.zeros((H, W), dtype=np.uint8)
    if axis == "x":
        x = np.arange(W)
        y_values = func(x) % H
        mask[y_values.astype(int), x] = 1
    else:
        y = np.arange(H)
        x_values = func(y) % W
        mask[y, x_values.astype(int)] = 1
    return mask


def mask_gradient(pixels: np.ndarray, direction: str = "horizontal") -> np.ndarray:
    """Градиентная маска от 0 до 1."""
    H, W = pixels.shape[:2]
    if direction == "horizontal":
        grad = np.tile(np.linspace(0, 1, W), (H, 1))
    else:
        grad = np.tile(np.linspace(0, 1, H), (W, 1)).T
    return grad  # тут возвращаем float-маску [0..1]


# ===== ПРОСТЫЕ ЭФФЕКТЫ ДЛЯ ТЕСТА =====

def shift_channel(pixels: np.ndarray, channel: int = 0, dx: int = 2, dy: int = 0):
    h, w, c = pixels.shape
    shifted = np.roll(pixels[:, :, channel], shift=dy, axis=0)
    shifted = np.roll(shifted, shift=dx, axis=1)
    pixels[:, :, channel] = shifted


def add_noise(pixels: np.ndarray, intensity: float = 0.05):
    """
    Добавляет случайный шум к каждому пикселю.
    intensity = стандартное отклонение шума (0.0–0.5 обычно).
    """
    noise = np.random.normal(0, intensity * 255, pixels.shape).astype(np.float32)
    pixels += noise
    np.clip(pixels, 0, 255, out=pixels)


def wave_distortion(pixels: np.ndarray, amplitude: float = 5.0, frequency: float = 20.0, direction: str = "horizontal"):
    """
    Волновое искажение.
    - amplitude: амплитуда волны (в пикселях)
    - frequency: частота волны
    - direction: "horizontal" или "vertical"
    """
    h, w, c = pixels.shape
    new_pixels = pixels.copy()

    if direction == "horizontal":
        for y in range(h):
            shift = int(amplitude * np.sin(2 * np.pi * y / frequency))
            new_pixels[y, :, :] = np.roll(pixels[y, :, :], shift, axis=0)
    else:
        for x in range(w):
            shift = int(amplitude * np.sin(2 * np.pi * x / frequency))
            new_pixels[:, x, :] = np.roll(pixels[:, x, :], shift, axis=0)

    pixels[:] = new_pixels


def create_what(image_path: str,
                text: Optional[Text] = None,
                with_distortions: bool = True,
                mem_min_side: int = 1000,
                margin: int = 300) -> str:
    image = Image.open(image_path).convert('RGB')
    ratio = image.height / image.width
    image = image.resize((mem_min_side, round(mem_min_side * ratio)), Image.LANCZOS)

    pixels = np.array(cast(np.ndarray, image)).astype(np.float32)

    invert_effect(pixels)

    mask = mask_function(dummy, func=lambda x: 50 + 20 * np.sin(x / 20), axis="x")
    out = apply_effect_with_mask(dummy, invert_effect, mask)
    print("pixels shape:", out.shape)

    image = Image.fromarray(pixels.astype(np.uint8))

    save_path = TEMP_DIR / unique_name(prefix='what', extension='.png')
    image.save(save_path, format='PNG')
    return save_path


if __name__ == '__main__':
    from utils.picture.picture_utils.models import Stroke
    from assets.fonts import FONT_IMPACT, FONT_LOBSTER

    test_text_block = Text(text='Что?', font=FONT_LOBSTER, color='#FFFFFF', stroke=Stroke(color='#000000', width=3))

    create_what(image_path=r'/temp/dog.jpg')
