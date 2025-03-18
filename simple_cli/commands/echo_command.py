"""Echo command implementation for outputting arguments to the console."""

from simple_cli.commands.command import Command


class EchoCommand(Command):
    """Command implementation for echoing arguments to stdout."""

    def execute(self, parsed_command) -> int:
        """Execute echo command.

        Args:
            parsed_command: Object containing command components. Must have:
                - args: Sequence of strings to concatenate and output

        Returns:
            int: Always returns 0 (success)
        """
        print(" ".join(parsed_command.args))
        return 0
