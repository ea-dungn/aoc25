from functools import reduce
from typing import Tuple


def process(position_and_count: Tuple[int, int], step: int) -> Tuple[int, int]:
    position, cnt = position_and_count
    position = (position + step) % 100
    cnt += position == 0
    return (position, cnt)


def process2(position_and_count: Tuple[int, int], step: int) -> Tuple[int, int]:
    position, cnt = position_and_count
    # change the modulo to match direction of step
    mod = position if step > 0 or position == 0 else position - 100
    cnt += abs(int((mod + step) / 100))
    position = (position + step) % 100
    return (position, cnt)


def parse(x: str) -> int:
    return int(x.replace("L", "-").replace("R", ""))


with open("example", "r") as file:
    lines = reduce(
        process2,
        map(parse, file.readlines()),
        (50, 0),
    )
    print(lines)


with open("input", "r") as file:
    lines = reduce(
        process2,
        map(parse, file.readlines()),
        (50, 0),
    )
    print(lines)
