"""
Usage: python generate.py <width:int> <height:int> <shape_count:int>
"""
import itertools
import math
import sys
import random


GAP = "-"
WALL = "+"


def oa(h, r):
    return int(math.sin(r) * h), int(math.cos(r) * h)


class Triangle(object):
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
    def __init__(self, x, y, length, angle, rotation=0):
        self.x = x
        self.y = y
        self.length = length
        self.radians = math.radians(angle)
        self.rotation = rotation

    def hypotenuse(self):
        for h in range(self.length):
            o, a = oa(h, self.radians)
            yield self.x + o, self.y + a

    def opposite(self):
        o, a = oa(self.length, self.radians)
        for x in range(min(self.x, self.x + o), max(self.x, self.x + o)):
            yield x, self.y + a

    def adjacent(self):
        o, a = oa(self.length, self.radians)
        for y in range(min(self.y, self.y + a), max(self.y, self.y + a)):
            yield self.x, y

    def outline(self):
        return itertools.chain(
            self.hypotenuse(),
            self.opposite(),
            self.adjacent(),
        )


class Vector(object):
    def __init__(self, x, y, length, angle):
        self.x = x
        self.y = y
        self.length = length
        self.angle = angle

    def outline(self):
        v = Triangle(self.x, self.y, self.length, self.angle)
        return v.hypotenuse()


class Square(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def outline(self):
        return itertools.chain(
            # Top
            Vector(
                x=self.x,
                y=self.y,
                length=self.width,
                angle=90
            ).outline(),
            # Right
            Vector(
                x=self.x + self.width,
                y=self.y,
                length=self.height,
                angle=0
            ).outline(),
            # Bottom
            Vector(
                x=self.x,
                y=self.y + self.height - 1,
                length=self.width,
                angle=90
            ).outline(),
            # Left
            Vector(
                x=self.x,
                y=self.y,
                length=self.height,
                angle=0
            ).outline(),
        )


def last(iterable):
    _sentinel = object()
    _last = _sentinel
    for i in iterable:
        _last = i

    if _last is not _sentinel:
        yield _last


class Circle(object):
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def outline(self):
        return itertools.chain(*[
            last(
                Vector(
                    x=self.x,
                    y=self.y,
                    length=self.radius,
                    angle=i,
                ).outline(),
            )
            for i in range(1, 360, 2)
        ])


class Canvas(object):
    def __init__(self, width, height, character=GAP):
        self.width = width
        self.height = height
        row = [character] * width
        self.grid = [row[:] for _ in range(height)]

    def draw(self, obj, character=WALL):
        for x, y in obj.outline():
            try:
                self.grid[y][x] = character
            except IndexError:
                pass

    def __str__(self):
        return "\n".join("".join(row) for row in self.grid)


def random_square(width, height):
    return Square(
        x=random.randint(0, width),
        y=random.randint(0, height),
        width=random.randint(10, width/2),
        height=random.randint(10, height/2),
    )


def random_triangle(width, height):
    return Triangle(
        x=random.randint(0, width),
        y=random.randint(0, height),
        length=random.randint(10, min(width, height)/2),
        angle=random.choice(list(a for a in range(0, 360, 45) if a % 90)),
    )


def random_vector(width, height):
    return Vector(
        x=random.randint(0, width),
        y=random.randint(0, height),
        length=random.randint(10, min(width, height)/2),
        angle=random.choice(range(0, 360, 10)),
    )


def random_circle(width, height):
    return Circle(
        x=random.randint(0, width),
        y=random.randint(0, height),
        radius=random.randint(10, min(width, height)/2),
    )


SHAPES = [
    random_square,
    random_triangle,
    random_vector,
    random_circle,
]


def random_maze(width, height, shape_count):
    canvas = Canvas(width, height)
    for i in range(shape_count):
        shape = random.choice(SHAPES)
        o = shape(width, height)
        canvas.draw(o)
    print(str(canvas))


def help():
    sys.stderr.write(__doc__ + "\n")


def main():
    if "-h"in sys.argv[1:]:
        help()
        return 0

    try:
        width, height, shape_count = map(int, sys.argv[1:])
    except (IndexError, ValueError):
        help()
        return 1

    random_maze(width, height, shape_count)


if __name__ == "__main__":
    raise SystemExit(main())
