"""Parser class implementation."""

import re
import shlex
from typing import List

from pydantic import BaseModel

from simple_cli.environment import Environment
from simple_cli.exceptions.empty_command_error import EmptyCommandError


class ParsedCommand(BaseModel):
    """Represents a parsed command with its name and a list of arguments."""

    name: str
    args: List[str]


class ParsedCommands(BaseModel):
    """Represents a sequence of parsed commands."""

    command_seq: List[ParsedCommand]


class Parser(BaseModel):
    """Parser class to tokenize and parse command line strings."""

    def _substitute(self, line: str, env: Environment) -> str:
        return re.sub(
            r"\$([A-Za-z_][A-Za-z0-9_]*)", lambda m: env.get(m.group(1)), line
        )

    def _append_command(
        self, command_seq: List[ParsedCommand], command_tokens: List[str]
    ):
        command_seq.append(
            ParsedCommand(
                name=command_tokens[0],
                args=command_tokens[1:],
            )
        )

    def parse(self, line: str, env: Environment) -> ParsedCommands:
        """Parse a line of command string into ParsedCommands.

        Args:
            line (str): The command line string to parse.

        Returns:
            ParsedCommands: An object containing a sequence of parsed commands.
        """
        tokens = shlex.split(self._substitute(line, env))

        if not tokens:
            raise EmptyCommandError()

        command_seq: List[ParsedCommand] = []
        command_tokens: List[str] = []
        is_assignment_mode = True

        for token in tokens:
            if is_assignment_mode and "=" in token and token.count("=") == 1:
                var, value = token.split("=", 1)
                if token.startswith("="):
                    raise ValueError(f"Invalid assignment: {token}")
                var, value = token.split("=", 1)
                if not var.isidentifier():
                    raise ValueError(f"Invalid variable name: {var}")
                if command_tokens:
                    self._append_command(command_seq, command_tokens)
                    command_tokens = []
                command_tokens = ["=", var, value]
                continue
            is_assignment_mode = False
            if token == "|":
                if not command_tokens:
                    raise ValueError("Pipe encountered without preceding command.")
                self._append_command(command_seq, command_tokens)
                command_tokens = []
                is_assignment_mode = True
            else:
                if command_tokens and command_tokens[0] == "=":
                    self._append_command(command_seq, command_tokens)
                command_tokens.append(token)

        if not command_tokens:
            raise ValueError("Pipeline ends with a pipe without a following command.")

        self._append_command(command_seq, command_tokens)

        return ParsedCommands(command_seq=command_seq)
