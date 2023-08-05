# GM.m

import numpy as np
from numba import njit
from numba.typed import List
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
    leaf_indices, leaf_geodesic_dists, centre_index = compute_x_leaves(X, k)
    return global_judge_x_precomputed(leaf_indices, leaf_geodesic_dists, centre_index, Y)


def global_judge_x_precomputed(leaf_indices, x_geodesic_dists, centre_index, Y):
    """
    :param leaf_indices: Indices of all the leaves of the SPT (size 1*L)
    :param x_geodesic_dists: Dists along the SPT from centre to each of the leaves (1*L)
    :param centre_index: Index of the approximate circumcenter of X
    :param Y: Embedded data (dim*num)
    :return global quality in [0,1].
    """

    # we only need the relevant distances
    y_euclidean_dists = leaves_to_centre_euclidean(Y.T, centre_index, np.asarray(leaf_indices))

    global_score = (1 + spearmanr(x_geodesic_dists, y_euclidean_dists)[0]) / 2
    return global_score


@njit(fastmath=True)
def leaves_to_centre_euclidean(Y_t, centre_index, leaf_indices):
    y_dists = np.zeros(len(leaf_indices))
    for i, leaf in enumerate(leaf_indices):
        y_dists[i] = np.linalg.norm(Y_t[centre_index] - Y_t[leaf])
    return y_dists



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


def brute_compute_minimum_K(X, max_k=None):
    """

    :param X: data (num*dim)
    :param max_k: Optional.
    :return: minimal K such that all points are in the same connected component.
    """
    # matlab's L2_distance converts feature-major to instance-major
    pairwise_euclidean_x = euclidean_distance(X.T)
    if not max_k:
        # hmm...
        max_k = int(np.ceil(np.sqrt(pairwise_euclidean_x.shape[0])))
        print('Defaulting to max-K of ' + str(max_k))
    # doesn't make sense to be any less.
    for K in range(1, max_k):
        paths, pairwise_geodesic_x = compute_paths(pairwise_euclidean_x, K)
        _isinf = np.isinf(pairwise_geodesic_x)
        if not _isinf.any():
            return K, pairwise_geodesic_x, paths
        else:
            missing = np.sum(_isinf)
            size = pairwise_geodesic_x.size
            print('{} of {} ({:2f}%) not connected for K of {}.'.format(missing, size, missing * 100 / size, K))
    raise ValueError('No valid K found for given X')


@njit(fastmath=True)
def compute_x_leaves(X, K, pairwise_geodesic_x=None, paths=None):
    """
    All the heavy pre-processing on the source data. Only needs to be run once, so it's not particularly efficient!
       :param X: Original data (dim1*num)
    :param K: Neighbourhood size
    :param pairwise_geodesic_x: Optional matrix of pairwise Euclidean distances.
    :param paths: Optional paths between each pair of instances.
    :return: leaf_indices, leaf_dists, centre_index
    """
    # matlab's L2_distance converts feature-major to instance-major
    if pairwise_geodesic_x is None:
        pairwise_euclidean_x = euclidean_distance(X.T)
        paths, pairwise_geodesic_x = compute_paths(pairwise_euclidean_x, K)

    return compute_leaves_fast(paths, pairwise_geodesic_x)


@njit(fastmath=True)
def compute_leaves_fast(paths, pairwise_geodesic):
    N = pairwise_geodesic.shape[0]
    a = np.empty(N)
    for i in range(N):
        a[i] = np.max(pairwise_geodesic[i])

    centre_index = int(np.argmin(a))
    max_dist = np.max(pairwise_geodesic[centre_index, :])
    indices = [x for x in range(N) if x != centre_index]
    candidate_leaves = []
    while len(indices) > 0:
        idx = indices[0]
        idx_path = list(paths[centre_index][idx])
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
        temp_leaf2 = paths[centre_index][temp_leaf][1]
        if temp_leaf2 in potential_leaves:
            temp_i = potential_leaves.index(temp_leaf2)
            if pairwise_geodesic[centre_index, temp_leaf] > pairwise_geodesic[centre_index, final_leaf_indices[temp_i]]:
                final_leaf_indices[temp_i] = temp_leaf
        elif pairwise_geodesic[centre_index, temp_leaf] > max_dist / 6:
            k = k + 1
            potential_leaves.insert(k, temp_leaf2)
            final_leaf_indices.insert(k, temp_leaf)
    leaf_geodesic_dists = np.empty(len(final_leaf_indices))
    i = 0
    for j in final_leaf_indices:
        leaf_geodesic_dists[i] = pairwise_geodesic[centre_index, j]
        i += 1
    return final_leaf_indices, leaf_geodesic_dists, centre_index


@njit(fastmath=True)
def compute_paths(pairwise_euclidean, K):
    N = pairwise_euclidean.shape[0]
    # INF = 1000 * np.amax(pairwise_x) * N  # effectively infinite distance
    # ind = np.argsort(pairwise_x, axis=1)[:, :K + 1]
    ind = np.empty((N, K + 1), dtype=np.int_)
    for i in range(N):
        ind[i, :] = np.argsort(pairwise_euclidean[i])[:K + 1]
    INF = 1000 * np.amax(pairwise_euclidean) * N  # effectively infinite distance
    pairwise_geodesic = np.full((N, N), np.inf)
    np.fill_diagonal(pairwise_geodesic, 0.)
    # geodesic_dists = np.zeros((N, N))
    for ii in range(N):
        # I think this is right for nx?
        for val in ind[ii]:
            pairwise_geodesic[ii, val] = pairwise_euclidean[ii, val]
        # geodesic_dists[ii, ind[ii]] = pairwise_x[ii, ind[ii]]
    pairwise_geodesic = np.minimum(pairwise_geodesic, pairwise_geodesic.T)
    # CHECK
    # otherwise it uses the same list for each row...
    paths = List()
    for i in range(N):
        row = List()
        for j in range(N):
            row.append([i, j])
        paths.append(row)
    # shortest paths
    for k in range(N):
        for ii in range(N):
            for jj in range(N):
                if pairwise_geodesic[ii, jj] > pairwise_geodesic[ii, k] + pairwise_geodesic[k, jj]:
                    paths[ii][jj] = paths[ii][k][:- 1] + paths[k][jj]
        pairwise_geodesic = np.minimum(pairwise_geodesic, np.repeat(pairwise_geodesic[:, k], N).reshape(N, N) + np.repeat(pairwise_geodesic[k, :], N).reshape(N, N).T)
    return paths, pairwise_geodesic
