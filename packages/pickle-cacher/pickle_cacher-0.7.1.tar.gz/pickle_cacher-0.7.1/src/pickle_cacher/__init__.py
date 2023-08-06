"""Pickle-based caching."""
from __future__ import annotations

from pickle_cacher.pickle_cacher import cached  # noqa: S403

from ._version import get_versions


__all__ = ["cached"]
__version__ = get_versions()["version"]
del get_versions
