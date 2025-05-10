"""
E2E test suite for simple CLI interpreter application.
"""

import os
import tempfile
import unittest
from io import StringIO
from unittest.mock import patch

from simple_cli.controller import Controller
from simple_cli.exceptions.exit_exception import ExitException


class TestCLIE2E(unittest.TestCase):
    """E2E test case for CLI command processing."""

    def setUp(self):
        """Initialize test environment before each test."""
        self.controller = Controller()

        # Create temporary test file for cat/wc commands
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.write(b"Hello World\nLine 2\nLine 3")
        self.temp_file.close()

    def tearDown(self):
        """Clean up test environment after each test."""
        os.unlink(self.temp_file.name)

    def _execute_test_sequence(self, inputs, expected_outputs, expected_codes):
        """Execute command sequence and validate results.

        Args:
            inputs: List of command strings to execute
            expected_outputs: List of expected output fragments
            expected_codes: List of expected return codes
        """
        with (
            patch("sys.stdout", new=StringIO()) as fake_out,
            patch("builtins.input", side_effect=inputs),
        ):

            actual_codes = []
            for inp, exp_out in zip(inputs, expected_outputs):
                # Execute command through controller
                code = self.controller._execute_command(inp)
                actual_codes.append(code)

                # Verify command output
                self.assertIn(exp_out, fake_out.getvalue())
                fake_out.truncate(0)  # Clear buffer after each command

            # Verify all return codes
            self.assertEqual(actual_codes, expected_codes)

    def test_command_sequence(self):
        """Test sequence of valid command executions."""
        test_inputs = [
            f"echo Test String",
            f"cat {self.temp_file.name}",
            f"wc {self.temp_file.name}",
            "pwd",
            "ls -l",  # Test external command passthrough
            "exit",
        ]

        expected_outputs = [
            "Test String",
            "Hello World\nLine 2\nLine 3",
            "2 6 25",
            os.getcwd(),
            "",  # ls output varies by system, not validated
            "",  # No output expected for exit
        ]

        expected_codes = [0, 0, 0, 0, 0, 0]  # echo  # cat  # wc  # pwd  # ls  # exit

        # Handle expected exit exception
        with self.assertRaises(ExitException):
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


if __name__ == "__main__":
    unittest.main()
