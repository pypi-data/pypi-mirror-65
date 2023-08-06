import os
import unittest

from src.aoc.helpers import read_input_from_file, input_lines


class TestHelpers(unittest.TestCase):
    def test_read_input_from_file(self):
        expected_data = '-1\n-19\n-7'
        file_path = os.path.join(os.path.dirname(__file__),
                                 'resources/input.txt')
        data = read_input_from_file(file_path)
        self.assertEqual(expected_data, data,
                         'Data should match expected data.')

    def test_input_lines(self):
        expected_data = ['-9', '-19', '-7']
        result = input_lines('\n'.join(expected_data))
        self.assertEqual(expected_data, result,
                         'input_lines should return expected result')
