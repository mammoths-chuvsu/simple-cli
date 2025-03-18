"""Implementation of the 'wc' command for file statistics analysis."""

import os

from simple_cli.commands.command import Command


class WcCommand(Command):
    """Command implementation for word count statistics."""

    def execute(self, parsed_command) -> int:
        """Execute wc command.

        Args:
            parsed_command: Object containing command components. Must have:
                - args[0]: Path to target file for analysis

        Returns:
            int: 0 on success, 1 on file handling errors
        """
        try:
            with open(parsed_command.args[0], "r") as f:
                content = f.read()
                lines = len(content.split("\n"))
                words = len(content.split())
                bytes = os.path.getsize(parsed_command.args[0])
                print(f"{lines} {words} {bytes}")
            return 0
        except Exception as e:
            print(f"Error: {e}")
            return 1
