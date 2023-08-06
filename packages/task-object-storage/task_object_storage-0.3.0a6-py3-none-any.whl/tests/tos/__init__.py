"""
This module contains `tos` test fixtures and variables.
"""
import os

import pytest
import mongomock

from tos.task_object_storage import TaskObjectStorage

DIRNAME = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(DIRNAME, "..", "test_data")

MOCK_SERVER = "127.0.0.1"
MOCK_PORT = 16


@pytest.fixture
def tos(mocker):
    def mocked_connect(*args):
        """Mock the mongo connect method."""
        return mongomock.MongoClient()

    mocker.patch('tos.task_object_storage.TaskObjectStorage.connect',
                 mocked_connect)

    # NOTE: Other option would be to use a real Mongo server
    # and mongomock.patch, see
    # https://github.com/mongomock/mongomock

    tos_object = TaskObjectStorage(
        db_server=f"{MOCK_SERVER}:{MOCK_PORT}",
        db_name="test_tos_db",
    )
    tos_object.initialize_tos()
    return tos_object


@pytest.fixture
def tos_with_inserted_object(tos):
    payload = {"data": 213213}

    item = tos.create_new_task_object(
        payload,
    )

    return tos, item
