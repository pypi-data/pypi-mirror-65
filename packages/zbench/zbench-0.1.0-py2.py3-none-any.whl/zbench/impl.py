from bz2 import BZ2File
from gzip import GzipFile
from lzma import LZMAFile
from zipfile import ZipFile
import zlib

from .util import CounterSink, transfer


def raw_py(path: str) -> int:
    with CounterSink() as sink:
        with open(path, "rb") as source:
            transfer(source, sink)
        return sink.size


def gzip_py(path: str) -> int:
    with CounterSink() as sink:
        with GzipFile(fileobj=sink, mode="wb") as target:
            with open(path, "rb") as source:
                transfer(source, target)
        return sink.size


def bz2_py(path: str) -> int:
    with CounterSink() as sink:
        with BZ2File(sink, mode="wb") as target:
            with open(path, "rb") as source:
                transfer(source, target)
        return sink.size


def lzma_py(path: str) -> int:
    with CounterSink() as sink:
        with LZMAFile(sink, mode="wb") as target:
            with open(path, "rb") as source:
                transfer(source, target)
        return sink.size


def zlib_py(path: str) -> int:
    with CounterSink() as sink:
        # zlib does not provide any file-like API
        compress = zlib.compressobj()
        with open(path, "rb") as source:
            while True:
                chunk = source.read1()
                if not chunk:
                    break
                sink.write(compress.compress(chunk))
            sink.write(compress.flush())
        return sink.size


def zip_py(path: str) -> int:
    with CounterSink() as sink:
        with ZipFile(sink, mode="w") as zipfile:
            with zipfile.open("x", mode="w") as target:
                with open(path, "rb") as source:
                    transfer(source, target)
        return sink.size


all_impls = [raw_py, gzip_py, bz2_py, lzma_py, zlib_py, zip_py]

try:
    from lz4.frame import LZ4FrameFile  # pylint: disable=import-error

    def lz4_py(path: str) -> int:
        with CounterSink() as sink:
            with LZ4FrameFile(sink, mode="wb") as target:
                with open(path, "rb") as source:
                    transfer(source, target)
            return sink.size

    all_impls.append(lz4_py)
except ModuleNotFoundError:
    pass
