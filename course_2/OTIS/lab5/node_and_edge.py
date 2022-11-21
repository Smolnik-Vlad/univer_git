class Node:
    def __init__(self, name, coord):
        self.name = name
        self.coord = coord
        self.edge=[]


class Edge:
    def __init__(self, node_1: Node, node_2: Node, direction: str):
        self.node_1 = node_1
        self.node_2 =node_2
        self.direction = direction


