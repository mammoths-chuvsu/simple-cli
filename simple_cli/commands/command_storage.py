"""Command storage implementation for mapping command names to executors."""

from simple_cli.commands import (
    AssignmentCommand,
    CatCommand,
    Command,
    DefaultCommand,
    EchoCommand,
    ExitCommand,
    PwdCommand,
    WcCommand,
)
from simple_cli.environment import Environment


class CommandStorage:
    """Registry for mapping command names to implementations."""

    def __init__(self, env: Environment):
        """Initialize command registry with built-in commands.

        Args:
            env: Environment instance to be used for variable assignments
        """
        self._commands = {
            "echo": EchoCommand(),
            "cat": CatCommand(),
            "wc": WcCommand(),
            "pwd": PwdCommand(),
            "exit": ExitCommand(),
            "=": AssignmentCommand(env),
        }

    def get_command(self, name: str) -> Command:
        """Retrieve command implementation by name.

        Args:
            name: Command name to look up

        Returns:
            Command:
                Concrete command implementation if found,
                DefaultCommand implementation otherwise
        """
        return self._commands.get(name, DefaultCommand())
