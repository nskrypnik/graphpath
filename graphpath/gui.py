# -*- coding: utf-8 *-*

import wx
from graph import Graph, Node
import string


class GraphGuiNode(wx.Panel):

    def __init__(self, parent, x, y, node):
        super(GraphGuiNode, self).__init__(parent, size=(21, 21),
                    pos=(x - 10, y - 10))
        self.color = 'red'
        self.node = node
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_UP, self.on_click)

    def on_click(self, event):
        if self.Parent.state == 'add_link':
            self.Parent.nodes_to_link.append(self)
            if len(self.Parent.nodes_to_link) == 1:
                self.color = 'green'
                self.Refresh()
                self.Parent.first_node_chosen()
            elif len(self.Parent.nodes_to_link) == 2:
                self.Parent.second_node_chosen()
        if self.Parent.state == 'get_directions':
            self.Parent.nodes_to_get_destination.append(self)
            if len(self.Parent.nodes_to_get_destination) == 1:
                self.color = 'green'
                self.Refresh()
            else:
                self.Parent.show_destinations()

    def on_paint(self, event):
        # drow circle on node panel widget
        dc = wx.PaintDC(self)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.SetPen(wx.TRANSPARENT_PEN)
        w, h = self.GetSizeTuple()
        dc.DrawRectangle(0, 0, w, h)
        dc.SetBrush(wx.Brush(self.color))
        dc.SetPen(wx.Pen(self.color, 1))
        dc.DrawCircle(10, 10, 10)
        dc.DrawText(self.node.name, 5, 0)


class GraphPannel(wx.Panel):

    def __init__(self, *args, **kwargs):
        super(GraphPannel, self).__init__(*args, **kwargs)
        self.state = ''
        self.gui_nodes = {}
        self.nodes_to_link = []
        self.nodes_to_get_destination = []
        self.graph = Graph()
        self.Bind(wx.EVT_PAINT, self.redraw)

    def add_new_node(self, event):
        # get here new node name
        letter_idex = len(self.gui_nodes)
        new_letter = string.ascii_uppercase[letter_idex]
        node = Node(new_letter)
        self.graph.add_node(node)
        gui_node = GraphGuiNode(self, event.X, event.Y, node)
        self.gui_nodes[new_letter] = gui_node

        self.Parent.enable_buttons()
        self.state = ''

    def first_node_chosen(self):
        pass

    def show_destinations(self):
        gnode1, gnode2 = self.nodes_to_get_destination
        destinations = self.graph.get_destinations(gnode1.node, gnode2.node)
        result_caption = 'Possible destinations:\n'
        for path in destinations:
            nodes = [node.name for node in path]
            result_caption += "%s\n" % " - ".join(nodes)
        self.Parent.results.Label = result_caption
        self.state = ''
        self.Refresh()
        self.Parent.enable_buttons()
        for gui_node in self.nodes_to_link:
            gui_node.color = 'red'
            gui_node.Refresh()

    def second_node_chosen(self):
        node1, node2 = [g.node for g in self.nodes_to_link]
        node1.add_neighbour(node2)
        node2.add_neighbour(node1)
        for gui_node in self.nodes_to_link:
            gui_node.color = 'red'
            gui_node.Refresh()
        self.nodes_to_link = []
        self.state = ''
        self.Refresh()
        self.Parent.enable_buttons()

    def redraw(self, event):
        """
            Redraw all lines between exiting nodes on Graph Panel
        """
        dc = wx.PaintDC(self)
        dc.SetPen(wx.Pen('red', 1))
        ## Ugly Indian code :/ but fast
        for node in self.graph.nodes:
            for node2 in node.neighbours:
                gnode1 = self.gui_nodes[node.name]
                gnode2 = self.gui_nodes[node2.name]
                x1 = gnode1.Position.x + 10
                y1 = gnode1.Position.y + 10
                x2 = gnode2.Position.x + 10
                y2 = gnode2.Position.y + 10
                dc.DrawLine(x1, y1, x2, y2)

    def clear(self):
        self.graph = Graph()
        for gnode in self.gui_nodes.values():
            gnode.Destroy()
        self.gui_nodes = {}
        self.nodes_to_get_destination = []
        self.nodes_to_link = []
        self.Refresh()

    _actions = {
            'add_node': add_new_node,
        }

    def click(self, event):
        method = self._actions.get(self.state, None)
        if method:
            method(self, event)


class MainWindow(wx.Frame):
    def __init__(self, parent, title):

        class DummyContainer(object):

            def get_items(self):
                return self.__dict__.values()

        super(MainWindow, self).__init__(parent, title=title,
                                                size=(800, 600))
        panel = GraphPannel(self, size=(800, 400), style=wx.TAB_TRAVERSAL)
        self.quote = wx.StaticText(panel,
                label="", pos=(10, 20))
        panel.SetBackgroundColour((230, 230, 230))
        panel.Bind(wx.EVT_LEFT_UP, panel.click)
        self.graph_panel = panel

        self.buttons = DummyContainer()
        self.buttons.addnode = wx.Button(self, label="Add node",
                                                        pos=(0, 400))
        self.buttons.addlink = wx.Button(self, label="Add link",
                                                        pos=(100, 400))
        self.buttons.directions = wx.Button(self,
                                            label="Get directions",
                                            pos=(200, 400))
        self.buttons.clear = wx.Button(self,
                                            label="Clear",
                                            pos=(320, 400))
        self.add_bindings()

        self.results = wx.StaticText(self,
                label="Results should be here", pos=(0, 450))

        self.Show()

    def add_bindings(self):
        self.buttons.addnode.Bind(wx.EVT_BUTTON, self.add_node)
        self.buttons.addlink.Bind(wx.EVT_BUTTON, self.add_link)
        self.buttons.directions.Bind(wx.EVT_BUTTON, self.get_directions)
        self.buttons.clear.Bind(wx.EVT_BUTTON, self.clear)

    def add_node(self, event):
        self.graph_panel.state = 'add_node'
        self.quote.Label = "Click on the panel to add new node"
        self.disable_buttons()

    def clear(self, event):
        self.graph_panel.clear()
        self.results.Label = "Results should be here"

    def add_link(self, event):
        if len(self.graph_panel.gui_nodes) < 2:
            wx.MessageDialog(self, "You should add at least two nodes to be able link them",
                    'Warning', wx.OK | wx.ICON_WARNING).ShowModal()
            return
        self.graph_panel.state = 'add_link'
        self.quote.Label = "Choose one node then another to make link"
        self.disable_buttons()

    def disable_buttons(self):
        for button in self.buttons.get_items():
            button.Disable()

    def enable_buttons(self):
        for button in self.buttons.get_items():
            button.Enable()
        self.quote.Label = ''

    def get_directions(self, event):
        self.graph_panel.state = 'get_directions'
        self.quote.Label = "Choose start node then chose end node to get destinations"
        self.disable_buttons()


def main():
    app = wx.App(False)
    frame = MainWindow(None, "Graph traversal")
    app.MainLoop()


if __name__ == '__main__':
    main()
