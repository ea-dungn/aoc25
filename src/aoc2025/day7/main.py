from functools import partial
from aoc2025 import pipe, compose, map, runner, filter
from aoc2025.lib import reducewith

import re
import operator


def solve(lines: list[str]):
    def pp(a):
        print(a)
        return a

    """
    a beam comes down from S, hit a spliter, turn into two beams
    puz 1 is counting the number of times it splitted, which might be a recursive problem...
    """

    def count_split(lines: list[list[str]], counter: int = 0) -> int:
        if len(lines) == 1:
            return counter

        line, rest = lines[0], lines[1:]
        if "S" in line:
            rest[0][line.index("S")] = "|"
        elif "^" in rest[0]:
            # check if beam in line hit splitter in rest[0]
            beams = [i for i, c in enumerate(line) if c == "|"]
            splitters = [i for i, c in enumerate(rest[0]) if c == "^"]
            for b in beams:
                if b not in splitters:
                    rest[0][b] = '|'
                    continue
                counter += 1
                if b - 1 >= 0:
                    rest[0][b - 1] = '|'
                if b + 1 < len(rest[0]):
                    rest[0][b + 1] = '|'
        else:
            beams = [i for i, c in enumerate(line) if c == "|"]
            for b in beams:
                rest[0][b] = '|'

        return count_split(rest, counter)

    sol_1 = pipe(
        lines,
        map(list),
        list,
        count_split,
    )
    # return sol_1

    """
    puz 2 is where the beam only takes one path at a time, which means we have to
    eliminate duplicate cases, or we should accumulate something only
    """
    cache = {}

    # sol_2 = pipe(
    #     lines,
    #     sum,
    # )
    # return sol_2


main = runner(__file__, solve)
