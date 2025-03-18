"""Definition of the abstract base command for CLI command implementations."""

from abc import ABC, abstractmethod


class Command(ABC):
    """Abstract base class for all command implementations."""

    @abstractmethod
    def execute(self, parsed_command) -> int:
        """Execute the command logic.

        Args:
            parsed_command: Contains parsed command name and arguments

        Returns:
            int: Exit status code (0 for success, non-zero for errors)
        """
