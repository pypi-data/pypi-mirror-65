"""
Test task object storage module.
"""
import pytest
import mongomock

from tos.task_object_storage import TaskObjectStorage
from . import (
    MOCK_PORT,
    MOCK_SERVER,
    tos,
    tos_with_inserted_object
)


def test_initializing_with_no_mongo_running():
    """Use real non-mocked TOS here to access the method.

    There should not be a running mongo server!
    """
    with pytest.raises(Exception) as err:
        tos_object = TaskObjectStorage(
            db_server=f"{MOCK_SERVER}:{MOCK_PORT}",
            db_name="test_tos_db",
            timeout=0.1  # low timeout because we know this should fail anyway
        )

    assert "Is MongoDB running?" in str(err.value)


def test_initializing_with_no_mongo_running_with_authentication():
    """Use real non-mocked TOS here to access the method.

    There should not be a running mongo server!
    """
    with pytest.raises(Exception) as err:
        tos_object = TaskObjectStorage(
            db_server=f"{MOCK_SERVER}:{MOCK_PORT}",
            db_name="test_tos_db",
            db_user="test_user",
            db_passw="test_passw",
            timeout=0.1  # low timeout because we know this should fail anyway
        )

    assert "Is MongoDB running?" in str(err.value)


def test_context_managed_task_object_storage(mocker):

    def mocked_connect(*args):
        """Mock the mongo connect method"""
        return mongomock.MongoClient()

    mocker.patch('tos.task_object_storage.TaskObjectStorage.connect',
                 mocked_connect)

    with TaskObjectStorage(
        db_server=f"{MOCK_SERVER}:{MOCK_PORT}",
        db_name="test_tos_db",
    ) as tos:
        assert tos._check_connection_established(tos.client)

    # NOTE: mongomock.MongoClient().close() doesn't do anything
    # so it's hard to test the disconnect method without real
    # mongodb instance.


@pytest.mark.xfail
def test_validation(tos_with_inserted_object):
    """Mongomock does not support validation.

    It raises NotImplementedError when passing kwargs
    to db.create_collection
    """
    raise NotImplementedError
