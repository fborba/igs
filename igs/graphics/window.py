from enum import Enum, auto

from igs.graphics.shape import Position, Rectangle
from igs.graphics.transform import Scaling, Translation


class Movement:
    class Direction(Enum):
        Left = auto()
        Right = auto()
        Up = auto()
        Down = auto()

        In = auto()
        Out = auto()

    def __init__(self, min_speed, max_speed):
        assert min_speed > 0
        assert max_speed > min_speed

        self._min_speed = min_speed
        self._max_speed = max_speed

        self._direction = None
        self._speed = min_speed

    def move(self, direction):
        if direction is self.direction():
            self.increase_speed()
        else:
            self.change_direction(direction)

    def change_direction(self, direction):
        self._direction = direction
        self._speed = self._min_speed

    def increase_speed(self):
        increase = self._min_speed if self._speed != self._max_speed else 0
        self._speed = min(self._speed + increase, self._max_speed)

    def direction(self):
        return self._direction

    def speed(self):
        return self._speed


class Window(Rectangle):
    def __init__(self, top_left, width, height):
        super().__init__(top_left, width, height)

        self._move = Movement(1, 10)
        self._zoom = Movement(0.01, 0.1)

    def zoom_in(self):
        new_window = self.try_zoom(1 - self._zoom.speed())

        if new_window.width() >= 1 or new_window.height() >= 1:
            self._points = new_window._points
            self._zoom.move(Movement.Direction.In)

    def zoom_out(self):
        new_window = self.try_zoom(1 + self._zoom.speed())

        self._points = new_window._points
        self._zoom.move(Movement.Direction.Out)

    def move_left(self):
        self.apply(Translation(-self._move.speed(), 0))
        self._move.move(Movement.Direction.Left)

    def move_right(self):
        self.apply(Translation(self._move.speed(), 0))
        self._move.move(Movement.Direction.Left)

    def move_up(self):
        self.apply(Translation(0, self._move.speed()))
        self._move.move(Movement.Direction.Up)

    def move_down(self):
        self.apply(Translation(0, -self._move.speed()))
        self._move.move(Movement.Direction.Down)

    def normalize(self, point):
        x = (point.x() - self.xmin()) / self.width()
        y = 1 - (point.y() - self.ymin()) / self.height()

        return Position(x, y)

    def center(self):
        x = self.xmin() + self.width() / 2
        y = self.ymin() + self.height() / 2

        return Position(x, y)

    def width(self):
        return self.xmax() - self.xmin()

    def height(self):
        return self.ymax() - self.ymin()

    def try_zoom(self, rate):
        dx = self.center().x()
        dy = self.center().y()

        return (
            self.clone()
            .apply(Translation(-dx, -dy))
            .apply(Scaling(rate, rate))
            .apply(Translation(dx, dy))
        )

    def xmin(self):
        return self._points[0].x()

    def xmax(self):
        return self._points[1].x()

    def ymin(self):
        return self._points[0].y()

    def ymax(self):
        return self._points[1].y()
