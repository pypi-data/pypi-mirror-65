"""
Module to deal with environment variables.
"""
import os


class TemporalEnvironmentVariable(object):
    """ Context manager to create an environment variable to perform test with it.

    If environment variable already existed then former value is stored before
    setting the new one. Former value is restored when context manager is left.

    This context manager returns an instance that let you update env var value using
    its set_var method.
    """

    def __init__(self, name: str, value: str):
        """ Constructor for TemporalEnvironmentVariable.

        :param name: Name of environment variable.
        :param value: Value that environment variable should have.
        """
        self.old_value = os.getenv(name, default=None)
        self.name = name
        self.value = ""
        self.set_var(value)

    def __enter__(self):
            return self

    def __exit__(self, type, value, traceback):
        if self.old_value is not None:
            os.environ[self.name] = self.old_value

    def set_var(self, new_value: str) -> None:
        """ Set a new current value for env var.

        :param new_value: New value to store.
        :return:
        """
        os.environ[self.name] = new_value
        self.value = new_value
