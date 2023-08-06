import unittest

from src.aoc import template


class TestPart1(unittest.TestCase):
    def test_part1(self):
        part1 = Part1(3, 2018)
        self.assertEqual(Part1.expected_result, part1.output(),
                         'Should return expected result')
        self.assertEqual(1, part1.part, 'parts should be equal')


class Part1(template.Part1):
    expected_result = 'Solved Part 1!'

    def __init__(self, day: int, year: int) -> None:
        super().__init__(day, year)

    def solve(self):
        return Part1.expected_result
