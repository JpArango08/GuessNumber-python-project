import sys
import os

sys.path.append(os.path.abspath("src"))

import unittest
from model.logic_guessnumber import GuessNumber

class TestNormalCase(unittest.TestCase):
    def test_normal_1(self):
        game_number = GuessNumber()
        game_number.random_numbers = [1,2,3,4]
        numbers_user= 1234
        result = game_number.check_number(numbers_user)
        self.assertEqual(result, "HECHO, MUY BIEN [1, 2, 3, 4]")
    def test_normal_2(self):
        game_number = GuessNumber()
        game_number.random_numbers = [1,2,3,4]
        numbers_user= 5000
        result = game_number.check_number(numbers_user)
        self.assertEqual(result, [None,None,None,None])
