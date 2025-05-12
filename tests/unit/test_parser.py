import pytest

from simple_cli.environment import Environment
from simple_cli.exceptions.empty_command_error import EmptyCommandError
from simple_cli.parser import ParsedCommand, ParsedCommands, Parser


@pytest.fixture
def env():
    return Environment()


@pytest.fixture
def parser():
    return Parser()


def test_parse_cat_command(parser, env):
    command = "cat filename.txt"
    expected = ParsedCommand(name="cat", args=["filename.txt"])
    result = parser.parse(command, env).command_seq[0]
    assert result == expected


def test_parse_echo_command(parser, env):
    command = "echo 'Hello World'"
    expected = ParsedCommand(name="echo", args=["Hello World"])
    result = parser.parse(command, env).command_seq[0]
    assert result == expected


def test_parse_wc_command(parser, env):
    command = "wc filename.txt"
    expected = ParsedCommand(name="wc", args=["filename.txt"])
    result = parser.parse(command, env).command_seq[0]
    assert result == expected


def test_parse_pwd_command(parser, env):
    command = "pwd"
    expected = ParsedCommand(name="pwd", args=[])
    result = parser.parse(command, env).command_seq[0]
    assert result == expected


def test_parse_exit_command(parser, env):
    command = "exit"
    expected = ParsedCommand(name="exit", args=[])
    result = parser.parse(command, env).command_seq[0]
    assert result == expected


def test_parse_unknown_command(parser, env):
    command = "unknown_command 'some argument'"
    expected = ParsedCommand(name="unknown_command", args=["some argument"])
    result = parser.parse(command, env).command_seq[0]
    assert result == expected


def test_parse_double_quoted_argument(parser, env):
    command = 'echo "Double quoted argument"'
    expected = ParsedCommand(name="echo", args=["Double quoted argument"])
    result = parser.parse(command, env).command_seq[0]
    assert result == expected


def test_parse_single_quoted_argument(parser, env):
    command = "echo 'Single quoted argument'"
    expected = ParsedCommand(name="echo", args=["Single quoted argument"])
    result = parser.parse(command, env).command_seq[0]
    assert result == expected


def test_parse_single_pipeline(parser, env):
    command = "cat file.txt | grep pattern"
    expected = ParsedCommands(
        command_seq=[
            ParsedCommand(name="cat", args=["file.txt"]),
            ParsedCommand(name="grep", args=["pattern"]),
        ]
    )
    result = parser.parse(command, env)
    assert result == expected


def test_parse_multiple_pipelines(parser, env):
    command = "cat file.txt | grep pattern | wc -l"
    expected = ParsedCommands(
        command_seq=[
            ParsedCommand(name="cat", args=["file.txt"]),
            ParsedCommand(name="grep", args=["pattern"]),
            ParsedCommand(name="wc", args=["-l"]),
        ]
    )
    result = parser.parse(command, env)
    assert result == expected


def test_parse_pipeline_with_quotes(parser, env):
    command = "echo 'Hello | World' | grep 'Hello |'"
    expected = ParsedCommands(
        command_seq=[
            ParsedCommand(name="echo", args=["Hello | World"]),
            ParsedCommand(name="grep", args=["Hello |"]),
        ]
    )
    result = parser.parse(command, env)
    assert result == expected


def test_parse_pipeline_with_double_quotes(parser, env):
    command = 'echo "Hello | World" | grep "Hello |"'
    expected = ParsedCommands(
        command_seq=[
            ParsedCommand(name="echo", args=["Hello | World"]),
            ParsedCommand(name="grep", args=["Hello |"]),
        ]
    )
    result = parser.parse(command, env)
    assert result == expected


def test_parse_pipeline_with_spaces(parser, env):
    command = "  cat file.txt  |  grep pattern  |  wc -l  "
    expected = ParsedCommands(
        command_seq=[
            ParsedCommand(name="cat", args=["file.txt"]),
            ParsedCommand(name="grep", args=["pattern"]),
            ParsedCommand(name="wc", args=["-l"]),
        ]
    )
    result = parser.parse(command, env)
    assert result == expected


