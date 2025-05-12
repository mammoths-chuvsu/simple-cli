"""Implementation of the 'cat' command for displaying file contents."""

from simple_cli.commands.command import Command


class CatCommand(Command):
    """Command implementation for printing file contents."""

    def execute(self, parsed_command, _stdin, stdout) -> int:
        """Execute cat command.

        Args:
            parsed_command: Object containing parsed arguments.
                Expected to have:
                - args[0]: filename to display

        Returns:
            int: 0 on success, 1 on file handling errors
        """
        try:
            with open(parsed_command.args[0], "r") as f:
                print(f.read(), file=stdout)
            return 0
        except Exception as e:
            print(f"Error: {e}", file=stdout)
            return 1
