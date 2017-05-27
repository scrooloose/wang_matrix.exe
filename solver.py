import sys
import time
from collections import namedtuple

Point = namedtuple("Point", "x y value")


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
            self.get(point.x, point.y - 1),
            self.get(point.x, point.y + 1),
            self.get(point.x - 1, point.y),
            self.get(point.x + 1, point.y),
        ] if p is not None)
        return neighbours

    def neighbouring_spaces(self, point):
        return list(
            p for p in self.neighbouring_points(point)
            if p.value != "+"
        )

    def height(self):
        return len(self.grid)

    def width(self):
        return max(len(row) for row in self.grid)

    def points(self):
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
            Point(column_number, row_number, value)
            for column_number, value in enumerate(line.rstrip("\n"))
        )
        for row_number, line in enumerate(f)
    )

    for row in grid:
        for point in row:
            if point.value == "s":
                start = point
            if point.value == "e":
                end = point
    return Grid(grid), start, end


def point_char(point, char):
    return Point(point.x, point.y, char)


class Solver(object):
    def __init__(self, grid, start, end):
        self.grid = grid
        self.start = start
        self.end = end
        self.current = set([start])
        self.visited = set()

    def iter_solve(self):
        while self.current:
            if self.end in self.current:
                break
            else:
                yield
            self.visited.update(self.current)
            next_points = set()
            for point in self.current:
                new_points = self.grid.neighbouring_spaces(point)
                next_points.update(new_points)
            self.current = next_points - self.visited


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
                str(row_number if row_number % 5 == 0 else "").rjust(gutter_width) +
                " " +
                "".join(
                    value for value in row
                ) +
                " " +
                str(row_number if row_number % 5 == 0 else "").rjust(gutter_width)
                for row_number, row in enumerate(self.grid, 1)
            ) +
            [header]
        )


def main():
    grid, start, end = parse(open(sys.argv[1]))
    solver = Solver(grid, start, end)
    for solution in solver.iter_solve():
        print("\x1B[2J")
        c = Canvas(grid.width(), grid.height())
        c.draw(grid.points())
        c.draw(point_char(p, "o") for p in solver.current)
        c.draw(point_char(p, "~") for p in solver.visited)
        c.draw([start])
        print(str(c))
        time.sleep(0.1)

if __name__ == "__main__":
    raise SystemExit(main())
