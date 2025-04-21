# Pair class
class Pair:
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __eq__(self, other):
        return (self.first == other.first and self.second == other.second)

# Edge class


class Edge:
    def __init__(self, node_a: str, node_b: str, weight: int):
        self.node_a = node_a
        self.node_b = node_b
        self.weight = weight

    # Two edges are equal if their nodes are the same in any order
    def __eq__(self, other):
        return (self.node_a == other.node_a and self.node_b == other.node_b) or (self.node_a == other.node_b and self.node_b == other.node_a)

    # Returns true if edge has node
    def has_node(self, node: str) -> bool:
        return (self.node_a == node or self.node_b == node)


# Graph


class Graph:
    def __init__(self, edges: list[Edge]):
        self.graph: list[Edge] = edges

    # Creates a new edge with given parameters and adds it to the graph
    # Makes sure that there does not exist another node_a -> node_b (or node_b -> node_a)
    # Returns true on success
    def add_edge(self, node_a: str, node_b: str, weight: int) -> bool:
        new_edge: Edge = Edge(node_a, node_b, weight)
        if self.in_graph(new_edge):
            return False
        else:
            self.graph.append(new_edge)
            return True

    # Returns true if edge is in self.graph
    def in_graph(self, edge: Edge) -> bool:
        return any(map(lambda e: e == edge, self.graph))

    # Runs Djikstra's Algorithm on the graph given a source node
    # Returns a list of pairs of nodes (defined by strings) with their corresponding minimal weight edge path from the source
    def djikstra(self, source: str) -> list[Pair]:
        # initialize empty set of nodes chosen with minimal distance
        sptset: list[str] = []
        # initialize matrix with distances to get to each node
        dist: list[Pair] = create_dist_matrix(self.graph, source)
        while len(sptset) != len(dist):
            # 0. create subset of dist containing all pairs not in sptset
            no_sptset_dist: list[Pair] = []
            for pair in dist:
                if not (pair.first in sptset):
                    no_sptset_dist.append(pair)
            # 1. find min distance node when considering all nodes not already in sptset and add to set
            assert (len(no_sptset_dist) > 0)
            min_pair: Pair = get_minimal_distance(no_sptset_dist)
            sptset.append(min_pair.first)
            # 2. Update distances for all adjacent nodes to min_pair
            dist = update_dist(self.graph, dist, min_pair)

        return dist


def create_dist_matrix(graph: list[Edge], source: str) -> list[Pair]:
    # From a graph and source node, return a list of pairs <str, int> where each node's distance from source is stored
    # Distance is infinity for nodes not the source
    dist_list: list[Pair] = []
    nodes: list[str] = get_all_nodes(graph)
    for node in nodes:
        if node == source:
            dist_list.append(Pair(node, 0))
        else:
            dist_list.append(Pair(node, None))

    return dist_list


def get_minimal_distance(dist_matrix: list[Pair]) -> Pair:
    # Given a distance matrix, return a Pair representing the node with minimal distance, discarding pairs with None distance
    # remove all None distances
    filtered_matrix: list[Pair] = []
    for pair in dist_matrix:
        if (pair.second is not None):
            filtered_matrix.append(pair)

    assert (len(filtered_matrix) > 0)
    min_pair = filtered_matrix[0]

    for pair in filtered_matrix:
        if pair.second < min_pair.second:
            min_pair = pair

    return min_pair


def get_all_nodes(graph: list[Edge]) -> list[str]:
    # From a graph, return a list of all unique nodes
    nodes: list[str] = []
    for edge in graph:
        if not (edge.node_a in nodes):
            nodes.append(edge.node_a)
        if not (edge.node_b in nodes):
            nodes.append(edge.node_b)
    return nodes


def update_dist(graph: list[Edge], dist: list[Pair], pair: Pair) -> list[Edge]:
    # For all adjacent nodes of pair, update their distances in dist
    # find all adjacent nodes
    for edge in graph:
        # update dist for the adjacent node to be equal to dist of pair + weight of edge
        if (edge.node_a == pair.first):
            dist = update_dist_helper(dist, edge.node_b, pair, edge.weight)
        elif (edge.node_b == pair.first):
            dist = update_dist_helper(dist, edge.node_a, pair, edge.weight)
    return dist


def update_dist_helper(dist: list[Pair], dst_node: str, src_pair: Pair, weight: int) -> list[Edge]:
    # Updates dist so that dst_node has a distance of pair distance + weight
    # find dst_node
    for i in range(len(dist)):
        if (dist[i].first == dst_node):
            # update distance if necessary
            new_distance: int = src_pair.second + weight
            if (dist[i].second is None) or (dist[i].second > new_distance):
                dist[i].second = new_distance

    return dist


class Vehicle:
    # Vehicle
    def __init__(self, id: int, start_node: str, end_node: str):
        self.id = id
        self.start_node = start_node
        self.end_node = end_node


# Testing
def print_pairs(list):
    for pair in list:
        print("node: ", pair.first, "distance: ", pair.second)


edge_1 = Edge("a", "b", 1)
edge_2 = Edge("a", "c", 5)
edge_3 = Edge("b", "c", 4)
graph_1 = Graph([edge_1, edge_2, edge_3])
distances_1 = graph_1.djikstra("a")
distances_2 = graph_1.djikstra("b")
distances_3 = graph_1.djikstra("c")
# print_pairs(distances_1)
# print_pairs(distances_2)
# print_pairs(distances_3)

assert (graph_1.add_edge("c", "a", 3)) is False
assert (graph_1.add_edge("a", "c", 3)) is False
assert (graph_1.add_edge("a", "d", 3)) is True
assert (graph_1.add_edge("a", "b", 1)) is False
