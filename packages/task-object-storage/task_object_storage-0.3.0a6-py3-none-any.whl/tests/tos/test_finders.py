import pytest

from . import tos, tos_with_inserted_object


def test_find_one_task_object_by_status_and_stage_with_sorting_by_date(tos):
    """
    Test that the method returns the object
    with the oldest creation time.

    Sorting by date is the default method.
    """
    payload = {"data": 213213}
    payload2 = {"data": 65646}
    status = "new"

    tos.create_new_task_object(
        payload,
    )
    tos.create_new_task_object(
        payload2,
    )
    tos.create_new_task_object(
        {"data": 7657},
    )

    obj = tos.find_one_task_object_by_status_and_stage(status, 0)

    assert obj["payload"] == payload
    assert obj["status"] == status

    obj2 = tos.find_one_task_object_by_status_and_stage(status, 0)
    assert obj2["payload"] == payload2
    assert obj2["status"] == status


def test_find_one_task_object_by_status_and_stage_with_different_priorities(tos):
    """
    Test that the method returns the object
    with the highest priority when multiple objects
    are inserted.

    Note that the highest priority object is not
    created first or last.
    """
    payload = {"data": 213213}
    priority = 10

    tos.create_new_task_object(
        {"data": 65646},
        priority=0
    )
    tos.create_new_task_object(
        {"data": 7657},
        priority=2
    )
    tos.create_new_task_object(
        payload,
        priority=priority
    )
    tos.create_new_task_object(
        {"data": 7657},
        priority=0
    )

    obj = tos.find_one_task_object_by_status_and_stage("new", 0, sort_condition="priority")

    assert obj["payload"] == payload
    assert obj["priority"] == 10
    assert obj["status"] == "new"


def test_find_one_task_object_by_status(tos):
    """
    Create two items with different stages but same status "new".
    Then create a third item with a different status "fail".

    Test getting both "new" items one at a time and only them.
    """

    _ = tos.create_new_task_object(
        {"data": 65646},
    )
    item2 = tos.create_new_task_object(
        {"data": 7657},
    )
    _ = tos.create_new_task_object(
        {"data": 7657},
    )
    tos.set_task_object_stage(item2["_id"], 1)
    tos.set_task_object_status(item2["_id"], "fail")

    to1 = tos.find_one_task_object_by_status("new")
    tos.set_task_object_status(to1["_id"], "pass")
    to2 = tos.find_one_task_object_by_status("new")
    tos.set_task_object_status(to2["_id"], "pass")

    assert not tos.find_one_task_object_by_status("new")


def test_find_one_task_object_by_status_and_stage_no_matches(tos):
    items = tos.find_one_task_object_by_status_and_stage("pass", 0)

    assert items is None


def test_find_all_failed_task_objects(tos_with_inserted_object):
    tos, item = tos_with_inserted_object
    inserted_item = tos.find_task_object_by_id(item["_id"])

    assert inserted_item["status"] == "new"

    tos.set_task_object_status(item["_id"], "fail")
    failed_objects = tos.find_all_failed_task_objects()

    assert failed_objects[0]["status"] == "fail"

    failed_objects[0].pop("status")
    failed_objects[0].pop("updatedAt")
    item.pop("status")

    assert failed_objects[0] == item


def test_find_one_task_object_marked_as_manual_and_not_passed(tos):

    expected_payload = {"data": 65646}
    item1 = tos.create_new_task_object(
        expected_payload,
    )
    _ = tos.create_new_task_object(
        {"data": 7657},
    )

    with pytest.warns(DeprecationWarning) as warn:
        tos.set_task_object_to_manual_handling(item1["_id"])
        to1 = tos.find_one_task_object_marked_as_manual_and_not_passed()
        tos.set_task_object_status(to1["_id"], "pass")

        to2 = tos.find_one_task_object_marked_as_manual_and_not_passed()

        assert to1["payload"] == expected_payload
        assert not to2

    assert "Use status instead of manual field" in str(warn.list[0].message)


def test_find_all_task_objects_by_status_and_stage_multiple_stages(tos):
    _ = tos.create_new_task_object(
        {"data": 65646},
    )
    item2 = tos.create_new_task_object(
        {"data": 7657},
    )
    item3 = tos.create_new_task_object(
        {},
    )

    tos.set_task_object_stage(item2["_id"], 2)
    tos.set_task_object_stage(item3["_id"], 3)

    objects = tos.find_all_task_objects_by_status_and_stage("new", [0, 2, 3])

    assert len(objects) == 3


def test_find_all_task_objects_by_status_and_stage_multiple_statuses(tos):
    _ = tos.create_new_task_object(
        {"data": 65646},
    )
    item2 = tos.create_new_task_object(
        {"data": 7657},
    )
    item3 = tos.create_new_task_object(
        {},
    )

    tos.set_task_object_status(item2["_id"], "fail")
    tos.set_task_object_status(item3["_id"], "processing")

    objects = tos.find_all_task_objects_by_status_and_stage(["new", "fail", "processing"])

    assert len(objects) == 3


def test_find_all_task_objects_by_stage(tos):
    _ = tos.create_new_task_object(
        {"data": 65646},
    )
    item2 = tos.create_new_task_object(
        {"data": 7657},
    )
    item3 = tos.create_new_task_object(
        {},
    )

    tos.set_task_object_stage(item2["_id"], 1)
    tos.set_task_object_stage(item3["_id"], 2)

    objects = tos.find_all_task_objects_by_stage([0, 1])

    assert len(objects) == 2


def test_find_all_task_objects_by_status_and_stage_invalid_arguments(tos):
    with pytest.raises(TypeError) as err:
        tos.find_all_task_objects_by_status_and_stage()

    assert "Pass statuses or stages or both." in str(err.value)


def test_find_one_task_object_by_status_and_stage_invalid_arguments(tos):
    with pytest.raises(TypeError) as err:
        tos.find_one_task_object_by_status_and_stage()

    assert "Pass statuses or stages or both." in str(err.value)


def test_find_one_task_object_by_status_and_stage_with_query_amend(tos_with_inserted_object):
    tos, _ = tos_with_inserted_object
    to = tos.find_one_task_object_by_status_and_stage(
        statuses="new",
        stages=0,
        query_amend={"payload.data": 213213}
    )
    assert to


def test_find_one_task_object_by_stage_with_query_amend(tos_with_inserted_object):
    tos, _ = tos_with_inserted_object
    to = tos.find_one_task_object_by_status_and_stage(
        stages=0,
        query_amend={"payload.data": 213213}
    )
    assert to


def test_find_one_task_object_by_stage(tos):
    _ = tos.create_new_task_object(
        {"data": 65646},
    )
    item2 = tos.create_new_task_object(
        {"data": 7657},
    )

    tos.set_task_object_stage(item2["_id"], 2)

    to = tos.find_one_task_object_by_stage(2)

    assert to
