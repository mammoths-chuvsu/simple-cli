"""Definition of the abstract base command for CLI command implementations."""

from abc import ABC, abstractmethod
from typing import IO

from simple_cli.parser import ParsedCommand


class Command(ABC):
    """Abstract base class for all command implementations."""

    @abstractmethod
    def execute(
        self,
        parsed_command: ParsedCommand,
        stdin: IO,
        stdout: IO,
    ) -> int:
        """Execute the command logic.

        Args:
            parsed_command: Contains parsed command name and arguments

        Returns:
            int: Exit status code (0 for success, non-zero for errors)
        """
