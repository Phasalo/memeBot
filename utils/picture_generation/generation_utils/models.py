from dataclasses import dataclass, field
from typing import NamedTuple, Optional, Tuple
from PIL import ImageFont
from assets.fonts import FONT_ARIAL


class Point(NamedTuple):
    x: int
    y: int


class Size(NamedTuple):
    width: int
    height: int

    @property
    def aspect_ratio(self) -> float:
        return self.width / self.height

    @property
    def center_point(self) -> Point:
        return Point(self.width // 2, self.height // 2)

    @property
    def as_tuple(self) -> Tuple[int, int]:
        return self.width, self.height


@dataclass
class MutablePoint:
    x: int
    y: int

    @property
    def point(self) -> Point:
        return Point(self.x, self.y)

    def __iter__(self):
        return iter((self.x, self.y))


class Area:
    def __init__(self, start_point: MutablePoint, end_point: MutablePoint):
        self._start = start_point
        self._end = end_point

    # --- Методы обновления ---
    def update_start(self, start_point: MutablePoint):
        self._start = start_point

    def update_end(self, end_point: MutablePoint):
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
    def start(self) -> MutablePoint:
        return self._start

    @property
    def end(self) -> MutablePoint:
        return self._end

    @property
    def start_point(self) -> Point:
        return Point(self._start.x, self._start.y)

    @property
    def end_point(self) -> Point:
        return Point(self._end.x, self._end.y)

    @property
    def aspect_ratio(self) -> float:
        return self.width / self.height

    @property
    def center_point(self) -> Point:
        return Point(self.width // 2, self.height // 2)

    @property
    def as_tuple(self) -> Tuple[int, int]:
        return self.width, self.height

    @property
    def rect(self) -> Tuple[int, int, int, int]:
        return (
            self._start.x,
            self._start.y,
            self._end.x,
            self._end.y
        )


class Stroke(NamedTuple):
    color: Optional[str] = None
    width: Optional[int] = None


class Line(NamedTuple):
    color: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None


@dataclass
class Font:
    path: str
    point_size: Optional[int] = None
    _true_type: Optional[ImageFont.FreeTypeFont] = field(default=None, init=False, repr=False)
    _ascent: Optional[int] = field(default=None, init=False, repr=False)
    _descent: Optional[int] = field(default=None, init=False, repr=False)
    _line_height: Optional[int] = field(default=None, init=False, repr=False)

    @property
    def true_type(self) -> ImageFont.FreeTypeFont:
        if self._true_type is None:
            if self.point_size is None:
                raise ValueError("point_size должен быть задан для загрузки шрифта")
            self._true_type = ImageFont.truetype(self.path, self.point_size)
        return self._true_type

    @property
    def ascent(self) -> int:
        if self._ascent is None:
            self._ascent, self._descent = (abs(x) for x in self.true_type.getmetrics())
        return self._ascent

    @property
    def descent(self) -> int:
        if self._descent is None:
            self._ascent, self._descent = (abs(x) for x in self.true_type.getmetrics())
        return self._descent

    @property
    def line_height(self) -> int:
        if self._line_height is None:
            self._line_height = self.ascent + self.descent
        return self._line_height


@dataclass
class TextStyle:
    font: Font
    color: str
    line_width: Optional[int] = None
    stroke: Optional[Stroke] = Stroke()

    @property
    def ascent(self) -> int:
        return self.font.ascent

    @property
    def descent(self) -> int:
        return self.font.descent

    @property
    def line_height(self) -> int:
        return self.font.line_height


@dataclass
class DefaultTextStyle(TextStyle):
    font: Font = Font(FONT_ARIAL)
    color: str = '#FFFFFF'
    stroke = Stroke(color='#000000', width=3)


class InsultStyle(NamedTuple):
    is_square: bool = True
    crop_top_text: bool = False
    crop_bottom_text: bool = False


class DemotivatorStyle(NamedTuple):
    background_color: str = '#000000'
    stroke: Stroke = Stroke(color='#FFFFFF', width=4)
    stroke_indent: int = 8


class FactStyle(NamedTuple):
    gradient_inner_color: str = "#000000AA"
    gradient_outer_color: str = "#00000000"
    line: Stroke = Stroke(color='#FFFFFFAA', width=4, length=200)
    shadow_color: str = "#000000"
