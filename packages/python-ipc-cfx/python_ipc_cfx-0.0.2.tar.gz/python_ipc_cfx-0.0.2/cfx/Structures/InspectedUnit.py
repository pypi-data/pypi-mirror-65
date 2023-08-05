"""Implementation of the InspectedUnit CFX Structure."""
from uuid import uuid4

from .base import CFXStructure, load_basic, load_enum, load_list_structure

from .Inspection import Inspection
from .TestResult import TestResult


class InspectedUnit(CFXStructure):
    """Describes the results of a series of inspections performed on a single production unit.

    inspections (list<Inspection>): A list of the inspections performed, along with the results
    overall_result (TestResult): The overall result of the inspections performed on this unit
    unit_identifier (str): Unique ID of Production Unit, Panel, or Carrier
    unit_position_number (nullable int): Logical reference of production unit
        as defined by CFX position rule (see CFX standard)
    """
    def __init__(self, **kwargs):
        self.overall_result = load_enum(kwargs, "overall_result", TestResult, default=TestResult.Passed)
        self.unit_identifier = load_basic(kwargs, "unit_identifier", str, str(uuid4()))
        self.unit_position_number = load_basic(kwargs, "unit_position_number", int)

        self.inspections = load_list_structure(
            kwargs,
            "inspections",
            Inspection,
            default=[{"result": self.overall_result}]
        )
