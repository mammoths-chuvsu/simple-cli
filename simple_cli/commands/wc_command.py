"""Implementation of the 'wc' command for file statistics analysis."""

import os

from simple_cli.commands.command import Command


class WcCommand(Command):
    """Command implementation for word count statistics."""

    def execute(self, parsed_command, _stdin, stdout) -> int:
        """Execute wc command.

        Args:
            parsed_command: Object containing command components. Must have:
                - args[0]: Path to target file for analysis

        Returns:
            int: 0 on success, 1 on file handling errors
        """
        try:
            file_path = parsed_command.args[0]
            with open(file_path, "r") as f:
                content = f.read()
                lines = content.count("\n")
                words = len(content.split())
                bytes = os.path.getsize(file_path)
                print(f"{lines} {words} {bytes}", file=stdout)
            return 0
        except Exception as e:
            print(f"Error: {e}", file=stdout)
            return 1
