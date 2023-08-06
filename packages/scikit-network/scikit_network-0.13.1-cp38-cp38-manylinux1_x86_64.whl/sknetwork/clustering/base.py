#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Nov, 2019
@author: Nathan de Lara <ndelara@enst.fr>
"""
from abc import ABC

from sknetwork.utils.base import Algorithm


class BaseClustering(Algorithm, ABC):
    """Base class for clustering algorithms.

    Attributes
    ----------
    labels_ : np.ndarray
        Label of each node.
    membership_ : sparse.csr_matrix
        Membership matrix.
    """

    def __init__(self):
        self.labels_ = None
        self.membership_ = None

    def fit_transform(self, *args, **kwargs):
        """Fit algorithm to the data and return the labels. Uses the same inputs as the ``fit`` method."""
        self.fit(*args, **kwargs)
        return self.labels_
