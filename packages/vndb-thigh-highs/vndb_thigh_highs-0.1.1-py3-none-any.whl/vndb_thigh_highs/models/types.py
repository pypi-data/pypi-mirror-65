from datetime import date
from . import table as t

def TIMESTAMP(timestamp):
    return date.fromtimestamp(timestamp)

def date_from_iso_format(date_string):
    return date.fromisoformat(date_string)

_identity = lambda x: x

BOOLEAN = _identity
DATE = _identity
ISO_DATE = date_from_iso_format
INTEGER = _identity
STRING = _identity

class JoinedStrings:
    def __init__(self, separator="\n"):
        self.separator = separator

    def __call__(self, string):
        return string.split(self.separator)

class ListOf:
    def __init__(self, field_constructor):
        self.field_constructor = t.Table.adapt_constructor(field_constructor)

    def __call__(self, objs):
        return [self.field_constructor(obj) for obj in objs]
