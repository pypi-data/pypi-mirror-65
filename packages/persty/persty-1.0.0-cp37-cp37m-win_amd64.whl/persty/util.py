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
    sim_tree.expansion(max_simplex_dim)

    return sim_tree
