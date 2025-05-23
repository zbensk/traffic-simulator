import random

# Triple class


class Triple:
    def __init__(self, first, second, third):
        self.first = first
        self.second = second
        self.third = third

    def __eq__(self, other):
        return (self.first == other.first and self.second == other.second)

    def __str__(self):
        return "node: " + self.first + " distance: " + str(self.second) + " path: " + str_edges(self.third)


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
    def __init__(self, edges: list[Edge] = None, num_vertices: int = None, max_weight: int = None):
        if (edges is None):
            if (num_vertices < 2):
                num_vertices = 2
            if (max_weight < 1):
                max_weight = 1
            self.generate_graph(num_vertices, max_weight)
        else:
            self.graph: list[Edge] = edges

    def __str__(self):
        msg = ""
        for edge in self.graph:
            msg += str(edge) + "\n"

        return msg

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

    def get_shortest_path(self, source: str, dest: str) -> Triple:
        # From the graph, given a source and destination node, run djikstras to determine the shortest path between the nodes and return that triple
        djikstra_output: list[Triple] = self.djikstra(source)
        # Filter to find triple with dest and return
        for triple in djikstra_output:
            if triple.first == dest:
                return triple

    def update_edge(self, edge: Edge, new_weight: int) -> None:
        # Updates edge in the graph to have the weight specified by new_weight
        for e in self.graph:
            if e == edge:
                e.weight = new_weight

    def generate_graph(self, num_vertices, max_weight) -> None:
        # Generates a random graph with given parameters and sets it to self.graph
        # 1. generate a connected graph by shuffling a list of vertices
        # 2. n = randomly determine how many more edges to add (determine upper bound st graph models a city)
        # 3. randomly generate more edges (n) to finalize graph with some redundancy
        connected_graph = generate_connected_graph(num_vertices, max_weight)
        # generate n to n*2 extra vertices
        num_add = random.randint(num_vertices, num_vertices * 2)
        self.graph = add_edges(
            connected_graph, num_vertices, num_add, max_weight)


def add_edges(connected_graph: list[Edge], num_vertices: int, num_add: int, max_weight: int) -> list[Edge]:
    # Determines random vertices to add num_add edges to with max_weight
    vertices: list[str] = []
    for i in range(num_vertices):
        vertices.append(str(i + 1))

    for i in range(num_add):
        rand_node_a: str = str(random.randint(1, num_vertices))
        while True:
            rand_node_b: str = str(random.randint(1, num_vertices))
            if (rand_node_b != rand_node_a):
                break

        rand_weight = random.randint(1, max_weight)
        edge = Edge(rand_node_a, rand_node_b, rand_weight)
        connected_graph.append(edge)

    return connected_graph


def generate_connected_graph(num_vertices: int, max_weight: int) -> list[Edge]:
    # Generate a random connected graph with nodes numbered up to num_vertices and weights up to max_weight
    graph: list[Edge] = []
    vertices: list[str] = []
    for i in range(num_vertices):
        vertices.append(str(i + 1))

    random.shuffle(vertices)
    for i in range(len(vertices) - 1):
        rand_weight = random.randint(1, max_weight)
        edge = Edge(vertices[i], vertices[i + 1], rand_weight)
        graph.append(edge)

    return graph


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


def copy_path(path: list[Edge]) -> list[Edge]:
    # Given a list of edges, create a deep copy so that modifying items in path don't affect the new list
    new_path: list[Edge] = []
    for edge in path:
        new_path.append(Edge(edge.node_a, edge.node_b, edge.weight))

    return new_path


class Vehicle:
    # Vehicle
    def __init__(self, id: int, start_node: str, end_node: str, graph: Graph):
        self.id = id
        self.start_node = start_node
        self.end_node = end_node
        # Get shortest path and update graph weights afterwards (increase by 1 to reflect vehicle usage of road)
        self.shortest_path_triple = graph.get_shortest_path(
            self.start_node, self.end_node)
        self.short_dist = self.shortest_path_triple.second
        self.short_path = copy_path(self.shortest_path_triple.third)
        for edge in self.short_path:
            graph.update_edge(edge, edge.weight + 1)


# Testing
def print_triples(list: list[Triple]):
    for triple in list:
        print(triple)


def str_edges(list: list[Edge]) -> str:
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
# print_triples(distances_1)
# print_triples(distances_2)
# print_triples(distances_3)
shortest_path_1 = graph_1.get_shortest_path("a", "c")
# print(shortest_path_1)

assert (graph_1.add_edge("c", "a", 3)) is False
assert (graph_1.add_edge("a", "c", 3)) is False
assert (graph_1.add_edge("a", "d", 3)) is True
assert (graph_1.add_edge("a", "b", 1)) is False

# Vehicle testing
# print(graph_1)  # initial graph
# vehicle_1 = Vehicle(0, "a", "c", graph_1)
# print(vehicle_1.short_dist)
# print(str_edges(vehicle_1.short_path))
# print(graph_1)  # graph after has weights along shortest path updated
# # now a new vehicle on the same route will take a different path since weights are updated
# vehicle_2 = Vehicle(1, "a", "c", graph_1)
# print(vehicle_2.short_dist)
# print(str_edges(vehicle_2.short_path))
# print(graph_1)

graph_2 = Graph(num_vertices=5, max_weight=5)
# print(graph_2)
# print_triples(graph_2.djikstra("1"))

graph_3 = Graph(num_vertices=100, max_weight=10)
print(graph_3)
