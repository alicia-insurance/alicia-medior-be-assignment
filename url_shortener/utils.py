"""
Utility functions for Shortener.

Includes secure, unique short code generation.
"""

import string
import secrets


def generate_short_code(length=6):
    """
    Generate a secure, unique, alphanumeric code.

    Args:
        length (int): The desired length.

    Returns:
        str: The generated code.
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))
