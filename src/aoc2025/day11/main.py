from collections import defaultdict
from functools import partial
from itertools import combinations, permutations
from aoc2025 import pipe, compose, map, runner, filter, reducewith


def solve(lines: list[str]):
    """
    input is a list of directed graph, node: outputs
    puz1 is to find the number of paths from 'you' to 'out'
    """

    def into_adj(line: str):
        node, tail = line.split(": ")
        outputs = tail.split(" ")
        return node, outputs

    def paths_to_out(
        adj: defaultdict[str, list[str]], curr: list[str] = ["you"]
    ) -> list[list[str]]:
        if curr[-1] == "out":
            return [curr]
        return pipe(
            adj[curr[-1]],
            reducewith(
                lambda acc, neighbor: acc + paths_to_out(adj, curr + [neighbor]), []
            ),
        )

    cache = {}

    def count_paths(
        adj: defaultdict[str, list[str]],
        curr: str,
        target: str,
        seen_fft: bool = False,
        seen_dac: bool = False,
    ):
        seen_fft = seen_fft or curr == "fft"
        seen_dac = seen_dac or curr == "dac"

        if curr == target and seen_fft and seen_dac:
            return 1

        cache_key = (curr, seen_fft, seen_dac)
        if cache_key not in cache:
            cache[cache_key] = pipe(
                adj[curr],
                reducewith(
                    lambda acc, neighbor: acc
                    + count_paths(adj, neighbor, target, seen_fft, seen_dac),
                    0,
                ),
            )
        return cache[cache_key]

    sol_1 = pipe(
        lines,
        map(into_adj),
        partial(defaultdict, list),
        paths_to_out,
        len,
    )

    # will get out of memory even with cache
    # idea: going from "out" to svr does not help
    # idea 2: only count, not returning the sequence cuz we don't need it
    sol_2 = pipe(
        lines,
        map(into_adj),
        partial(defaultdict, list),
        partial(count_paths, curr="svr", target="out"),
    )

    return sol_1, sol_2


main = runner(__file__, solve)
