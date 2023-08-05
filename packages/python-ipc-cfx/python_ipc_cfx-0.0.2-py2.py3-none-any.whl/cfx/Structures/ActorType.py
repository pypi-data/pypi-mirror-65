"""Implementation of the ActorType CFX Enumeration."""
from .base import CFXEnum


class ActorType(CFXEnum):
    """Types of Operators.

    Human: A human being is performing the operation
    Robot: A robotic / automated device is performing the operation
    RemoteSystem: A remote system or artificial intelligence entity is performing the operation
    """
    Human = 0
    Robot = 1
    RemoteSystem = 2
