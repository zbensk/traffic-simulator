# Pair class
class Pair:
    def __init__(self, first, second):
        self.first = first
        self.second = second

# Edge class
class Edge:
    def __init__(self, node_a: str, node_b:str, weight:int):
        self.node_a = node_a
        self.node_b = node_b
        self.weight = weight

    # Two edges are equal if their nodes are the same in any order
    def __eq__(self, other):
        return (self.node_a == other.node_a and self.node_b == other.node_b) or (self.node_a == other.node_b and self.node_b == other.node_a)

# Graph
class Graph:
    def __init__(self, edges:list[Edge]):
        self.graph:list = edges
    
    # Creates a new edge with given parameters and adds it to the graph
    # Makes sure that there does not exist another node_a -> node_b (or node_b -> node_a)
    # Returns true on success
    def add_edge(self, node_a: str, node_b: str, weight: int) -> bool:
        new_edge:Edge = Edge(node_a, node_b, weight)
        if self.in_graph(new_edge):
            return False
        else:
            self.graph.append(new_edge)
            return True
    
    # Returns true if edge is in self.graph
    def in_graph(self, edge:Edge) -> bool:
        return any(map(lambda e: e == edge, self.graph))
    
    # Runs Djikstra's Algorithm on the graph given a source node
    # Returns a list of pairs of nodes (defined by strings) with their corresponding minimal weight edge path from the source 
    def djikstra(self, source: str) -> list[Pair]:
        ...


# Vehicle
class Vehicle:
    def __init__(self, id:int, start_node:str, end_node:str):
        self.id = id
        self.start_node = start_node
        self.end_node = end_node


# Testing
edge_1 = Edge("a", "b", 1)
edge_2 = Edge("a", "c", 5)
edge_3 = Edge("b", "c", 4)
graph_1 = Graph([edge_1, edge_2, edge_3])

assert(graph_1.add_edge("c", "a", 3)) is False
assert(graph_1.add_edge("a", "c", 3)) is False
assert(graph_1.add_edge("a", "d", 3)) is True
assert(graph_1.add_edge("a", "b", 1)) is False