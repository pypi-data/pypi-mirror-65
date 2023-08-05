from schematics.models import Model
from schematics.types import ListType, StringType


class Capability(Model):
    supported_schema = ListType(StringType())
