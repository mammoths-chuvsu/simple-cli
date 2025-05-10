"""
E2E test suite for simple CLI interpreter application.
"""

import os
import sys
import tempfile
import unittest
from io import StringIO
from unittest.mock import patch

from simple_cli.controller import Controller
from simple_cli.exceptions.exit_exception import ExitError


class TestCLIE2E(unittest.TestCase):
    """E2E test case for CLI command processing."""

    def setUp(self):
        """Initialize test environment before each test."""
        self.controller = Controller()
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()

        # Create temporary test file for cat/wc commands
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.write(b"Hello World\nLine 2\nLine 3")
        self.temp_file.close()

    def tearDown(self):
        """Clean up test environment after each test."""
        sys.stdout = self.original_stdout
        sys.stderr = self.original_stderr
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def _execute_and_capture(self, command):
        """Execute single command and capture output."""
        sys.stdout.truncate(0)
        sys.stdout.seek(0)
        sys.stderr.truncate(0)
        sys.stderr.seek(0)

        code = self.controller._execute_command(command)
        output = sys.stdout.getvalue() + sys.stderr.getvalue()
        return code, output.strip()

    def _execute_test_sequence(self, inputs, expected_outputs, expected_codes):
        """Execute command sequence and validate results."""
        actual_codes = []
        for inp, exp_out in zip(inputs, expected_outputs):
            code, output = self._execute_and_capture(inp)
            actual_codes.append(code)
            self.assertIn(exp_out, output)

        self.assertEqual(actual_codes, expected_codes)

    def test_command_sequence(self):
        """Test sequence of valid command executions."""
        test_inputs = [
            f"echo Test String",
            f"cat {self.temp_file.name}",
            f"wc {self.temp_file.name}",
            "pwd",
            "exit",
        ]

        expected_outputs = [
            "Test String",
            "Hello World\nLine 2\nLine 3",
            "2 6 25",
            os.getcwd(),
            "",
        ]

        expected_codes = [0, 0, 0, 0, 0]

        with self.assertRaises(ExitError):
            self._execute_test_sequence(test_inputs, expected_outputs, expected_codes)

    def test_non_zero_return_code_continuation(self):
        """Test command execution continues after non-zero return code."""
        test_inputs = [
            "cat non_existent_file.txt",  # Command with error
            "echo Success after failure",  # Next valid command
        ]

        expected_outputs = [
            "Error",  # Error message from cat
            "Success after failure",  # Success message from echo
        ]

        expected_codes = [1, 0]  # cat  # echo

        with patch("sys.stdout", new=StringIO()) as fake_out:
            actual_codes = []
            for inp, exp_out in zip(test_inputs, expected_outputs):
                code = self.controller._execute_command(inp)
                actual_codes.append(code)
                self.assertIn(exp_out, fake_out.getvalue())
                fake_out.truncate(0)

            self.assertEqual(actual_codes, expected_codes)

    def test_pipe_commands(self):
        """Test command chaining with pipes."""
        test_inputs = [f"echo 'Hello World' | echo 'Goodbye'", "exit"]  # Simple pipe

        expected_outputs = ["Goodbye", ""]

        expected_codes = [0, 0]

        with self.assertRaises(ExitError):
            self._execute_test_sequence(test_inputs, expected_outputs, expected_codes)

    def test_environment_variables(self):
        """Test environment variable expansion and persistence."""
        test_inputs = [
            "TEST_VAR=cli_env",
            "echo $TEST_VAR",  # Simple variable expansion
            "exit",
        ]

        expected_outputs = ["", "cli_env", ""]

        expected_codes = [0, 0, 0]

        with self.assertRaises(ExitError):
            self._execute_test_sequence(test_inputs, expected_outputs, expected_codes)


if __name__ == "__main__":
    unittest.main()
