#!/usr/bin/env python

"""Tests for `simple_stats` package."""

import pytest
import numpy as np

from simple_stats.simple_stats import ecdf, pearson_r


@pytest.fixture
def sample_1d_data():
    """pytest fixture of a unsorted 1d numpy array of floating point data."""

    # Setup 1D array of unsorted data for testing
    test_1d_arr = np.array([4.7, 4.5, 4.9, 4.0, 4.6, 4.5, 4.7, 3.3, 4.6, 3.9, 3.5, 4.2, 4.0,
                            4.7, 3.6, 4.4, 4.5, 4.1, 4.5, 3.9, 4.8, 4.0, 4.9, 4.7, 4.3, 4.4,
                            4.8, 5.0, 4.5, 3.5, 3.8, 3.7, 3.9, 5.1, 4.5, 4.5, 4.7, 4.4, 4.1,
                            4.0, 4.4, 4.6, 4.0 , 3.3, 4.2, 4.2, 4.2, 4.3, 3.0, 4.1])

    return test_1d_arr


def test_ecdf_param_is_1d_numpy_arr_fail():
    """Ensure that a TypeError is raised if the wrong data type is passed to the ecdf function"""

    wrong_type = 'Wrong_type'

    with pytest.raises(TypeError):
        result_x, result_y = ecdf(wrong_type)


def test_ecdf_param_is_1d_numpy_arr_pass(sample_1d_data):
    """Ensure that a TypeError is NOT raised if an 1d numpy array is passed to the ecdf function"""

    result_x, result_y = ecdf(sample_1d_data)


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

# Tests for person_r
@pytest.fixture
def sample_1d_x():

    sample_x = np.array([4.7, 4.5, 4.9, 4.0 , 4.6, 4.5, 4.7, 3.3, 4.6, 3.9, 3.5, 4.2, 4.0, 4.7, 3.6, 4.4, 4.5, 4.1, 4.5,
                         3.9, 4.8, 4.0, 4.9, 4.7, 4.3, 4.4, 4.8, 5.0, 4.5, 3.5, 3.8, 3.7, 3.9, 5.1, 4.5, 4.5, 4.7,
                         4.4, 4.1, 4.0, 4.4, 4.6, 4. , 3.3, 4.2, 4.2, 4.2, 4.3, 3.0, 4.1])

    return sample_x


@pytest.fixture
def sample_1d_y():

    sample_y = np.array([1.4, 1.5, 1.5, 1.3, 1.5, 1.3, 1.6, 1.0, 1.3, 1.4, 1.0, 1.5, 1.0, 1.4, 1.3, 1.4, 1.5,
                         1.0, 1.5, 1.1, 1.8, 1.3, 1.5, 1.2, 1.3, 1.4, 1.4, 1.7, 1.5, 1.0, 1.1, 1.0, 1.2, 1.6, 1.5,
                         1.6, 1.5, 1.3, 1.3, 1.3, 1.2, 1.4, 1.2, 1.0, 1.3, 1.2, 1.3, 1.3, 1.1, 1.3])

    return sample_y


def test_person_r_raises_error_wrong_x_arg_type(sample_1d_x, sample_1d_y):

    wrong_type_x = "Wrong_type_x"

    with pytest.raises(TypeError):
        pearson_r(wrong_type_x, sample_1d_y)


def test_person_r_raises_error_wrong_y_arg_type(sample_1d_x, sample_1d_y):

    wrong_type_y = "Wrong_type_y"

    with pytest.raises(TypeError):
        pearson_r(sample_1d_x, wrong_type_y)


def test_person_r_raises_error_x_y_diff_lengths(sample_1d_x, sample_1d_y):

    short_y = np.array([2.0, 6.0])

    with pytest.raises(RuntimeError):
        pearson_r(sample_1d_x, short_y)


def test_correct_person_r_result(sample_1d_x, sample_1d_y):

    result = pearson_r(sample_1d_x, sample_1d_y)

    assert result == 0.7866680885228169

