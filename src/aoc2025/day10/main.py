from functools import partial
from itertools import combinations, permutations
from aoc2025 import pipe, compose, map, runner, filter, reducewith


def solve(lines: list[str]):
    # each line is a machine with [target indicator light] (button wiring) {joltage requirements}
    # all lights are initially off
    # button wiring means that pressing that button would result in toggling those certain lights

    def into_configs(line: str):
        parts = line.split(" ")
        indicators, wirings, joltage = (
            pipe(
                parts[0][1:-1],  # remove [ ]
                list,
            ),
            pipe(
                parts[1:-1],
                map(
                    lambda wiring: pipe(
                        wiring[1:-1].split(","),  # remove ( )
                        map(int),
                        list,
                    )
                ),
                list,
            ),
            pipe(
                parts[-1][1:-1].split(","),  # remove { }
                map(int),
                list,
            ),
        )
        return indicators, wirings, joltage

    def into_wiring_combinations(wirings: list[int]) -> list[list[int]]:
        return pipe(
            range(1, len(wirings) + 1),
            reducewith(lambda acc, size: acc + list(combinations(wirings, size)), []),
        )

    def apply_wiring(wirings: list[int], light: int = 0) -> int:
        return pipe(wirings, reducewith(lambda acc, w: acc ^ w, light))

    # puz1: find fewest number of presses to satisfy the indicator, across all machines
    # toggling can be thought of as xor? and if we can generate all the permutations then we can
    # determine the least that would satisfy the requirement
    sol_1 = pipe(
        lines,
        map(into_configs),
        map(
            lambda machine_config: pipe(
                machine_config[1],  # wirings, since python pattern matching is a joke
                map(
                    lambda wiring_list: pipe(
                        wiring_list,
                        reducewith(
                            lambda acc, wiring_idx: acc
                            | 1 << (len(machine_config[0]) - int(wiring_idx) - 1),
                            0,
                        ),
                    ),
                ),
                list,
                into_wiring_combinations,
                filter(
                    lambda wiring_combination: apply_wiring(wiring_combination)
                    == pipe(
                        machine_config[0],
                        reducewith(lambda acc, char: acc << 1 | int(char == "#"), 0),
                    )
                ),
                map(len),
                min,
            ),
        ),
        sum,
    )

    # puz2: each wiring increases the lights to the joltage requirement, so it is more like linear
    # equation solver, or more like linear optimization
    sol_2 = pipe(
        lines,
        map(into_configs),
        map(
            lambda machine_config: pipe(
                machine_config,
                list,
            )
        ),
    )
    return sol_2


main = runner(__file__, solve)
