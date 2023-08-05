import json

class Node:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.parents = set()
        self.children = set()

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return "<%s (%s) %s>" % (self.__class__.__name__, self.id, self.name)

    def add_parent(self, parent_node, *, _reverse=True):
        self.parents.add(parent_node)
        if _reverse:
            parent_node.add_child(self, _reverse=False)

    def add_child(self, child_node, *, _reverse=True):
        self.children.add(child_node)
        if _reverse:
            child_node.add_parent(self)

    def get_full_name(self):
        if not self.parents:
            return self.name
        parent_names = [
            parent.get_full_name() for parent in self.parents
        ]
        if len(parent_names) > 1:
            parent_names = ["[%s]" % name for name in parent_names]
        return "%s > %s" % ("|".join(parent_names), self.name)

    def get_root_parents(self):
        if not self.parents:
            return set([self])
        root_parents = set()
        for parent in self.parents:
            root_parents.update(parent.get_root_parents())
        return root_parents

    def get_all_parents(self):
        if not self.parents:
            return set()
        parents = set()
        parents.update(self.parents)
        for parent in self.parents:
            parents.update(parent.get_all_parents())
        return parents

    @classmethod
    def from_dict(cls, node_dict):
        return cls(
            node_dict['id'],
            node_dict['name'],
        )

class Tree:
    def __init__(self):
        self.nodes = {}

    def __len__(self):
        return len(self.nodes)

    def add_node(self, node):
        self.nodes[node.id] = node

    def get_node(self, node_id):
        return self.nodes[node_id]

class TreeBuilder:
    def __init__(self, tree_class=None, node_class=None):
        self.tree = None
        self.tree_class = tree_class or Tree
        self.node_class = node_class or Node

    def build_with_file_path(self, file_path, **kwargs):
        if 'encoding' not in kwargs:
            kwargs['encoding'] = 'utf8'
        with open(file_path, 'r', **kwargs) as nodes_file:
            return self.build_with_file(nodes_file)

    def build_with_file(self, nodes_file):
        return self.build_with_dict_list(json.load(nodes_file))

    def build_with_dict_list(self, node_dict_list):
        self.tree = self.tree_class()
        self.add_nodes(node_dict_list)
        self.add_parent_child_links(node_dict_list)
        return self.tree

    def add_nodes(self, node_dict_list):
        for node_dict in node_dict_list:
            node = self.node_class.from_dict(node_dict)
            self.tree.add_node(node)

    def add_parent_child_links(self, node_dict_list):
        for node_dict in node_dict_list:
            child_node = self.tree.get_node(node_dict['id'])
            parent_ids = node_dict['parents']
            for parent_id in parent_ids:
                parent_node = self.tree.get_node(parent_id)
                child_node.add_parent(parent_node)
