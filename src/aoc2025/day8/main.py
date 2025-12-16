from functools import partial
from itertools import combinations
from aoc2025 import pipe, compose, map, runner, filter
from aoc2025.lib import reducewith, take

from dataclasses import dataclass
import math


def solve(lines: list[str]):
    def pp(a):
        print(a)
        return a

    """
    positions in 3d
    puz 1 is counting the number of times it splitted, which might be a recursive problem...
    """

    def distance(a, b):
        return sum([(a - b) ** 2 for a, b in zip(a, b)])

    def into_circuits(circuits_lim, pair):
        circuits, lim = circuits_lim
        if lim == 0:
            return circuits, lim

        p1, p2 = pair
        p1in = [i for i, c in enumerate(circuits) if p1 in c]
        p2in = [i for i, c in enumerate(circuits) if p2 in c]

        assert len(p1in) <= 1
        assert len(p2in) <= 1

        # four cases
        if len(p1in) == 0 and len(p2in) == 0:
            circuits.append([p1, p2])
            lim -= 1
            return circuits, lim
        elif len(p1in) == 1 and len(p2in) == 1:
            (id1,) = p1in
            (id2,) = p2in
            if id1 == id2:
                # already connected, do nothing
                lim -= 1
                return circuits, lim
            else:
                # join two disjoint circuits
                min_id, max_id = (id1, id2) if id1 < id2 else (id2, id1)
                circuits[min_id].extend(circuits.pop(max_id))
                lim -= 1
                return circuits, lim
        elif len(p1in) == 1:
            (id1,) = p1in
            circuits[id1].append(p2)
            lim -= 1
            return circuits, lim
        else:
            (id2,) = p2in
            circuits[id2].append(p1)
            lim -= 1
            return circuits, lim

    sol_1 = pipe(
        lines,
        map(
            compose(
                lambda line: line.split(","),
                map(int),
                list,
            )
        ),
        partial(combinations, r=2),
        partial(sorted, key=lambda x: distance(x[0], x[1])),
        reducewith(into_circuits, ([], 1000)),
        lambda a: a[0],
        map(len),
        partial(sorted, reverse=True),
        list,
        take(3),
        math.prod,
    )
    # return sol_1

    def into_circuits_2(circuits_lim, pair):
        circuits = circuits_lim

        p1, p2 = pair
        p1in = [i for i, c in enumerate(circuits) if p1 in c]
        p2in = [i for i, c in enumerate(circuits) if p2 in c]

        assert len(p1in) <= 1
        assert len(p2in) <= 1

        # four cases
        if len(p1in) == 0 and len(p2in) == 0:
            circuits.append([p1, p2])
        elif len(p1in) == 1 and len(p2in) == 1:
            (id1,) = p1in
            (id2,) = p2in
            if id1 == id2:
                # already connected, do nothing
                pass
            else:
                # join two disjoint circuits
                min_id, max_id = (id1, id2) if id1 < id2 else (id2, id1)
                circuits[min_id].extend(circuits.pop(max_id))
        elif len(p1in) == 1:
            (id1,) = p1in
            circuits[id1].append(p2)
        else:
            (id2,) = p2in
            circuits[id2].append(p1)

        # stop when this pair will make the thing into one big thing
        # which means that the largest circuit is as big as whole thing
        if len(circuits) == 1 and len(circuits[0]) == len(input_2):
            print(p1 * p2)
            exit(0)

        return circuits

    # until the last pair that cause the whole thing to be one big tree
    input_2 = pipe(
        lines,
        map(
            compose(
                lambda line: line.split(","),
                map(int),
                list,
            )
        ),
        list,
    )
    sol_2 = pipe(
        input_2,
        partial(combinations, r=2),
        partial(sorted, key=lambda x: distance(x[0], x[1])),
        reducewith(into_circuits_2, []),
    )
    return sol_2

    # sol_2 = pipe(
    #     lines,
    #     sum,
    # )
    # return sol_2


main = runner(__file__, solve)
