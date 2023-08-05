# VNDB Thigh-highs
This module provide a VNDB client api implementation. It aims to provide some high level features to easily use VNDB api. It also includes some helper functions and classes to easily use database dumps.

## API Quick start
```
from vndb_thigh_highs import VNDB
from vndb_thigh_highs.models import VN

vndb = VNDB()
vns = vndb.get_vn(VN.id == 17)
vn = vns[0]
```

## Dumps Quick start
```
from vndb_thigh_highs.dumps import TagDatabaseBuilder

builder = TagDatabaseBuilder()
tag_db = builder.build_with_file_path("path/to/tags.json")
tag = tag_db.get_tag(tag_id)
```

## Testing
Run `test/main.py`.
Some tests will need some extra data, otherwise they are skipped:
- Database dumps tests need a dump in the `data/` directory
- Set command tests require to be logged in, the password field in `data/login.json` must be valid

Some other troublesome tests are also skipped by default.
