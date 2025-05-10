"""Implementation of the 'pwd' command to display working directory."""

import os

from simple_cli.commands.command import Command


class PwdCommand(Command):
    """Command implementation for printing working directory."""

    def execute(self, _) -> int:
        """Execute pwd command.

        Args:
            _: Ignored parameter (command requires no arguments)

        Returns:
            int: Always returns 0 (success)
        """
        print(os.getcwd())
        return 0
