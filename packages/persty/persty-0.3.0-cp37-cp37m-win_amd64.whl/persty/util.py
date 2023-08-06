from itertools import combinations
from scipy.spatial.distance import chebyshev
from gudhi import SimplexTree
from numpy import max as npmax
from numpy import fromiter

def clique_triangles(edges, number_points, dimension=2):
    """Return the clique triangles on `edges`

    Parameters
    ----------
    edges: list pairs of indices, list of list of int
        The edges of a graph built on some finite set of points
    number_points: int
        The number of vertices of the graph to which the edges belong
    dimension: int >=2
        Dimension of clique simplices returned

    Return
    ------
    clique_triangles: list of list of int
        The clique triangles on the given edges

    """

    dict_graph = {i: list() for i in range(number_points)}
    for i, j in edges:
        dict_graph[i].append(j)
        dict_graph[j].append(i)
    dict_graph = {key: set(value) for key, value in dict_graph.items()}

    triangles = set()
    for i, j in edges:
        for el in dict_graph[i]:
            if el in dict_graph[j]:
                triangles.add(tuple(sorted([i, j, el])))
    return list(triangles)


def clique_simplices(edges, number_points, dimension=2):
    """Return the clique simplices on `edges`

    Parameters
    ----------
    edges: list pairs of indices, list of list of int
        The edges of a graph built on some finite set of points
    number_points: int
        The number of vertices of the graph to which the edges belong
    dimension: int >=2
        Dimension of clique simplices returned

    Return
    ------
    clique_simplices: list of list of int
        The cliques on the given edges

    """
    edges = set(edges)
    all_simplices = list(combinations(range(number_points), dimension+1))
    edges_in_simplex = list(combinations(range(dimension+1), 2))
    simplices = []
    not_found = False

    for sim in all_simplices:
        not_found = False
        for e in edges_in_simplex:
            v1, v2 = sim[e[0]], sim[e[1]]
            if (v1, v2) not in edges:
                not_found = True
                break
        if not not_found:
            simplices.append(sim)
    return simplices

def make_gudhi_simplex_tree(points, edges, max_simplex_dim=2, metric=chebyshev):
    """Returns the `gudhi.SimplexTree()` object containing all simplices up to dimension `max_sim_dim`

    Parameters
    ----------
    points: list of list of floats
    """
    sim_tree = SimplexTree()
    vertices = list(range(len(points)))

    for v in vertices:
        sim_tree.insert(simplex=[v], filtration=0.0)
    for e in edges:
        p, q = points[e[0]], points[e[1]]
        sim_tree.insert(simplex=e, filtration=metric(p, q))

    for k in range(2, max_simplex_dim+1):
        if k == 2:
            simplices = clique_triangles(edges, len(points), k)
        else:
            simplices = clique_simplices(edges, len(points), k)

        edges_in_simplices = list(combinations(range(k+1), 2))
        for sim in simplices:
            iterable = (metric(points[sim[i]], points[sim[j]])
                        for i, j in edges_in_simplices)
            distances = fromiter(iterable, float)
            sim_tree.insert(simplex=sim, filtration=npmax(distances))

    return sim_tree
