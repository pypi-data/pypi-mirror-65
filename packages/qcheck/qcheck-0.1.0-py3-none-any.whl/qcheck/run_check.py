from __future__ import annotations

import inspect
from typing import AsyncIterable, Iterable, List, Union

from .error import Error

ErrorsProducer = Union[Iterable[Error], AsyncIterable[Error]]


def _is_error_produced_with_field(error_value) -> bool:
    """
    Check if error was yielded with field definition.

    e.g.
    yield "field", Error("err")
    yield "field", [Error("err1"), Error("err2")]
    yield "field", _sub_validation(data)
    yield 123, Error("err")
    yield ["field1", "field2"], Error("err")
    """
    return (
        isinstance(error_value, tuple)
        and len(error_value) == 2
        and isinstance(error_value[0], (list, str, int))
    )


async def run_check_async(errors_producer: ErrorsProducer) -> List[Error]:
    """Validate data and collect errors."""
    if inspect.isawaitable(errors_producer):
        errors_producer = await errors_producer

    result_errors = []

    produced_values = []
    if isinstance(errors_producer, AsyncIterable):
        async for val in errors_producer:
            produced_values.append(val)

    elif isinstance(errors_producer, Iterable):
        produced_values.extend(errors_producer)

    else:
        raise TypeError(
            f"Cannot handle errors_producer={errors_producer!r}: unexpected type."
        )

    for val in produced_values:
        if inspect.isawaitable(val):
            val = await val

        if not val:
            continue

        if _is_error_produced_with_field(val):
            _locations, _errors = val

            if isinstance(_errors, Error):
                _errors = [_errors]
            else:
                _errors = await run_check_async(_errors)

            for err in _errors:
                err.prepend_locations(_locations)

            result_errors.extend(_errors)

        elif isinstance(val, (AsyncIterable, Iterable)):
            result_errors.extend(await run_check_async(val))

        elif isinstance(val, Error):
            result_errors.append(val)

        else:
            raise TypeError(f"Cannot handle {val!r}: unexpected type.")

    return result_errors


def run_check_sync(errors_producer: Iterable[Error]) -> List[Error]:
    """Validate data and collect errors."""
    result_errors = []

    produced_values = []

    if isinstance(errors_producer, Iterable):
        produced_values.extend(errors_producer)

    else:
        raise TypeError(
            f"Cannot handle errors_producer={errors_producer!r}: unexpected type."
        )

    for val in produced_values:
        if not val:
            continue

        if _is_error_produced_with_field(val):
            _affected_locations, _errors = val

            if isinstance(_errors, Error):
                _errors = [_errors]
            else:
                _errors = run_check_sync(_errors)

            for err in _errors:
                err.prepend_locations(_affected_locations)

            result_errors.extend(_errors)

        elif isinstance(val, Iterable):
            result_errors.extend(run_check_sync(val))

        elif isinstance(val, Error):
            result_errors.append(val)

        else:
            raise TypeError(f"Cannot handle {val!r}: unexpected type.")

    return result_errors
