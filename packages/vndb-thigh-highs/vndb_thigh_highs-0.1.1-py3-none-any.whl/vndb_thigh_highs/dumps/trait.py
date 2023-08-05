from .tree import Node, Tree, TreeBuilder

class Trait(Node):
    def __init__(self, id, name, description, meta, aliases, character_count):
        super().__init__(id, name)
        self.description = description
        self.meta = meta
        self.aliases = aliases
        self.character_count = character_count

    @classmethod
    def from_dict(cls, trait_dict):
        return cls(
            trait_dict['id'],
            trait_dict['name'],
            trait_dict['description'],
            trait_dict['meta'],
            trait_dict['aliases'],
            trait_dict['chars'],
        )

class TraitDatabase(Tree):
    def get_trait(self, trait_id):
        return self.get_node(trait_id)

class TraitDatabaseBuilder(TreeBuilder):
    def __init__(self):
        super().__init__(TraitDatabase, Trait)
