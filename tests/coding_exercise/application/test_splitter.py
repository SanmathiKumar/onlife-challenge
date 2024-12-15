# -----------------------------------------------------------------------------
# Author: Sanmathi Kumar
# Description: Unit tests for the Splitter class to ensure correct behavior
#              when splitting cables of different lengths and configurations.
# -----------------------------------------------------------------------------


import pytest
from assertpy import assert_that

from coding_exercise.application.splitter import *


# Test that splitting a cable doesn't return None
def test_should_not_return_none_when_splitting_cable():
    assert_that(Splitter().split(Cable(10, "coconuts"), 1)).is_not_none()


# Test that cable names are generated correctly
def test_should_generate_cable_names():
    result = Splitter().split(Cable(10, "coconuts"), 2)
    assert_that(result).is_length(4)
    assert_that(result[0].name).is_equal_to("coconuts-0")
    assert_that(result[1].name).is_equal_to("coconuts-1")
    assert_that(result[2].name).is_equal_to("coconuts-2")

    result = Splitter().split(Cable(100, "coconuts"), 10)
    assert_that(result).is_length(12)
    assert_that(result[0].name).is_equal_to("coconuts-00")
    assert_that(result[-1].name).is_equal_to("coconuts-11")


def test_equal_split():
    splitter = Splitter()
    cable = Cable(10, "coconut")
    result = splitter.split(cable, 1)
    assert_that(result).is_length(2)
    assert_that(result[0].length).is_equal_to(5)
    assert_that(result[1].length).is_equal_to(5)


def test_unequal_split():
    splitter = Splitter()
    cable = Cable(10, "coconut")
    result = splitter.split(cable, 3)
    assert_that(result).is_length(5)
    assert_that(result[0].length).is_equal_to(2)
    assert_that(result[1].length).is_equal_to(2)
    assert_that(result[2].length).is_equal_to(2)
    assert_that(result[3].length).is_equal_to(2)
    assert_that(result[4].length).is_equal_to(2)


def test_unequal_split_with_remainder():
    splitter = Splitter()
    cable = Cable(11, "coconut")
    result = splitter.split(cable, 3)
    assert_that(result).is_length(6)
    assert_that(result[0].length).is_equal_to(2)
    assert_that(result[1].length).is_equal_to(2)
    assert_that(result[2].length).is_equal_to(2)
    assert_that(result[3].length).is_equal_to(2)
    assert_that(result[4].length).is_equal_to(2)
    assert_that(result[5].length).is_equal_to(1)


def test_remainder_edge_case():
    splitter = Splitter()
    cable = Cable(5, "coconut")
    result = splitter.split(cable, 2)
    assert_that(result).is_length(5)
    assert_that(result[0].length).is_equal_to(1)
    assert_that(result[1].length).is_equal_to(1)
    assert_that(result[2].length).is_equal_to(1)
    assert_that(result[3].length).is_equal_to(1)
    assert_that(result[4].length).is_equal_to(1)


def test_remainder_greater_than_split_length():
    splitter = Splitter()
    cable = Cable(7, "coconut")  # A 7-length cable
    result = splitter.split(cable, 2)  # Splitting into 3 parts (split length = 2, remainder = 1)
    assert_that(result).is_length(4)  # 3 splits of 2, and 1 remainder of 1
    assert_that(result[-1].length).is_equal_to(1)  # Check that the remainder is appended


# Test splitting a cable with the minimum valid length
def test_validation_constraints_for_splitting():
    splitter = Splitter()
    # validation for `times` parameter
    with pytest.raises(
            ValueError,
            match=f"The number of times must be between {MIN_ALLOWED_SPLITS} and {MAX_ALLOWED_SPLITS}.",
    ):
        splitter.split(Cable(2, "coconuts"), 0)

    with pytest.raises(
            ValueError,
            match=f"The number of times must be between {MIN_ALLOWED_SPLITS} and {MAX_ALLOWED_SPLITS}.",
    ):
        splitter.split(Cable(2, "coconuts"), 65)

    # validation for `cable.length` parameter
    with pytest.raises(
            ValueError,
            match=f"The cable length must be between {MIN_CABLE_LENGTH} and {MAX_CABLE_LENGTH}.",
    ):
        splitter.split(Cable(1, "coconuts"), 1)

    with pytest.raises(
            ValueError,
            match=f"The cable length must be between {MIN_CABLE_LENGTH} and {MAX_CABLE_LENGTH}.",
    ):
        splitter.split(Cable(1025, "coconuts"), 1)

    # validation for `times` and `cable.length` parameters
    with pytest.raises(
            ValueError, match="The number of splits must be less than the cable length."
    ):
        splitter.split(Cable(5, "coconuts"), 6)
