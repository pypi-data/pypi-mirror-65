"""Main module."""

import random
import string


def generate_random_string(length):
    symbols = string.digits + string.ascii_letters
    return "".join([random.choice(symbols) for _ in range(length)])
