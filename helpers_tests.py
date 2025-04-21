from graph_functions import *

# Constants
edge_1 = Edge("a", "b", 1)
edge_2 = Edge("a", "c", 5)
edge_3 = Edge("b", "c", 4)
graph_1 = Graph([edge_1, edge_2, edge_3])

dist_1 = create_dist_matrix(graph_1.graph, "a")
dist_2 = create_dist_matrix(graph_1.graph, "b")


def lists_pairs_equal(list1, list2) -> bool:
    if (len(list1) != len(list2)):
        return False

    for i in range(len(list1)):
        if list1[i] != list2[i]:
            print("item 1:", list1[i].first, list1[i].second,
                  " item 2:", list2[i].first, list2[i].second)
            return False
    return True


def test_create_dist_matrix():
    assert (lists_pairs_equal(dist_1, [
        Pair("a", 0), Pair("b", None), Pair("c", None)]))
    assert (lists_pairs_equal(dist_2, [
        Pair("a", None), Pair("b", 0), Pair("c", None)]))
    assert (lists_pairs_equal(create_dist_matrix(graph_1.graph, "c"), [
        Pair("a", None), Pair("b", None), Pair("c", 0)]))


def test_get_minimal_distance():
    assert (get_minimal_distance(dist_1) == Pair("a", 0))
    assert (get_minimal_distance(dist_2) == Pair("b", 0))


def test_update_dist():
    # new_dist = update_dist(graph_1.graph, dist_1, Pair("a", 0))
    # for pair in new_dist:
    #     print(pair.first, pair.second)
    assert (lists_pairs_equal(update_dist(graph_1.graph, dist_1, Pair("a", 0)),
                              [Pair("a", 0), Pair("b", 1), Pair("c", 5)]))
    ...


def test_update_dist_helper():
    # new_dist = update_dist_helper(dist_1, "b", Pair("a", 0), 1)
    # for pair in new_dist:
    #     print(pair.first, pair.second)
    assert (lists_pairs_equal(update_dist_helper(dist_2, "a", Pair("b", 0), 1),
            [Pair("a", 1), Pair("b", 0), Pair("c", None)]))


def test_all():
    test_create_dist_matrix()
    test_get_minimal_distance()
    test_update_dist()
    test_update_dist_helper()


test_all()
