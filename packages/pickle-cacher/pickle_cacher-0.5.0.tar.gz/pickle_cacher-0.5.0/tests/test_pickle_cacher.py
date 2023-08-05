from __future__ import annotations

from logging import DEBUG
from pathlib import Path
from typing import Any
from typing import List

from pickle_cacher import cached
from pickle_cacher.pickle_cacher import LOGGER
from pickle_cacher.pickle_cacher import PICKLE_CACHE

LOGGER.setLevel(DEBUG)


def test_cached_on_a_function(caplog: Any) -> None:
    @cached
    def increment(x: int) -> int:
        return x + 1

    assert not hasattr(increment, PICKLE_CACHE)
    assert increment(0) == 1
    cache = getattr(increment, PICKLE_CACHE)
    assert isinstance(cache, dict)
    assert list(cache.values()) == [1]
    (record,) = caplog.records
    assert record.message == "Computed and cached: <BoundArguments (x=0)> -> 1"
    assert increment(0) == 1
    _, record = caplog.records
    assert record.message == "Retrieved from cache: <BoundArguments (x=0)> -> 1"


def test_cached_on_an_unhashable_argument(caplog: Any) -> None:
    @cached
    def append(x: List[int]) -> List[int]:
        return x + [len(x)]

    assert append([]) == [0]
    (record,) = caplog.records
    assert record.message == "Computed and cached: <BoundArguments (x=[])> -> [0]"


def test_cached_on_a_function_with_disk_persistence(tmp_path: Path, caplog: Any) -> None:
    def disk(wrapped: Any, instance: Any) -> Path:
        return tmp_path

    @cached(disk=disk)
    def increment(x: int) -> int:
        return x + 1

    assert increment(0) == 1
    (record,) = caplog.records
    assert record.message == "Computed and cached: <BoundArguments (x=0)> -> 1"
    assert increment(0) == 1
    *_, record = caplog.records
    assert record.message == "Retrieved from cache: <BoundArguments (x=0)> -> 1"


#
# class ExampleCacher(PickleCacher):
#     def __init__(self: ExampleCacher, root: Path, name: str) -> None:
#         self.root = root
#         self.name = name
#
#     def __eq__(self: ExampleCacher, other: Any) -> bool:
#         if isinstance(other, ExampleCacher):
#             return self.name == other.name
#         else:
#             return NotImplemented
#
#     def __hash__(self: ExampleCacher) -> int:
#         return hash(self.name)
#
#     @property
#     def path(self: ExampleCacher) -> Path:
#         return self.root.joinpath(self.name)
#
#     @cached
#     def increment(self: ExampleCacher, x: int, *, n: int = 1) -> int:
#         print(f"Incrementing {x} by {n}...")  # : WPS421
#         return x + n
#
#     @cached
#     def decrement(self: ExampleCacher, x: int) -> int:
#         print(f"Decrementing {x}...")  # : WPS421
#         return x - 1
#
#
# def test_pickle_cacher(tmp_path: Path, capfd: Any) -> None:
#     cacher = ExampleCacher(tmp_path, "test_pickle_cacher")
#
#     # initialization
#     assert not capfd.readouterr().out
#     root = tmp_path.joinpath("test_pickle_cacher")
#     assert not root.exists()
#
#     # first call
#     assert cacher.increment(0) == 1
#     assert capfd.readouterr().out == "Incrementing 0 by 1...\n"
#     path_increment = root.joinpath("increment")
#     assert set(root.iterdir()) == {path_increment}
#     assert len(set(path_increment.iterdir())) == 1
#     with gzip.open(next(path_increment.iterdir()), mode="rb") as fh:
#         assert pickle.loads(fh.read()) == 1  :
#
#     # second call
#     assert cacher.increment(0) == 1
#     assert not capfd.readouterr().out
#     assert len(set(path_increment.iterdir())) == 1
#
#     # third call
#     assert cacher.increment(1) == 2
#     assert capfd.readouterr().out == "Incrementing 1 by 1...\n"
#     assert len(set(path_increment.iterdir())) == 2
#
#     # fourth call
#     assert cacher.decrement(0) == -1
#     assert capfd.readouterr().out == "Decrementing 0...\n"
#     path_decrement = root.joinpath("decrement")
#     assert set(root.iterdir()) == {path_increment, path_decrement}
#     assert len(set(path_increment.iterdir())) == 2
#     assert len(set(path_decrement.iterdir())) == 1
#
#
# def test_wrapping(tmp_path: Path) -> None:
#     cacher = ExampleCacher(tmp_path, "test_wrapping")
#
#     def increment(self: ExampleCacher, x: int, *, n: int = 1) -> int:
#         pass
#
#     assert signature(cacher.increment) == signature(increment)
#
#
# def test_defaults_are_bound(tmp_path: Path) -> None:
#     path_increment = tmp_path.joinpath("test_defaults_are_bound").joinpath("increment")
#     assert not path_increment.exists()
#
#     # call with no defaults
#     cacher = ExampleCacher(tmp_path, "test_defaults_are_bound")
#     assert cacher.increment(0) == 1
#     assert len(set(path_increment.iterdir())) == 1
#
#     # call with defaults
#     cacher = ExampleCacher(tmp_path, "test_defaults_are_bound")
#     assert cacher.increment(0, n=1) == 1
#     assert len(set(path_increment.iterdir())) == 1
