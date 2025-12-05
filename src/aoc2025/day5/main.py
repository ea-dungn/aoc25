from functools import partial
from aoc2025 import pipe, compose, map, runner, filter
from aoc2025.lib import reducewith


def fresh_count(ranges: list[tuple[int, int]], vals: list[int]) -> int:
    return (
        len(set([val if x <= val <= y else None for val in vals for (x, y) in ranges]))
        - 1
    )


# https://blog.seancoughlin.me/mastering-the-merging-of-overlapping-intervals-in-python
def merge(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not intervals:
        return []

    head, tail = intervals[0], intervals[1:]

    def add_segment(acc: list[tuple[int, int]], current: tuple[int, int]):
        init, [lastx, lasty] = acc[:-1], acc[-1]
        currx, curry = current
        return init + (
            [[lastx, max(lasty, curry)]]
            if currx <= lasty
            else [[lastx, lasty], current]
        )

    return pipe(
        tail,
        reducewith(add_segment, [head]),
    )


def possible_fresh_count(ranges: list[tuple[int, int]], _vals: list[int]) -> int:
    return pipe(
        ranges,
        partial(sorted, key=lambda x: x[0]),
        merge,
        reducewith(lambda acc, r: acc + r[1] - r[0] + 1, 0),
    )


def solve(lines: list[str]):
    sep = lines.index("")
    ranges, vals = (
        pipe(
            lines[:sep],
            map(
                compose(
                    lambda line: line.split("-"),
                    map(int),
                    tuple,
                ),
            ),
            list,
        ),
        pipe(
            lines[sep + 1 :],
            map(int),
            list,
        ),
    )
    # return fresh_count(ranges, vals)
    return possible_fresh_count(ranges, vals)


main = runner(__file__, solve)
