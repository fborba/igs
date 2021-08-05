import math

import numpy

from igs.graphics.shape import Position


class Transform:
    def __init__(self):
        self._matrix = numpy.array(
            [
                [1, 0, 0],
                [0, 1, 0],
                [0, 0, 1],
            ]
        )

    def __call__(self, point):
        vector = numpy.array([[point.x(), point.y(), 1]])
        result = numpy.matmul(vector, self._matrix)

        return Position(result[0, 0], result[0, 1])

    def combine(self, transform):
        self._matrix = numpy.matmul(self._matrix, transform._matrix)


class Translation(Transform):
    def __init__(self, dx, dy):
        self._matrix = numpy.array(
            [
                [1, 0, 0],
                [0, 1, 0],
                [dx, dy, 1],
            ]
        )


class Scaling(Transform):
    def __init__(self, sx, sy):
        self._matrix = numpy.array(
            [
                [sx, 0, 0],
                [0, sy, 0],
                [0, 0, 1],
            ]
        )


class Rotation(Transform):
    def __init__(self, angle):
        c = math.cos(angle)
        s = math.sin(angle)

        self._matrix = numpy.array(
            [
                [c, -s, 0],
                [s, c, 0],
                [0, 0, 1],
            ]
        )


def combine(*transforms):
    transform = Transform()

    for t in transforms:
        transform.combine(t)

    return transform
