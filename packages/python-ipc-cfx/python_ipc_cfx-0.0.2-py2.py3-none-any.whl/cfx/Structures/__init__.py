"""Root namespace for all data structures referenced by CFX messages."""
from .base import CFXStructure, CFXEnum, load_basic, load_enum, load_list_enum, load_structure, load_list_structure

from .ActorType import ActorType
from .ComponentDesignator import ComponentDesignator
from .Defect import Defect
from .Image import Image
from .InspectedUnit import InspectedUnit
from .Inspection import Inspection
from .InspectionMethod import InspectionMethod
from .Measurement import Measurement, BooleanMeasurement
from .Operator import Operator
from .SamplingInformation import SamplingInformation
from .SamplingMethod import SamplingMethod
from .Segment import Segment
from .Symptom import Symptom
from .TestResult import TestResult
from .UnitPosition import UnitPosition
