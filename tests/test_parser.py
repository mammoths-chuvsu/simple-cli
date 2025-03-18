import pytest

from simple_cli.parser import ParsedCommand, Parser


@pytest.fixture
def parser():
    return Parser()


def test_parse_cat_command(parser):
    command = "cat filename.txt"
    expected = ParsedCommand(name="cat", args=["filename.txt"])
    result = parser.parse(command).command_seq[0]
    assert result == expected


def test_parse_echo_command(parser):
    command = "echo 'Hello World'"
    expected = ParsedCommand(name="echo", args=["Hello World"])
    result = parser.parse(command).command_seq[0]
    assert result == expected


def test_parse_wc_command(parser):
    command = "wc filename.txt"
    expected = ParsedCommand(name="wc", args=["filename.txt"])
    result = parser.parse(command).command_seq[0]
    assert result == expected


def test_parse_pwd_command(parser):
    command = "pwd"
    expected = ParsedCommand(name="pwd", args=[])
    result = parser.parse(command).command_seq[0]
    assert result == expected


def test_parse_exit_command(parser):
    command = "exit"
    expected = ParsedCommand(name="exit", args=[])
    result = parser.parse(command).command_seq[0]
    assert result == expected


def test_parse_unknown_command(parser):
    command = "unknown_command 'some argument'"
    expected = ParsedCommand(name="unknown_command", args=["some argument"])
    result = parser.parse(command).command_seq[0]
    assert result == expected


def test_parse_double_quoted_argument(parser):
    command = 'echo "Double quoted argument"'
    expected = ParsedCommand(name="echo", args=["Double quoted argument"])
    result = parser.parse(command).command_seq[0]
    assert result == expected


def test_parse_single_quoted_argument(parser):
    command = "echo 'Single quoted argument'"
    expected = ParsedCommand(name="echo", args=["Single quoted argument"])
    result = parser.parse(command).command_seq[0]
    assert result == expected
