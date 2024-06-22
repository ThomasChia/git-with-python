from enum import Enum
from functools import partial

from lit.add import add_to_staging
from lit.commit import commit_files_to_local
from lit.initialise import create_dot_lit_directory


class LitCommand(Enum):
    init = partial(create_dot_lit_directory)
    add = partial(add_to_staging)
    commit = partial(commit_files_to_local)


def run(command: str, *args):
    command_function = LitCommand[command].value
    if args:
        command_function(args)
    else:
        command_function()
