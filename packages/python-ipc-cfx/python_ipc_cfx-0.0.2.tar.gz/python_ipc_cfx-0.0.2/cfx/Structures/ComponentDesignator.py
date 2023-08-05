"""Implementation of the ComponentDesignator CFX Structure."""
from uuid import uuid4

from .base import CFXStructure, load_basic, load_structure

from .UnitPosition import UnitPosition


class ComponentDesignator(CFXStructure):
    """
    Represents and identifies a particular component (instance of a part) on a production unit,
    or a particular aspect of a particular component, such as an individual pin of an electronic component.

    part_number (str): The internal part number of the designated component.
    reference_designator (str): A dot (".") and comma (",") delimeted string identifying
        a particular component on a production unit.
        Examples: C34, U2.11(component U2, Pin 11), U2.1-45 (component U2, Pins 1 to 45)
    unit_position (UnitPosition): Identifies the related production unit
    """
    def __init__(self, **kwargs):
        self.part_number = load_basic(kwargs, "part_number", str, str(uuid4()))
        self.reference_designator = load_basic(kwargs, "reference_designator", str, default="")
        self.unit_position = load_structure(kwargs, "unit_position", UnitPosition)
