import pytest

from . import tos, tos_with_inserted_object


def test__insert_task_object_and_find_task_object(tos):
    """Test that the object status does not change."""
    object_to_insert = {
        "status": "new",
        "priority": 0,
        "payload": {"data": 213213}
    }
    tos._insert_task_object(object_to_insert)
    object_id = object_to_insert["_id"]

    inserted_object = tos.find_task_object_by_id(object_id)

    assert inserted_object["_id"] == object_id
    assert inserted_object["status"] == object_to_insert["status"]
    assert inserted_object["priority"] == object_to_insert["priority"]
    assert inserted_object["payload"] == object_to_insert["payload"]


def test_create_new_task_object(tos):
    payload = {"data": 213213}
    priority = 0
    tos.create_new_task_object(
        payload,
        priority=priority
    )

    inserted_object = tos.find_one_task_object_by_status_and_stage("new", 0)

    assert inserted_object["status"] == "new"
    assert inserted_object["priority"] == priority
    assert inserted_object["payload"] == payload


def test_create_new_task_object_with_deprecated_process_name(tos, capsys):
    """Using process_name in task_object creation prints out a DeprecationWarning."""
    with pytest.warns(DeprecationWarning) as warn:
        tos.create_new_task_object(
            {"data": 213213},
            "process_name_not_needed",
            priority=0
        )

    assert "process_name should not be used anymore" in str(warn.list[0].message)


@pytest.mark.skip(reason="deprecated method")
def test_delete_task_object(tos_with_inserted_object):
    # TODO: remove this as the whole functionality is deprecated!
    tos, item = tos_with_inserted_object
    tos.delete_task_object(item["_id"])
    updated_item = tos.find_task_object_by_id(item["_id"])

    assert updated_item is None
