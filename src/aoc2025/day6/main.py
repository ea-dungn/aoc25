from functools import partial
from aoc2025 import pipe, compose, map, runner, filter
from aoc2025.lib import reducewith

import re
import operator


def solve(lines: list[str]):
    def pp(a):
        print(a)
        return a

    def transpose(mat: list[list[str]]) -> list[list[str]]:
        new_mat = [["" for _ in range(len(mat))] for _ in range(len(mat[0]))]
        for x in range(len(mat)):
            for y in range(len(mat[0])):
                new_mat[y][x] = mat[x][y]
        return new_mat

    def eval_line(line: list[str]):
        numbers, op, initial = (
            pipe(line[0:-1], map(int), list),
            operator.add if line[-1] == "+" else operator.mul,
            0 if line[-1] == "+" else 1,
        )
        return pipe(numbers, reducewith(op, initial))

    reg = r"(\d+|[+*])"
    sol_1 = pipe(
        lines,
        map(lambda line: re.findall(reg, line)),
        list,
        transpose,
        # map(eval_line),
        # sum,
    )

    sol_2 = pipe(
        lines,
        map(list),
        list,
        transpose,
        map(lambda line: re.findall(reg, "".join(line))),
        reducewith(
            lambda acc, l: acc + [l]
            if len(l) == 2
            else acc[0:-1]
            + [
                acc[-1][0:-1] + l + [acc[-1][-1]]
            ]  # add the number to the penultimate of the last chunk
            if len(l) == 1
            else acc,
            [],
        ),
        map(eval_line),
        sum,
    )
    return sol_2


main = runner(__file__, solve)
