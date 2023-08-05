from __future__ import annotations

from inspect import signature
from itertools import zip_longest
from logging import DEBUG
from pathlib import Path
from re import search
from typing import Any
from typing import List
from typing import Set

from pickle_cacher import cached
from pickle_cacher.pickle_cacher import LOGGER


LOGGER.setLevel(DEBUG)


def assert_caplog_records(caplog: Any, length: int, *patterns: str) -> None:
    records = caplog.records
    assert len(records) == length
    for record, pattern in reversed(list(zip_longest(reversed(records), reversed(patterns)))):
        if pattern is not None:
            assert search(pattern, record.message)


def test_cached_on_a_function(caplog: Any) -> None:
    elements: Set[int] = set()

    @cached
    def get_size() -> int:
        return len(elements)

    assert get_size() == 0
    assert_caplog_records(caplog, 1, r"^Computed and cached: <BoundArguments \(\)> -> 0$")
    elements.add(0)
    assert get_size() == 0
    assert_caplog_records(caplog, 2, r"^Retrieved from cache: <BoundArguments \(\)> -> 0$")

    def dummy(*, overwrite: bool = False) -> int:
        pass

    assert signature(get_size) == signature(dummy)
    assert get_size(overwrite=True) == 1
    assert_caplog_records(caplog, 3, r"^Re-computed and cached: <BoundArguments \(\)> -> 1$")
    elements.add(1)
    assert get_size() == 1
    assert_caplog_records(caplog, 4, r"^Retrieved from cache: <BoundArguments \(\)> -> 1$")


def test_cached_on_a_function_with_unhashable_arguments(caplog: Any) -> None:
    @cached
    def append(x: List[int]) -> List[int]:
        return x + [len(x)]

    assert append([]) == [0]
    assert_caplog_records(caplog, 1, r"^Computed and cached: <BoundArguments \(x=\[\]\)> -> \[0\]$")


def test_cached_on_a_function_with_disk_persistence(tmp_path: Path, caplog: Any) -> None:
    path = Path(tmp_path).joinpath("cache")

    def disk(wrapped: Any, instance: Any) -> Path:
        return path

    elements: Set[int] = set()

    @cached(disk=disk)  # type: ignore
    def get_size() -> int:
        return len(elements)

    assert get_size() == 0
    assert_caplog_records(
        caplog,
        2,
        r"^Computed and cached: <BoundArguments \(\)> -> 0$",
        fr"^Persisted to {path}/\w+: <BoundArguments \(\)> -> 0$",
    )
    elements.add(0)
    assert get_size() == 0
    assert_caplog_records(
        caplog, 3, r"^Retrieved from cache: <BoundArguments \(\)> -> 0$",
    )
    assert get_size(overwrite=True) == 1
    assert_caplog_records(
        caplog,
        5,
        r"^Re-computed and cached: <BoundArguments \(\)> -> 1$",
        fr"^Re-persisted to {path}/\w+: <BoundArguments \(\)> -> 1$",
    )
    elements.add(1)
    assert get_size() == 1
    assert_caplog_records(
        caplog, 6, r"^Retrieved from cache: <BoundArguments \(\)> -> 1$",
    )


def test_defaults_are_bound(caplog: Any) -> None:
    @cached
    def add(x: int, y: int = 1) -> int:
        return x + y

    assert add(0) == 1
    assert_caplog_records(
        caplog, 1, r"^Computed and cached: <BoundArguments \(x=0, y=1\)> -> 1$",
    )
    assert add(0, y=1) == 1
    assert_caplog_records(
        caplog, 2, r"^Retrieved from cache: <BoundArguments \(x=0, y=1\)> -> 1$",
    )
