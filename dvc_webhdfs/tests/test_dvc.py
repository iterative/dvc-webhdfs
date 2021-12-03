import pytest
from dvc.testing.test_api import TestAPI  # noqa, pylint: disable=unused-import
from dvc.testing.test_remote import (  # noqa, pylint: disable=unused-import
    TestRemote,
)
from dvc.testing.test_workspace import (  # noqa, pylint: disable=unused-import
    TestAdd,
    TestImport,
)


@pytest.fixture
def cloud_name():
    return "webhdfs"


@pytest.fixture
def remote(make_remote, cloud_name):
    yield make_remote(name="upstream", typ=cloud_name)


@pytest.fixture
def workspace(make_workspace, cloud_name):
    yield make_workspace(name="workspace", typ=cloud_name)


@pytest.fixture
def stage_md5():
    return "3869631c193f0a3c206c6f04e84cb2b6"


@pytest.fixture
def is_object_storage():
    return False


@pytest.fixture
def dir_md5():
    return "32f6597da5c3c1dead9dc562faac09a2.dir"


@pytest.fixture
def hash_name():
    return "checksum"


@pytest.fixture
def hash_value():
    return "000002000000000000000000a86fe4d846edc1bf4c355cb6112f141e00000000"


@pytest.fixture
def dir_hash_value(dir_md5):
    pytest.skip("external outputs are broken for hdfs dirs")
