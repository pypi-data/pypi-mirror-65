from __future__ import annotations

import gzip
import inspect
import pickle
from functools import partial
from hashlib import md5
from inspect import FullArgSpec
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
from typing import Type
from typing import Union

from atomic_write_path import atomic_write_path
from wrapt import adapter_factory
from wrapt import decorator


_PICKLE_CACHE = "pickle_cache"
_ATTR_NAME = f"_{_PICKLE_CACHE}"
LOGGER = getLogger(_PICKLE_CACHE)
_HANDLER = StreamHandler(stream=stdout)
_HANDLER.setLevel(DEBUG)
LOGGER.addHandler(_HANDLER)


def _gzip_load(file: Union[str, Path]) -> object:
    """Load a Gzipped-pickle."""

    with gzip.open(str(file), mode="rb") as file_handle:
        return pickle.loads(file_handle.read())


def _gzip_dump(obj: object, file: Union[str, Path]) -> None:
    """Dump an object as a Gzipped-pickle."""

    with gzip.open(file, mode="wb") as file_handle:
        file_handle.write(pickle.dumps(obj))


def cached(
    func: Any = None,
    *,
    disk: Optional[Callable[[Any, Any], Optional[Path]]] = None,
    load: Callable[[Union[str, Path]], Any] = _gzip_load,
    dump: Callable[[Any, Union[str, Path]], None] = _gzip_dump,
) -> Any:
    """Make a function/method caching.

    By default, the decorator (or decorator factory) caches results on the pickled-representation of the input
    arguments. Optionally, the decorator can persist results to disk.
    """

    if func is None:
        return partial(cached, disk=disk, load=load, dump=dump)
    else:

        @decorator(adapter=adapter_factory(_argspec_factory))  # type: ignore
        def wrapper(
            wrapped: Callable[..., Any],
            instance: Any,
            args: Tuple[Any, ...],
            kwargs: Dict[str, Any],
        ) -> Any:
            name = wrapped.__name__

            if instance is None:
                try:
                    cache = getattr(wrapped, _ATTR_NAME)
                except AttributeError:
                    setattr(wrapped, _ATTR_NAME, {})
                    cache = getattr(wrapped, _ATTR_NAME)
            else:
                try:
                    instance_cache = getattr(instance, _ATTR_NAME)
                except AttributeError:
                    setattr(instance, _ATTR_NAME, {})
                    instance_cache = getattr(instance, _ATTR_NAME)
                try:
                    cache = instance_cache[name]
                except KeyError:
                    cache = instance_cache[name] = {}

            overwrite = kwargs.pop("overwrite", False)
            bound_args = BoundArguments.from_wrapped(wrapped, *args, **kwargs)

            if disk is None:
                path: Optional[Path] = None
            else:
                maybe_path = disk(wrapped, instance)
                if maybe_path is None:
                    path = maybe_path
                else:
                    if instance is None:
                        path = maybe_path.joinpath(bound_args.md5)
                    else:
                        path = maybe_path.joinpath(name, bound_args.md5)

            if overwrite:
                out = cache[bound_args] = wrapped(*args, **kwargs)
                LOGGER.debug(f"Re-computed and cached: {bound_args} -> {out}")
                if path is not None:
                    with atomic_write_path(path, overwrite=overwrite) as temp1:
                        dump(out, temp1)
                    LOGGER.debug(f"Re-persisted to {path}: {bound_args} -> {out}")
            else:
                try:
                    out = cache[bound_args]
                except KeyError:
                    if path is None:
                        out = cache[bound_args] = wrapped(*args, **kwargs)
                        LOGGER.debug(f"Computed and cached: {bound_args} -> {out}")
                    else:
                        try:
                            out = load(path)
                        except FileNotFoundError:
                            out = cache[bound_args] = wrapped(*args, **kwargs)
                            LOGGER.debug(f"Computed and cached: {bound_args} -> {out}")
                            with atomic_write_path(path, overwrite=overwrite) as temp3:
                                dump(out, temp3)
                            LOGGER.debug(f"Persisted to {path}: {bound_args} -> {out}")
                        else:
                            LOGGER.debug(f"Retrieved from {path}: {bound_args} -> {out}")
                else:
                    LOGGER.debug(f"Retrieved from cache: {bound_args} -> {out}")
            return out

        return wrapper(func)


def _argspec_factory(wrapped: Callable[..., Any]) -> FullArgSpec:
    full_arg_spec = inspect.getfullargspec(wrapped)
    return full_arg_spec._replace(  # noqa: WPS437
        kwonlyargs=full_arg_spec.kwonlyargs + ["overwrite"],
        kwonlydefaults={
            **({} if full_arg_spec.kwonlydefaults is None else full_arg_spec.kwonlydefaults),
            **{"overwrite": False},
        },
        annotations={**full_arg_spec.annotations, **{"overwrite": "bool"}},
    )


class BoundArguments(inspect.BoundArguments):
    """Sub-class of inspect.BoundArguments which is hashable."""

    @classmethod
    def from_wrapped(
        cls: Type[BoundArguments], wrapped: Callable[..., Any], *args: Any, **kwargs: Any,
    ) -> BoundArguments:
        """Create an instance from a function and the call args/kwargs."""

        sig = signature(wrapped)
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        return cls(sig, bound_args.arguments)  # type: ignore

    def __bytes__(self: BoundArguments) -> bytes:
        return pickle.dumps((self.args, self.kwargs))

    def __hash__(self: BoundArguments) -> int:
        return hash(bytes(self))

    @property
    def md5(self: BoundArguments) -> str:
        """Get the MD5 hash of the bound arguments."""

        return md5(bytes(self)).hexdigest()
