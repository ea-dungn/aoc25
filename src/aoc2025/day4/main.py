from toolz import partial
import copy
from aoc2025 import pipe, map, runner, filter


def into_coord(mat: list[list[str]]) -> list[tuple[int, int]]:
    return [(x, y) for x in range(len(mat)) for y in range(len(mat[0]))]


def is_paper_roll(location: tuple[int, int], mat: list[list[str]]) -> bool:
    x, y = location
    return mat[x][y] == "@"


def into_neighbors(
    location: tuple[int, int], mat: list[list[str]]
) -> list[tuple[int, int]]:
    max_x, max_y = len(mat), len(mat[0])
    loc_x, loc_y = location
    return [
        (x, y)
        for x in range(loc_x - 1, loc_x + 2)
        for y in range(loc_y - 1, loc_y + 2)
        if (x != loc_x or y != loc_y) and x >= 0 and y >= 0 and x < max_x and y < max_y
    ]


def is_accessible(neighbors: list[tuple[int, int]], mat: list[list[str]]) -> bool:
    return sum([mat[x][y] == "@" for (x, y) in neighbors]) < 4


def unload(mat: list[list[str]]):
    return pipe(
        mat,
        into_coord,
        filter(partial(is_paper_roll, mat=mat)),
        map(partial(into_neighbors, mat=mat)),
        map(partial(is_accessible, mat=mat)),
        sum,
    )


def unload_continuously(mat: list[list[str]], acc=0):
    new_sum = unload(mat)
    if not new_sum:
        return acc

    # get list of removeables
    removables = pipe(
        mat,
        into_coord,
        filter(partial(is_paper_roll, mat=mat)),
        filter(
            lambda location: pipe(
                location,
                partial(into_neighbors, mat=mat),
                partial(is_accessible, mat=mat),
            )
        ),
        list,
    )
    new_mat = [
        [mat[x][y] if (x, y) not in removables else "." for y in range(len(mat[0]))]
        for x in range(len(mat))
    ]

    return unload_continuously(new_mat, new_sum + acc)


def solve(lines: list[str]):
    # for each paper roll, if less than 4 rolls of paper in neighbors then it can be accessed
    mat = pipe(lines, map(lambda line: list(line)), list)
    return unload_continuously(mat)


main = runner(__file__, solve)
