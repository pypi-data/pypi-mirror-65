from enum import Enum
from .table import ColumnBuilder

class Flag(Enum):
    BASIC = "basic"
    DETAILS = "details"
    ANIME = "anime"
    RELATIONS = "relations"
    TAGS = "tags"
    STATS = "stats"
    SCREENS = "screens"
    STAFF = "staff"
    VN = "vn"
    PRODUCERS = "producers"
    MEASURES = "meas"
    TRAITS = "traits"
    VNS = "vns"
    VOICED = "voiced"
    INSTANCES = "instances"
    ALIASES = "aliases"
    LABELS = "labels"

    NONE = None

    def __str__(self):
        return self.value

    def Column(self, field_constructor):
        return ColumnBuilder(field_constructor, self)
