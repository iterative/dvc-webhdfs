from contextlib import contextmanager

from dvc.testing.cloud import Cloud
from dvc.testing.path_info import CloudURLInfo


class WebHDFS(Cloud, CloudURLInfo):  # pylint: disable=abstract-method
    @contextmanager
    def _webhdfs(self):
        from hdfs import InsecureClient

        client = InsecureClient(
            f"http://{self.host}:{self.port}", self.user, root="/"
        )
        yield client

    def is_file(self):
        with self._webhdfs() as _hdfs:
            return _hdfs.status(self.path)["type"] == "FILE"

    def is_dir(self):
        with self._webhdfs() as _hdfs:
            return _hdfs.status(self.path)["type"] == "DIRECTORY"

    def exists(self):
        with self._webhdfs() as _hdfs:
            return _hdfs.status(self.path, strict=False) is not None

    def mkdir(self, mode=0o777, parents=False, exist_ok=False):
        assert mode == 0o777
        assert parents

        with self._webhdfs() as _hdfs:
            # NOTE: hdfs.makekdirs always creates parents
            _hdfs.makedirs(self.path, permission=mode)

    def write_bytes(self, contents):
        with self._webhdfs() as _hdfs:
            with _hdfs.write(self.path, overwrite=True) as writer:
                writer.write(contents)

    def read_bytes(self):
        with self._webhdfs() as _hdfs:
            with _hdfs.read(self.path) as reader:
                return reader.read()

    @property
    def config(self):
        return {"url": self.url}

    @property
    def fs_path(self):
        return "/" + self.path.lstrip("/")
