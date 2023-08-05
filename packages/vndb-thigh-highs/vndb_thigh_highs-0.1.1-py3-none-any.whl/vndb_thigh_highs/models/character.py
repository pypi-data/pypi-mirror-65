from enum import Enum
from .flag import Flag
from .table import Table, Search
from .types import INTEGER, STRING, ListOf, JoinedStrings
from .common import Gender, SpoilerLevel

class BloodType(Enum):
    A = 'a'
    B = 'b'
    AB = 'ab'
    O = 'o'

class Role(Enum):
    MAIN = 'main'
    PRIMARY = 'primary'
    SIDE = 'side'
    APPEARS = 'appears'

class Birthday:
    def __init__(self, list):
        self.day = list[0]
        self.month = list[1]

class CharacterTrait:
    def __init__(self, list):
        self.id = list[0]
        self.spoiler_level = SpoilerLevel(list[1])

class CharacterAppearance:
    def __init__(self, list):
        self.vn_id = list[0]
        self.release_id = list[1]
        self.spoiler_level = SpoilerLevel(list[2])
        self.role = Role(list[3])

none = Flag.NONE

class CharacterVoiced(Table):
    staff_id = none.Column(INTEGER).with_name('id')
    staff_alias_id = none.Column(INTEGER).with_name('aid')
    vn_id = none.Column(INTEGER).with_name('vid')
    note = none.Column(STRING)

class CharacterInstance(Table):
    id = none.Column(INTEGER)
    spoiler_level = none.Column(SpoilerLevel).with_name('spoiler')
    name = none.Column(STRING)
    original_name = none.Column(STRING).with_name('original')

basic = Flag.BASIC
details = Flag.DETAILS
meas = Flag.MEASURES
traits = Flag.TRAITS
vns = Flag.VNS
voiced = Flag.VOICED
instances = Flag.INSTANCES

class Character(Table):
    id = none.Column(INTEGER)
    name = basic.Column(STRING)
    original_name = basic.Column(STRING).with_name('original')
    gender = basic.Column(Gender)
    blood_type = basic.Column(BloodType).with_name('bloodt')
    birthday = basic.Column(Birthday)
    aliases = details.Column(JoinedStrings())
    description = details.Column(STRING)
    image = details.Column(STRING)
    bust = meas.Column(INTEGER)
    waist = meas.Column(INTEGER)
    hip = meas.Column(INTEGER)
    height = meas.Column(INTEGER)
    weight = meas.Column(INTEGER)
    traits = traits.Column(ListOf(CharacterTrait))
    vns = vns.Column(ListOf(CharacterAppearance))
    voiced = voiced.Column(ListOf(CharacterVoiced))
    instances = instances.Column(ListOf(CharacterInstance))

    search = Search()
    vn_id = Search().with_name('vn')
