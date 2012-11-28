"""
Of course for graph representation we may use just python dict but
I decide to add a little bit OOP here :-), else it'd bee great to make
such algorythm on Cython but as it's python test, lets do it next way.
Here I've overided some python builtin types functions like containement
in list type, I undrstand that it works slow but my goal was just to
demonstrate algorythm.
"""


class Node(object):
    """
        This class represents Node in Graph
    """
    def __init__(self, name, neighbours=None):
        self.name = name
        if neighbours:
            self.neighbours = neighbours
        else:
            self.neighbours = []

    def __repr__(self):
        return "<Node: %s>" % self.name


class PathTreeNode(object):

    def __init__(self, node):
        self.node = node
        self.branches = []
        self.parent = None
        self.parents_graph_nodes = []

    def add_branch(self, tree_node):
        self.branches.append(tree_node)
        tree_node.parent = self
        tree_node.parents_graph_nodes.extend(self.parents_graph_nodes)
        tree_node.parents_graph_nodes.append(self.node)

    def check_in_parents(self, node):
        return node in self.parents_graph_nodes


class Graph(dict):

    def __init__(self):
        super(Graph, self).__init__()

    def append(self, node):
        if isinstance(node, Node):
            super(Graph, self).append(node)
        else:
            raise Exception('You may add only node for graph')

    def load_from_file(self, filename):
        f = open(filename, 'rb+')
        try:
            graph_desc = eval(f.read())
        except Exception, e:
            raise Exception('Wrong graph description in file:\n%s' % e)
        self.import_from_dict(graph_desc)

    @property
    def nodes(self):
        return self.values()

    def import_from_dict(self, graph_dict):
        """
            Import graph structure from python dictionary
        """
        for node_name in graph_dict.keys():
            self[node_name] = Node(node_name)

        for node_name, neighbours in graph_dict.items():
            node = self[node_name]
            for neighbour_name in neighbours:
                neighbour = self.get(neighbour_name, None)
                if neighbour:
                    if not neighbour in node.neighbours:
                        node.neighbours.append(neighbour)
                    # else check if we have back reference to the node
                    if not node in neighbour.neighbours:
                        neighbour.neighbours.append(node)

    def get_destination_tree(self, node1, node2):
        """
            Our core function which should get destination tree from
            given node1 to node2. This returns tree of paths from
            node1 to node2 and list of dead end nodes in that tree
        """

        graph_traversed = False
        path_tree_root = PathTreeNode(node1)
        start_nodes = [path_tree_root, ]
        dead_end_nodes = []

        while not graph_traversed:
            new_start_tree_nodes = []
            for path_tree_node in start_nodes:
                for neighbour in path_tree_node.node.neighbours:
                    if not path_tree_node.check_in_parents(neighbour):
                        new_tree_node = PathTreeNode(neighbour)
                        path_tree_node.add_branch(new_tree_node)
                        if neighbour != node2:
                            new_start_tree_nodes.append(new_tree_node)
                        else:
                            dead_end_nodes.append(new_tree_node)
                if not new_start_tree_nodes:
                    graph_traversed = True
                else:
                    start_nodes = new_start_tree_nodes

        return path_tree_root, dead_end_nodes

    def get_destinations(self, node1, node2):
        """
            This function get us destinations as list of nodes, from
            node1 to node2
        """
        destinations = []
        tree, dead_ends = self.get_destination_tree(node1, node2)

        for dead_end in dead_ends:
            path = []
            tree_node = dead_end
            while not tree_node is None:
                path.insert(0, tree_node.node)
                tree_node = tree_node.parent
            destinations.append(path)

        return destinations




