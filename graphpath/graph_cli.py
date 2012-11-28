# -*- coding: utf-8 *-*

from optparse import OptionParser
from graph import Graph
import sys

parser = OptionParser('Usage: %prog -f<graph description> '\
                            '-s<source node> -d<destination node>')
parser.add_option("-f", "--file", dest="filename",
                  help="file with graph description")
parser.add_option("-s", "--start",
                  dest="start", help="Start node")
parser.add_option("-d", "--destination",
                  dest="destination", help="Destination node")


def main():
    (options, args) = parser.parse_args()
    if not options.filename:
        print "You should specify file with graph description"
        sys.exit()
    if not options.start:
        print "You should specify start node"
        sys.exit()
    if not options.destination:
        print "You should specify destination node"
        sys.exit()

    graph = Graph()
    graph.load_from_file(options.filename)
    node1 = graph.get(options.start)
    if not node1:
        print "Wrong start node name"
        sys.exit(-1)
    node2 = graph.get(options.destination)
    if not node2:
        print "Wrong destination node name"
        sys.exit(-1)

    destinations = graph.get_destinations(node1, node2)

    for path in destinations:
            nodes = [node.name for node in path]
            print " - ".join(nodes)

if __name__ == '__main__':
    main()
