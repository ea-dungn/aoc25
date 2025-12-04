from functools import reduce

def joule(bank: list[str]) -> int:
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

    return int(''.join(choice))

# with open("example", "r") as file:
with open("input", "r") as file:
    banks = list(map(lambda line: list(line.strip()), file.readlines()))

    bank_len = len(banks[0])
    ooo = 12

    total = sum(map(joule, banks))
    print(total)
