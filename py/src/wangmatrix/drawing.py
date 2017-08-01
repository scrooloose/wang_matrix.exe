import itertools
import math
from collections import namedtuple

import attr
from zope.interface import Interface, implementer

Point = namedtuple("Point", "x y")


class Pixel(object):
    def __init__(self, point, value):
        self.point = point
        self.value = value

    @property
    def x(self):
        return self.point.x

    @property
    def y(self):
        return self.point.y


def oa(h, r):
    return int(math.sin(r) * h), int(math.cos(r) * h)


class IShape(Interface):
    def outline():
        """
        The `Point`s for the shape outline.
        """


class Drawable(object):
    def pixels(self, char):
        return [Pixel(p, char) for p in self.points()]

    def render(self, canvas, char="."):
        canvas.draw(self.pixels(char=char))

    #template method
    def points(self):
        pass


@implementer(IShape)
@attr.s
class Triangle(Drawable):
    """
    SohCahToa

      #r
      #  #
    a #     #
      #        #
      #           #
      ###############
             o

    sin(r) = o / h
    o = sin(r) * h
    cos(r) = a / h
    a = cos(r) * h
    """
    x = attr.ib()
    y = attr.ib()
    length = attr.ib()
    angle = attr.ib()
    rotation = attr.ib(default=0)

    @property
    def radians(self):
        return math.radians(self.angle)

    def hypotenuse(self):
        for h in range(self.length):
            o, a = oa(h, self.radians)
            yield Point(self.x + o, self.y + a)

    def opposite(self):
        o, a = oa(self.length, self.radians)
        for x in range(min(self.x, self.x + o), max(self.x, self.x + o)):
            yield Point(x, self.y + a)

    def adjacent(self):
        o, a = oa(self.length, self.radians)
        for y in range(min(self.y, self.y + a), max(self.y, self.y + a)):
            yield Point(self.x, y)

    def outline(self):
        return itertools.chain(
            self.hypotenuse(),
            self.opposite(),
            self.adjacent(),
        )


@implementer(IShape)
@attr.s
class Vector(Drawable):
    x = attr.ib()
    y = attr.ib()
    length = attr.ib()
    angle = attr.ib()

    def outline(self):
        v = Triangle(self.x, self.y, self.length, self.angle)
        return v.hypotenuse()


@implementer(IShape)
@attr.s
class Square(Drawable):
    x = attr.ib()
    y = attr.ib()
    width = attr.ib()
    height = attr.ib()

    def top(self):
        return Vector(
            x=self.x, y=self.y, length=self.width, angle=90
        ).outline()

    def right(self):
        return Vector(
            x=self.x + self.width - 1, y=self.y, length=self.height, angle=0
        ).outline()

    def bottom(self):
        return Vector(
            x=self.x, y=self.y + self.height - 1, length=self.width, angle=90
        ).outline()

    def left(self):
        return Vector(
            x=self.x, y=self.y, length=self.height, angle=0
        ).outline()

    def outline(self):
        return itertools.chain(
            self.top(),
            self.right(),
            self.bottom(),
            self.left(),
        )


def last(iterable):
    _sentinel = object()
    _last = _sentinel
    for i in iterable:
        _last = i

    if _last is not _sentinel:
        yield _last


@implementer(IShape)
@attr.s
class Circle(Drawable):
    x = attr.ib()
    y = attr.ib()
    radius = attr.ib()

    def outline(self):
        return itertools.chain(
            * [
                last(
                    Vector(
                        x=self.x + self.radius,
                        y=self.y + self.radius,
                        length=self.radius,
                        angle=i,
                    ).outline(),
                ) for i in range(1, 360, 2)
            ]
        )


class Canvas(object):
    def __init__(self, width, height, background=" "):
        self.width = width
        self.height = height
        row = [background] * width
        self.grid = [row[:] for _ in range(height)]

    def draw(self, pixels):
        for p in pixels:
            try:
                self.grid[p.y][p.x] = p.value
            except IndexError:
                pass

    def __str__(self):
        return "\n".join("".join(row) for row in self.grid)


def ticks(width, every):
    for c in " " * (every - 1):
        yield c
    for i in (i for i in range(1, width) if (i % every) == 0):
        buffer = str(i).ljust(every)
        for c in buffer:
            yield c


def decorate(canvas):
    width = canvas.width
    gutter_width = len(str(canvas.height))
    horizontal_border = " " * gutter_width + " " +  "-"*width
    header = " " * gutter_width + " " + "".join(ticks(width, 5))
    return "\n".join(
        [header] +
        [horizontal_border] +
        list(
            str(row_number if row_number % 5 == 0 else "").rjust(gutter_width)
            + "|" + "".join(value for value in row) + "|" +
            str(row_number if row_number % 5 == 0 else "").rjust(gutter_width)
            for row_number, row in enumerate(canvas.grid, 1)
        ) +
        [horizontal_border] +
        [header]
    )
