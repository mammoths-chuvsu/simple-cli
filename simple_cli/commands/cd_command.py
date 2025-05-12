import os
from simple_cli.commands.command import Command
from simple_cli.environment import Environment

class CdCommand(Command):
    """Command implementation for changing the current directory."""
    
    def execute(self, parsed_command, _stdin, _stdout) -> int:
        """Execute cd command.
        
        Args:
            parsed_command: Parsed command with the directory path (if provided).
        
        Returns:
            int: 0 on success, 1 on failure.
        """
        try:
            if len(parsed_command.args) == 0:
                # Change to the user's home directory if no argument is provided
                target_dir = os.path.expanduser("~")
            elif len(parsed_command.args) == 1:
                # Change to the directory specified in args[0]
                target_dir = parsed_command.args[0]
            else:
                print("Usage: cd [dir]", file=_stdout)
                return 1
            
            # Attempt to change the directory
            os.chdir(target_dir)
            return 0
        except Exception as e:
            print(f"Error: {e}", file=_stdout)
            return 1
