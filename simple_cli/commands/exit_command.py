"""Exit command implementation for terminating the interpreter."""

from simple_cli.commands.command import Command
from simple_cli.exceptions.exit_exception import ExitError


class ExitCommand(Command):
    """Command implementation for terminating the interpreter."""

    def execute(self, _) -> int:
        """Execute exit command.

        Args:
            _: Ignored parameter (command requires no arguments)

        Raises:
            ExitException: Always raises to signal termination

        Returns:
            int: Never actually returns (method raises instead)
        """
        raise ExitError()
