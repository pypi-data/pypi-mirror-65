#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on January, 22nd 2020
@author: Quentin Lutz <qlutz@enst.fr>
"""

from typing import Optional, Union

import numpy as np
from scipy import sparse

from sknetwork.clustering.louvain import Louvain
from sknetwork.hierarchy.base import BaseHierarchy
from sknetwork.hierarchy.postprocess import get_dendrogram
from sknetwork.utils.check import check_format, is_square


class LouvainHierarchy(BaseHierarchy):
    """Iterative clustering algorithm for hierarchical clustering.

    Using the Louvain clustering algorithm on each previously obtained cluster yields a tree-like structure.

    Parameters
    ----------
    Parameters are the same as the ``sknetwork.clustering.Louvain``

    Attributes
    ----------
    dendrogram_ : np.ndarray
        Dendrogram.

    Notes
    -----
    Each row of the dendrogram = children, distance, size of cluster :math:`\\sum` nodes.

    See Also
    --------
    scipy.cluster.hierarchy.dendrogram
    """

    def __init__(self, **kwargs):
        super(LouvainHierarchy, self).__init__()

        self._clustering_method = Louvain(**kwargs)

    def recursive_louvain(self, adjacency: Union[sparse.csr_matrix, np.ndarray],
                          nodes: Optional[np.ndarray] = None):
        """
        Recursive function for fit. Returns a tree rather than a dendrogram.

        Parameters
        ----------
        adjacency :
            Adjacency matrix of the graph.
        nodes :
            The current nodes index in the original graph.

        Returns
        -------
        tree: :class:`Tree`
        """
        labels = self._clustering_method.fit_transform(adjacency)

        clusters = np.unique(labels)

        if nodes is None:
            nodes = np.arange(adjacency.shape[0])

        result = []

        if len(clusters) == 1:
            if len(nodes) > 1:
                return [[node] for node in nodes]
            else:
                return [nodes[0]]

        else:
            for cluster in clusters:
                mask = (labels == cluster)
                subgraph_nodes = nodes[mask]
                subgraph = adjacency[mask, :][:, mask]
                result.append(self.recursive_louvain(subgraph, subgraph_nodes))
            return result

    def fit(self, adjacency: Union[sparse.csr_matrix, np.ndarray]) -> 'LouvainHierarchy':
        """
        Hierarchical clustering using several Louvain instances.

        Parameters
        ----------
        adjacency :
            Adjacency matrix of the graph.

        Returns
        -------
        self: :class:`LouvainHierarchy`
        """
        adjacency = check_format(adjacency)
        if not is_square(adjacency):
            raise ValueError('The adjacency matrix is not square.')

        tree = self.recursive_louvain(adjacency)
        dendrogram, _ = get_dendrogram(tree)
        dendrogram = np.array(dendrogram)
        dendrogram[:, 2] -= min(dendrogram[:, 2])

        self.dendrogram_ = dendrogram

        return self
