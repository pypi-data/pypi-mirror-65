from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, NewType, Optional, Tuple, Union

from .location import UserLocationsDefinition, ensure_locations, prepend_locations

Location = NewType("Location", Tuple[Union[str, int], ...])

LocationDefinition = Union[str, int, Location]
locationsDefinition = Union[LocationDefinition, List[LocationDefinition]]


@dataclass
class Error:
    message: str
    # Message code name
    code: Optional[str] = None
    # Extra payload; arbitrary data
    data: Optional[Any] = None
    # Affected locations
    locations: Optional[UserLocationsDefinition] = None

    def __post_init__(self) -> None:
        if self.locations is not None:
            self.locations = ensure_locations(self.locations)

    def __eq__(self, other: Union[Error, str]) -> Union[bool, NotImplemented]:
        if isinstance(other, Error):
            return (
                self.message == other.message
                and self.code == other.code
                and self.locations == other.locations
                and self.data == other.data
            )

        if isinstance(other, str):
            return (
                self.message == other
                and self.code is None
                and self.locations is None
                and self.data is None
            )

        return NotImplemented

    def prepend_locations(self, root_locations: UserLocationsDefinition) -> None:
        self.locations = prepend_locations(self.locations, root_locations)
