"""
Tests for TOSLibrary.helpers
"""
import pytest
from testfixtures import LogCapture

from TOSLibrary.helpers import (
    repeat_call_until,
    take_screenshot
)


def test_take_screenshot_rf_not_running():
    with LogCapture() as logs:
        take_screenshot()

    assert "Robot needs to be running for screenshotting to work" in str(logs)


@pytest.fixture
def test_class():

    class TestClass:
        def __init__(self):
            self.counter = 0

        def increase_counter(self):
            self.counter += 1

        def wrap_text(self, text):
            self.increase_counter()
            return f"<{text}>"

        def divide(self, numerator=0, denominator=1):
            self.increase_counter()
            return numerator / denominator

        def print_fail(self):
            """Don't increase counter here
            so that the condition never equals True."""
            print("fail")

    return TestClass


def test_repeat_call_until(test_class):
    tc = test_class()

    counter_limit = 3

    assert tc.counter == 0

    repeat_call_until(
        callable=tc.increase_counter,
        condition=lambda: tc.counter >= counter_limit,
        sleep=0
    )

    assert tc.counter == counter_limit


def test_repeat_call_until_with_arguments(test_class):
    tc = test_class()

    counter_limit = 3

    assert tc.counter == 0

    value = repeat_call_until(
        callable=tc.wrap_text,
        condition=lambda: tc.counter >= counter_limit,
        arguments=("hello",),
        sleep=0
    )
    expected = f"<hello>"

    assert tc.counter == counter_limit
    assert value == expected


def test_repeat_call_until_with_keyword_arguments(test_class):
    tc = test_class()

    counter_limit = 3

    assert tc.counter == 0

    value = repeat_call_until(
        callable=tc.divide,
        condition=lambda: tc.counter >= counter_limit,
        kwarguments={"numerator": 8, "denominator": 2},
        sleep=0
    )
    expected = 4.0

    assert tc.counter == counter_limit
    assert value == expected


def test_repeat_call_until_fails(test_class):
    tc = test_class()

    counter_limit = 3

    assert tc.counter == 0

    with pytest.raises(RuntimeError) as err:
        repeat_call_until(
            callable=tc.print_fail,
            condition=lambda: tc.counter >= counter_limit,
            sleep=0
        )

    assert tc.counter == 0
    assert err.type == RuntimeError
    assert "Tried to retry action" in str(err.value)


def test_repeat_call_until_missing_required_arguments(test_class):
    tc = test_class()

    assert tc.counter == 0

    with pytest.raises(TypeError) as err:
        repeat_call_until(
            callable=tc.print_fail,
            sleep=0
        )

    assert tc.counter == 0
    assert err.type == TypeError
    assert "Missing required kwargs" in str(err.value)
