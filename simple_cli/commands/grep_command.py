"""Implementation of the 'grep' command for file content searching.

This module provides functionality similar to Unix grep command with support for:
- Regular expression patterns
- Whole-word matching (-w flag)
- Case-insensitive search (-i flag)
- After-context lines display (-A flag)
"""

import argparse
import re

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

    def _parse_args(self, parsed_command: ParsedCommand):
        parser = argparse.ArgumentParser(
            prog="grep", add_help=False, exit_on_error=False
        )
        parser.add_argument("pattern", help="The pattern to search for")
        parser.add_argument("file", help="File to search in")
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

        args = parser.parse_args(parsed_command.args)
        return args

    def _merge_intervals(self, intervals):
        if not intervals:
            return []
        sorted_intervals = sorted(intervals, key=lambda x: x[0])
        merged = [sorted_intervals[0]]
        for current in sorted_intervals[1:]:
            last = merged[-1]
            if current[0] <= last[1] + 1:
                merged[-1] = (last[0], max(last[1], current[1]))
            else:
                merged.append(current)
        return merged

    def execute(self, parsed_command: ParsedCommand, _stdin, stdout) -> int:
        """Execute the grep command with given arguments.

        Args:
            parsed_command: Contains command name and arguments

        Returns:
            int: 0 on success, 1 on error
        """
        try:
            args = self._parse_args(parsed_command)
        except (argparse.ArgumentError, FileNotFoundError) as e:
            print(f"Error: {str(e)}", file=stdout)
            return 1

        pattern: str = args.pattern
        if args.word:
            pattern = r"\b{}\b".format(re.escape(pattern))

        flags = re.IGNORECASE if args.ignore_case else 0
        try:
            regex = re.compile(pattern, flags)
        except re.error as e:
            print(f"Regex error: {str(e)}", file=stdout)
            return 1

        try:
            with open(args.file, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except IOError as e:
            print(f"File error: {str(e)}", file=stdout)
            return 1

        matches = [idx for idx, line in enumerate(lines) if regex.search(line)]
        intervals = [(idx, idx + args.after_context) for idx in matches]
        merged = self._merge_intervals(intervals)

        output_lines = []
        first_interval = True
        for start, end in merged:
            if first_interval:
                first_interval = False
            else:
                output_lines.append("--\n")
            start = max(0, start)
            end = min(len(lines) - 1, end)
            output_lines.extend(lines[i] for i in range(start, end + 1))

        for line in output_lines:
            print(line, file=stdout, end="")

        return 0
