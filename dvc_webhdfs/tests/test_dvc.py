import pytest

from dvc.testing.api_tests import (  # noqa: F401
    TestAPI,
)
from dvc.testing.remote_tests import (  # noqa: F401
    TestRemote,
)
from dvc.testing.workspace_tests import TestImport as _TestImport


@pytest.fixture
def remote(make_remote):
    return make_remote(name="upstream", typ="webhdfs")


@pytest.fixture
def workspace(make_workspace):
    return make_workspace(name="workspace", typ="webhdfs")


class TestImport(_TestImport):
    @pytest.fixture
    def stage_md5(self):
        return "f5f3369ef4fa451ddd6ab51f7fb42f7f"

    @pytest.fixture
    def is_object_storage(self):
        return False

    @pytest.fixture
    def dir_md5(self):
        return "32f6597da5c3c1dead9dc562faac09a2.dir"
