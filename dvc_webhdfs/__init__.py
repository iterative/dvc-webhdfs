import threading
from typing import Any

# pylint:disable=abstract-method
from dvc.utils.objects import cached_property
from dvc_objects.fs.base import FileSystem
from funcy import wrap_prop


class WebHDFSFileSystem(FileSystem):
    protocol = "webhdfs"
    REQUIRES = {"fsspec": "fsspec"}
    PARAM_CHECKSUM = "checksum"

    def __init__(self, fs=None, **kwargs: Any):
        self._ssl_verify = kwargs.pop("ssl_verify", True)
        super().__init__(fs, **kwargs)

    @classmethod
    def _strip_protocol(cls, path: str) -> str:
        from fsspec.utils import infer_storage_options

        return infer_storage_options(path)["path"]

    def unstrip_protocol(self, path: str) -> str:
        host = self.fs_args["host"]
        port = self.fs_args["port"]
        path = path.lstrip("/")
        return f"webhdfs://{host}:{port}/{path}"

    @staticmethod
    def _get_kwargs_from_urls(urlpath):
        from fsspec.implementations.webhdfs import WebHDFS

        return (
            WebHDFS._get_kwargs_from_urls(  # pylint:disable=protected-access
                urlpath
            )
        )

    def _prepare_credentials(self, **config):
        principal = config.pop("kerberos_principal", None)
        if principal:
            config["kerb_kwargs"] = {"principal": principal}
        return config

    @wrap_prop(threading.Lock())
    @cached_property
    def fs(self):
        from fsspec.implementations.webhdfs import WebHDFS

        # If target data_proxy provided construct the source from host/port
        if "data_proxy_target" in self.fs_args:
            host = self.fs_args["host"]
            port = self.fs_args["port"]

            protocol = "https" if self.fs_args.get("use_https") else "http"

            self.fs_args["data_proxy"] = {
                f"{protocol}://{host}:{port}/webhdfs/v1":self.fs_args["data_proxy_target"]
            }

        fs = WebHDFS(**self.fs_args)
        fs.session.verify = self._ssl_verify
        return fs

    def checksum(self, path):
        ukey = self.fs.ukey(path)
        return ukey["bytes"]
