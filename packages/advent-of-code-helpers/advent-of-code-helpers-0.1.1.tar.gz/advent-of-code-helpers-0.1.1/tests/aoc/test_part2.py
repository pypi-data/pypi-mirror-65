import unittest

from src.aoc import template


class TestPart2(unittest.TestCase):
    def test_part2(self):
        part2 = Part2(3, 2018)
        self.assertEqual(Part2.expected_result, part2.output(),
                         'Should return expected result')
        self.assertEqual(2, part2.part, 'parts should be equal')


class Part2(template.Part2):
    expected_result = 'Solved Part 1!'

    def __init__(self, day: int, year: int) -> None:
        super().__init__(day, year)

    def solve(self):
        return Part2.expected_result
