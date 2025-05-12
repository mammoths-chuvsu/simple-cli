"""Tests for CLI command implementations using pytest."""

import os
import subprocess
import sys
import tempfile
from io import StringIO

import pytest

from simple_cli.commands import (
    CatCommand,
    DefaultCommand,
    EchoCommand,
    ExitCommand,
    GrepCommand,
    PwdCommand,
    WcCommand,
)
from simple_cli.commands.cd_command import CdCommand
from simple_cli.commands.ls_command import LsCommand
from simple_cli.environment import Environment
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


def test_grep_basic_pattern(tmp_path, capsys):
    file = tmp_path / "test.txt"
    file.write_text("apple\nbanana\ngrape\napple pie")
    parsed = MockParsedCommand("grep", ["apple", str(file)])
    cmd = GrepCommand()
    exit_code = cmd.execute(parsed, None, sys.stdout)
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "apple\n--\napple pie"


def test_grep_case_insensitive(tmp_path, capsys):
    file = tmp_path / "test.txt"
    file.write_text("Apple\nBANANA\ngrape\nAPPLE PIE")
    parsed = MockParsedCommand("grep", ["-i", "apple", str(file)])
    cmd = GrepCommand()
    exit_code = cmd.execute(parsed, None, sys.stdout)
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "Apple\n--\nAPPLE PIE"


def test_grep_whole_word(tmp_path, capsys):
    file = tmp_path / "test.txt"
    file.write_text("cat\ncategory\nconcatenate")
    parsed = MockParsedCommand("grep", ["-w", "cat", str(file)])
    cmd = GrepCommand()
    exit_code = cmd.execute(parsed, None, sys.stdout)
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "cat\n"


def test_grep_after_context(tmp_path, capsys):
    file = tmp_path / "test.txt"
    content = "line1\nmatch1\nline2\nline3\nmatch2\nline4"
    file.write_text(content)
    parsed = MockParsedCommand("grep", ["-A", "1", "match", str(file)])
    cmd = GrepCommand()
    exit_code = cmd.execute(parsed, None, sys.stdout)
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "match1\nline2\n--\nmatch2\nline4"


def test_grep_after_context_overlapping(tmp_path, capsys):
    file = tmp_path / "test.txt"
    content = "0\nmatch1\n2\nmatch2\n4\n5"
    file.write_text(content)
    parsed = MockParsedCommand("grep", ["-A", "2", "match", str(file)])
    cmd = GrepCommand()
    exit_code = cmd.execute(parsed, None, sys.stdout)
    captured = capsys.readouterr()
    expected = "match1\n2\nmatch2\n4\n5"
    assert exit_code == 0
    assert captured.out == expected


def test_grep_invalid_regex(tmp_path, capsys):
    file = tmp_path / "test.txt"
    file.write_text("test")
    parsed = MockParsedCommand("grep", ["a(b", str(file)])
    cmd = GrepCommand()
    exit_code = cmd.execute(parsed, None, sys.stdout)
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Regex error" in captured.out


def test_grep_invalid_after_context_value(capsys):
    parsed = MockParsedCommand("grep", ["-A", "two", "pattern", "file.txt"])
    cmd = GrepCommand()
    exit_code = cmd.execute(parsed, None, sys.stdout)
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Error" in captured.out


def test_grep_after_context_merged_intervals(tmp_path, capsys):
    content = ["match1", "line1", "line2", "match2", "line4", "line5"]
    file = tmp_path / "test.txt"
    file.write_text("\n".join(content))
    parsed = MockParsedCommand("grep", ["-A", "2", "match", str(file)])
    cmd = GrepCommand()
    exit_code = cmd.execute(parsed, None, sys.stdout)
    captured = capsys.readouterr()
    expected = "match1\nline1\nline2\nmatch2\nline4\nline5"
    assert exit_code == 0
    assert captured.out == expected


def test_grep_after_context_separate_blocks(tmp_path, capsys):
    content = ["match1", "line1", "line2", "line3", "match2", "line5"]
    file = tmp_path / "test.txt"
    file.write_text("\n".join(content))
    parsed = MockParsedCommand("grep", ["-A", "1", "match", str(file)])
    cmd = GrepCommand()
    exit_code = cmd.execute(parsed, None, sys.stdout)
    captured = capsys.readouterr()
    expected = "match1\nline1\n--\nmatch2\nline5"
    assert exit_code == 0
    assert captured.out == expected


