import os
import test_common._random.strings as random_strings
import test_common.system.env as system_env


def _get_not_existing_env_var_name() -> str:
    DESIRED_LENGTH = 10
    while os.getenv(new_var_name := random_strings.random_string(DESIRED_LENGTH)) is not None:
        continue
    return new_var_name


def test_not_previously_existing_environment_variable_creation():
    DESIRED_VALUE = "Hello"
    new_var_name = _get_not_existing_env_var_name()
    with system_env.TemporalEnvironmentVariable(new_var_name, DESIRED_VALUE):
        assert os.getenv(new_var_name) == DESIRED_VALUE


def test_previoously_existing_environment_variable_creation():
    OLD_VALUE = "Bye"
    DESIRED_VALUE = "Hello"
    # Create a previous env var.
    new_var_name = _get_not_existing_env_var_name()
    os.environ[new_var_name] = OLD_VALUE
    # Check we can store a new value.
    with system_env.TemporalEnvironmentVariable(new_var_name, DESIRED_VALUE):
        assert os.getenv(new_var_name) == DESIRED_VALUE
    # Check old value has been restored.
    assert os.getenv(new_var_name) == OLD_VALUE


def test_set_var():
    DESIRED_VALUE = "Hello"
    NEW_VALUE = "Hello world"
    # Give a previous value to env var.
    new_var_name = _get_not_existing_env_var_name()
    with system_env.TemporalEnvironmentVariable(new_var_name, DESIRED_VALUE) as temp_env_var:
        assert os.getenv(new_var_name) == DESIRED_VALUE
        # Update env var value.
        temp_env_var.set_var(NEW_VALUE)
        assert os.getenv(new_var_name) ==  NEW_VALUE



