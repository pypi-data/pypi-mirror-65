"""
Test TOSLibrary class
"""
import re

import pymongo
import pytest
from testfixtures import LogCapture
from robot.api import logger

from TOSLibrary.RPALibrary import RPALibrary
from TOSLibrary.exceptions import CannotCreateTaskObject, DataAlreadyProcessed
# have to import all the fixtures if one fixture depends on others:
from .test_TOSLibrary import (
    mocked_TOSLibrary,
    mocked_collection,
    mocked_collection_with_multiple_documents,
    mocked_TOSLibrary_with_multiple_documents
)


ACTION_MESSAGE = "You're doing me an action"
POST_MESSAGE = "Let's post act"
PRE_MESSAGE = "You're doing me a prepare"
FAIL_MESSAGE = "Why u fail?"


@pytest.fixture
def library(mocker, mocked_TOSLibrary):
    class mocked_BuiltIn():
        def get_library_instance(self, lib_name):
            if lib_name == "TOSLibrary":
                return mocked_TOSLibrary

        def get_variable_value(self, var_name):
            return ["stage_1", "consumer_1"]

        def run_keyword(self, kw, *args):
            logger.info(f"Running keyword {kw}")

    mocker.patch('TOSLibrary.RPALibrary.BuiltIn',
                 mocked_BuiltIn)

    class TestLibrary(RPALibrary):
        """
        Class mimicking a real Robot Framework
        keyword library.
        """
        def __init__(self, should_fail=False):
            super(TestLibrary, self).__init__()
            self.should_fail = should_fail
            self.seen = False

        def main_action(self, to):
            if self.should_fail:
                raise RuntimeError("Should fail now.")
            logger.info(ACTION_MESSAGE)

        def get_input_data(self):
            if self.should_fail:
                if not self.seen:
                    self.seen = True
                    raise CannotCreateTaskObject("Should fail now.")
            if not self.seen:
                # otherwise infinite loop
                self.seen = True
                return {"data": "x"}

    return TestLibrary


@pytest.fixture
def library_with_multiple_documents(mocker, mocked_TOSLibrary_with_multiple_documents):
    """Do the same as above but with multiple (4) documents.

    First one should pass, two should fail, and the last one should pass.
    """
    class mocked_BuiltIn():
        def get_library_instance(self, lib_name):
            if lib_name == "TOSLibrary":
                return mocked_TOSLibrary_with_multiple_documents

        def get_variable_value(self, var_name):
            return ["stage_1", "consumer_1"]

        def run_keyword(self, kw, *args):
            logger.info(f"Running keyword {kw}")

    mocker.patch('TOSLibrary.RPALibrary.BuiltIn',
                 mocked_BuiltIn)

    class TestLibrary(RPALibrary):
        """
        Class mimicking a real Robot Framework
        keyword library.
        """
        def __init__(self, should_fail=False):
            super(TestLibrary, self).__init__()
            self.should_fail = should_fail
            self.seen = False

        def main_action(self, to):
            if self.should_fail:
                raise RuntimeError("Should fail now.")
            if to["analytics"]["should_fail"]:
                raise RuntimeError(FAIL_MESSAGE)
            logger.info(ACTION_MESSAGE)

        def post_action(self, to, status):
            logger.info(f"Consecutive failures: {self.consecutive_failures}")

    return TestLibrary


@pytest.fixture
def library_with_post_action(library):
    class TestLibrary(library):
        def post_action(self, *args, **kwargs):
            logger.info(POST_MESSAGE)
    return TestLibrary


@pytest.fixture
def library_with_pre_action(library):
    class TestLibrary(library):
        def pre_action(self, to):
            logger.info(PRE_MESSAGE)
    return TestLibrary


@pytest.fixture
def library_with_pre_action_and_main_action(library):
    """Test that information passes from pre_action
    to main_action properly."""
    class TestLibrary(library):
        def pre_action(self, to):
            logger.info(PRE_MESSAGE)
            to["analytics"]["message"] = PRE_MESSAGE
            return to

        def main_action(self, to):
            logger.info(ACTION_MESSAGE)
            logger.info(f'Prepared message: {to["analytics"]["message"]}')

    return TestLibrary


@pytest.fixture
def library_with_exception_inside_pre_action(library):
    """Test that errors from pre_action are handled."""
    class TestLibrary(library):
        def pre_action(self, to):
            raise RuntimeError(FAIL_MESSAGE)
            return to

        def main_action(self, to):
            logger.info(ACTION_MESSAGE)

    return TestLibrary


