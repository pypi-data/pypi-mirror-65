"""Implementation of the SamplingInformation CFX Structure."""
from .base import CFXStructure, load_basic, load_enum
from .SamplingMethod import SamplingMethod


class SamplingInformation(CFXStructure):
    """Describes the sampling strategy to be employed on a particular lot of material / units during test or inspection.

    lot_size (nullable number): The total number of units in the lot
    sample_size (nullable number): The number of units from the total lot to be inspected / tested.
        This is a subset of the total lot.
    sampling_method (SamplingInformation): An enumeration describing the sampling method that was employed (if any)
    """
    def __init__(self, **kwargs):
        self.lot_size = load_basic(kwargs, "lot_size", "number", None)

        self.sample_size = load_basic(kwargs, "sample_size", "number", None)

        self.sampling_method = load_enum(kwargs, "sampling_method", SamplingMethod, SamplingMethod.default())