def test_grep_file_not_found(capsys):
    parsed = MockParsedCommand("grep", ["pattern", "nonexistent.txt"])
    cmd = GrepCommand()
    exit_code = cmd.execute(parsed, None, sys.stdout)
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "File error" in captured.out


def test_grep_empty_file(tmp_path, capsys):
    file = tmp_path / "empty.txt"
    file.write_text("")
    parsed = MockParsedCommand("grep", ["pattern", str(file)])
    cmd = GrepCommand()
    exit_code = cmd.execute(parsed, None, sys.stdout)
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == ""


def test_grep_pattern_not_found(tmp_path, capsys):
    file = tmp_path / "test.txt"
    file.write_text("line1\nline2")
    parsed = MockParsedCommand("grep", ["notfound", str(file)])
    cmd = GrepCommand()
    exit_code = cmd.execute(parsed, None, sys.stdout)
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == ""


def test_grep_after_context_exceeds_file(tmp_path, capsys):
    content = ["line1", "match", "line3"]
    file = tmp_path / "test.txt"
    file.write_text("\n".join(content))
    parsed = MockParsedCommand("grep", ["-A", "5", "match", str(file)])
    cmd = GrepCommand()
    exit_code = cmd.execute(parsed, None, sys.stdout)
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "match\nline3"


def test_cd_no_argument():
    Environment()
    cmd = CdCommand()
    parsed = MockParsedCommand("cd", [])
    cmd.execute(parsed, None, StringIO())
    assert os.getcwd() == os.path.expanduser("~")


def test_cd_with_argument(tmp_path):
    Environment()
    cmd = CdCommand()
    parsed = MockParsedCommand("cd", [str(tmp_path)])
    cmd.execute(parsed, None, StringIO())
    assert os.getcwd() == str(tmp_path)


def test_cd_invalid_directory():
    cmd = CdCommand()
    parsed = MockParsedCommand("cd", ["nonexistent_directory"])
    result = cmd.execute(parsed, None, StringIO())
    assert result == 1


def test_cd_affects_other_commands(tmp_path):
    cd_cmd = CdCommand()
    parsed_cd = MockParsedCommand("cd", [str(tmp_path)])
    cd_cmd.execute(parsed_cd, None, StringIO())

    pwd_cmd = PwdCommand()
    parsed_pwd = MockParsedCommand("pwd", [])
    output = StringIO()
    pwd_cmd.execute(parsed_pwd, None, output)
    result = output.getvalue().strip()

    assert result == str(tmp_path)


def test_cd_then_default_command_sees_new_cwd(tmp_path):
    cd_cmd = CdCommand()
    parsed_cd = MockParsedCommand("cd", [str(tmp_path)])
    cd_cmd.execute(parsed_cd, None, StringIO())

    test_file = tmp_path / "hi.txt"
    test_file.write_text("Hello from new dir")

    cmd = DefaultCommand()
    parsed = MockParsedCommand("cat", ["hi.txt"])

    with tempfile.TemporaryFile(mode="w+", encoding="utf-8") as tmp_out:
        result = cmd.execute(parsed, None, tmp_out)
        tmp_out.seek(0)
        output = tmp_out.read()

    assert result == 0
    assert "Hello from new dir" in output


def test_ls_no_argument(tmp_path):
    os.mkdir(tmp_path / "dir1")
    os.mkdir(tmp_path / "dir2")

    cmd = LsCommand()
    parsed = MockParsedCommand("ls", [str(tmp_path)])
    output = StringIO()

    cmd.execute(parsed, None, output)
    content = output.getvalue()

    assert "dir1" in content
    assert "dir2" in content


def test_ls_with_argument(tmp_path):
    os.mkdir(tmp_path / "dir1")
    os.mkdir(tmp_path / "dir2")
    cmd = LsCommand()
    parsed = MockParsedCommand("ls", [str(tmp_path)])
    output = StringIO()
    cmd.execute(parsed, None, output)
    content = output.getvalue()
    assert "dir1" in content
    assert "dir2" in content
