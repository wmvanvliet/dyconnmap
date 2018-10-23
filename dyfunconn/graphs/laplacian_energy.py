# -*- coding: utf-8 -*-
""" Laplcian Energy

The Laplcian energy (LE) for a graph :math:`G` is computed as

.. math::
    ξ(A_1, A_2 ; t) = ‖exp⁡(-tL_1 ) - exp⁡(-tL_2 )‖_F^2

Where :math:``\mu_i` denote the eigenvalue associated with the node of the Laplcian
matrix of :math:`G` (Laplcian spectrum) and :math:`\frac{2m}{n}` the average vertex degree.

For a details please go through the original work (Gutman2006_).

|

-----
.. [Gutman2006] Gutman, I., & Zhou, B. (2006). Laplacian energy of a graph. Linear Algebra and its applications, 414(1), 29-37.

"""
# Author: Avraam Marimpis <avraam.marimpis@gmail.com>"


import numpy as np
import scipy
from scipy import sparse


def laplacian_energy(mtx):
    """ Laplacian Energy


    Parameters
    ----------
    mtx : array-like, shape(N, N)
        Symmetric, weighted and undirected connectivity matrix.


    Returns
    -------
    le : float
        The Laplacian Energy.
    """

    compute_degree = None
    try:
        import bct
        compute_degree = bct.degrees_und
    except:
        compute_degree = __impl_degree

    lmtx = scipy.sparse.csgraph.laplacian(mtx)
    w, v = np.linalg.eig(lmtx)
    avg_degree = np.mean(compute_degree(mtx))
    le = np.sum(np.abs(w - avg_degree))

    return le

def __impl_degree(mtx):
    bool_mtx = mtx.astype(np.bool)
    int_mtx = bool_mtx.astype(np.int32)

    degree = np.sum(int_mtx, axis=0)

    return degree

if __name__ == '__main__':
    rng = np.random.RandomState(1)
    mtx = rng.rand(5, 5)

    mtx = np.abs(mtx)
    mtx[1, 3] = 0.0
    mtx[3, 1] = 0.0
    mtx[4, 2] = 0.0
    mtx[2, 4] = 0.0

    mtx = mtx + mtx.T
    mtx = mtx / 2.0
    np.fill_diagonal(mtx, 1.0)

    le = laplacian_energy(mtx)
    print(le)