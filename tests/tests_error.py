import sys
import os

sys.path.append(os.path.abspath("src"))

import unittest
from model.logic_guessnumber import GuessNumber, InputEmpty, StringInput, WrongLengthNumberUser

class TestErrorCase(unittest.TestCase):
    def test_error_empty_input(self):
        game_number = GuessNumber()
        with self.assertRaises(InputEmpty):
            game_number.check_number()
            

    def test_error_wrong_length(self):
        game_number= GuessNumber()
        numbers_user= 12345
        with self.assertRaises(WrongLengthNumberUser):
            game_number.check_number(numbers_user)
    
    def test_error_string(self):
        game_number= GuessNumber()
        numbers_user= "1234a"
        with self.assertRaises(StringInput):
            game_number.check_number(numbers_user)