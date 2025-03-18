"""Implementation of the command for external program execution."""

import subprocess

from simple_cli.commands.command import Command


class DefaultCommand(Command):
    """Fallback command implementation for external program execution."""

    def execute(self, parsed_command) -> int:
        """Execute external command via subprocess.

        Args:
            parsed_command: Structure containing:
                - command: Program name to execute
                - args: List of string arguments for the program

        Returns:
            int: Exit code from subprocess or 127 for command-not-found
        """
        try:
            result = subprocess.run(
                [parsed_command.command] + parsed_command.args,
                capture_output=True,
                text=True,
            )
            print(result.stdout)
            return result.returncode
        except FileNotFoundError:
            print(f"Command not found: {parsed_command.command}")
            return 127
