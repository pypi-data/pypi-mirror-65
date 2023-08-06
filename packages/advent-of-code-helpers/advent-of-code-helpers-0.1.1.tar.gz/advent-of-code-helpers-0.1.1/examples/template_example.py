import os

from src.aoc import template
from src.aoc.helpers import input_lines


class Part1(template.Part1):
    def __init__(self, day: int, year: int) -> None:
        super().__init__(day, year)

    def solve(self):
        # Read input
        lines = input_lines(self.input())
        # Do some work here

        # Sample output
        result = ','.join(lines)
        return result


class Part2(template.Part2):
    def __init__(self, day: int, year: int) -> None:
        super().__init__(day, year)

    def solve(self):
        # Read input
        lines = input_lines(self.input())
        # Do some work here

        # Sample output
        result = ','.join(lines)
        return result


def main():
    output_dir = '../out'
    test_data = os.path.join(os.path.dirname(__file__),
                             'resources/test_input.txt')
    Part1(1, 2018).data(test_data).output(output_dir)
    Part2(1, 2018).data(test_data).output(output_dir)

    data = os.path.join(os.path.dirname(__file__), 'resources/input.txt')
    Part1(1, 2018).data(data).output(output_dir)
    Part2(1, 2018).data(data).output(output_dir)


if __name__ == "__main__":
    main()
