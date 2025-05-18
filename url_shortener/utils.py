from django.conf import settings
import string

ALPHABET: str = string.digits + string.ascii_letters
BASE: int = len(ALPHABET)


def base62_encode(n: int) -> str:
    """
    Encode a non-negative integer to a base62 string.

    Args:
        n (int): The integer to encode. Must be non-negative.

    Returns:
        str: The base62 encoded string.
    """
    if n == 0:
        return ALPHABET[0]
    s = []
    while n:
        s.append(ALPHABET[n % BASE])
        n //= BASE
    return "".join(reversed(s))


def base62_decode(s: str) -> int:
    """
    Decode a base62 string to an integer.

    Args:
        s (str): The base62 encoded string.

    Returns:
        int: The decoded integer.
    """
    n = 0
    for char in s:
        n = n * BASE + ALPHABET.index(char)
    return n


def encode_id(id: int) -> str:
    """
    Encode an integer ID by XORing it with a secret pepper and then base62 encoding it.

    Args:
        id (int): The integer ID to encode.

    Returns:
        str: The encoded string.
    """
    return base62_encode(id ^ settings.URL_PEPPER)


def decode_code(code: str) -> int:
    """
    Decode a base62 encoded string by decoding it and then XORing with the secret pepper.

    Args:
        code (str): The base62 encoded string to decode.

    Returns:
        int: The original integer ID.
    """
    return base62_decode(code) ^ settings.URL_PEPPER
