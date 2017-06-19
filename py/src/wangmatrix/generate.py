"""
Usage: python generate.py <width:int> <height:int> <shape_count:int>
"""
import sys
import random

from .drawing import Triangle, Square, Vector, Circle, Canvas, Pixel

CLOSED = "#"
OPEN = " "


def random_square(width, height):
    return Square(
        x=random.randint(0, width-1),
        y=random.randint(0, height-1),
        width=random.randint(0, width),
        height=random.randint(0, height),
    )


def random_triangle(width, height):
    return Triangle(
        x=random.randint(0, width-1),
        y=random.randint(0, height-1),
        length=random.randint(0, min(width, height)),
        angle=random.choice(list(a for a in range(0, 360, 45) if a % 90)),
    )


def random_vector(width, height):
    return Vector(
        x=random.randint(0, width-1),
        y=random.randint(0, height-1),
        length=random.randint(0, min(width, height)),
        angle=random.choice(range(0, 360, 10)),
    )


def random_circle(width, height):
    return Circle(
        x=random.randint(0, width-1),
        y=random.randint(0, height-1),
        radius=random.randint(0, min(width, height)),
    )


SHAPES = [
    random_square,
    random_triangle,
    random_vector,
    random_circle,
]


def random_maze(width, height, shape_count):
    canvas = Canvas(width, height, background="#")
    for i in range(shape_count):
        shape = random.choice(SHAPES)
        shape(width, height).render(canvas)

    edges = list(
        (x, y) for x, y in
        list((x, 0) for x in range(width)) +
        list((x, height-1) for x in range(width)) +
        list((0, y) for y in range(height)) +
        list((width-1, y) for y in range(height))
        if canvas.grid[y][x] == OPEN
    )
    sx, sy = random.choice(edges)
    ex, ey = random.choice(edges)
    canvas.grid[sy][sx] = "s"
    canvas.grid[ey][ex] = "e"
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
