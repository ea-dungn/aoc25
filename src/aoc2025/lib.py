from pathlib import Path
from typing import Callable, Any
from toolz import pipe, reduce
from toolz.curried import map, filter, take, drop, first, last, concat


def reducewith(func, initial):
    """Curried reduce that supports initial value for use in pipe."""
    return lambda seq: reduce(func, seq, initial)


def slurp(filename: str) -> list[str]:
    """Read all lines from a file."""
    with open(filename, "r") as f:
        return f.readlines()


def slurp_strip(filename: str) -> list[str]:
    """Read all lines from a file, stripping whitespace."""
    with open(filename, "r") as f:
        return [line.strip() for line in f]


def runner(
    day_file: str,
    solve: Callable[[list[str]], Any],
    example_file: str = "example",
    input_file: str = "input",
):
    """Returns a main function for a day module."""
    dir_path = Path(day_file).parent

    def main(mode: str | None = None):
        if mode == "example" or mode is None:
            lines = slurp_strip(dir_path / example_file)
            print(solve(lines))
        if mode == "input" or mode is None:
            lines = slurp_strip(dir_path / input_file)
            print(solve(lines))

    return main
