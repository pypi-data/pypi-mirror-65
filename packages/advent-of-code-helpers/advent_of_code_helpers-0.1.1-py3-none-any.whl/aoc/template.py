import os
from abc import ABC, abstractmethod

from src.aoc.helpers import output, read_input_from_file


class Puzzle(ABC):
    def __init__(self, part: int, day: int, year: int) -> None:
        self.part = part
        self.day = day
        self.year = year
        self.input_file = None
        super().__init__()

    def input(self):
        if self.input_file:
            return read_input_from_file(self.input_file)
        else:
            raise Exception('Use .data to provide data file.')

    @abstractmethod
    def solve(self):
        pass

    def data(self, input_file: str):
        self.input_file = input_file
        return self

    def output(self, output_dir: str = None):
        result = self.solve()
        file_prefix = None
        if self.input_file:
            file_prefix = \
                os.path.splitext(os.path.basename(self.input_file))[0]
        output(result, self.part, self.day, self.year, output_dir, file_prefix)
        return result


class Part1(Puzzle):
    def __init__(self, day: int, year: int) -> None:
        super().__init__(1, day, year)

    @abstractmethod
    def solve(self):
        pass


class Part2(Puzzle):
    def __init__(self, day: int, year: int) -> None:
        super().__init__(2, day, year)

    @abstractmethod
    def solve(self):
        pass
