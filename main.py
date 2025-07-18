from os import *
from rich import print
from prompt_toolkit import *
from argparse import *
from click import *
from rich.console import *
from textual import *
from inquirer import *
from tqdm import *
import importlib

__framework__ = "ConSolar"
__version__ = "0.0.1b"
__doc__ = "A Console Framework "

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

#---Plugin management---#
class Framework:
    def __init__(self):
        self.plugins = []

    def register_plugin(self, plugin):
        try:
            self.plugins.append(plugin)
            plugin.register(self)
        except Exception as e:
            print(f"Error registering plugin {plugin}: {e}")

class Plugin:
    def run(self):
        pass  # Plugins must implement this method

def load_plugin(module_name, class_name):
    module = importlib.import_module(module_name)
    plugin_class = getattr(module, class_name)
    return plugin_class()

def unload_plugin(plugin):
    try:
        plugin.unregister()
    except Exception as e:
        print(f"Error unloading plugin {plugin}: {e}")
#---Plugin management---#

#FIXME: Return type of generator function must be compatible with "Generator[Any, Any, Any]"
#"Generator[Any, Any, Any]" is not assignable to "None" 
def logger(target, show_target, repeat:int = 1) -> None:
    if show_target:
        for i in range(repeat):
            print(target)
    else:
        print("[red]Logging is disabled because 'show_target' is set to False.[/red]")

if KeyboardInterrupt == True:
    exit()                     # --> Handling Ctrl + C (KeyboardInterrupt)

user = user()