@pytest.fixture
def library_with_action_on_fail(library):
    class TestLibrary(library):
        def action_on_fail(self, to):
            logger.info(FAIL_MESSAGE)
    return TestLibrary


@pytest.fixture
def library_gives_duplicate_data(library):

    class TestLibraryGivesDuplicate(library):
        def get_input_data(self):
            """
            This will result in an infinite loop
            because ``main_loop_when_creating`` will call this
            method infinitely. Simulates a case when ``get_input_data``
            doesn't control if it returns the same data over and over again.
            """
            return {"data": "x"}

    return TestLibraryGivesDuplicate


@pytest.fixture
def library_without_main_action(mocker, mocked_TOSLibrary):
    class mocked_BuiltIn():
        def get_library_instance(self, lib_name):
            if lib_name == "TOSLibrary":
                return mocked_TOSLibrary

        def get_variable_value(self, var_name):
            return var_name

    mocker.patch('TOSLibrary.RPALibrary.BuiltIn',
                 mocked_BuiltIn)

    class TestLibrary(RPALibrary):
        """
        Class mimicking a real Robot Framework
        keyword library but with main_action missing.
        """
        def __init__(self):
            super(TestLibrary, self).__init__()
            self.data = {}

    return TestLibrary


@pytest.fixture
def library_with_sort_condition_default(library_with_multiple_documents):
    class TestLibrary(RPALibrary):
        """
        Class mimicking a real Robot Framework
        keyword library.
        """
        def __init__(self):
            super(TestLibrary, self).__init__()

        def main_action(self, to):
            logger.info(to)
    return TestLibrary


@pytest.fixture
def library_with_sort_condition_descending(mocker, mocked_TOSLibrary_with_multiple_documents):
    class mocked_BuiltIn():
        def get_library_instance(self, lib_name):
            if lib_name == "TOSLibrary":
                return mocked_TOSLibrary_with_multiple_documents

        def get_variable_value(self, var_name):
            return ["stage_1", "consumer_1"]

        def run_keyword(self, kw, *args):
            logger.info(f"Running keyword {kw}")

    mocker.patch('TOSLibrary.RPALibrary.BuiltIn',
                 mocked_BuiltIn)

    class TestLibrary(RPALibrary):
        """
        Class mimicking a real Robot Framework
        keyword library.
        """
        def __init__(self):
            sort_condition = [("_id", pymongo.DESCENDING)]
            super(TestLibrary, self).__init__(sort_condition=sort_condition)

        def main_action(self, to):
            logger.info(to)

    return TestLibrary


@pytest.fixture
def library_with_sigint_inside_main_action(library):
    """Test that errors from pre_action are handled."""
    class TestLibrary(library):

        def main_action(self, to):
            raise KeyboardInterrupt


    return TestLibrary


def test_main_loop(library):
    """
    Mimick calling a robot framework keyword.

    There is only one item in the mocked collection
    that matches the search criteria here (stage=0, status=pass).
    The main loop method should return counter value=1 when first run.
    It should return counter value=0 when run a second time.
    """

    lib = library()

    def run_loop_once():
        return lib.main_loop(current_stage=1)

    def run_next_stage():
        return lib.main_loop(current_stage=2)

    assert run_loop_once() == 1
    assert run_loop_once() == 0
    # now try running the next stage
    assert run_next_stage() == 1
    assert run_next_stage() == 0


def test_library_main_action_logging(library):
    lib = library()
    with LogCapture() as logs:
        _ = lib.main_loop(current_stage=1)

    with LogCapture() as logs_again:
        _ = lib.main_loop(current_stage=1)

    expected_text = (
        f"RobotFramework INFO\n  "
        f"{ACTION_MESSAGE}\n"
        f"RobotFramework INFO\n  1 task object(s) processed"
    )

    assert expected_text in str(logs)
    assert str(logs_again) == 'RobotFramework WARNING\n  No task objects processed'


def test_library_no_main_action(library_without_main_action):
    lib = library_without_main_action()

    expected_text = "Make your own implementation of this method"
    with pytest.raises(NotImplementedError) as err:
        _ = lib.main_loop(current_stage=1)

    assert err.type == NotImplementedError
    assert expected_text in str(err.value)


