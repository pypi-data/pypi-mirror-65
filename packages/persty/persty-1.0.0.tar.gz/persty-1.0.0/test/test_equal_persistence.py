import numpy as np
import persty.minibox
import persty.delaunay
import persty.util
from scipy.spatial.distance import chebyshev

def sorted_pairs_from_gudhi(diag, dim=1):
    diag = np.array(diag)
    new_diag = np.array([list(el[1])
                             for el in diag
                                 if el[0] == dim])
    if len(new_diag) == 0:
        sorted_indices = []
    else:
        sorted_indices = np.argsort(new_diag[:,1])
    return new_diag[sorted_indices]

def test_equal_diagrams_0_1():
    np.random.seed(0)
    points = np.random.rand(200, 3).tolist()

    minibox_edges = persty.minibox.edges(points)
    delaunay_edges = persty.delaunay.edges(points)

    minibox_sim_tree = persty.util.make_gudhi_simplex_tree(points,
                                                           minibox_edges,
                                                           max_simplex_dim=2,
                                                           metric=chebyshev)
    delaunay_sim_tree = persty.util.make_gudhi_simplex_tree(points,
                                                           delaunay_edges,
                                                            max_simplex_dim=2,
                                                            metric=chebyshev)
    minibox_dgms  = minibox_sim_tree.persistence()
    delaunay_dgms = delaunay_sim_tree.persistence()

    minibox_dgm0 = sorted_pairs_from_gudhi(minibox_dgms, 0)
    minibox_dgm1 = sorted_pairs_from_gudhi(minibox_dgms, 1)
    delaunay_dgm0 = sorted_pairs_from_gudhi(delaunay_dgms, 0)
    delaunay_dgm1 = sorted_pairs_from_gudhi(delaunay_dgms, 1)

    equal_dgm0 = np.isclose(minibox_dgm0, delaunay_dgm0).all()
    equal_dgm1 = np.isclose(minibox_dgm1, delaunay_dgm1).all()

    assert equal_dgm0 and equal_dgm1
