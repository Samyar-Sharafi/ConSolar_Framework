from os import *
from rich import print
from prompt_toolkit import *
from argparse import *
from click import *
from rich.console import *
from textual import *
from inquirer import *
from tqdm import tqdm

__framework__ = "ConSolar",
__author__ = "Samyar-Sharafi",
__version__ = "0.0.1a"

class user:
    def __init__(self) -> None:
        self.question = None
        self.user_value = None

    def user_input(self, question) -> None:
        self.question = question
        self.user_value = input(self.question + " >>> ")
        # Now self.user_value holds the answer
        """
        code example:
        user_input(question)
        """

    def multi_choice(self, question, options) -> None:
        
        self.question = question
        questions = [
            List('choice', message=question, choices=options)
        ]
        answers = prompt(questions)
        self.user_value = answers['choice'] if answers else None
        # Now self.user_value holds the answer
        """
        code example:
        multi_choice(question, [option1, option2, option3, ...])
        """

if KeyboardInterrupt == True:
    exit()                     # --> Handling Ctrl + C (KeyboardInterrupt)

user = user()

