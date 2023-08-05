from .flag import Flag
from .table import Table, Search
from .types import INTEGER, STRING, ListOf, JoinedStrings

none = Flag.NONE

class Links(Table):
    homepage = none.Column(STRING)
    wikipedia = none.Column(STRING)

class ProducerRelation(Table):
    id = none.Column(INTEGER)
    relation = none.Column(STRING)
    name = none.Column(STRING)
    original_name = none.Column(STRING).with_name('original')

basic = Flag.BASIC
details = Flag.DETAILS
relations = Flag.RELATIONS

class Producer(Table):
    id = none.Column(INTEGER)
    name = basic.Column(STRING)
    original_name = basic.Column(STRING).with_name('original')
    type = basic.Column(STRING)
    language = basic.Column(STRING)
    links = details.Column(Links)
    aliases = details.Column(JoinedStrings())
    description = details.Column(STRING)
    relations = relations.Column(ListOf(ProducerRelation))

    search = Search()
