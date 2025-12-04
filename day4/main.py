with open("example", "r") as file:
    lines = list(map(lambda line: line.strip(), file.readlines()))
    print(lines)
