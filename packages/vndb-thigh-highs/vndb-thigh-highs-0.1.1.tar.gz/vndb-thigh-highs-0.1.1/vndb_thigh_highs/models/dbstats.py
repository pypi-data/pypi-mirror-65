from .flag import Flag
from .table import Table
from .types import INTEGER

none = Flag.NONE

class DBStats(Table):
    users = none.Column(INTEGER)
    threads = none.Column(INTEGER)
    tags = none.Column(INTEGER)
    releases = none.Column(INTEGER)
    producers = none.Column(INTEGER)
    characters = none.Column(INTEGER).with_name('chars')
    posts = none.Column(INTEGER)
    vns = none.Column(INTEGER).with_name('vn')
    traits = none.Column(INTEGER)
