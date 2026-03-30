import random
from typing import Any,List

class WrongLengthNumberUser(Exception):
    """The numbers user must have a length of four"""
    def __init__(self, numbers_user): 
        super().__init__(f"The number {numbers_user} must have exactly 4 digits")


class InputEmpty(Exception):
    """No empty inputs for play"""
    def __init__(self): 
        super().__init__("Please enter a number")


class StringInput(Exception):
    """No string inputs, only int"""
    def __init__(self, numbers_user): 
        super().__init__(f"You entered a string: {numbers_user}, please enter only numbers")


class ValidateInput:
    def validate_parameters(numbers_user: int) -> None:
        if numbers_user is None or str(numbers_user).strip() == "":
            raise InputEmpty()
        if isinstance(numbers_user, str):
            raise StringInput(numbers_user)
        if len(str(numbers_user)) != 4:
            raise WrongLengthNumberUser(numbers_user)
        
class GuessNumber:
   def __init__(self):
      self.random_numbers= [int(individual_number) for individual_number in str(random.randint(1000, 9999))] 
      self.guessed_numbers = [None,None,None,None] 
   
   def check_number(self, numbers_user: int = None) -> List:
      ValidateInput.validate_parameters(numbers_user)
      numbers_user_list = [int(n) for n in str(numbers_user)]
      for pos, number in enumerate(numbers_user_list):
        if number == self.random_numbers[pos]:
           self.guessed_numbers[pos] = number
      if None not in self.guessed_numbers:
        return f"HECHO, MUY BIEN {self.guessed_numbers}"
      return self.guessed_numbers     
               
               
      