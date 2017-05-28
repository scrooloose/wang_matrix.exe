import sys
import time
from collections import namedtuple

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


class Grid(object):
    def __init__(self, grid):
        self.grid = grid

    def get(self, x, y):
        width = self.width()
        height = self.height()
        if x < 0:
            x = x + width
        if x >= width:
            x = x - width
        if y < 0:
            y = y + height
        if y >= height:
            y = y - height

        try:
            return self.grid[y][x]
        except IndexError:
            return None

    def neighbouring_points(self, point):
        neighbours = list(p for p in [
            # N
            self.get(point.x, point.y - 1),
            # NE
            self.get(point.x + 1, point.y - 1),
            # E
            self.get(point.x + 1, point.y),
            # SE
            self.get(point.x + 1, point.y + 1),
            # S
            self.get(point.x, point.y + 1),
            # SW
            self.get(point.x - 1, point.y + 1),
            # W
            self.get(point.x - 1, point.y),
            # NW
            self.get(point.x - 1, point.y - 1),

        ] if p is not None)
        return neighbours

    def neighbouring_spaces(self, point):
        return list(
            p for p in self.neighbouring_points(point)
            if p.value != "#"
        )

    def height(self):
        return len(self.grid)

    def width(self):
        return max(len(row) for row in self.grid)

    def pixels(self):
        for row in self.grid:
            for point in row:
                yield point


def ticks(width, every):
    for c in " " * (every - 1):
        yield c
    for i in (i for i in range(1, width) if (i % every) == 0):
        buffer = str(i).ljust(every)
        for c in buffer:
            yield c


def parse(f):
    start = None
    end = None
    grid = tuple(
        tuple(
            Pixel(Point(column_number, row_number), value)
            for column_number, value in enumerate(line.rstrip("\n"))
        )
        for row_number, line in enumerate(f)
    )

    for row in grid:
        for pixel in row:
            if pixel.value == "s":
                start = pixel.point
            if pixel.value == "e":
                end = pixel.point
    return Grid(grid), start, end


class Solver(object):
    def __init__(self, grid, start, end):
        self.grid = grid
        self.start = start
        self.end = end
        self.current = {start: []}
        self.visited = set()

    def iter_solve(self):
        while self.current:
            if self.end in self.current:
                break
            else:
                yield
            self.visited.update(self.current.keys())
            current_items = self.current.items()
            self.current = {}
            for point, tail in current_items:
                for next_pixel in self.grid.neighbouring_spaces(point):
                    next_point = next_pixel.point
                    if next_point in self.visited:
                        continue
                    self.current[next_point] = tail + [point]


class Canvas(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        row = [""] * width
        self.grid = [row[:] for _ in range(height)]

    def draw(self, points):
        for point in points:
            try:
                self.grid[point.y][point.x] = point.value
            except IndexError:
                pass

    def __str__(self):
        width = self.width
        gutter_width = len(str(self.height))
        header = " " * gutter_width + " " + "".join(ticks(width, 5))
        return "\n".join(
            [header] +
            list(
                str(row_number if row_number % 5 == 0 else "").rjust(
                    gutter_width
                ) +
                " " +
                "".join(
                    value for value in row
                ) +
                " " +
                str(row_number if row_number % 5 == 0 else "").rjust(
                    gutter_width
                )
                for row_number, row in enumerate(self.grid, 1)
            ) +
            [header]
        )

RED = "\x1B[31m"
RESET = "\x1B[39;49m"
CLEAR = "\x1B[2J"


def main():
    grid, start, end = parse(open(sys.argv[1]))
    width = grid.width()
    height = grid.height()
    solver = Solver(grid, start, end)
    for _ in solver.iter_solve():
        print(CLEAR)
        c = Canvas(width, height)
        c.draw(grid.pixels())
        c.draw(Pixel(p, "o") for p in solver.current)
        c.draw(Pixel(p, RED + "~" + RESET) for p in solver.visited)
        c.draw([Pixel(start, "s")])
        c.draw([Pixel(end, "e")])
        print(str(c))
        time.sleep(0.1)

    solution = solver.current.get(end)
    if solution is None:
        print("No solution")
    else:
        print(CLEAR)
        c = Canvas(width, height)
        c.draw(grid.pixels())
        c.draw(Pixel(p, RED + "o" + RESET) for p in solution)
        c.draw([Pixel(start, "s")])
        c.draw([Pixel(end, "e")])
        print(str(c))
