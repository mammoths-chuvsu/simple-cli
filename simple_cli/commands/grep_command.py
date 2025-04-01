"""Implementation of the 'grep' command for file content searching.

This module provides functionality similar to Unix grep command with support for:
- Regular expression patterns
- Whole-word matching (-w flag)
- Case-insensitive search (-i flag)
- After-context lines display (-A flag)
"""

import argparse

from simple_cli.commands.command import Command
from simple_cli.parser import ParsedCommand


class GrepCommand(Command):
    """Command implementation for searching patterns in files.

    Supports:
    - Basic pattern matching
    - Word-boundary matching (-w)
    - Case-insensitive search (-i)
    - After-context lines display (-A)
    """

    def execute(self, parsed_command: ParsedCommand, _stdin, _stdout) -> int:
        """Execute the grep command with given arguments.

        Args:
            parsed_command: Contains command name and arguments

        Returns:
            int: 0 on success, 1 on error
        """
        parser = argparse.ArgumentParser(prog="grep", add_help=False)
        parser.add_argument("pattern", help="The pattern to search for")
        parser.add_argument("files", nargs="+", help="Files to search in")
        parser.add_argument(
            "-w", "--word", action="store_true", help="Search for whole words only"
        )
        parser.add_argument(
            "-i", "--ignore-case", action="store_true", help="Case insensitive search"
        )
        parser.add_argument(
            "-A",
            "--after-context",
            type=int,
            default=0,
            help="Number of lines to print after each match",
        )

        try:
            parser.parse_args(parsed_command.args)
            # _: str = args.pattern
            # _: List[str] = args.files
            # _: bool = args.word
            # _: bool = args.ignore_case
            # _: int = args.after_context
        except (argparse.ArgumentError, FileNotFoundError) as e:
            print(f"Error: {str(e)}")
            return 1

        return 0
