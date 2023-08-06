import pytest

from tos.components import query_helpers
from . import tos, tos_with_inserted_object


def test_create_status_query_invalid_arguments(tos):
    with pytest.raises(TypeError) as err:
        query_helpers.create_status_query({})

    assert "Pass status as a string or a sequence of strings" in str(err.value)


def test_create_stage_query_invalid_arguments(tos):
    with pytest.raises(TypeError) as err:
        query_helpers.create_stage_query({})

    assert "Pass stages as an int or a sequence of ints." in str(err.value)


def test_create_stage_query_string_argument(tos):
    """Robot Framework passes arguments as strings so this is important."""
    expected = {'stage': {'$eq': 2}}
    result = query_helpers.create_stage_query("2")

    assert result == expected
