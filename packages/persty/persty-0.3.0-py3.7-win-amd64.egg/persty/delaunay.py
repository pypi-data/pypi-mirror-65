import persty.minibox
import persty.c_util
from scipy.spatial.distance import chebyshev

def edges(points):
    """Delaunay edges on d-dimensional points

    Find the Delaunay edges iterating on all possible
    pairs of indices in `points`.

    Parameters
    ----------
    points: list of `n` lists containing `d` floats each
        The list of d-dimensional points.

    Return
    ------
    delaunay_edges: list of pairs of integers
        The indices of elements in `points` forming a
        Delaunay edge.
    """
    minibox_edges = persty.minibox.edges(points)
    delaunay_edges = []

    list_debug = [] # [1, 6], [3, 9] [8, 9]
    for i, j in minibox_edges:
        p = points[i]
        q = points[j]
        r = chebyshev(p, q) / 2.0
        A = persty.c_util.get_A([p, q])
        hyperrect = [A]
        for index in range(len(points)):
            if index == i or index == j:
                continue
            y = points[index]
            hyperrect = persty.c_util.update_list_hyperrectangles([hyperrect, y, r])
            if len(hyperrect) == 0:
                break

        if len(hyperrect) != 0:
            delaunay_edges.append((i,j))
    return delaunay_edges
