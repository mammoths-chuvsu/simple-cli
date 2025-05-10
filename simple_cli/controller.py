"""Controller class implementation."""

from simple_cli.exceptions.exit_exception import ExitException
from simple_cli.executor import Executor
from simple_cli.parser import Parser


class Controller:
    """The Controller class orchestrates the parsing and execution."""

    def __init__(self):
        """Initialize the Controller with Parser and Executor instance."""
        self._parser = Parser()
        self._executor = Executor()

    def run(self):
        """Run main loop of program.

        Continuously reads commands from user input, parses them,
        and executes them.
        The loop exits gracefully when an ExitException is raised.
        """
        while True:
            try:
                command = input(">>> ")
                self._execute_command(command)
            except ExitException:
                break

    def _execute_command(self, command: str) -> int:
        """Parse and execute a given command.

        Args:
            command (str): The command string to be parsed and executed.

        Returns:
            int: The result code from the executed command.
        """
        parsed = self._parser.parse(command)
        return self._executor.execute(parsed)
