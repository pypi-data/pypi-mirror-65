"""Implementation of the Region CFX Structure."""
from .base import CFXStructure, load_basic, load_list_structure

from .Segment import Segment


class Region(CFXStructure):
    """
    Describes a planar, 2 dimensional region as defined by a series of X, Y
        coordinates that when plotted, form the region.

    region_segments (list<Segment>): Collection of (X, Y) coordinates that when plotted form a planar region.
    start_point_x (number): X coordinate of first point in region outline
    start_point_y (number): Y coordinate of first point in region outline
    """
    def __init__(self, **kwargs):
        self.region_segments = load_list_structure(kwargs, "region_segments", Segment)
        self.start_point_x = load_basic(kwargs, "start_point_x", "number", 0)
        self.start_point_y = load_basic(kwargs, "start_point_y", "number", 0)
