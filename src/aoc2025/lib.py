from pathlib import Path
from typing import Callable, Any
from functools import reduce as _reduce
import itertools


def pipe(data, *funcs):
    """Thread data through a sequence of functions."""
    for func in funcs:
        data = func(data)
    return data


def reduce(func, seq, initial=None):
    """Reduce a sequence with a function."""
    if initial is None:
        return _reduce(func, seq)
    return _reduce(func, seq, initial)


def reducewith(func, initial):
    """Curried reduce that supports initial value for use in pipe."""
    return lambda seq: reduce(func, seq, initial)


def map(func):
    """Curried map - returns a function that maps over an iterable."""
    return lambda iterable: builtins_map(func, iterable)


builtins_map = __builtins__["map"] if isinstance(__builtins__, dict) else getattr(__builtins__, "map")
builtins_filter = __builtins__["filter"] if isinstance(__builtins__, dict) else getattr(__builtins__, "filter")


def filter(func):
    """Curried filter - returns a function that filters an iterable."""
    return lambda iterable: builtins_filter(func, iterable)


def take(n):
    """Returns a function that takes first n items from an iterable."""
    return lambda iterable: itertools.islice(iterable, n)


def drop(n):
    """Returns a function that drops first n items from an iterable."""
    return lambda iterable: itertools.islice(iterable, n, None)


def first(iterable):
    """Get the first item from an iterable."""
    return next(iter(iterable))


def last(iterable):
    """Get the last item from an iterable."""
    item = None
    for item in iterable:
        pass
    return item


def concat(iterables):
    """Flatten one level of nesting."""
    return itertools.chain.from_iterable(iterables)


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
