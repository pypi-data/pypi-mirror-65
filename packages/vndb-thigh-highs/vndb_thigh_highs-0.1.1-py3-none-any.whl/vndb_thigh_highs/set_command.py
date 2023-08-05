import json
from enum import Enum
from datetime import date
from .command import TableCommand
from .response_parser import OkResponseParser
from .error import TableUsedError
from .models import (
    Comparable,
    UserVN
)

class SetCommand(TableCommand):
    def __init__(self, socket, table):
        super().__init__(socket, OkResponseParser.for_set(), table)

    def set(self, entry_id, field_dict):
        field_dict = self.analyse_field_dict(field_dict)
        command = self.make_command(entry_id, field_dict)
        self.communicate(command)

    def delete(self, entry_id):
        self.set(entry_id, None)

    def make_command(self, entry_id, field_dict):
        command = "set %s %s %s" % (
            self.get_name(),
            entry_id,
            json.dumps(field_dict) if field_dict is not None else "",
        )
        return command

    def analyse_field_dict(self, field_dict):
        if field_dict is None:
            return None
        self.check_table_used(field_dict)
        return {
            str(key): self.analyse_field_value(key, value)
            for key, value in field_dict.items()
        }

    def analyse_field_value(self, key, value):
        if isinstance(value, Enum):
            return value.value
        if isinstance(value, date):
            return date.isoformat(value)
        return value

    def check_table_used(self, field_dict):
        for key in field_dict.keys():
            if isinstance(key, Comparable) and key.table != self.table:
                raise TableUsedError(key.table, self.table)

class SetCommandFactory:
    def __init__(self, socket):
        self.socket = socket
        self.tables = [
            UserVN,
        ]

    def all_commands(self):
        return [
            SetCommand(self.socket, table)
            for table in self.tables
        ]
