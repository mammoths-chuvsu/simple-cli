"""Executor class implementation."""

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
        for command in parsed_commands.command_seq:
            command_executor = self._command_storage.get_command(command.name)
            result_code = command_executor.execute(command)
        return result_code
