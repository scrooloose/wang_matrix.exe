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
            if p.value != "#"
        )

    def __str__(self):
        width = max(len(row) for row in self.grid)
        spacer = len(str(len(self.grid)-1))
        header = "".join((" " if ((i+1) % 5) else "*") for i in range(width))
        return (
            " " * spacer + " " + header + "\n" +
            "\n".join(
                str(row_number).rjust(spacer) + " " + "".join(point.value for point in row)
                for row_number, row in enumerate(self.grid)
            )
        )


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
