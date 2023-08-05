"""Implementation of the Defect CFX Structure."""
from uuid import uuid4

from .base import CFXStructure, load_basic, load_structure, load_list_structure

from .ComponentDesignator import ComponentDesignator
from .Image import Image
from .Region import Region
from .Measurement import Measurement
from .Symptom import Symptom


class Defect(CFXStructure):  # pylint: disable=too-many-instance-attributes;
    """Describes a defect that was discovered on a production unit

    comments (str): Optional comments from the inspector who discovered this defect
    component_of_interest (ComponentDesignator): An optional component or specific component pins related to this defect
    confidence_level (number): A floating-point number from 1 to 100 indicating the level of
        confidence in the validity of this defect.
        Intended to be used by humans that screen the results of inspections made by automated inspection equipment,
        which may produce false defects from time to time.
    defect_category (str): An optional defect category for this particular type of defect
    defect_code (str): A code identifying the type of defect
    defect_images (list<Image>): One of more pictures/images of the defect
    description (str): A human friendly description of the defect
    priority (int): The priority of this defect as compared to other defects discovered for this unit.
        A priority of 1 indicates the highest priority.
    region_of_interest (Region): An optional location or area on the production unit where the defect is located
        (for cases where there is no specific component related, such as a scratch or cosmetic defect).
    related_measurements (list<Measurement>): A list of measurements that were taken
        in the course of discovering this defect
    related_symptoms (list<Symptom>): A list of symptoms that were discovered in the course of identifying this defect.
    unique_identifier (str): A unique identifier for this particular defect instance
        (new and unique each time a new defect is discovered).
    """
    def __init__(self, **kwargs):
        self.comments = load_basic(kwargs, "comments", str)
        self.component_of_interest = load_structure(kwargs, "component_of_interest", ComponentDesignator)
        self.confidence_level = load_basic(kwargs, "confidence_level", "number", 100.0)
        if self.confidence_level < 0.0 or self.confidence_level > 100.0:
            raise ValueError("Defect: confidence_level out of [0.0, 100.0] range")
        self.defect_category = load_basic(kwargs, "defect_category", str)
        self.defect_code = load_basic(kwargs, "defect_code", str, "")
        self.defect_images = load_list_structure(kwargs, "defect_images", Image)
        self.description = load_basic(kwargs, "description", str, "")
        self.priority = load_basic(kwargs, "priority", int, 1)
        self.region_of_interest = load_structure(kwargs, "region_of_interest", Region)
        self.related_measurements = load_list_structure(kwargs, "related_measurements", Measurement)
        self.related_symptoms = load_list_structure(kwargs, "related_symptoms", Symptom)
        self.unique_identifier = load_basic(kwargs, "unique_identifier", str, str(uuid4()))
