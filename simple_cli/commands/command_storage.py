"""Command storage implementation for mapping command names to executors."""

from simple_cli.commands import (
    CatCommand,
    Command,
    DefaultCommand,
    EchoCommand,
    ExitCommand,
    PwdCommand,
    WcCommand,
)


class CommandStorage:
    """Registry for mapping command names to implementations."""

    def get_command(self, name: str) -> Command:
        """Retrieve command implementation by name.

        Args:
            name: Command name to look up

        Returns:
            Command:
                Concrete command implementation if found,
                DefaultCommand implementation otherwise
        """
        commands = {
            "echo": EchoCommand(),
            "cat": CatCommand(),
            "wc": WcCommand(),
            "pwd": PwdCommand(),
            "exit": ExitCommand(),
        }
        return commands.get(name, DefaultCommand())
