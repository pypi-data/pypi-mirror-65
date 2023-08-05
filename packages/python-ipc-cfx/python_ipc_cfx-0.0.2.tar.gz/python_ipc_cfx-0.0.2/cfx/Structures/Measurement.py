"""
Implementation of the Measurement abstract CFX Structure

Also contains various Measurement implementations.
"""
import abc

from datetime import datetime
from uuid import uuid4

from .base import CFXStructure, load_basic, load_enum

from .TestResult import TestResult


class Measurement(abc.ABC, CFXStructure):
    """Abstract base class for dynamic data structure which describes
        a measurement that was made by a human or by automated equipment
        in the course of inspecting or testing a production unit.

    crds (str): An optional list of component designators (instances of a part)
        on a production unit(s) to be associated with this measurement.
        May include sub-components in "." notation. Examples: R1, R2, R3 or R2.3 (R2, pin 3)
    measurement_name (string): A name that uniquely describes the test or measurement that was performed.
    result (TestResult): An enumeration indicating whether or not this measurement is considered acceptable.
    sequence (int): An optional positive integer describing the sequence in which
        the tests or measurements were performed that resulted in this Reading.
    time_recorded (nullable datetime): The date/time when this Measurement was recorded (if known, otherwise null)
    unique_identifier (str): A unique identifier that for this particular measurement instance
        (new and unique each time a new measurement is made or repeated).
    """
    def __init__(self, **kwargs):
        self.crds = load_basic(kwargs, "crds", str)
        self.measurement_name = load_basic(kwargs, "measurement_name", str, "")
        self.result = load_enum(kwargs, "result", TestResult, default=TestResult.Passed)
        self.sequence = load_basic(kwargs, "sequence", int)
        self.time_recorded = load_basic(kwargs, "time_recorded", datetime)
        self.unique_identifier = load_basic(kwargs, "unique_identifier", str, uuid4().hex)


class BooleanMeasurement(Measurement):
    """
    Describes a measurement that was made by a human or by automated equipment in the course of inspecting
        or testing a production unit in which the result of the measurement is a boolean (true / fales) value.

    expected_value (bool): The expected value of this measurement
    value (bool): The acutal resulting value of this measurement
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.expected_value = load_basic(kwargs, "expected_value", bool, True)
        self.value = load_basic(kwargs, "value", bool, True)
        self.result = (self.expected_value == self.value)
