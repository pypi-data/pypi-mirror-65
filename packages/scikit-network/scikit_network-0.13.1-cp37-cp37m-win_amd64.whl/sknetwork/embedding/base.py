#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Nov, 2019
@author: Nathan de Lara <ndelara@enst.fr>
"""
from abc import ABC

import numpy as np

from sknetwork.utils.base import Algorithm


class BaseEmbedding(Algorithm, ABC):
    """Base class for embedding algorithms."""

    def __init__(self):
        self.embedding_ = None

    def fit_transform(self, *args, **kwargs):
        """Fit to data and returns the embedding of the rows.
        Use the same inputs as the ``fit`` method."""
        self.fit(*args, **kwargs)
        return self.embedding_

    def predict(self, *args, **kwargs) -> np.ndarray:
        """Compute the embedding of new nodes."""
        raise NotImplementedError('Predict method is currently unavailable for this algorithm.')
