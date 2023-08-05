"""Base CFX messages implementation."""
import abc


class CFXMessage(abc.ABC):  # pylint: disable=too-few-public-methods;
    """
    Abstract base class for all CFX Messages.

    Contains no data members.

    Provides for the serialization and deserialization of messages to and from JSON format.
    """
