from enum import Enum
from .tree import Node, Tree, TreeBuilder

class TagCategory(Enum):
    CONTENT = 'cont'
    SEXUAL_CONTENT = 'ero'
    TECHNICAL = 'tech'

class Tag(Node):
    def __init__(self, id, name, description, category, meta, aliases, vn_count):
        super().__init__(id, name)
        self.description = description
        self.category = category
        self.meta = meta
        self.aliases = aliases
        self.vn_count = vn_count

    @classmethod
    def from_dict(cls, tag_dict):
        return cls(
            tag_dict['id'],
            tag_dict['name'],
            tag_dict['description'],
            TagCategory(tag_dict['cat']),
            tag_dict['meta'],
            tag_dict['aliases'],
            tag_dict['vns'],
        )

class TagDatabase(Tree):
    def get_tag(self, tag_id):
        return self.get_node(tag_id)

class TagDatabaseBuilder(TreeBuilder):
    def __init__(self):
        super().__init__(TagDatabase, Tag)
