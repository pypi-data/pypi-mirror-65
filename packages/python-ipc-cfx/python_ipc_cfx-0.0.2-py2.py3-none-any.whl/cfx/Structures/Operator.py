"""Implementation of the CFX Operator Structure."""
from .base import CFXStructure, load_basic, load_enum

from .ActorType import ActorType


class Operator(CFXStructure):
    """Represents an operator who performs a function

    actor_type (ActorType): The nature of the operator
    first_name (str): The Given Name of the Operator
    last_name (str): The Family Name of the Operator
    login_name (str): The Login Name for this Operator
    operator_identifier (str): An optional unique identifier for the Operator
    """
    def __init__(self, **kwargs):
        self.actor_type = load_enum(kwargs, "actor_type", ActorType, ActorType.default())
        self.first_name = load_basic(kwargs, "first_name", str)
        self.last_name = load_basic(kwargs, "last_name", str)
        self.login_name = load_basic(kwargs, "login_name", str)
        self.operator_identifier = load_basic(kwargs, "operator_identifier", str)
