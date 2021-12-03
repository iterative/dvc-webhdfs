import uuid

import pytest

from .cloud import WebHDFS


@pytest.fixture
def make_webhdfs(hdfs_server):
    def _make_webhdfs():
        port = hdfs_server["webhdfs"]
        url = f"webhdfs://127.0.0.1:{port}/{uuid.uuid4()}"
        return WebHDFS(url)

    return _make_webhdfs


@pytest.fixture
def webhdfs(make_webhdfs):
    return make_webhdfs()
