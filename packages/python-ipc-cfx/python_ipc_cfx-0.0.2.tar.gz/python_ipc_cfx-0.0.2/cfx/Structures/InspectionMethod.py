"""Implementation of the CFX InspectionMethod Enumeration."""
from .base import CFXEnum


class InspectionMethod(CFXEnum):
    """Method of testing"""
    Human = 0
    AOI = 1
    SPI = 2
