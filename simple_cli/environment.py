"""Environment class implementation."""


class Environment:
    """Holds and manages environment variables for the shell.

    Attributes:
        _env_variables: Dictionary storing variable name-value pairs
    """

    def __init__(self):
        """Initialize the environment with empty variable storage."""
        self._env_variables = {}

    def get(self, var_name: str) -> str:
        """Get the value of an environment variable.

        Args:
            var_name: Name of the variable to retrieve

        Returns:
            Value of the variable or empty string if not found
        """
        return self._env_variables.get(var_name, "")

    def set(self, var_name: str, value: str) -> None:
        """Set the value of an environment variable.

        Args:
            var_name: Name of the variable to set
            value: Value to assign to the variable
        """
        self._env_variables[var_name] = value
