"""Tests for CLI command implementations using pytest."""

import os
import subprocess
import sys

import pytest

from simple_cli.commands import (
    CatCommand,
    DefaultCommand,
    EchoCommand,
    ExitCommand,
    PwdCommand,
    WcCommand,
)
from simple_cli.exceptions.exit_exception import ExitError


class MockParsedCommand:
    def __init__(self, command: str, args: list):
        self.name = command
        self.args = args


def test_echo_command(capsys):
    cmd = EchoCommand()
    parsed = MockParsedCommand("echo", ["Hello", "World"])
    assert cmd.execute(parsed, sys.stdin, sys.stdout) == 0
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello World"


def test_cat_command_success(tmp_path, capsys):
    file = tmp_path / "test.txt"
    file.write_text("Line1\nLine2\nLine3")

    cmd = CatCommand()
    parsed = MockParsedCommand("cat", [str(file)])
    assert cmd.execute(parsed, sys.stdin, sys.stdout) == 0
    assert "Line1\nLine2\nLine3" in capsys.readouterr().out


def test_cat_command_failure(capsys):
    cmd = CatCommand()
    parsed = MockParsedCommand("cat", ["nonexistent.txt"])
    assert cmd.execute(parsed, sys.stdin, sys.stdout) == 1
    captured = capsys.readouterr()
    assert "Error" in captured.out


def test_wc_command_success(tmp_path, capsys):
    file = tmp_path / "test.txt"
    content = "Hello\nWorld\n"
    file.write_text(content)
    expected_bytes = len(content.encode("utf-8"))

    cmd = WcCommand()
    parsed = MockParsedCommand("wc", [str(file)])
    assert cmd.execute(parsed, sys.stdin, sys.stdout) == 0

    output = capsys.readouterr().out.strip()
    assert output == f"2 2 {expected_bytes}"


def test_pwd_command(capsys):
    cmd = PwdCommand()
    parsed = MockParsedCommand("pwd", [])
    assert cmd.execute(parsed, sys.stdin, sys.stdout) == 0
    assert os.getcwd() in capsys.readouterr().out.strip()


def test_exit_command():
    cmd = ExitCommand()
    parsed = MockParsedCommand("exit", [])
    with pytest.raises(ExitError):
        cmd.execute(parsed, sys.stdin, sys.stdout)


def test_default_command_success(capsys):
    cmd = DefaultCommand()
    parsed = MockParsedCommand("echo", ["test"])
    in_pipe, out_pipe = os.pipe()
    stdout = os.fdopen(out_pipe, "w")
    assert cmd.execute(parsed, subprocess.DEVNULL, stdout) == 0
    stdin = os.fdopen(in_pipe, "r")
    stdout.close()
    assert "test" in stdin.read().strip()


def test_default_command_not_found(capsys):
    cmd = DefaultCommand()
    parsed = MockParsedCommand("nonexistent_command", [])
    in_pipe, out_pipe = os.pipe()
    stdout = os.fdopen(out_pipe, "w")
    assert cmd.execute(parsed, subprocess.DEVNULL, stdout) == 127
    stdin = os.fdopen(in_pipe, "r")
    stdout.close()
    assert "Command not found" in stdin.read().strip()
