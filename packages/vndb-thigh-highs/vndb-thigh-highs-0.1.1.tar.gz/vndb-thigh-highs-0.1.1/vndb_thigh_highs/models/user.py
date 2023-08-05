from .flag import Flag
from .table import Table
from .types import INTEGER, STRING

none = Flag.NONE
basic = Flag.BASIC

class User(Table):
    id = none.Column(INTEGER)
    username = basic.Column(STRING)
