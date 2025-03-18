"""Parser class implementation."""

import shlex
from typing import List

from pydantic import BaseModel


class ParsedCommand(BaseModel):
    """Represents a parsed command with its name and a list of arguments."""

    name: str
    args: List[str]


class ParsedCommands(BaseModel):
    """Represents a sequence of parsed commands."""

    command_seq: List[ParsedCommand]


class Parser(BaseModel):
    """Parser class to tokenize and parse command line strings."""

    def _tokenize(self, command: str) -> ParsedCommand:
        args: List[str] = shlex.split(command)
        name: str = args.pop(0)
        return ParsedCommand(name=name, args=args)

    def parse(self, line: str) -> ParsedCommands:
        """Parse a line of command string into ParsedCommands.

        Args:
            line (str): The command line string to parse.

        Returns:
            ParsedCommands: An object containing a sequence of parsed commands.
        """
        command: ParsedCommand = self._tokenize(line)
        return ParsedCommands(command_seq=[command])
