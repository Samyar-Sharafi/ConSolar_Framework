# Core Python modules
from os import *
from sys import exit, argv, path as sys_path
from json import load, loads, dump, dumps
from logging import getLogger, basicConfig, DEBUG, INFO, WARNING, ERROR, CRITICAL
from subprocess import run, Popen, PIPE, call
from pathlib import Path
from datetime import datetime, date, time, timedelta
from typing import Optional, List, Dict, Any, Union, Tuple
from enum import Enum
from time import sleep
from random import choice, randint
from re import search, match, findall, sub
from glob import glob
from shutil import copy, move, rmtree
from keyboard import *

# CLI and argument parsing
from argparse import *
from click import *

# Rich ecosystem for beautiful output
from rich import print
from rich.console import Console
from rich.table import Table
from rich.progress import track, Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.columns import Columns
from rich.layout import Layout
from rich.live import Live
from rich.spinner import Spinner
from rich.status import Status
from rich.tree import Tree
from rich.rule import Rule
from rich.align import Align
from rich.padding import Padding
from rich.markdown import Markdown

# Interactive prompts and UI
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import confirm
from prompt_toolkit.completion import WordCompleter, PathCompleter
from prompt_toolkit.history import FileHistory
from inquirer import prompt as inquirer_prompt
from inquirer import List, Checkbox, Text as InquirerText, Confirm as InquirerConfirm, Editor, Path as InquirerPath

# Progress bars and indicators
from tqdm import tqdm, trange

# Textual for TUI apps (if needed)
from textual.app import App, ComposeResult
from textual.widgets import Button, Static, Input, TextArea, DataTable, ListView
from textual.containers import Container, Horizontal, Vertical

# File and configuration handling
from configparser import ConfigParser
from pathlib import Path

# HTTP requests (commonly needed)
try:
    from requests import get, post, put, delete, patch, Session
except ImportError:
    get = post = put = delete = patch = Session = None

# Data handling
try:
    from pandas import DataFrame, read_csv, read_json, read_excel # type: ignore
except ImportError:
    DataFrame = read_csv = read_json = read_excel = None

# ConSolar specific imports
from logger import ConSolarLogger, LogLevel
from error_handler import (
    ConSolarError, PluginError, ConfigurationError, ValidationError,
    safe_execute, SafeOperation, validate_not_empty, validate_file_exists, validate_positive_int
)
from plugin_manger import (
    PluginManager, Plugin, EnhancedPlugin, PluginInfo, 
    scan_for_plugins, plugin_manager
)
from config_manager import (
    ConfigManager, EnvConfig, config_manager
)

# for parser error handling
import wrapt


__framework__ = "ConSolar"
__version__ = "1.0.0"
__doc__ = "A Console Framework for Interactive Applications"

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


# KeyboardInterrupt handling is now done properly in error_handler.py
# This was moved to avoid syntax errors

user = user()

@wrapt.decorator
def handle_errors(wrapped, instance, args, kwargs):
    try:
        return wrapped(*args, **kwargs)
    except Exception:
        # Handle the error silently or log it
        pass

@handle_errors
def parse(args:callable, func:callable): 
    if user.user_value == args:return func(args)

user.user_input("Type smth")
parse(args="h", func=print(f"you have Typed 'h' !"))