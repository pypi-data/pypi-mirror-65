"""
Test custom error handler code.
"""
from enum import Enum

import pytest

from TOSLibrary.deco import error_name
from TOSLibrary.error_library import ErrorLibrary
from TOSLibrary.exceptions import NoErrorHandlerFound


@pytest.fixture
def errors():
    class Errors(Enum):
        """Define variables for error types in robot code.

        Use descriptive texts as values.
        Put these inside an enum.
        """
        CANNOT_DIVIDE_BY_ZERO = "Cannot divide by zero"
        COUNTER_OVER_THE_LIMIT = "Counter is over the limit"
        ERROR_WITHOUT_HANDLER = "This is an error without a proper handler"

    return Errors


@pytest.fixture
def error_handlers(errors):
    class ErrorHandlers:
        """These should be defined in the robot code."""
        @error_name(errors.CANNOT_DIVIDE_BY_ZERO)
        def handle_divide_by_zero(self, message):
            return message

        @error_name(errors.COUNTER_OVER_THE_LIMIT, critical=True)
        def handle_counter_over_the_limit(self, message):
            # TODO: TEST THIS!
            return message

    return ErrorHandlers


def test_error_handlers(errors, error_handlers):
    el = ErrorLibrary()
    el.errors = errors
    el.handlers = error_handlers
    to = {
        "last_error": "RuntimeError: Cannot divide by zero"
    }

    result = el.get_error_handler(to)()

    assert result == errors.CANNOT_DIVIDE_BY_ZERO.value


def test_error_handlers_invalid_handler(errors, error_handlers):
    el = ErrorLibrary()
    el.errors = errors

    with pytest.raises(TypeError) as err:
        el.handlers = error_handlers()

    assert "Handlers object should be a class" in str(err.value)


def test_error_handlers_invalid_errors(errors, error_handlers):
    el = ErrorLibrary()
    el.handlers = error_handlers

    with pytest.raises(TypeError) as err:
        el.errors = {"error1": "terrible error"}

    assert "Errors object should be an Enum" in str(err.value)


def test_error_handlers_no_handler_found(errors, error_handlers):
    """
    When error is defined in Errors enum, but the corresponding
    handler does not exist.
    """

    el = ErrorLibrary()
    el.errors = errors
    el.handlers = error_handlers
    to = {
        "last_error": errors.ERROR_WITHOUT_HANDLER.value
    }

    with pytest.raises(ValueError) as err:
        el.get_error_handler(to)()


    assert f"No handler found for {errors.ERROR_WITHOUT_HANDLER.name}" in str(err.value)


def test_error_handlers_no_task_object_passed(errors, error_handlers):
    """
    Should result in error if no proper task object is passed in.
    Task object should be a dict with a field 'last_error'.
    """
    el = ErrorLibrary()
    el.errors = errors
    el.handlers = error_handlers
    to = {
        "payload": {}
    }

    with pytest.raises(ValueError) as err:
        el.get_error_handler(to)()

    assert "Argument to should be a task object with 'last_error'" in str(err.value)


def test_error_handlers_unknown_error(errors, error_handlers):
    """
    Should raise exception if the encountered error is not defined
    in Errors.

    This is handled and logged in RPALibrary. Unexpected errors should not
    fail the robot execution.
    """
    last_error = "Totally horrible exception happened"

    el = ErrorLibrary()
    el.errors = errors
    el.handlers = error_handlers
    to = {
        "last_error": last_error
    }

    with pytest.raises(NoErrorHandlerFound) as err:
        el.get_error_handler(to)()

    assert f"Unknown error: {last_error}" in str(err.value)
