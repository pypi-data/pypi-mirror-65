"""Implementation of the Segment CFX Structure."""
from .base import CFXStructure, load_basic


class Segment(CFXStructure):
    """An X/Y coordinate that is used to define a planar region.

    x (number): The X coordinate
    y (number): The y coordinate
    """
    def __init__(self, **kwargs):
        self.x = load_basic(kwargs, "x", "number", 0.0)  # pylint:disable=invalid-name;
        self.y = load_basic(kwargs, "y", "number", 0.0)  # pylint:disable=invalid-name;
