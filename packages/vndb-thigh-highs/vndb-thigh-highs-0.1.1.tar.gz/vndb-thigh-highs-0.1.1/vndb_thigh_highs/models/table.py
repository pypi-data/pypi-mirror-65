import json
from abc import ABCMeta, abstractmethod
from enum import Enum
from .types import STRING
from ..error import TableUsedError

class Operator(Enum):
    EQ = '='
    NE = '!='
    LE = '<='
    LT = '<'
    GE = '>='
    GT = '>'

    SEARCH = '~'
    AND = 'and'
    OR = 'or'

    def __str__(self):
        return self.value

    def join(self, iterable):
        return self.value.join(iterable)

    def make_filter(self, left, right):
        return Filter(left, self, right)

class Filter:
    def __init__(self, left_expression, operator, right_expression):
        self.left_expression = left_expression
        self.operator = operator
        self.right_expression = right_expression

    def __str__(self):
        return "%s %s %s" % (
            self.expression_to_string(self.left_expression),
            self.operator,
            self.expression_to_string(self.right_expression)
        )

    @staticmethod
    def expression_to_string(expression):
        if isinstance(expression, (Filter, Comparable)):
            return str(expression)
        return json.dumps(expression)

    def check_table_used(self, table):
        for expression in (self.left_expression, self.right_expression):
            if isinstance(expression, Filter):
                expression.check_table_used(table)
            elif isinstance(expression, Comparable):
                if expression.table != table:
                  raise TableUsedError(expression.table, table)

class Comparable:
    def __init__(self, table, api_name, field_name, field_constructor):
        self.table = table
        self.api_name = api_name
        self.field_name = field_name
        self.field_constructor = Table.adapt_constructor(field_constructor)

    def __repr__(self):
        return "<Column '%s.%s'>" % (self.table.table_name, self.api_name)

    def __str__(self):
        return self.api_name

    def __hash__(self):
        return hash(self._get_key())

    def __eq__(self, other):
        if isinstance(other, Comparable):
            return self._get_key() == other._get_key()
        return Filter(self, Operator.EQ, other)
    def __ne__(self, other):
        if isinstance(other, Comparable):
            return self._get_key() != other._get_key()
        return Filter(self, Operator.NE, other)

    def __le__(self, other):
        return Filter(self, Operator.LE, other)
    def __lt__(self, other):
        return Filter(self, Operator.LT, other)
    def __ge__(self, other):
        return Filter(self, Operator.GE, other)
    def __gt__(self, other):
        return Filter(self, Operator.GT, other)

    def _get_key(self):
        return (
            self.table,
            self.api_name,
            self.field_name,
            self.field_constructor
        )

class _Search(Comparable):
    def __init__(self, table, api_name, field_name):
        super().__init__(table, api_name, field_name, STRING)

class _Column(Comparable):
    def __init__(self, table, api_name, field_name, field_constructor, flag):
        super().__init__(table, api_name, field_name, field_constructor)
        self.flag = flag

    def get_from(self, dict):
        if self.api_name in dict and dict[self.api_name] is not None:
            return self.field_constructor(dict[self.api_name])
        return None

    def set_on(self, obj, value):
        setattr(obj, self.field_name, value)

class ComparableBuilder(metaclass=ABCMeta):
    def __init__(self):
        self.api_name = None

    def with_name(self, name):
        self.api_name = name
        return self

    def build(self, table, name):
        api_name = self.api_name or name
        return self.build_comparable(table, api_name, name)

    @abstractmethod
    def build_comparable(self, table, api_name, name):
        pass

class SearchBuilder(ComparableBuilder):
    def build_comparable(self, table, api_name, name):
        return _Search(table, api_name, name)

class Search(SearchBuilder):
    pass

class ColumnBuilder(ComparableBuilder):
    def __init__(self, field_constructor, flag):
        super().__init__()
        self.field_constructor = field_constructor
        self.flag = flag

    def build_comparable(self, table, api_name, name):
        return _Column(
            table, api_name, name, self.field_constructor, self.flag)

class TableMeta(type):
    def __new__(cls, name, bases, attributes):
        column_builders = cls.extract_builders(attributes, ColumnBuilder)
        search_builders = cls.extract_builders(attributes, SearchBuilder)
        table = super().__new__(cls, name, bases, attributes)
        cls._init_table(table, name, column_builders, search_builders)
        return table

    @staticmethod
    def extract_builders(attributes, builder_class):
        builders = {}
        for key, value in attributes.items():
            if not isinstance(value, builder_class):
                continue
            builders[key] = value
        for key in builders:
            del attributes[key]
        return builders

    @classmethod
    def _init_table(cls, table, name, column_builders, search_builders):
        columns = cls.build_comparables(table, column_builders)
        searchs = cls.build_comparables(table, search_builders)
        cls.add_comparable_attributes(table, columns)
        cls.add_comparable_attributes(table, searchs)
        table.table_name = cls.get_table_name(table, name)
        table.columns = columns
        table.searchs = searchs
        table.flags = cls.get_flags(columns)

    @classmethod
    def build_comparables(cls, table, column_builders):
        return [
            column_builder.build(table, key)
            for key, column_builder in column_builders.items()
        ]

    @classmethod
    def add_comparable_attributes(cls, table, comparables):
        for comparable in comparables:
            setattr(table, comparable.field_name, comparable)

    @staticmethod
    def get_table_name(table, name):
        if hasattr(table, 'table_name'):
            return table.table_name
        return name.lower()

    @staticmethod
    def get_flags(columns):
        flags = set()
        for column in columns:
            if column.flag.value is not None:
                flags.add(column.flag)
        return flags

class Table(metaclass=TableMeta):
    @staticmethod
    def adapt_constructor(constructor):
        if isinstance(constructor, TableMeta):
            return constructor.from_dict
        return constructor

    @classmethod
    def from_dict(cls, dict, flags=None):
        instance = cls()
        flags = flags or cls.flags
        for column in cls.columns:
            value = column.get_from(dict)
            column.set_on(instance, value)
        return instance

del Table.table_name
