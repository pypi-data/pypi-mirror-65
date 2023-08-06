import pytest

import test_common._random.strings as random_strings


@pytest.mark.strings
def test_random_string():
    DESIRED_LENGTH = 7
    generated_string = random_strings.random_string(DESIRED_LENGTH)
    generated_length = len(generated_string)
    assert DESIRED_LENGTH, generated_length

