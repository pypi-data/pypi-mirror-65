from typing import BinaryIO
import io
import time


def transfer(source: BinaryIO, target: BinaryIO):
    """
    Read from source and write to target until source is exhausted.
    """
    while True:
        chunk = source.read1()
        if not chunk:
            return
        target.write(chunk)


class CounterSink(io.IOBase):
    """
    Writable file-like object that discards written bytes after counting them.
    """

    size: int = 0

    def readable(self) -> bool:
        return False

    def write(self, b: bytes) -> int:
        bsize = len(b)
        self.size += bsize
        return bsize


class TimerContext:
    begin: float
    end: float

    @property
    def elapsed(self) -> float:
        if self.begin:
            if self.end:
                return self.end - self.begin
            return time.time() - self.begin
        return None

    def __enter__(self):
        self.begin = time.time()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.end = time.time()
