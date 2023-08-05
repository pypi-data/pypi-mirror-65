from enum import Enum
from .flag import Flag
from .table import Table, Search
from .types import BOOLEAN, DATE, INTEGER, STRING, ListOf, JoinedStrings
from .common import SpoilerLevel

class Length(Enum):
    VERY_SHORT = 1
    SHORT = 2
    MEDIUM = 3
    LONG = 4
    VERY_LONG = 5

class VNTag:
    def __init__(self, list):
        self.tag_id = list[0]
        self.score = list[1]
        self.spoiler_level = SpoilerLevel(list[2])

none = Flag.NONE

class Links(Table):
    wikipedia = none.Column(STRING)
    encubed = none.Column(STRING)
    renai = none.Column(STRING)

class Anime(Table):
    id = none.Column(INTEGER)
    ann_id = none.Column(INTEGER)
    nfo_id = none.Column(INTEGER)
    title_romaji = none.Column(STRING)
    title_kanji = none.Column(STRING)
    year = none.Column(INTEGER)
    type = none.Column(STRING)

class VNRelation(Table):
    id = none.Column(INTEGER)
    relation = none.Column(STRING)
    title = none.Column(STRING)
    original_title = none.Column(STRING).with_name('original')
    official = none.Column(BOOLEAN)

class Screenshot(Table):
    image = none.Column(STRING)
    release_id = none.Column(INTEGER).with_name('rid')
    nsfw = none.Column(BOOLEAN)
    height = none.Column(INTEGER)
    width = none.Column(INTEGER)

class VNStaff(Table):
    staff_id = none.Column(INTEGER).with_name('sid')
    staff_alias_id = none.Column(INTEGER).with_name('aid')
    name = none.Column(STRING)
    original_name = none.Column(STRING).with_name('original')
    role = none.Column(STRING)
    note = none.Column(STRING)

basic = Flag.BASIC
details = Flag.DETAILS
anime = Flag.ANIME
relations = Flag.RELATIONS
tags = Flag.TAGS
stats = Flag.STATS
screens = Flag.SCREENS
staff = Flag.STAFF

class VN(Table):
    id = none.Column(INTEGER)
    title = basic.Column(STRING)
    original_title = basic.Column(STRING).with_name('original')
    released_date = basic.Column(DATE).with_name('released')
    languages = basic.Column(ListOf(STRING))
    original_languages = basic.Column(ListOf(STRING)).with_name('orig_lang')
    platforms = basic.Column(ListOf(STRING))
    aliases = details.Column(JoinedStrings())
    length = details.Column(Length)
    description = details.Column(STRING)
    links = details.Column(Links)
    image = details.Column(STRING)
    image_nsfw = details.Column(BOOLEAN)
    anime = anime.Column(ListOf(Anime))
    relations = relations.Column(ListOf(VNRelation))
    tags = tags.Column(ListOf(VNTag))
    popularity = stats.Column(INTEGER)
    rating = stats.Column(INTEGER)
    votecount = stats.Column(INTEGER)
    screens = screens.Column(ListOf(Screenshot))
    staff = staff.Column(ListOf(VNStaff))

    search = Search()
    firstchar = Search()
