import pytest

from simple_cli.parser import ParsedCommand, ParsedCommands, Parser


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


def test_parse_single_pipeline(parser):
    command = "cat file.txt | grep pattern"
    expected = ParsedCommands(
        command_seq=[
            ParsedCommand(name="cat", args=["file.txt"]),
            ParsedCommand(name="grep", args=["pattern"]),
        ]
    )
    result = parser.parse(command)
    assert result == expected


def test_parse_multiple_pipelines(parser):
    command = "cat file.txt | grep pattern | wc -l"
    expected = ParsedCommands(
        command_seq=[
            ParsedCommand(name="cat", args=["file.txt"]),
            ParsedCommand(name="grep", args=["pattern"]),
            ParsedCommand(name="wc", args=["-l"]),
        ]
    )
    result = parser.parse(command)
    assert result == expected


def test_parse_pipeline_with_quotes(parser):
    command = "echo 'Hello | World' | grep 'Hello |'"
    expected = ParsedCommands(
        command_seq=[
            ParsedCommand(name="echo", args=["Hello | World"]),
            ParsedCommand(name="grep", args=["Hello |"]),
        ]
    )
    result = parser.parse(command)
    assert result == expected


def test_parse_pipeline_with_double_quotes(parser):
    command = 'echo "Hello | World" | grep "Hello |"'
    expected = ParsedCommands(
        command_seq=[
            ParsedCommand(name="echo", args=["Hello | World"]),
            ParsedCommand(name="grep", args=["Hello |"]),
        ]
    )
    result = parser.parse(command)
    assert result == expected


def test_parse_pipeline_with_spaces(parser):
    command = "  cat file.txt  |  grep pattern  |  wc -l  "
    expected = ParsedCommands(
        command_seq=[
            ParsedCommand(name="cat", args=["file.txt"]),
            ParsedCommand(name="grep", args=["pattern"]),
            ParsedCommand(name="wc", args=["-l"]),
        ]
    )
    result = parser.parse(command)
    assert result == expected


def test_parse_pipeline_starts_with_pipe(parser):
    command = "| cat file.txt"
    with pytest.raises(ValueError):
        parser.parse(command)


def test_parse_pipeline_ends_with_pipe(parser):
    command = "cat file.txt |"
    with pytest.raises(ValueError):
        parser.parse(command)


def test_parse_empty_command_between_pipes(parser):
    command = "cat file.txt | | grep pattern"
    with pytest.raises(ValueError):
        parser.parse(command)


def test_parse_pipeline_with_empty_string(parser):
    command = ""
    with pytest.raises(ValueError):
        parser.parse(command)


def test_parse_pipeline_with_only_spaces(parser):
    command = "   "
    with pytest.raises(ValueError):
        parser.parse(command)


def test_parse_pipeline_with_special_chars(parser):
    command = r"echo $HOME | grep '^/'"
    expected = ParsedCommands(
        command_seq=[
            ParsedCommand(name="echo", args=[r"$HOME"]),
            ParsedCommand(name="grep", args=[r"^/"]),
        ]
    )
    result = parser.parse(command)
    assert result == expected


def test_parse_complex_pipeline(parser):
    command = "ls -la | grep '^.d' | sort -r | head -n 5"
    expected = ParsedCommands(
        command_seq=[
            ParsedCommand(name="ls", args=["-la"]),
            ParsedCommand(name="grep", args=["^.d"]),
            ParsedCommand(name="sort", args=["-r"]),
            ParsedCommand(name="head", args=["-n", "5"]),
        ]
    )
    result = parser.parse(command)
    assert result == expected
