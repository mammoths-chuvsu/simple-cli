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

    def _append_command(
        self, command_seq: List[ParsedCommand], command_tokens: List[str]
    ):
        command_seq.append(
            ParsedCommand(
                name=command_tokens[0],
                args=command_tokens[1:],
            )
        )

    def parse(self, line: str) -> ParsedCommands:
        """Parse a line of command string into ParsedCommands.

        Args:
            line (str): The command line string to parse.

        Returns:
            ParsedCommands: An object containing a sequence of parsed commands.
        """
        tokens = shlex.split(line)

        if not tokens:
            raise ValueError("Input command line string is empty.")

        command_seq: List[ParsedCommand] = []
        command_tokens: List[str] = []

        for token in tokens:
            if token == "|":
                if not command_tokens:
                    raise ValueError("Pipe encountered without preceding command.")
                self._append_command(command_seq, command_tokens)
                command_tokens = []
            else:
                command_tokens.append(token)

        if not command_tokens:
            raise ValueError("Pipeline ends with a pipe without a following command.")

        self._append_command(command_seq, command_tokens)

        return ParsedCommands(command_seq=command_seq)
