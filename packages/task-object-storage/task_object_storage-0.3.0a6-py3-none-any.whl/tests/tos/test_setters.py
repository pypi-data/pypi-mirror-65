import os

import pytest

from . import tos, tos_with_inserted_object


def test_set_task_object_priority(tos):
    initial_priority = 0
    changed_priority = 10
    object_to_insert = {
        "status": "new",
        "priority": initial_priority,
        "payload": {"data": 213213}
    }
    tos._insert_task_object(object_to_insert)
    object_id = object_to_insert["_id"]

    inserted_object = tos.find_task_object_by_id(object_id)
    tos.set_task_object_priority(object_id, changed_priority)
    inserted_object_again = tos.find_task_object_by_id(object_id)

    assert inserted_object["priority"] == initial_priority
    assert inserted_object_again["priority"] == changed_priority


def test_set_task_object_payload(tos):
    initial_payload = {"data": 213213}
    changed_payload = {"data": 213213, "additional_data": 124}
    object_to_insert = {
        "status": "new",
        "priority": 0,
        "payload": initial_payload
    }
    tos._insert_task_object(object_to_insert)
    object_id = object_to_insert["_id"]

    inserted_object = tos.find_task_object_by_id(object_id)
    tos.set_task_object_payload(object_id, changed_payload)
    inserted_object_again = tos.find_task_object_by_id(object_id)

    assert inserted_object["payload"] == initial_payload
    assert inserted_object_again["payload"] == changed_payload


def test__validate_status_text_valid_status(tos):
    status = "pass"
    tos._validate_status_text(status)


def test__validate_status_text_invalid_status(tos):
    status = "AWEFDSC"
    with pytest.raises(ValueError):
        tos._validate_status_text(status)


def test_set_task_object_status(tos_with_inserted_object):
    tos, item = tos_with_inserted_object
    inserted_item = tos.find_task_object_by_id(item["_id"])
    old_status = "new"
    new_status = "processing"

    assert inserted_item["status"] == old_status

    tos.set_task_object_status(item["_id"], new_status)
    updated_item = tos.find_task_object_by_id(item["_id"])

    assert updated_item["status"] == new_status


def test_set_task_object_stage(tos_with_inserted_object):
    tos, item = tos_with_inserted_object
    inserted_item = tos.find_task_object_by_id(item["_id"])
    new_stage = 1

    assert inserted_item["stage"] == 0

    tos.set_task_object_stage(item["_id"], new_stage)
    updated_item = tos.find_task_object_by_id(item["_id"])

    assert updated_item["stage"] == new_stage


@pytest.fixture
def test_set_task_object_analytics(tos_with_inserted_object):
    tos, item = tos_with_inserted_object
    inserted_item = tos.find_task_object_by_id(item["_id"])
    new_analytics = {
        "marked_for_manual": True,
        "customer_type": 2
    }

    assert inserted_item["analytics"] == {}

    tos.set_task_object_analytics(item["_id"], new_analytics)
    updated_item = tos.find_task_object_by_id(item["_id"])

    assert updated_item["analytics"] == new_analytics

    return tos, item


def test_set_task_object_analytics_item(test_set_task_object_analytics):
    tos, item = test_set_task_object_analytics
    key = "marked_for_manual"
    new_value = False

    tos.set_task_object_analytics_item(item["_id"], key, new_value)
    updated_item = tos.find_task_object_by_id(item["_id"])

    assert updated_item["analytics"][key] == new_value


def test_set_task_object_last_error(tos_with_inserted_object):
    tos, item = tos_with_inserted_object
    with pytest.raises(ZeroDivisionError) as err:
        1/0
    tos.set_task_object_last_error(
        item["_id"],
        f"{err.type}: {err.value}"
    )

    updated_item = tos.find_task_object_by_id(item["_id"])

    assert "ZeroDivisionError" in updated_item["last_error"]


def test_increment_and_decrement_task_object_stage(tos_with_inserted_object):
    tos, item = tos_with_inserted_object

    tos.increment_task_object_stage(item["_id"])
    item_after_increment = tos.find_task_object_by_id(item["_id"])
    tos.decrement_task_object_stage(item["_id"])
    item_after_decrement = tos.find_task_object_by_id(item["_id"])

    assert item["stage"] == 0
    assert item_after_increment["stage"] == 1
    assert item_after_decrement["stage"] == 0


def test_set_task_object_for_rerun(tos_with_inserted_object):
    tos, item = tos_with_inserted_object

    tos.set_task_object_stage(item["_id"], 2)
    tos.set_task_object_status(item["_id"], "fail")
    item_after_failure = tos.find_task_object_by_id(item["_id"])
    tos.set_task_object_for_rerun(item["_id"])

    item_after_reset = tos.find_task_object_by_id(item["_id"])

    assert item_after_failure["status"] == "fail"
    assert item_after_failure["stage"] == 2
    assert item_after_failure["retry_count"] == 0
    assert item_after_reset["status"] == "pass"
    assert item_after_reset["stage"] == 1
    assert item_after_reset["retry_count"] == 1


def test_set_task_object_for_rerun_invalid_stage(tos_with_inserted_object):
    """Test that the stage is never decremented to a negative number"""
    tos, item = tos_with_inserted_object
    expected_message = "Cannot decrement stage to negative number"

    item["stage"] = 0
    with pytest.raises(ValueError) as err:
        tos.set_task_object_for_rerun(item["_id"])

    assert expected_message in str(err.value)


def test_set_task_object_executor(tos_with_inserted_object):
    tos, item = tos_with_inserted_object
    executor = "Super Star Destroyer"
    os.environ["NODE_NAME"] = executor

    _ = tos.set_task_object_executor(item["_id"])
    inserted_item = tos.find_task_object_by_id(item["_id"])

    assert executor in inserted_item["executor"]


def test_set_task_object_build_number(tos_with_inserted_object):
    tos, item = tos_with_inserted_object
    build_number = "222"
    os.environ["BUILD_NUMBER"] = build_number

    _ = tos.set_task_object_build_number(item["_id"])
    inserted_item = tos.find_task_object_by_id(item["_id"])

    assert inserted_item["build_number"] == build_number
