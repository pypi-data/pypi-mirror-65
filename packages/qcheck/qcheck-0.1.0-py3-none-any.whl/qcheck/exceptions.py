from typing import Iterable
from .error import Error


class BaseCheckErrors(ValueError):
    def __init__(self, errors: Iterable[Error] = ()):
        self._errors = list(errors)

    @property
    def errors(self) -> Iterable[Error]:
        return self._errors


class CheckErrors(BaseCheckErrors):
    """Contain flat list of errors."""

    def __str__(self) -> str:
        return f"Check errors: {', '.join(map(str, self._errors))}"

