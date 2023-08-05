"""Implementation of the Symptom CFX Structure."""

from uuid import uuid4

from .base import CFXStructure, load_basic, load_structure, load_list_structure

from .ComponentDesignator import ComponentDesignator
from .Measurement import Measurement
from .Region import Region


class Symptom(CFXStructure):  # pylint: disable=too-many-instance-attributes;
    """
    Describes a situation where a problem is identified via one or more failed tests.
        A symptom does not identify the actual cause of the failure(s),
        only that there is a problem that needs to be investigated.

    comments (str): Optional comments from the tester who discovered this symptom
    components_of_interest (list<ComponentDesignator>): A list of the components or specific
        component pins related to this symptom (if known)
    description (str): A human friendly description of the symptom
    priority (int): The priority of this symptom as compared to other symptom discovered for this unit.
        A priority of 1 indicates the highest priority.
    region_of_interest (Region): An optional location or area on the production unit where the symptom is located
        (for cases where there is no specific components that can be definitively related).
    related_measurements (list<Measurement>): A list of measurements
        that were taken which caused this symptom to be created
    symptom_category (string): An optional symptom category for this particular type of symptom
    symptom_code (string): A code identifying the type of symptom
    unique_identifier (string): A unique identifier for this particular symptom instance
        (new and unique each time a new symptom is discovered).
    """
    def __init__(self, **kwargs):
        self.comments = load_basic(kwargs, "comments", str, "")
        self.components_of_interest = load_list_structure(kwargs, "components_of_interest", ComponentDesignator)
        self.description = load_basic(kwargs, "description", str, "")
        self.priority = load_basic(kwargs, "priority", int, 1)
        self.region_of_interest = load_structure(kwargs, "region_of_interest", Region, default=Region())
        self.related_measurements = load_list_structure(kwargs, "related_measurements", Measurement)
        self.symptom_category = load_basic(kwargs, "symptom_category", str, "")
        self.symptom_code = load_basic(kwargs, "symptom_code", str, "")
        self.unique_identifier = load_basic(kwargs, "unique_identifier", str, str(uuid4()))
