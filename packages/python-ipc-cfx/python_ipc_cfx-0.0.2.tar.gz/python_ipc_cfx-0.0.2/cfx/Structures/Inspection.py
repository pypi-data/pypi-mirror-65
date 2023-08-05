"""Implementation of the Inspection CFX Structure."""
from datetime import datetime
from uuid import uuid4

from .base import CFXStructure, load_basic, load_enum, load_list_structure

from .Defect import Defect
from .Measurement import BooleanMeasurement, Measurement
from .Symptom import Symptom
from .TestResult import TestResult


class Inspection(CFXStructure):  # pylint: disable=too-many-instance-attributes;
    """
    Describes a single step in a series of steps that an inspector
    makes (both human or automation) in the course of inspecting a production unit.

    comments (str): Optional comments from the inspector who inspected the unit
    defects_found (list<Defect>): The defects that were discovered in the course of performing this inspection (if any)
    error (str): In the case that the inspection cannot be completed, the error that was the cause of this outcome.
    inspection_end_time (nullable datetime): Indicates the time when this particular inspection ended (if known)
    inspection_name (str): Identifies the nature of the inspection performed
    inspection_start_time (nullable datetime): Indicates the time when this particular inspection began (if known)
    measurements (list<Measurement>): The measurements that were taken in the course of performing
        this inspection (if any).
    result (TestResult): The overall result of the inspection
    symptoms (List<Symptom>): Any symptoms that were discovered during the inspection (if any).
    test_procedure (str): Procedure to be followed to perform this inspection (primarily for human driven inspection)
    unique_identifier (str): A unique indentifier describing a particular instance of an inspection was made.
        Each new occurrence or recurrence of this same inspection gets a new unique identifier.
    """
    def __init__(self, **kwargs):
        self.comments = load_basic(kwargs, "comments", str, "")
        self.error = load_basic(kwargs, "error", str, "")
        self.inspection_end_time = load_basic(kwargs, "inspection_end_time", datetime)
        self.inspection_name = load_basic(kwargs, "inspection_name", str, "")
        self.inspection_start_time = load_basic(kwargs, "inspection_start_time", datetime)
        self.result = load_enum(kwargs, "result", TestResult, default=TestResult.Passed)
        self.symptoms = load_list_structure(kwargs, "symptoms", Symptom)
        self.test_procedure = load_basic(kwargs, "test_procedure", str, "")
        self.unique_identifier = load_basic(kwargs, "unique_identifier", str, str(uuid4()))

        default_defects = [{}] if self.result == TestResult.Failed else []
        self.defects_found = load_list_structure(kwargs, "defects_found", Defect, default=default_defects)

        default_measurement = [BooleanMeasurement(expected_value=True, value=self.result == TestResult.Failed)]
        self.measurements = load_list_structure(kwargs, "measurements", Measurement, default=default_measurement)
