import random
import string


def random_string(len: int) -> str:
    """ Generate a _random string of desired length.

    :param len: Desired character length for generated string.
    :return: Generated _random string.
    """
    alphanumeric_alphabet = ''.join([string.ascii_letters, string.digits])
    generated_string = ''.join(random.choice(alphanumeric_alphabet) for _ in range(len))
    return generated_string
