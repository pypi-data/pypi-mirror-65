"""Implementation of the SamplingMethod CFX Enumeration."""
from .base import CFXEnum


class SamplingMethod(CFXEnum):
    """Describes a particular sampling methodology.

    NoSampling: No sampling. All units are inspected (100% Inspection).
    ANSI_Z14: Units sampled according to ANSI/ASQ Z1.4 AQL methods.
    MIL_STD_105: Units sampled according to MIL-STD-105 mil standard.
    MIL_STD_1916: Units sampled according to MIL-STD-1916 mil standard.
    Squeglia: Units sampled according to the Squeglia AQL method.
    FixedSample: A fixed number of units were sampled (lot size disregarded).
    """
    NoSampling = 0
    ANSI_Z14 = 1
    MIL_STD_105 = 2
    MIL_STD_1916 = 3
    Squeglia = 4
    FixedSample = 5
