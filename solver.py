import sys
from collections import namedtuple

Point = namedtuple("Point", "x y value")


class Grid(object):
    def __init__(self, grid):
        self.grid = grid

    def get(self, x, y):
        if x < 0 or y < 0:
            return None
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

    def __str__(self):
        width = max(len(row) for row in self.grid)
        gutter_width = len(str(len(self.grid)-1))
        header = " " * gutter_width + " " + "".join(ticks(width, 5))
        return "\n".join(
            [header] +
            list(
                str(row_number if row_number % 5 == 0 else "").rjust(gutter_width) +
                " " +
                "".join(
                    point.value for point in row
                ) +
                " " +
                str(row_number if row_number % 5 == 0 else "").rjust(gutter_width)
                for row_number, row in enumerate(self.grid, 1)
            ) +
            [header]
        )


def ticks(width, every):
    for c in " " * (every - 1):
        yield c
    for i in (i for i in range(1, width) if (i % every) == 0):
        buffer = str(i).ljust(every)
        for c in buffer:
            yield c


def parse():
    start = None
    end = None
    grid = tuple(
        tuple(
            Point(column_number, row_number, value)
            for column_number, value in enumerate(line.rstrip())
        )
        for row_number, line in enumerate(sys.stdin)
    )

    for row in grid:
        for point in row:
            if point.value == "s":
                start = point
            if point.value == "e":
                end = point
    return Grid(grid), start, end


def solve(grid, start, end):
    visited_points = set()
    current_points = set([start])
    while current_points and end not in current_points:
        visited_points.update(current_points)
        next_points = set()
        for point in current_points:
            new_points = grid.neighbouring_spaces(point)
            next_points.update(new_points)
        current_points = next_points - visited_points

    return end in current_points


def main():
    grid, start, end = parse()
    print("START:", start)
    print("END:", end)
    solution = solve(grid, start, end)
    print(str(grid))
    print("SOLUTION:", solution)


if __name__ == "__main__":
    raise SystemExit(main())
