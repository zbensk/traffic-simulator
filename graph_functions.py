# Triple class
class Triple:
    def __init__(self, first, second, third):
        self.first = first
        self.second = second
        self.third = third

    def __eq__(self, other):
        return (self.first == other.first and self.second == other.second)

    def __str__(self):
        return "node: " + self.first + " distance: " + str(self.second) + " path: " + print_edge(self.third)


# Edge class


class Edge:
    def __init__(self, node_a: str, node_b: str, weight: int):
        self.node_a = node_a
        self.node_b = node_b
        self.weight = weight

    # Two edges are equal if their nodes are the same in any order
    def __eq__(self, other):
        return (self.node_a == other.node_a and self.node_b == other.node_b) or (self.node_a == other.node_b and self.node_b == other.node_a)

    def __str__(self):
        return self.node_a + " --> " + self.node_b + ": " + str(self.weight)

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
    # Returns a list of triples of nodes (defined by strings) with their corresponding minimal weight edge path from the source (and path)
    def djikstra(self, source: str) -> list[Triple]:
        # initialize empty set of nodes chosen with minimal distance
        sptset: list[str] = []
        # initialize matrix with distances to get to each node
        dist: list[Triple] = create_dist_matrix(self.graph, source)
        while len(sptset) != len(dist):
            # 0. create subset of dist containing all triples not in sptset
            no_sptset_dist: list[Triple] = []
            for triple in dist:
                if not (triple.first in sptset):
                    no_sptset_dist.append(triple)
            # 1. find min distance node when considering all nodes not already in sptset and add to set
            assert (len(no_sptset_dist) > 0)
            min_triple: Triple = get_minimal_distance(no_sptset_dist)
            sptset.append(min_triple.first)
            # 2. Update distances for all adjacent nodes to min_triple
            dist = update_dist(self.graph, dist, min_triple)

        return dist


def create_dist_matrix(graph: list[Edge], source: str) -> list[Triple]:
    # From a graph and source node, return a list of triples <str, int> where each node's distance from source is stored
    # Distance is infinity for nodes not the source
    dist_list: list[Triple] = []
    nodes: list[str] = get_all_nodes(graph)
    for node in nodes:
        if node == source:
            dist_list.append(Triple(node, 0, []))
        else:
            dist_list.append(Triple(node, None, []))

    return dist_list


def get_minimal_distance(dist_matrix: list[Triple]) -> Triple:
    # Given a distance matrix, return a Triple representing the node with minimal distance, discarding triples with None distance
    # remove all None distances
    filtered_matrix: list[Triple] = []
    for triple in dist_matrix:
        if (triple.second is not None):
            filtered_matrix.append(triple)

    assert (len(filtered_matrix) > 0)
    min_triple = filtered_matrix[0]

    for triple in filtered_matrix:
        if triple.second < min_triple.second:
            min_triple = triple

    return min_triple


def get_all_nodes(graph: list[Edge]) -> list[str]:
    # From a graph, return a list of all unique nodes
    nodes: list[str] = []
    for edge in graph:
        if not (edge.node_a in nodes):
            nodes.append(edge.node_a)
        if not (edge.node_b in nodes):
            nodes.append(edge.node_b)
    return nodes


def update_dist(graph: list[Edge], dist: list[Triple], triple: Triple) -> list[Edge]:
    # For all adjacent nodes of triple, update their distances in dist
    # find all adjacent nodes
    for edge in graph:
        # update dist for the adjacent node to be equal to dist of triple + weight of edge
        if (edge.node_a == triple.first):
            dist = update_dist_helper(dist, edge.node_b, edge, triple)
        elif (edge.node_b == triple.first):
            dist = update_dist_helper(dist, edge.node_a, edge, triple)
    return dist


def update_dist_helper(dist: list[Triple], dst_node: str, edge: Edge, src_triple: Triple) -> list[Edge]:
    # Updates dist so that dst_node has a distance of triple distance + weight
    # find dst_node
    weight: int = edge.weight
    for i in range(len(dist)):
        if (dist[i].first == dst_node):
            # update distance if necessary
            new_distance: int = src_triple.second + weight
            new_path: list[Edge] = src_triple.third + [edge]
            if (dist[i].second is None) or (dist[i].second > new_distance):
                dist[i].second = new_distance
                # update path taken
                dist[i].third = new_path

    return dist


class Vehicle:
    # Vehicle
    def __init__(self, id: int, start_node: str, end_node: str):
        self.id = id
        self.start_node = start_node
        self.end_node = end_node


# Testing
def print_triples(list: list[Triple]):
    for triple in list:
        print(triple)


def print_edge(list: list[Edge]):
    msg = ""
    for edge in list:
        msg += str(edge) + " "
    return msg


edge_1 = Edge("a", "b", 1)
edge_2 = Edge("a", "c", 5)
edge_3 = Edge("b", "c", 3)
graph_1 = Graph([edge_1, edge_2, edge_3])
distances_1 = graph_1.djikstra("a")
distances_2 = graph_1.djikstra("b")
distances_3 = graph_1.djikstra("c")
print_triples(distances_1)
# print_triples(distances_2)
# print_triples(distances_3)

assert (graph_1.add_edge("c", "a", 3)) is False
assert (graph_1.add_edge("a", "c", 3)) is False
assert (graph_1.add_edge("a", "d", 3)) is True
assert (graph_1.add_edge("a", "b", 1)) is False
