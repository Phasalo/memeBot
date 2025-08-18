from dataclasses import dataclass
from typing import NamedTuple, Optional, Tuple
from assets.fonts import FONT_ARIAL


@dataclass
class Size:
    width: int
    height: int

    @property
    def tuple(self):
        return self.width, self.height


@dataclass
class Point:
    x: int
    y: int

    @property
    def tuple(self):
        return self.x, self.y


class AvailableArea:
    def __init__(self, start_point: Point, end_point: Point):
        self._start = start_point
        self._end = end_point

    # --- Методы обновления ---
    def update_start(self, start_point: Point):
        self._start = start_point

    def update_end(self, end_point: Point):
        self._end = end_point

    def update_start_x(self, x: int):
        self._start.x = x

    def update_start_y(self, y: int):
        self._start.y = y

    def update_end_x(self, x: int):
        self._end.x = x

    def update_end_y(self, y: int):
        self._end.y = y

    def shift_start_x(self, dx: int):
        self._start.x += dx

    def shift_start_y(self, dy: int):
        self._start.y += dy

    def shift_end_x(self, dx: int):
        self._end.x += dx

    def shift_end_y(self, dy: int):
        self._end.y += dy

    @property
    def width(self) -> int:
        return abs(self._end.x - self._start.x)

    @property
    def height(self) -> int:
        return abs(self._end.y - self._start.y)

    @property
    def start(self) -> Point:
        return self._start

    @property
    def end(self) -> Point:
        return self._end

    @property
    def rect(self) -> Tuple[int, int, int, int]:
        return (
            self._start.x,
            self._start.y,
            self._end.x,
            self._end.y
        )


class Stroke(NamedTuple):
    color: str
    width: int
    length: Optional[int] = None


@dataclass
class Text:
    text: str
    font: str = FONT_ARIAL
    color: str = '#FFFFFF'
    stroke: Stroke = Stroke(color='#000000', width=3)


class DemotivatorStyle(NamedTuple):
    background_color: str = '#000000'
    stroke: Stroke = Stroke(color='#FFFFFF', width=4)
    stroke_indent: int = 8


class FactStyle(NamedTuple):
    gradient_inner_color: str = "#000000AA"
    gradient_outer_color: str = "#00000000"
    line: Stroke = Stroke(color='#FFFFFFAA', width=4, length=200)
    shadow_color: str = "#000000"
