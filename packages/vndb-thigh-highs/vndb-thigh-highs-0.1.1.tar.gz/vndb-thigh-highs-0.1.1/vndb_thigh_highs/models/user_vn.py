from enum import IntEnum
from .flag import Flag
from .table import Table, Search
from .types import INTEGER, STRING, TIMESTAMP, ISO_DATE, ListOf

class BuiltInLabelId(IntEnum):
    UNKNOWN = 0
    PLAYING = 1
    FINISHED = 2
    STALLED = 3
    DROPPED = 4
    WISHLIST = 5
    BLACKLIST = 6
    VOTED = 7

none = Flag.NONE

class Label(Table):
    id = none.Column(INTEGER)
    name = none.Column(STRING).with_name('label')

basic = Flag.BASIC
labels = Flag.LABELS

class UserVN(Table):
    table_name = "ulist"

    user_id = basic.Column(INTEGER).with_name('uid')
    vn_id = basic.Column(INTEGER).with_name('vn')
    added_date = basic.Column(TIMESTAMP).with_name('added')
    last_modification_date = basic.Column(TIMESTAMP).with_name('lastmod')
    voted_date = basic.Column(TIMESTAMP).with_name('voted')
    vote = basic.Column(INTEGER)
    notes = basic.Column(STRING)
    started_date = basic.Column(ISO_DATE).with_name('started')
    finished_date = basic.Column(ISO_DATE).with_name('finished')
    labels = labels.Column(ListOf(Label))

    label = Search()
