"""Executor class implementation."""

import os
import sys

from simple_cli.commands.command_storage import CommandStorage
from simple_cli.environment import Environment
from simple_cli.parser import ParsedCommands


class Executor:
    """Executor class to handle pipes and execute commands.

    The Executor class is responsible for executing a
    sequence of parsed commands using the available
    command implementations from CommandStorage.
    """

    def __init__(self, env: Environment):
        """Initialize the Executor with a CommandStorage instance."""
        self._command_storage = CommandStorage(env)

    def execute(self, parsed_commands: ParsedCommands) -> int:
        """Execute a sequence of parsed commands.

        Args:
            parsed_commands (ParsedCommands): A container of parsed
            commands to be executed.

        Returns:
            int: The result code from the last executed command.
        """
        result_code: int = 0
        prev_stdin = None
        num_commands = len(parsed_commands.command_seq)

    for idx, command in enumerate(parsed_commands.command_seq):
        command_executor = self._command_storage.get_command(command.name)

        # Create a pipe if there is a next command (i.e., setting up a pipeline)
        stdin_pipe, stdout_pipe = (
            os.pipe() if idx < num_commands - 1 else (None, None)
        )

        # Use previous stdout as stdin if available (from previous pipe output)
        stdin = os.fdopen(prev_stdin, "r") if prev_stdin is not None else sys.stdin

        # If this is not the last command, set up its stdout to a pipe
        stdout = (
            os.fdopen(stdout_pipe, "w") if stdout_pipe is not None else sys.stdout
        )
        result_code = command_executor.execute(command, stdin, stdout)

        # Save current input pipe to be used as input for next command
        prev_stdin = stdin_pipe

        return result_code
