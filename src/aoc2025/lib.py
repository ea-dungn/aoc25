from collections.abc import Callable, Iterable, Iterator
from pathlib import Path
from typing import Any, TypeVar, overload
from functools import reduce as _reduce
import itertools

T = TypeVar("T")
S = TypeVar("S")
A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
D = TypeVar("D")
E = TypeVar("E")
F = TypeVar("F")


@overload
def pipe(data: A) -> A: ...
@overload
def pipe(data: A, f1: Callable[[A], B]) -> B: ...
@overload
def pipe(data: A, f1: Callable[[A], B], f2: Callable[[B], C]) -> C: ...
@overload
def pipe(data: A, f1: Callable[[A], B], f2: Callable[[B], C], f3: Callable[[C], D]) -> D: ...
@overload
def pipe(data: A, f1: Callable[[A], B], f2: Callable[[B], C], f3: Callable[[C], D], f4: Callable[[D], E]) -> E: ...
@overload
def pipe(data: A, f1: Callable[[A], B], f2: Callable[[B], C], f3: Callable[[C], D], f4: Callable[[D], E], f5: Callable[[E], F]) -> F: ...
@overload
def pipe(data: A, f1: Callable[[A], B], f2: Callable[[B], C], f3: Callable[[C], D], f4: Callable[[D], E], f5: Callable[[E], F], *funcs: Callable[..., Any]) -> Any: ...
def pipe(data: Any, *funcs: Callable[..., Any]) -> Any:
    """Thread data through a sequence of functions."""
    for func in funcs:
        data = func(data)
    return data


@overload
def compose(f1: Callable[[A], B]) -> Callable[[A], B]: ...
@overload
def compose(f1: Callable[[A], B], f2: Callable[[B], C]) -> Callable[[A], C]: ...
@overload
def compose(f1: Callable[[A], B], f2: Callable[[B], C], f3: Callable[[C], D]) -> Callable[[A], D]: ...
@overload
def compose(f1: Callable[[A], B], f2: Callable[[B], C], f3: Callable[[C], D], f4: Callable[[D], E]) -> Callable[[A], E]: ...
@overload
def compose(f1: Callable[[A], B], f2: Callable[[B], C], f3: Callable[[C], D], f4: Callable[[D], E], f5: Callable[[E], F]) -> Callable[[A], F]: ...
@overload
def compose(f1: Callable[[A], B], f2: Callable[[B], C], f3: Callable[[C], D], f4: Callable[[D], E], f5: Callable[[E], F], *funcs: Callable[..., Any]) -> Callable[[A], Any]: ...
def compose(*funcs: Callable[..., Any]) -> Callable[..., Any]:
    """Compose functions left-to-right."""
    def composed(data: Any) -> Any:
        return pipe(data, *funcs)
    return composed


@overload
def reduce(func: Callable[[T, T], T], seq: Iterable[T]) -> T: ...
@overload
def reduce(func: Callable[[T, S], T], seq: Iterable[S], initial: T) -> T: ...
def reduce(func: Callable[..., Any], seq: Iterable[Any], initial: Any | None = None) -> Any:
    """Reduce a sequence with a function."""
    if initial is None:
        return _reduce(func, seq)
    return _reduce(func, seq, initial)


def reducewith(func: Callable[[T, S], T], initial: T) -> Callable[[Iterable[S]], T]:
    """Curried reduce that supports initial value for use in pipe."""
    return lambda seq: reduce(func, seq, initial)


def map(func: Callable[[T], S]) -> Callable[[Iterable[T]], Iterator[S]]:
    """Curried map - returns a function that maps over an iterable."""
    return lambda iterable: builtins_map(func, iterable)


builtins_map = __builtins__["map"] if isinstance(__builtins__, dict) else getattr(__builtins__, "map")
builtins_filter = __builtins__["filter"] if isinstance(__builtins__, dict) else getattr(__builtins__, "filter")


def filter(func: Callable[[T], bool] | None) -> Callable[[Iterable[T]], Iterator[T]]:
    """Curried filter - returns a function that filters an iterable."""
    return lambda iterable: builtins_filter(func, iterable)


def take(n: int) -> Callable[[Iterable[T]], Iterator[T]]:
    """Returns a function that takes first n items from an iterable."""
    return lambda iterable: itertools.islice(iterable, n)


def drop(n: int) -> Callable[[Iterable[T]], Iterator[T]]:
    """Returns a function that drops first n items from an iterable."""
    return lambda iterable: itertools.islice(iterable, n, None)


def first(iterable: Iterable[T]) -> T:
    """Get the first item from an iterable."""
    return next(iter(iterable))


def last(iterable: Iterable[T]) -> T | None:
    """Get the last item from an iterable."""
    item = None
    for item in iterable:
        pass
    return item


def concat(iterables: Iterable[Iterable[T]]) -> Iterator[T]:
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
