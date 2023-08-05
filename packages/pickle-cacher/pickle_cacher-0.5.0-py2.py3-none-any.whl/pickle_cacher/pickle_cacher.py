from __future__ import annotations

import gzip
import inspect
import pickle
from functools import partial
from hashlib import md5
from inspect import signature
from logging import DEBUG
from logging import getLogger
from logging import StreamHandler
from pathlib import Path
from sys import stdout
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional
from typing import Tuple
from typing import TypeVar
from typing import Union

from atomic_write_path import atomic_write_path
from wrapt import adapter_factory
from wrapt import decorator


LOGGER = getLogger("pickle_cacher")
_HANDLER = StreamHandler(stream=stdout)
_HANDLER.setLevel(DEBUG)
LOGGER.addHandler(_HANDLER)
PICKLE_CACHE = "_pickle_cache"
T = TypeVar("T")


def _gzip_load(file: Union[str, Path]) -> object:
    """Load a Gzipped-pickle."""

    with gzip.open(str(file), mode="rb") as file_handle:
        return pickle.loads(file_handle.read())


def _gzip_dump(obj: object, file: Union[str, Path]) -> None:
    """Dump an object as a Gzipped-pickle."""

    with gzip.open(file, mode="wb") as file_handle:
        file_handle.write(pickle.dumps(obj))


def cached(
    wrapped: Any = None,
    *,
    disk: Optional[Callable[[Any, Any], Path]] = None,
    load: Callable[[Union[str, Path]], Any] = _gzip_load,
    dump: Callable[[Any, Union[str, Path]], None] = _gzip_dump,
):
    if wrapped is None:
        return partial(cached, disk=disk)
    else:
        if disk is None:

            @decorator
            def wrapper(
                wrapped: Callable, instance: Any, args: Tuple[Any, ...], kwargs: Dict[str, Any],
            ) -> Any:
                return _cache_decorator(wrapped)(*args, **kwargs)

        else:

            @decorator(adapter=adapter_factory(_argspec_factory))
            def wrapper(
                wrapped: Callable, instance: Any, args: Tuple[Any, ...], kwargs: Dict[str, Any],
            ) -> Any:
                decorated = _cache_decorator(wrapped)
                overwrite = kwargs.get("overwrite", False)
                bound_args = BoundArguments.from_wrapped(
                    decorated, *args, **{k: v for k, v in kwargs.items() if k != "overwrite"},
                )
                path = disk(decorated, instance).joinpath(decorated.__name__, bound_args.md5)
                if overwrite:
                    out = decorated(*bound_args.args, **bound_args.kwargs)
                    with atomic_write_path(path, overwrite=overwrite) as temp:
                        dump(out, temp)
                    LOGGER.debug(
                        f"Computed (overwrite) and persisted to {path}: {bound_args} -> {out}",
                    )
                    return out
                else:
                    try:
                        out = load(path)
                    except FileNotFoundError:
                        out = decorated(*bound_args.args, **bound_args.kwargs)
                        with atomic_write_path(path, overwrite=overwrite) as temp:
                            dump(out, temp)
                        LOGGER.debug(f"Computed and persisted to {path}: {bound_args} -> {out}")
                        return out
                    else:
                        LOGGER.debug(f"Retrived from {path}: {bound_args} -> {out}")
                        return out

        return wrapper(wrapped)


@decorator
def _cache_decorator(
    wrapped: Callable[..., T], instance: Any, args: Tuple[Any, ...], kwargs: Dict[str, Any],
) -> Callable[..., T]:
    if instance is None:
        try:
            cache = getattr(wrapped, PICKLE_CACHE)
        except AttributeError:
            setattr(wrapped, PICKLE_CACHE, {})
            cache = getattr(wrapped, PICKLE_CACHE)
    else:
        try:
            instance_cache = getattr(instance, PICKLE_CACHE)
        except AttributeError:
            setattr(instance, PICKLE_CACHE, {})
            instance_cache = getattr(instance, PICKLE_CACHE)
        name = wrapped.__name__
        try:
            cache = instance_cache[name]
        except KeyError:
            cache = instance_cache[name] = {}
    bound_args = BoundArguments.from_wrapped(wrapped, *args, **kwargs)
    try:
        out = cache[bound_args]
    except KeyError:
        out = cache[bound_args] = wrapped(*bound_args.args, **bound_args.kwargs)
        LOGGER.debug(f"Computed and cached: {bound_args} -> {out}")
        return out
    else:
        LOGGER.debug(f"Retrieved from cache: {bound_args} -> {out}")
        return out


class BoundArguments(inspect.BoundArguments):
    @classmethod
    def from_wrapped(cls, wrapped, *args, **kwargs):
        sig = signature(wrapped)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        return cls(sig, bound_args.arguments)

    def __bytes__(self):
        return pickle.dumps((self.args, self.kwargs))

    def __hash__(self):
        return hash(bytes(self))

    @property
    def md5(self):
        return md5(bytes(self)).hexdigest()


def _argspec_factory(wrapped):
    full_arg_spec = inspect.getfullargspec(wrapped)
    return full_arg_spec._replace(
        kwonlyargs=["overwrite"],
        kwonlydefaults={"overwrite": False},
        annotations={"overwrite": bool},
    )
