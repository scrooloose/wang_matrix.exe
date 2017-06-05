from __future__ import print_function

import itertools
import random

from drawing import Canvas, Square, Pixel

OPEN = " "


def main():
    width = 80
    height = 40
    size = 5

    canvas = Canvas(width=width, height=height, background=OPEN)

    for y in range(0, height, size-1):
        for x in range(0, width, size-1):
            s = Square(x=x, y=y, width=size, height=size)
            side1 = random.choice([s.top, s.bottom, s.left, s.right])
            canvas.draw(Pixel(p, "#") for p in itertools.chain(side1()))

    edges = list(
        (x, y) for x, y in
        list((x, 0) for x in range(width)) +
        list((x, height-1) for x in range(width)) +
        list((0, y) for y in range(height)) +
        list((width-1, y) for y in range(height))
        if canvas.grid[y][x] == OPEN
    )

    canvas.draw(Pixel(p, "#") for p in Square(0, 0, width, height).outline())

    sx, sy = random.choice(edges)
    ex, ey = random.choice(edges)
    canvas.grid[sy][sx] = "s"
    canvas.grid[ey][ex] = "e"

    print(canvas)
