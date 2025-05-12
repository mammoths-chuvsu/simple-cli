import os
from simple_cli.commands.command import Command

class LsCommand(Command):
    """Command implementation for listing directory contents."""
    
    def execute(self, parsed_command, _stdin, stdout) -> int:
        """Execute ls command.
        
        Args:
            parsed_command: Parsed command with the directory path (if provided).
        
        Returns:
            int: 0 on success, 1 on failure.
        """
        try:
            if len(parsed_command.args) == 0:
                # List contents of the current directory if no argument is provided
                target_dir = os.getcwd()
            elif len(parsed_command.args) == 1:
                # List contents of the specified directory
                target_dir = parsed_command.args[0]
            else:
                print("Usage: ls [dir]", file=stdout)
                return 1

            # List the contents of the directory
            contents = os.listdir(target_dir)
            for item in contents:
                print(item, file=stdout)
            return 0
        except Exception as e:
            print(f"Error: {e}", file=stdout)
            return 1
