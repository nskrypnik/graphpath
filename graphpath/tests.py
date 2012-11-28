# -*- coding: utf-8 *-*

import unittest
import graph


class GraphTestCase(unittest.TestCase):

    graph1 = {
            'a': ['b', 'c', 'd'],
            'b': ['a', 'c', 'd'],
            'c': ['a', 'b', 'd'],
            'd': ['a', 'b', 'c'],
        }

    graph2 = {
            'a': ['b', 'c', 'd'],
            'b': ['a', 'c', 'd', 'e'],
            'c': ['a', 'b', 'd'],
            'd': ['a', 'b', 'c', 'e'],
            'e': ['d', 'b']
        }

    graph3 = {
            'a': ['b', ],
            'b': ['c', 'd', 'a'],
            'c': ['d', 'b', 'e'],
            'd': ['c', 'b'],
            'e': ['c', ]
        }

    def test_import_from_dict(self):
        g = graph.Graph()
        g.import_from_dict(self.graph2)
        node1 = g['a']
        self.assertEqual(node1.neighbours[0].name, 'b')
        self.assertEqual(node1.neighbours[1].name, 'c')
        self.assertEqual(node1.neighbours[2].name, 'd')

        node2 = g['e']
        self.assertEqual(len(node2.neighbours), 2)

    def test_get_destinations_tree(self):
        g = graph.Graph()
        g.import_from_dict(self.graph1)

        node1 = g['a']
        node2 = g['c']
        tree, end_nodes = g.get_destination_tree(node1, node2)
        self.assertEqual(len(end_nodes), 5)

    def test_get_destinations(self):
        g = graph.Graph()
        g.import_from_dict(self.graph1)
        dests = g.get_destinations(g['a'], g['c'])
        self.assertEqual(len(dests), 5)

        g = graph.Graph()
        g.import_from_dict(self.graph2)
        dests = g.get_destinations(g['a'], g['e'])
        self.assertEqual(len(dests), 10)
        for d in dests:
            nds = [node.name for node in d]
            print " - ".join(nds)

        g = graph.Graph()
        g.import_from_dict(self.graph3)
        dests = g.get_destinations(g['e'], g['c'])
        self.assertEqual(len(dests), 1)
        for d in dests:
            nds = [node.name for node in d]
            print " - ".join(nds)

        dests = g.get_destinations(g['e'], g['a'])
        self.assertEqual(len(dests), 2)
        for d in dests:
            nds = [node.name for node in d]
            print " - ".join(nds)

if __name__ == '__main__':
    unittest.main()