def test_library_change_status_on_failure(library):
    lib = library(should_fail=True)

    def run_loop_once():
        return lib.main_loop(current_stage=1)

    to1 = lib.tos.find_one_task_object_by_status_and_stage("pass", 0)
    lib.tos.set_task_object_status(to1["_id"], "pass")
    run_loop_once()
    to2 = lib.tos.find_one_task_object_by_status_and_stage("fail", 1)

    assert to2
    assert to1["_id"] == to2["_id"]


def test_library_dont_change_status_on_failure(library):
    lib = library(should_fail=True)

    def run_loop_once():
        return lib.main_loop(current_stage=1, change_status=False)

    to1 = lib.tos.find_one_task_object_by_status_and_stage("pass", 0)
    lib.tos.set_task_object_status(to1["_id"], "pass")
    run_loop_once()
    to2 = lib.tos.find_one_task_object_by_status_and_stage("pass", 1)

    assert to2
    assert to1["_id"] == to2["_id"]


def test_main_loop_when_creating(library):
    """There should be two task objects now."""
    lib = library()

    def run_loop_once():
        lib.main_loop_when_creating()

    to1 = lib.tos.find_one_task_object_by_status_and_stage("pass", 0)
    lib.tos.set_task_object_stage(to1["_id"], 1)
    run_loop_once()
    to2 = lib.tos.find_one_task_object_by_status_and_stage("pass", 0)
    lib.tos.set_task_object_stage(to2["_id"], 1)
    to3 = lib.tos.find_one_task_object_by_status_and_stage("pass", 0)

    assert to2["payload"] == {"data": "x"}
    assert not to3


def test_main_loop_when_creating_failure(library):
    """There should be two task objects now."""
    lib = library(should_fail=True)

    def run_loop_once():
        lib.main_loop_when_creating()

    to1 = lib.tos.find_one_task_object_by_status_and_stage("pass", 0)
    lib.tos.set_task_object_stage(to1["_id"], 1)
    run_loop_once()

    to2 = lib.tos.find_one_task_object_by_status_and_stage("pass", 0)

    assert not to2


def test_main_loop_when_creating_fails_on_duplicate_data(library_gives_duplicate_data):
    """
    Test the failsafe mechanism preventing an infinite loop
    resulting from a badly designed ``get_input_data``.
    Simulate processing the same input data by getting it again and again
    in an infinite loop.
    """
    lib = library_gives_duplicate_data()

    def run_loop_once():
        lib.main_loop_when_creating()

    to1 = lib.tos.find_one_task_object_by_status_and_stage("pass", 0)

    with pytest.raises(DataAlreadyProcessed) as err:
        run_loop_once()

    assert "Input data was just processed" in str(err.value)


def test_main_loop_with_stage_0(library):
    """Test that you can call ``main_loop`` when you really want
    to call ``main_loop_when_creating``.
    """
    lib = library()
    lib.tags = ["stage_0"]

    def run_loop_once():
        return lib.main_loop()

    assert run_loop_once() == 1


def test__get_stage_from_tags(library):
    lib = library()
    tag = lib._get_stage_from_tags()

    assert tag == 1


def test__get_stage_from_tags_fails(library):
    lib = library()
    lib.tags = ["producer"]

    with pytest.raises(StopIteration):
        _ = lib._get_stage_from_tags()


def test_main_loop_no_stage_passed_as_argument(library):
    """Test that if stage is not given as a keyword argument
    ``main_loop`` will try to get the stage number from the task tags.

    Assert that one task object was processed.
    """

    lib = library()

    def run_loop_once():
        return lib.main_loop()

    assert run_loop_once() == 1


def test_main_loop_no_stage_passed_as_argument_no_valid_task_objects(library):
    """Test that if stage is not given as a keyword argument
    ``main_loop`` will try to get the stage number from the task tags.

    There should be no valid task objects for the desired stage
    available.

    Assert that no task objects were processed.
    """

    lib = library()
    lib.tags = ["stage_2"]

    def run_loop_once():
        return lib.main_loop()

    assert run_loop_once() == 0


def test_main_loop_with_custom_main_action(library):

    lib = library()
    custom_keyword = "Some Other Action"

    def run_loop_once():
        return lib.main_loop(main_keyword=custom_keyword)

    with LogCapture() as logs:
        run_loop_once()

    assert f"Running keyword {custom_keyword}" in str(logs)


