from aoc2025 import pipe, map, runner


def joule(bank: list[str], bank_len: int, ooo: int) -> int:
    choice = []
    left = 0
    # find max in bank[left:right]
    # set left equals max's index
    for i in range(ooo):
        right = bank_len + i - ooo + 1

        max_ = max(bank[left:right])
        max_idx = bank[left:right].index(max_)
        choice.append(max_)
        left += max_idx + 1

    return int("".join(choice))


def solve(lines: list[str]):
    bank_len = len(lines[0])
    ooo = 3 if bank_len == 16 else 12
    return pipe(
        lines,
        map(list),
        map(lambda bank: joule(bank, bank_len, ooo)),
        sum,
    )


main = runner(__file__, solve)
