"""Section 3: vocabulary tree built with hierarchical k-means.

Run:    python vocab_tree.py
Use:    from vocab_tree import hi_kmeans, add_database, assign_leaves
        tree = hi_kmeans(desc, b=5, depth=7)
        add_database(tree, desc, obj)      # fills the leaves (inverted files + idf)
        leaves = assign_leaves(tree, query_desc)
"""
import time

import numpy as np
from scipy import sparse
from sklearn.cluster import KMeans


class Node:
    """3(a): every node stores the center of its cluster. A query descriptor
    compares itself with the b child centers and moves to the nearest one."""

    def __init__(self, center):
        self.center = center        # (128,) float32
        self.children = []          # empty at a leaf
        self.leaf_id = -1           # 0..n_leaves-1 at a leaf


class Tree:
    def __init__(self, root, b, depth):
        self.root, self.b, self.depth = root, b, depth
        self.n_leaves = 0
        # 3(c), filled by add_database():
        self.inv = None             # (n_leaves, n_objects) counts: how often each object's features land in each leaf
        self.idf = None             # (n_leaves,) ln(N / N_i), N_i = objects that reach leaf i
        self.object_ids = None      # object id of each column in inv


def hi_kmeans(data, b, depth, seed=0):
    """Build the tree. data: (N, 128) SIFT descriptors of the database objects."""
    data = np.asarray(data, np.float32)
    root = Node(data.mean(axis=0))
    tree = Tree(root, b, depth)
    _split(tree, root, data, depth, seed)
    return tree


def _split(tree, node, data, levels_left, seed):
    # Stop when the tree is deep enough or there are too few points to form b clusters.
    if levels_left == 0 or len(data) < tree.b:
        node.leaf_id = tree.n_leaves
        tree.n_leaves += 1
        return
    km = KMeans(n_clusters=tree.b, n_init=1, random_state=seed).fit(data)
    for k in range(tree.b):
        child = Node(km.cluster_centers_[k].astype(np.float32))
        node.children.append(child)
        _split(tree, child, data[km.labels_ == k], levels_left - 1, seed)


def assign_leaves(tree, desc):
    """Push descriptors down the tree, b distances per level. Returns leaf id per descriptor."""
    desc = np.asarray(desc, np.float32)
    leaf = np.empty(len(desc), np.int64)
    stack = [(tree.root, np.arange(len(desc)))]
    while stack:
        node, idx = stack.pop()
        if not node.children:
            leaf[idx] = node.leaf_id
            continue
        centers = np.stack([c.center for c in node.children])
        # squared euclidean distance to each child center, pick the nearest
        d = ((desc[idx, None, :] - centers[None]) ** 2).sum(-1)
        nearest = d.argmin(1)
        for k, child in enumerate(node.children):
            sel = idx[nearest == k]
            if len(sel):
                stack.append((child, sel))
    return leaf


def add_database(tree, desc, obj):
    """3(c): store in the leaves what TF-IDF needs.
    inv[i, j] = number of features of object j in leaf i (term frequency counts)
    idf[i]    = ln(N / N_i), rare leaves count more"""
    leaf = assign_leaves(tree, desc)
    tree.object_ids, col = np.unique(obj, return_inverse=True)
    tree.inv = sparse.csr_matrix(
        (np.ones(len(leaf)), (leaf, col)), shape=(tree.n_leaves, len(tree.object_ids)))
    n_i = np.diff((tree.inv > 0).tocsr().indptr)          # objects per leaf
    tree.idf = np.log(len(tree.object_ids) / np.maximum(n_i, 1))
    return leaf


if __name__ == "__main__":
    from extract import load_features

    server = load_features("server")
    for b, depth in [(4, 3), (4, 5), (5, 7)]:
        t0 = time.time()
        tree = hi_kmeans(server["desc"], b, depth)
        t_build = time.time() - t0
        add_database(tree, server["desc"], server["obj"])
        used = np.diff(tree.inv.indptr) > 0
        print(f"b={b} depth={depth}: {tree.n_leaves:,} leaves (max {b ** depth:,}), "
              f"{used.sum():,} non-empty, built in {t_build:.0f} s")
        print(f"   distances per descriptor: tree {b * depth}, flat vocabulary {b ** depth:,}")
