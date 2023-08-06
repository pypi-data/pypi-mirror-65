import os

import pytest
from bson.binary import Binary

from . import (
    TEST_DATA_DIR,
    tos,
    tos_with_inserted_object
)


def test_add_binary_data_to_payload(tos_with_inserted_object):
    tos, item = tos_with_inserted_object
    test_pdf = os.path.join(TEST_DATA_DIR, "letter.pdf")
    pdf_title = "testi-pdf"

    tos.add_binary_data_to_payload(item["_id"], test_pdf, pdf_title)

    updated_item = tos.find_task_object_by_id(item["_id"])

    assert updated_item["payload"].get(pdf_title)
    assert isinstance(updated_item["payload"][pdf_title], Binary)


def test_save_binary_payload_to_tmp(tos):
    test_pdf = os.path.join(TEST_DATA_DIR, "letter.pdf")
    to = {
        "status": "new",
        "priority": 0,
        "payload": {
            "data": 213213,
            "test-pdf": tos._encode_binary_data(test_pdf),
        }
    }

    tmp_file = tos.save_binary_payload_to_tmp(to, "test-pdf")

    assert isinstance(to["payload"]["test-pdf"], Binary)
    assert os.path.isfile(tmp_file)

    os.remove(tmp_file)


def test_update_payload(tos):
    initial_payload = {"data": 213213}
    new_data = {
        "new_data": "xxxx",
        "more_new_data": "yyy"
    }

    to = {
        "status": "new",
        "priority": 0,
        "payload": initial_payload
    }

    tos._insert_task_object(to)
    object_id = to["_id"]

    inserted_object = tos.find_task_object_by_id(object_id)
    _ = tos.update_payload(object_id, new_data)
    inserted_object_again = tos.find_task_object_by_id(object_id)

    assert inserted_object["payload"] == initial_payload
    assert inserted_object_again["payload"] == {**initial_payload, **new_data}


def test_update_payload_with_error(tos):
    initial_payload = {"data": 213213}
    new_data = ("new_data", "xxxx")

    to = {
        "status": "new",
        "priority": 0,
        "payload": initial_payload
    }

    tos._insert_task_object(to)
    object_id = to["_id"]

    with pytest.raises(TypeError) as err:
        _ = tos.update_payload(object_id, new_data)

    assert "Argument update should be a dict" in str(err.value)


def test_push_value_to_array_field(tos_with_inserted_object):
    tos, item = tos_with_inserted_object
    alert_text = "2 transactions confirmed"

    tos.push_value_to_array_field(item["_id"], alert_text, "payload.alerts")
    to = tos.find_task_object_by_id(item["_id"])

    assert to["payload"]["alerts"][0] == alert_text