def test_library_with_post_action(library_with_post_action):
    lib = library_with_post_action()

    expected_text = (
        f"RobotFramework INFO\n  "
        f"{ACTION_MESSAGE}\n"
        f"RobotFramework INFO\n  "
        f"{POST_MESSAGE}\n"
        f"RobotFramework INFO\n  1 task object(s) processed"
    )

    with LogCapture() as logs:
        lib.main_loop()

    assert expected_text in str(logs)


def test_library_with_pre_action(library_with_pre_action):
    lib = library_with_pre_action()

    expected_text = (
        f"RobotFramework INFO\n  "
        f"{PRE_MESSAGE}\n"
        f"RobotFramework INFO\n  "
        f"{ACTION_MESSAGE}\n"
        f"RobotFramework INFO\n  1 task object(s) processed"
    )

    with LogCapture() as logs:
        lib.main_loop()

    assert expected_text in str(logs)


def test_library_with_pre_action_and_main_action(library_with_pre_action_and_main_action):
    lib = library_with_pre_action_and_main_action()

    expected_text = (
        f"RobotFramework INFO\n  "
        f"{PRE_MESSAGE}\n"
        f"RobotFramework INFO\n  "
        f"{ACTION_MESSAGE}\n"
        f"RobotFramework INFO\n  "
        f"Prepared message: {PRE_MESSAGE}\n"
        f"RobotFramework INFO\n  "
        "1 task object(s) processed"
    )

    with LogCapture() as logs:
        lib.main_loop()

    assert expected_text in str(logs)


def test_library_with_error_happening_inside_pre_action(library_with_exception_inside_pre_action):
    """Implement a test for when an exception is raised inside pre_action"""
    lib = library_with_exception_inside_pre_action()

    expected_text = (
        f"{FAIL_MESSAGE}\n"
        f"RobotFramework WARNING\n  "
        f"Robot needs to be running for screenshotting to work: Cannot access execution context\n"
        f"RobotFramework DEBUG\n  "
        f"Predefined action on fail not yet implemented\n"
        f"RobotFramework INFO\n  "
        f"1 task object(s) processed"
    )

    with LogCapture() as logs:
        lib.main_loop()

    assert expected_text in str(logs)


def test_consecutive_error_counter(library_with_multiple_documents):
    """First and last task object should pass, second and third should fail.

    So there should only be two consecutive failures.
    """
    expected_consecutive_failures = [0, 1, 2, 0]
    lib = library_with_multiple_documents()
    with LogCapture() as logs:
        lib.main_loop(current_stage=1)

    matches = map(int, re.findall(r"Consecutive failures: (\d)\n", str(logs)))

    assert list(matches) == expected_consecutive_failures


def test_library_with_action_on_fail(library_with_action_on_fail):
    lib = library_with_action_on_fail(should_fail=True)

    expected_text = (
        f"RobotFramework WARNING\n  "
        f"Robot needs to be running for screenshotting to work: Cannot access execution context\n"
        f"RobotFramework DEBUG\n  "
        f"Predefined action on fail not yet implemented\n"
        f"RobotFramework INFO\n  "
        f"{FAIL_MESSAGE}\n"
        f"RobotFramework INFO\n  1 task object(s) processed"
    )

    with LogCapture() as logs:
        lib.main_loop()

    assert expected_text in str(logs)


def test_library_with_sort_condition_default(library_with_sort_condition_default):
    """Test default sorting.

    That is, sort ascending by creation date. Oldest first.
    """
    lib = library_with_sort_condition_default()

    def parse_age_from_log_string(text):
        return re.findall(r"\'payload\': {'age': '(.*)'},", text)

    with LogCapture() as logs:
        lib.main_loop()

    expected_ages = ["oldest", "older", "middle", "youngest"]
    ages = parse_age_from_log_string(str(logs))

    assert expected_ages == ages


def test_library_with_sort_condition_descending(library_with_sort_condition_descending):
    """Test inverted sorting.

    That is, sort descending by creation date. Newest first.
    """
    lib = library_with_sort_condition_descending()

    def parse_age_from_log_string(text):
        return re.findall(r"\'payload\': {'age': '(.*)'},", text)

    with LogCapture() as logs:
        lib.main_loop()

    expected_ages = ["youngest", "middle", "older", "oldest"]
    ages = parse_age_from_log_string(str(logs))

    assert expected_ages == ages


@pytest.mark.skip(reason="Testing SIGINT is not working at the moment")
def test_library_with_sigint_inside_main_action(library_with_sigint_inside_main_action):
    lib = library_with_sigint_inside_main_action()

    with LogCapture() as logs:
        lib.main_loop()
