from abc import ABC

from igs.graphics.traits import Clonable, Drawable


class Position(Clonable):
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
        self._name = self.__class__.__name__

    def __str__(self):
        hash_value = str(hex(hash(self)))
        return f"{self._name} ({hash_value[-6:]})"

    def apply(self, transform):
        self._points = [transform(p) for p in self._points]
        return self

    def add(self, point):
        self._points.append(point)

    def set_name(self, name):
        self._name = name

    def point_at(self, index):
        return self._points[index]

    def num_of_points(self):
        return len(self._points)


class Line(Shape):
    def __init__(self, p0, p1):
        super().__init__()
        self.add(p0)
        self.add(p1)

    def draw(self, painter):
        p0 = self.point_at(0)
        p1 = self.point_at(1)

        painter.drawLine(p0.x(), p0.y(), p1.x(), p1.y())


class Polyline(Shape):
    def __init__(self, points):
        super().__init__()

        for p in points:
            self.add(p)

    def draw(self, painter):
        for i in range(1, self.num_of_points()):
            p0 = self.point_at(i - 1)
            p1 = self.point_at(i)

            painter.drawLine(p0.x(), p0.y(), p1.x(), p1.y())


class ClosedPolyline(Polyline):
    def __init__(self, points):
        super().__init__(points)

    def draw(self, painter):
        super().draw(painter)

        p0 = self.point_at(0)
        p1 = self.point_at(self.num_of_points() - 1)

        painter.drawLine(p0.x(), p0.y(), p1.x(), p1.y())


class Point(Shape):
    def __init__(self, p):
        super().__init__()

        self.add(p)

    def draw(self, painter):
        p = self.point_at(0)
        painter.drawLine(p.x(), p.y(), p.x(), p.y())


class Rectangle(Shape):
    def __init__(self, top_left, width, height):
        if width <= 0:
            raise ValueError("non-positive width")
        if height <= 0:
            raise ValueError("non-positive height")

        super().__init__()

        bottom_right = Position(top_left.x() + width, top_left.y() + height)

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
