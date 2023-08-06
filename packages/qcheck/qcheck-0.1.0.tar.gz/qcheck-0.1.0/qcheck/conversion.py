from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum
import inspect
from functools import wraps, partial
from typing import List, Optional, Callable, Union, Any


from .error import Error
from .exceptions import BaseCheckErrors, CheckErrors


class ErrorSource(Enum):
    QCHECK = "qcheck"
    PYDANTIC = "pydantic"
    DRF_SERIALIZER = "drf-serializer"
    DJANGO_FORM = "django-form"


KNOWN_EXCEPTIONS = {
    ErrorSource.QCHECK.value: {
        BaseCheckErrors: lambda exc: exc.errors,
        CheckErrors: lambda exc: exc.errors,
    }
}

try:
    import pydantic

    def pydantic_error_parser(error: pydantic.ValidationError) -> List[Error]:
        return [
            Error(
                message=err["msg"],
                code=err.get("type"),
                locations=err.get("loc"),
                data=err.get("ctx"),
            )
            for err in error.errors()
        ]

    KNOWN_EXCEPTIONS[ErrorSource.PYDANTIC.value] = {
        pydantic.ValidationError: pydantic_error_parser
    }
except ImportError:
    pass


def try_extract_errors(
    e: Exception, error_sources: Optional[List[ErrorSource]] = None
) -> List[Error]:
    """
    Convert `e` to a list of `qcheck.Error`.

    If `e` is unknown exception, the func returns `None`.

    `error_sources` allows to narrow the set of know exceptions for handling `e`.
    """
    if error_sources is None:
        error_sources = KNOWN_EXCEPTIONS.keys()

    for source_name in error_sources:
        if source_name not in KNOWN_EXCEPTIONS:
            raise RuntimeError(f"Unknown error source: {source_name}")

        exception_parsers = KNOWN_EXCEPTIONS[source_name]

        error_parser = exception_parsers.get(e.__class__, None)
        if error_parser:
            return list(error_parser(e))

        for exc_class, error_parser in exception_parsers.items():
            if issubclass(e.__class__, exc_class):
                exception_parsers[e.__class__] = error_parser
                return list(error_parser(e))

    return None


@contextmanager
def catch_errors(error_sources: Optional[List[ErrorSource]] = None):
    """
    Wrap a block of code, catch known exceptions
    and convert them to qcheck errors.

    with catch_errors() as errors:
        run_some_validation()

    print(errors)
    """
    errors = []
    try:
        yield errors
    except Exception as e:
        _parsed_errors = try_extract_errors(e, error_sources)
        if _parsed_errors is None:
            raise
        errors.extend(_parsed_errors)


def reraise_errors(
    fn: Optional[Callable] = None,
    *,
    result_exception_factory: Callable[
        [List[Error]], Exception
    ] = lambda errors: CheckErrors(errors),
    error_sources: Optional[List[ErrorSource]] = None,
) -> Callable:
    """
    Decorate `fn`, catch all known errors, convert them to
    qcheck's errors and then pass them to `result_exception_factory`
    to prepare an exception which will be re-raised.

    `error_sources` allows to specify a subset of known exceptions
    which must be caught.
    """
    if fn is None:
        return partial(
            reraise_errors,
            result_exception_factory=result_exception_factory,
            error_sources=error_sources,
        )

    is_async = inspect.iscoroutinefunction(fn)

    if is_async:

        @wraps(fn)
        async def async_wrapper(*args, **kwargs):
            with catch_errors(error_sources=error_sources) as errors:
                return await fn(*args, **kwargs)

            if errors:
                raise result_exception_factory(errors=errors)

        return async_wrapper

    else:

        @wraps(fn)
        def sync_wrapper(*args, **kwargs):
            with catch_errors(error_sources=error_sources) as errors:
                return fn(*args, **kwargs)

            if errors:
                raise result_exception_factory(errors=errors)

        return sync_wrapper


def default_prepare_result_from_errors(errors: List[Error]) -> List[dict]:
    """Convert to a list of dicts with code, message, data, locations keys."""
    from dataclasses import asdict

    return [asdict(e) for e in errors]


def convert_errors_to_result(
    fn: Optional[Callable] = None,
    *,
    prepare_result_fn: Callable[
        [List[Error]], Any
    ] = default_prepare_result_from_errors,
    error_sources: Optional[List[ErrorSource]] = None,
) -> Callable:
    """
    Decorate `fn`, catch known errors, convert them to
    qcheck's errors and then pass them to `prepare_result_fn`
    for building the return value.

    `error_sources` allows to specify a subset of known exceptions
    which must be caught.
    """
    is_async = inspect.iscoroutinefunction(fn)

    if is_async:

        @wraps(fn)
        async def async_wrapper(*args, **kwargs):
            with catch_errors(error_sources=error_sources) as errors:
                return await fn(*args, **kwargs)

            return prepare_result_fn(errors=errors)

        return async_wrapper

    else:

        @wraps(fn)
        def sync_wrapper(*args, **kwargs):
            with catch_errors(error_sources=error_sources) as errors:
                return fn(*args, **kwargs)

            return prepare_result_fn(errors=errors)

        return sync_wrapper
