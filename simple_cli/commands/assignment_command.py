"""Implementation of assignment command to handle environment variable assignments."""

from simple_cli.commands.command import Command
from simple_cli.environment import Environment


class AssignmentCommand(Command):
    """Handles variable assignment operations in the format VAR=value.

    Inherits from the base Command class and implements logic to parse
    and execute variable assignment commands.
    """

    def __init__(self, env: Environment):
        """Initialize the AssignmentCommand with an environment instance.

        Args:
            env: Environment instance where variables will be stored
        """
        self._env = env

    def execute(self, parsed_command) -> int:
        """Execute the variable assignment operation.

        Args:
            parsed_command: Parsed command containing variable name and value
                in args attribute. Expected format: ["var_name", "value"]

        Returns:
            int: Status code (0 - success, 1 - error)

        Raises:
            ValueError: If arguments format is invalid
        """
        if len(parsed_command.args) != 2:
            return 1

        var = parsed_command.args[0]
        value = parsed_command.args[1]
        self._env.set(var, value)
        return 0
