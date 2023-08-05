"""Implementation of the UnitPosition CFX Structure."""
from uuid import uuid4

from .base import CFXStructure, load_basic


class UnitPosition(CFXStructure):
    """
    This structure contains information about a one of a set of production units that are processed
        simultaneously under a single transaction by an endpoint.
    Units may be identified in one of two ways:
        1. The UnitIdentifier property represents the actual unique identifier of the production unit.
        2. The UnitIdentifier property represents the unique identifier of the "carrier" or "PCB panel"
            AND the PositionNumber property represents the position of the unit within the carrier/panel.
            PositionNumber's are established as defined in the CFX Standard.

    flip_x (bool): Is production unit flipped in X-direction
    flip_y (bool): Is production unit flipped in Y-direction
    position_name (str): Optional name of position
    position_number (int): Logical reference of production unit as defined by CFX position rule
        (see CFX standard section 5.6).
    rotation (number): Original rotation of Production unit, as it is known to the endpoint, expressed in degrees
    unit_identifier (str): Unique ID of Production Unit, Panel, or Carrier
    x (number): X coordinate of Production unit origin, as it is known to the endpoint, expressed in millimeters (mm)
    y (number): Y coordinate of Production unit origin, as it is known to the endpoint, expressed in millimeters (mm)
    """
    def __init__(self, **kwargs):
        self.flip_x = load_basic(kwargs, "flip_x", bool, False)
        self.flip_y = load_basic(kwargs, "flip_y", bool, False)
        self.position_name = load_basic(kwargs, "position_name", str)
        self.position_number = load_basic(kwargs, "position_number", int)
        self.rotation = load_basic(kwargs, "rotation", "number", 0)
        self.unit_identifier = load_basic(kwargs, "unit_identifier", str, str(uuid4()))
        self.x = load_basic(kwargs, "x", "number", 0)  # pylint: disable=invalid-name;
        self.y = load_basic(kwargs, "y", "number", 0)  # pylint: disable=invalid-name;
