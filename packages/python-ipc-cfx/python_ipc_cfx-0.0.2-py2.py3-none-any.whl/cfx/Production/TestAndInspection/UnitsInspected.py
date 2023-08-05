"""The units_inspected class and various helper functions."""
from uuid import uuid4
from ...cfx import CFXMessage
from ...Structures import CFXStructure, load_basic, load_enum, load_structure, load_list_structure,\
    InspectionMethod, SamplingInformation, Operator, InspectedUnit


class UnitsInspected(CFXMessage, CFXStructure):
    """
    Sent by a process endpoint when one or more units have been inspected.

    Includes pass/fail information, as well as a detailed report of the inspection, including the specific
    measurements and inspections that were made, and defects that were discovered during the process.

    inspected_units (list<InspectedUnit>): A list of the units that were inspected,
        along with the inspections made, and inspection results.
    inspection_method (InspectionMethod): Describes how the inspections were performed
    inspector (Operator): Identifies the person who performed the inspections,
        or operator of the automated equipment that performed the inspections (optional)
    sampling_information (SamplingInformation): Describes the sampling method that was
        used during the inspections (if any)
    transaction_id (str): The id of the work transaction with which this inspection session is associated.
    """
    def __init__(self, **kwargs):
        self.transaction_id = load_basic(kwargs, "transaction_id", str, default=str(uuid4()))
        self.inspection_method = load_enum(kwargs, "inspection_method", InspectionMethod, InspectionMethod.default())
        self.sampling_information = load_structure(
            kwargs,
            "sampling_information",
            SamplingInformation,
            SamplingInformation()
        )

        self.inspector = load_structure(kwargs, "inspector", Operator, Operator())
        self.inspected_units = load_list_structure(kwargs, "inspected_units", InspectedUnit)
