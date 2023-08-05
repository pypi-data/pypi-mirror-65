from .flag import Flag
from .table import Table
from .types import INTEGER, STRING, BOOLEAN

basic = Flag.BASIC

class UserLabel(Table):
    table_name = "ulist-labels"

    user_id = basic.Column(INTEGER).with_name('uid')
    label_id = basic.Column(INTEGER).with_name('id')
    name = basic.Column(STRING).with_name('label')
    private = basic.Column(BOOLEAN)
