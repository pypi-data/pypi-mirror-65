import json
from collections import Iterable
from .command import TableCommand
from .response_parser import GetResponseParser
from .error import TableUsedError, InvalidFlagError
from .models import (
    Flag, Comparable, Operator, Filter,
    VN, Release, Producer, Character, Staff, User, UserLabel, UserVN
)

class GetCommandOption:
    def __init__(self, api_name, name=None, *, transform=None):
        self.api_name = api_name
        self.name = name or api_name
        self.transform = transform or (lambda x: x)

    def init_attribute(self, obj):
        setattr(obj, self.name, None)

    def add_value_to_dict(self, obj, options_dict):
        value = getattr(obj, self.name)
        if value is not None:
            options_dict[self.api_name] = self.transform(value)

class GetCommandOptions:
    send_options = (
        GetCommandOption('page'),
        GetCommandOption('results', 'max_results'),
        GetCommandOption('sort', transform=str),
        GetCommandOption('reverse'),
    )

    def __init__(self):
        self.limit = float("inf")
        for send_option in self.send_options:
            send_option.init_attribute(self)

    def make_options_dict(self):
        options_dict = {}
        for send_option in self.send_options:
            send_option.add_value_to_dict(self, options_dict)
        return options_dict

    def start_pagination(self):
        self.page = 1

    def next_page(self):
        self.page += 1

    def check_table_used(self, table):
        self.check_sort_table_used(table)

    def check_sort_table_used(self, table):
        if (self.sort is not None
            and isinstance(self.sort, Comparable)
            and self.sort.table != table):
            raise TableUsedError(self.sort, table)

class GetCommandResult(list):
    def __init__(self, items, more):
        super().__init__(items)
        self.more = more

    def extend(self, result):
        super().extend(result)
        self.more = self.more and result.more

    def has_reached_limit(self, limit):
        return not self.more or len(self) >= limit

    @classmethod
    def empty(cls):
        return cls([], True)

    @classmethod
    def from_dict(cls, result_dict):
        return cls(result_dict['items'], result_dict['more'])

class GetCommand(TableCommand):
    def __init__(self, socket, table):
        super().__init__(socket, GetResponseParser(), table)

    def get(self, filters, flags=None, options=None):
        filters = self.analyse_filters(filters)
        flags = self.analyse_flags(flags)
        options = self.analyse_options(options)
        command = self.make_command(filters, flags, options)
        response_dict = self.communicate(command)
        return self.parse_response_dict(response_dict, flags)

    def get_all(self, filters, flags=None, options=None):
        options = self.analyse_options(options)
        options.start_pagination()
        main_result = GetCommandResult.empty()
        while True:
            result = self.get(filters, flags, options)
            main_result.extend(result)
            if main_result.has_reached_limit(options.limit):
                break
            options.next_page()
        return main_result

    def make_command(self, filters, flags, options):
        options_dict = options.make_options_dict()
        command = "get %s %s (%s) %s" % (
            self.get_name(),
            ",".join([str(flag) for flag in flags]),
            Operator.AND.join([str(filter_) for filter_ in filters]),
            json.dumps(options_dict) if options_dict else "",
        )
        return command

    def analyse_filters(self, filters):
        if isinstance(filters, str) or not isinstance(filters, Iterable):
            filters = [filters]
        for filter_ in filters:
            if isinstance(filter_, Filter):
                filter_.check_table_used(self.table)
        return filters

    def analyse_flags(self, flags):
        if flags is None:
            flags = self.table.flags
        elif isinstance(flags, Flag):
            flags = [flags]
        error_flags = set(flags) - self.table.flags
        if error_flags:
            raise InvalidFlagError("Invalid flag usage in '%s'" % str(error_flags))
        return flags

    def analyse_options(self, options):
        if options is None:
            return GetCommandOptions()
        options.check_table_used(self.table)
        return options

    def parse_response_dict(self, response_dict, flags):
        response_dict['items'] = [
            self.table.from_dict(item, flags)
            for item in response_dict['items']
        ]
        return GetCommandResult.from_dict(response_dict)

class GetCommandFactory:
    def __init__(self, socket):
        self.socket = socket
        self.tables = [
            VN,
            Release,
            Producer,
            Character,
            Staff,
            User,
            UserLabel,
            UserVN,
        ]

    def all_commands(self):
        return [
            GetCommand(self.socket, table)
            for table in self.tables
        ]
