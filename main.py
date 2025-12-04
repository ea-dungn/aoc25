import sys
import importlib


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run python main.py <day> [example|input]")
        print("Example: uv run python main.py day1")
        print("         uv run python main.py day1 example")
        sys.exit(1)

    day = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        module = importlib.import_module(f"aoc2025.{day}.main")
        module.main(mode)
    except ModuleNotFoundError:
        print(f"Day '{day}' not found")
        sys.exit(1)


if __name__ == "__main__":
    main()
