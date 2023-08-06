import numpy as np
import persty.delaunay
import persty.util
from scipy.spatial.distance import chebyshev
from time import time

def test_compute_persistence_delaunay():
    start = time()
    np.random.seed(0)
    points = np.random.rand(100, 3).tolist()
    delaunay_edges = persty.delaunay.edges(points)
    simplex_tree = persty.util.make_gudhi_simplex_tree(points,
                                                       delaunay_edges,
                                                       max_simplex_dim=2,
                                                       metric=chebyshev)
    persistence_diagrams = simplex_tree.persistence(homology_coeff_field=2,
                                                    persistence_dim_max=False)
    assert len(persistence_diagrams) == 151


if __name__ == "__main__":
    start = time()
    np.random.seed(0)
    points = np.random.rand(100, 3).tolist()
    print("Points done")

    delaunay_edges = persty.delaunay.edges(points)
    print("Delaunay edges done")

    simplex_tree = persty.util.make_gudhi_simplex_tree(points,
                                                       delaunay_edges,
                                                       max_simplex_dim=2,
                                                       metric=chebyshev)
    print("Simplex tree done")

    persistence_diagrams = simplex_tree.persistence(homology_coeff_field=2,
                                                    persistence_dim_max=False)
    print("Diagrams done\n")
    print(f"The persistence diagrams contain {len(persistence_diagrams)} points "
           "in dimensions zero and one.")

    end = time()
    print(f"Total elapsed time: {end - start: .3f} seconds.")
