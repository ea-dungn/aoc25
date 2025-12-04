from aoc2025 import pipe, map, reducewith, runner


def step(state: tuple[int, int], delta: int) -> tuple[int, int]:
    position, cnt = state
    mod = position if delta > 0 or position == 0 else position - 100
    cnt += abs(int((mod + delta) / 100))
    position = (position + delta) % 100
    return (position, cnt)


def parse(x: str) -> int:
    return int(x.replace("L", "-").replace("R", ""))


def solve(lines: list[str]):
    return pipe(
        lines,
        map(parse),
        reducewith(step, (50, 0)),
    )


main = runner(__file__, solve)
