from argparse import Action
from dataclasses import dataclass
from typing import List, Union, Type


@dataclass
class Argument(object):
    config_name: str
    name_or_flags: List[str]
    help_str: str = None
    required: bool = None
    action:  Union[str, Type[Action]] = None


@dataclass
class Command(object):
    command_class: type
    args: List[Argument]
