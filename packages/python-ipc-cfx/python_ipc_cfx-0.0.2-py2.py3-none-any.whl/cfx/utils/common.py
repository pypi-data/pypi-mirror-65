"""Common functions to the whole CFX package."""
from stringcase import pascalcase, snakecase

DIRECT = {}

REVERSE = {v: k for k, v in DIRECT.items()}

def to_pascal_case(query):
    """Transforms a string into PascalCase.

    Args:
        query (str): The input to be transformed
    Returns:
        str: The PascalCase version of the input string
    """
    return DIRECT.get(query, pascalcase(query))

def from_pascal_case(query):
    """Transforms a string into snake_case.

    Args:
        query (str): The input to be transformed
    Returns:
        str: The snake_case version of the input string
    """
    return REVERSE.get(query, snakecase(query))
