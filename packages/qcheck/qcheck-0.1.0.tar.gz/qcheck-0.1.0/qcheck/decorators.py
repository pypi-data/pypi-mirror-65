from __future__ import annotations

import inspect
from functools import wraps, partial
from typing import Callable, List, Optional

from .error import Error
from .exceptions import BaseCheckErrors, CheckErrors
from .run_check import run_check_async, run_check_sync


def default_extract_errors_fn(e: Exception) -> Optional[List[Error]]:
    if isinstance(e, BaseCheckErrors):
        return e.errors
    return None


def default_exeption_class_factory(errors: List[Error]) -> CheckErrors:
    return CheckErrors(errors)


def _decorate(
    fn: Callable,
    *,
    raise_exception: bool = False,
    exception_class_factory: Callable[
        [List[Error]], Exception
    ] = default_exeption_class_factory,
    extract_errors_fn: Callable[
        [Exception], Optional[List[Error]]
    ] = default_extract_errors_fn,
) -> Callable:
    if not callable(fn):
        raise TypeError(f"Improperly decorated, expected a function, got {fn!r}")

    is_async = inspect.iscoroutinefunction(fn) or inspect.isasyncgenfunction(fn)

    if is_async:

        @wraps(fn)
        async def _check_fn(*args, **kwargs):
            _raise_exception = kwargs.pop("raise_exception", raise_exception)

            try:
                errors = await run_check_async(errors_producer=fn(*args, **kwargs))
                if errors and _raise_exception:
                    raise exception_class_factory(errors)

            except Exception as e:
                errors = extract_errors_fn(e)
                if errors is None:
                    raise

                if errors and _raise_exception:
                    raise exception_class_factory(errors) from e

            return errors

    else:

        @wraps(fn)
        def _check_fn(*args, **kwargs):
            _raise_exception = kwargs.pop("raise_exception", raise_exception)

            try:
                errors = run_check_sync(errors_producer=fn(*args, **kwargs))
                if errors and _raise_exception:
                    raise exception_class_factory(errors)

            except Exception as e:
                errors = extract_errors_fn(e)
                if errors is None:
                    raise

                if errors and _raise_exception:
                    raise exception_class_factory(errors) from e

            return errors

    return _check_fn


def checker(fn: Optional[Callable] = None, **kwargs) -> Callable:
    if fn is not None:
        return _decorate(fn, **kwargs)
    return partial(_decorate, **kwargs)
