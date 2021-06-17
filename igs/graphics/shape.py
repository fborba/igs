from abc import ABC

from igs.graphics.traits import Clonable, Drawable


class Point(Clonable):
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def x(self):
        return self._x

    def y(self):
        return self._y


class Shape(ABC, Clonable, Drawable):
    def __init__(self):
        self._points = []

    def __str__(self):
        name = self.__class__.__name__
        hash_value = str(hex(hash(self)))

        return f"{name} ({hash_value[-6:]})"

    def apply(self, transform):
        self._points = [transform(p) for p in self._points]
        return self

    def add(self, point):
        self._points.append(point)

    def point_at(self, index):
        return self._points[index]


class Line(Shape):
    def __init__(self, p0, p1):
        super().__init__()
        self.add(p0)
        self.add(p1)

    def draw(self, painter):
        p0 = self.point_at(0)
        p1 = self.point_at(1)

        painter.drawLine(p0.x(), p0.y(), p1.x(), p1.y())


class Rectangle(Shape):
    def __init__(self, top_left, width, height):
        if width <= 0:
            raise ValueError("non-positive width")
        if height <= 0:
            raise ValueError("non-positive height")

        super().__init__()

        bottom_right = Point(top_left.x() + width, top_left.y() + height)

        self.add(top_left)
        self.add(bottom_right)

    def draw(self, painter):
        p0 = self.point_at(0)
        p1 = self.point_at(1)

        painter.drawLine(p0.x(), p0.y(), p1.x(), p0.y())
        painter.drawLine(p0.x(), p0.y(), p0.x(), p1.y())
        painter.drawLine(p1.x(), p1.y(), p0.x(), p1.y())
        painter.drawLine(p1.x(), p1.y(), p1.x(), p0.y())


class Square(Rectangle):
    def __init__(self, top_left, size):
        if size <= 0:
            raise ValueError("non-positive size")

        super().__init__(top_left, size, size)


class Mark(Shape):
    def __init__(self, center):
        super().__init__()
        self.add(center)

    def draw(self, painter):
        x = self.center().x()
        y = self.center().y()

        painter.drawLine(x - 1, y, x + 1, y)
        painter.drawLine(x, y - 1, x, y + 1)

    def center(self):
        return self.point_at(0)