def test_parse_pipeline_starts_with_pipe(parser, env):
    command = "| cat file.txt"
    with pytest.raises(ValueError):
        parser.parse(command, env)


def test_parse_pipeline_ends_with_pipe(parser, env):
    command = "cat file.txt |"
    with pytest.raises(ValueError):
        parser.parse(command, env)


def test_parse_empty_command_between_pipes(parser, env):
    command = "cat file.txt | | grep pattern"
    with pytest.raises(ValueError):
        parser.parse(command, env)


def test_parse_pipeline_with_empty_string(parser, env):
    command = ""
    with pytest.raises(EmptyCommandError):
        parser.parse(command, env)


def test_parse_pipeline_with_only_spaces(parser, env):
    command = "   "
    with pytest.raises(EmptyCommandError):
        parser.parse(command, env)


def test_parse_pipeline_with_special_chars(parser, env):
    env.set("HOME", "home")
    command = r"echo $HOME | grep '^/'"
    expected = ParsedCommands(
        command_seq=[
            ParsedCommand(name="echo", args=[r"home"]),
            ParsedCommand(name="grep", args=[r"^/"]),
        ]
    )
    result = parser.parse(command, env)
    assert result == expected


def test_parse_complex_pipeline(parser, env):
    command = "ls -la | grep '^.d' | sort -r | head -n 5"
    expected = ParsedCommands(
        command_seq=[
            ParsedCommand(name="ls", args=["-la"]),
            ParsedCommand(name="grep", args=["^.d"]),
            ParsedCommand(name="sort", args=["-r"]),
            ParsedCommand(name="head", args=["-n", "5"]),
        ]
    )
    result = parser.parse(command, env)
    assert result == expected


def test_parse_single_assignment(parser, env):
    command = "x=1"
    expected = ParsedCommands(
        command_seq=[
            ParsedCommand(name="=", args=["x", "1"]),
        ]
    )
    result = parser.parse(command, env)
    assert result == expected


def test_parse_multiple_assignments(parser, env):
    command = "x=1 y=2"
    expected = ParsedCommands(
        command_seq=[
            ParsedCommand(name="=", args=["x", "1"]),
            ParsedCommand(name="=", args=["y", "2"]),
        ]
    )
    result = parser.parse(command, env)
    assert result == expected


def test_parse_invalid_assignment_format(parser, env):
    command = "=value"
    with pytest.raises(ValueError):
        parser.parse(command, env)


def test_parse_assignment_without_value(parser, env):
    command = "VAR="
    expected = ParsedCommands(
        command_seq=[
            ParsedCommand(name="=", args=["VAR", ""]),
        ]
    )
    result = parser.parse(command, env)
    assert result == expected


def test_parse_assignment_with_special_chars(parser, env):
    command = "FILE=test_$HOME.txt"
    expected = ParsedCommands(
        command_seq=[
            ParsedCommand(name="=", args=["FILE", f"test_{env.get('HOME')}.txt"]),
        ]
    )
    result = parser.parse(command, env)
    assert result == expected


def test_parse_assignment_after_command(parser, env):
    command = "echo test x=1"
    expected = ParsedCommands(
        command_seq=[
            ParsedCommand(name="echo", args=["test", "x=1"]),
        ]
    )
    result = parser.parse(command, env)
    assert result == expected

def test_parse_cd_command(parser, env):
    command = "cd /home/user"
    expected = ParsedCommand(name="cd", args=["/home/user"])
    result = parser.parse(command, env).command_seq[0]
    assert result == expected

def test_parse_ls_command(parser, env):
    command = "ls /home/user"
    expected = ParsedCommand(name="ls", args=["/home/user"])
    result = parser.parse(command, env).command_seq[0]
    assert result == expected
