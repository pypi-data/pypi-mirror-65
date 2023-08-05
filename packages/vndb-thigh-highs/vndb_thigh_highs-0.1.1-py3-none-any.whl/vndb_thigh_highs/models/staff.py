from .flag import Flag
from .table import Table, Search
from .types import INTEGER, STRING, ListOf
from .common import Gender

class Alias:
    def __init__(self, list):
        self.id = list[0]
        self.name = list[1]
        self.original_name = list[2]

none = Flag.NONE

class Links(Table):
    homepage = none.Column(STRING)
    wikipedia = none.Column(STRING)
    twitter = none.Column(STRING)
    anidb = none.Column(STRING)

class VNStaffWorkedOn(Table):
    vn_id = none.Column(INTEGER).with_name('id')
    staff_alias_id = none.Column(INTEGER).with_name('aid')
    role = none.Column(STRING)
    note = none.Column(STRING)

class VNStaffVoiced(Table):
    vn_id = none.Column(INTEGER).with_name('id')
    staff_alias_id = none.Column(INTEGER).with_name('aid')
    character_id = none.Column(INTEGER).with_name('cid')
    note = none.Column(STRING)

basic = Flag.BASIC
details = Flag.DETAILS
aliases = Flag.ALIASES
vns = Flag.VNS
voiced = Flag.VOICED

class Staff(Table):
    id = none.Column(INTEGER)
    name = basic.Column(STRING)
    original_name = basic.Column(STRING).with_name('original')
    gender = basic.Column(Gender)
    language = basic.Column(STRING)
    links = details.Column(Links)
    description = details.Column(STRING)
    main_alias = aliases.Column(INTEGER)
    aliases = aliases.Column(ListOf(Alias))
    vns = vns.Column(ListOf(VNStaffWorkedOn))
    voiced = voiced.Column(ListOf(VNStaffVoiced))

    search = Search()
    alias_id = Search().with_name('aid')
