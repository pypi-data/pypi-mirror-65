#!/usr/bin/env python

"""Tests for `simple_stats` package."""

import pytest
import numpy as np

from simple_stats.simple_stats import ecdf


@pytest.fixture
def sample_1d_data():
    """pytest fixture of a unsorted 1d numpy array of floating point data."""

    # Setup 1D array of unsorted data for testing
    test_1d_arr = np.array([4.7, 4.5, 4.9, 4.0, 4.6, 4.5, 4.7, 3.3, 4.6, 3.9, 3.5, 4.2, 4.0,
                            4.7, 3.6, 4.4, 4.5, 4.1, 4.5, 3.9, 4.8, 4.0, 4.9, 4.7, 4.3, 4.4,
                            4.8, 5.0, 4.5, 3.5, 3.8, 3.7, 3.9, 5.1, 4.5, 4.5, 4.7, 4.4, 4.1,
                            4.0, 4.4, 4.6, 4.0 , 3.3, 4.2, 4.2, 4.2, 4.3, 3.0, 4.1])

    return test_1d_arr


def test_ecdf_return_2_arr(sample_1d_data):
    """Test that the return value of the ecdf function is that of two 1d numpy arrays"""

    result_x, result_y = ecdf(sample_1d_data)

    assert isinstance(result_x, np.ndarray)
    assert isinstance(result_y, np.ndarray)


def test_ecdf_sorted(sample_1d_data):
    """Test that the returned numpy arrays of the ecdf function are sorted."""

    result_x, result_y = ecdf(sample_1d_data)

    assert sorted(result_x)
    assert sorted(result_y)


def test_ecdf_max_y_is_1(sample_1d_data):
    """Test that the numpy array of y values has a max of 1.0"""

    result_x, result_y = ecdf(sample_1d_data)

    assert max(result_y) == 1.0
