from typing import Union
from collections import Iterator

from aimrecords.record_storage.reader import RecordReader


class ArtifactReader(Iterator):
    def __init__(self, path: str):
        self.path = path
        self._artifact = RecordReader(path)
        self._iter = None

    def __next__(self):
        try:
            idx = next(self._iter)
            return self._artifact.get(idx)
        except (IndexError, StopIteration):
            self._iter = None
            raise StopIteration

    def __getitem__(self, item: Union[int, tuple, slice]):
        if isinstance(item, int):
            self._iter = iter((item,))
        elif isinstance(item, tuple):
            self._iter = iter(item)
        elif isinstance(item, slice):
            start, stop, step = item.start, item.stop, item.step
            indices_range = range(self._artifact.records_num)
            self._iter = iter(indices_range[start:stop:step])
        else:
            raise TypeError('expected slice or list of indices')

        return iter(self)
