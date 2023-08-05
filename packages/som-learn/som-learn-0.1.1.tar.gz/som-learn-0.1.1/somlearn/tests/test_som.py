"""
Test the som module.
"""

import numpy as np
from sklearn.datasets import make_classification

from ..som import SOM

RANDOM_STATE = 10
X, _ = make_classification(random_state=RANDOM_STATE)


def test_generate_labels_mapping():
    """Test the generation of the labels mapping."""
    grid_labels = np.array([[1, 1], [0, 0], [0, 1], [1, 0], [1, 1], [1, 0], [0, 1]])
    labels_mapping = {(0, 0): 0, (0, 1): 1, (1, 0): 2, (1, 1): 3}
    assert SOM._generate_labels_mapping(grid_labels) == labels_mapping


def test_return_topological_neighbors_rectangular():
    """Test the topological neighbors of a neuron for rectangular grid type."""
    som = SOM(random_state=RANDOM_STATE).fit(X)
    assert set(som._return_topological_neighbors(0, 0)).issubset(set([(1, 0), (0, 1)]))
    assert set(som._return_topological_neighbors(1, 1)).issubset(
        set([(0, 1), (2, 1), (1, 0), (1, 2)])
    )


def test_return_topological_neighbors_hexagonal():
    """Test the topological neighbors of a neuron for hexagonal grid type."""
    som = SOM(random_state=RANDOM_STATE, gridtype='hexagonal').fit(X)
    assert set(som._return_topological_neighbors(0, 0)).issubset(set([(1, 0), (0, 1)]))
    assert set(som._return_topological_neighbors(1, 1)).issubset(
        set([(0, 1), (2, 1), (1, 0), (1, 2), (2, 2), (2, 0)])
    )


def test_fit():
    """Test the SOM fitting process."""

    som = SOM(random_state=RANDOM_STATE)
    assert not hasattr(som, 'labels_')
    assert not hasattr(som, 'neighbors_')
    assert not hasattr(som, 'algorithm_')
    assert not hasattr(som, 'n_columns_')
    assert not hasattr(som, 'n_rows_')

    som.fit(X)
    assert hasattr(som, 'labels_')
    assert hasattr(som, 'neighbors_')
    assert hasattr(som, 'algorithm_')
