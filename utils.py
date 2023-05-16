import uuid
import string
import random


def get_random_string(length: int) -> str:
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


def get_random_int(length: int) -> int:
    ones = int("1" * length)
    nines = int("9" * length)
    return random.randint(ones, nines)


def get_string_uuid() -> str:
    return str(uuid.uuid4())
