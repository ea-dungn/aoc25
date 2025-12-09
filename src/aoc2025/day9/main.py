from functools import partial
from itertools import combinations
from aoc2025 import pipe, compose, map, runner, filter, reducewith


def is_valid_rect(
    coords: tuple[tuple[int, int], tuple[int, int]],
    points: list[tuple[int, int]],
) -> bool:
    (x1, y1), (x2, y2) = coords
    x, y = max(x1, x2), max(y1, y2)  # diagonal
    # we can infer all four points

    # check if any point stick out of the blob (what is IN the blob?)
    # we can have a map to color all points in the blob?
    # start by greedily draw lines? then how do we determine the area of the
    # blob?

    return True


def into_rect_area(coords: tuple[tuple[int, int], tuple[int, int]]) -> int:
    (x1, y1), (x2, y2) = coords
    return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)


def solve(lines: list[str]):
    points = pipe(
        lines,
        map(
            compose(
                lambda line: line.split(","),
                map(int),
                tuple,
            ),
        ),
    )
    combs = pipe(
        points,
        partial(combinations, r=2),
    )
    sol1 = pipe(
        combs,
        map(into_rect_area),
        max,
    )
    sol2 = pipe(
        combs,
        filter(partial(is_valid_rect, points=points)),
        map(into_rect_area),
        list,
    )
    return sol2


main = runner(__file__, solve)
