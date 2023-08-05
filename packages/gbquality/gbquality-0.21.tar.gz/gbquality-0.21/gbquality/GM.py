# GM.m

import numpy as np
from numba import njit, numba
from scipy.stats import spearmanr


def global_judge(X, Y, k):
    """
    Please cite: "Deyu Meng, Yee Leung, Zongben Xu.
    Evaluating nonlinear dimensionality reduction based on its local
    and global quality assessments, Neurocomputing, 2011, 74(6): 941-948."

    The code is written by Deyu Meng & adapted by Andrew Lensen

    :param X: Original data (dim1*num)
    :param Y: Embedded data (dim2*num): dim2 < dim1
    :param k: Neighborhood size
    :return global quality in [0,1].
    """
    leaf_indices, leaf_dists, centre_index = compute_x_leaves(X, k)
    return global_judge_x_precomputed(leaf_indices, leaf_dists, centre_index, Y)


def global_judge_x_precomputed(leaf_indices, x_dists, centre_index, Y):
    """
    :param leaf_indices: Indices of all the leaves of the SPT (size 1*L)
    :param x_dists: Dists along the SPT from centre to each of the leaves (1*L)
    :param centre_index: Index of the approximate circumcenter of X
    :param Y: Embedded data (dim*num)
    :return global quality in [0,1].
    """

    # we only need the relevant distances
    y_dists = leaves_to_centre_euclidean(Y.T, centre_index, np.asarray(leaf_indices))

    global_score = (1 + spearmanr(x_dists, y_dists)[0]) / 2
    return global_score

@njit(fastmath=True)
def leaves_to_centre_euclidean(_Y, centre_index, leaf_indices):
    y_dists = np.zeros(len(leaf_indices))
    for i, leaf in enumerate(leaf_indices):
        y_dists[i] = np.linalg.norm(_Y[centre_index] - _Y[leaf])
    return y_dists


@njit(fastmath=True)
def euclidean_distance_2(X, Y):
    """
    Just let numba make this efficient for us!
    :param X: data (num*dim)
    :param Y: data2 (num*dim2)
    """
    X_N = X.shape[0]
    Y_N = Y.shape[0]

    dists = np.zeros((X_N, Y_N), np.float64)
    for i in range(X_N):
        for j in range(Y_N):
            dists[i][j] = np.linalg.norm(X[i] - Y[j])
    return dists


@njit(fastmath=True)
def euclidean_distance(X):
    """
    Just let numba make this efficient for us!
    :param X: data (num*dim)
    """
    N = X.shape[0]
    dists = np.zeros((N, N), np.float64)
    for i in range(N):
        for j in range(N):
            dists[i][j] = np.linalg.norm(X[i] - X[j])
    # just in case..
    np.fill_diagonal(dists, 0.)
    return dists


@njit(fastmath=True)
def compute_x_leaves(X, K):
    """
    All the heavy pre-processing on the source data. Only needs to be run once, so it's not particularly efficient!
    :param X: Original data (dim1*num)
    :param K: Neighbourhood size
    :return: leaf_indices, leaf_dists, centre_index
    """
    # matlab's L2_distance converts feature-major to instance-major
    pairwise_x = euclidean_distance(X.T)
    N = pairwise_x.shape[0]
    INF = 1000 * np.amax(pairwise_x) * N  # effectively infinite distance
    # ind = np.argsort(pairwise_x, axis=1)[:, :K + 1]
    ind = np.empty((N, K + 1), dtype=numba.int_)
    for i in range(N):
        ind[i, :] = np.argsort(pairwise_x[i])[:K + 1]
    _D = np.full((N, N), INF)
    np.fill_diagonal(_D, 0.)
    # _D = np.zeros((N, N))
    for ii in range(N):
        # I think this is right for nx?
        for val in ind[ii]:
            _D[ii, val] = pairwise_x[ii, val]
        # _D[ii, ind[ii]] = pairwise_x[ii, ind[ii]]
    pairwise_x = _D
    pairwise_x = np.minimum(pairwise_x, pairwise_x.T)
    # CHECK
    # otherwise it uses the same list for each row...
    PP = []
    for i in range(N):
        row = []
        for j in range(N):
            row.append([i, j])
        PP.append(row)
    # shortest paths
    for k in range(N):
        for ii in range(N):
            for jj in range(N):
                if pairwise_x[ii, jj] > pairwise_x[ii, k] + pairwise_x[k, jj]:
                    PP[ii][jj] = PP[ii][k][:- 1] + PP[k][jj]
        pairwise_x = np.minimum(pairwise_x,
                                np.repeat(pairwise_x[:, k], N).reshape(N, N) + np.repeat(pairwise_x[k, :], N).reshape(N,
                                                                                                                      N).T)
    spt_dists_x = pairwise_x
    a = np.empty(N)
    for i in range(N):
        a[i] = np.max(pairwise_x[i])
    # a = np.max(pairwise_x,axis=0)
    centre_index = int(np.argmin(a))
    max_dist = np.max(pairwise_x[centre_index, :])
    indices = [x for x in range(N) if x != centre_index]
    candidate_leaves = []
    while len(indices) > 0:
        idx = indices[0]
        idx_path = list(PP[centre_index][idx])
        candidate_leaves.append(idx)
        idx_path.remove(centre_index)

        while len(idx_path) > 1:
            if idx_path[0] in indices:
                # it can't be a leaf
                indices.remove(idx_path[0])
            if idx_path[0] in candidate_leaves:
                # it can't be a leaf
                candidate_leaves.remove(idx_path[0])
            idx_path.remove(idx_path[0])

        indices.remove(idx_path[0])
        idx_path.remove(idx_path[0])
    n_leaves = len(candidate_leaves)
    potential_leaves = []
    final_leaf_indices = []
    k = 0
    for i in range(n_leaves):
        temp_leaf = candidate_leaves[i]
        temp_leaf2 = PP[centre_index][temp_leaf][1]
        if temp_leaf2 in potential_leaves:
            Tempi = potential_leaves.index(temp_leaf2)
            if pairwise_x[centre_index, temp_leaf] > pairwise_x[centre_index, final_leaf_indices[Tempi]]:
                final_leaf_indices[Tempi] = temp_leaf
        elif pairwise_x[centre_index, temp_leaf] > max_dist / 6:
            k = k + 1
            potential_leaves.insert(k, temp_leaf2)
            final_leaf_indices.insert(k, temp_leaf)
    leaf_dists = np.empty(len(final_leaf_indices))
    i = 0
    for j in final_leaf_indices:
        leaf_dists[i] = spt_dists_x[centre_index, j]
        i += 1
    return final_leaf_indices, leaf_dists, centre_index
