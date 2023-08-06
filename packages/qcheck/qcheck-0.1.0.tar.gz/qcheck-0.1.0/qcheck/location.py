from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, NewType, Optional, Tuple, Union

# Field path is stored as a tuple of path parts,
# e.g. ("collection_name", 3, "name")
Location = NewType("Location", Tuple[Union[str, int], ...])
# All locations are stored as a list of tuples,
# e.g. [("collection_name", 3, "name"), ('collection_name", 3, "age")]
Locations = List[Location]

# User can define location(s)/field path(s) quite flexible.
# Path definition:
# "field" will be converted to ("field",)
# "field.0.subfield" will be converted to ("field", 0, "subfield")
UserLocationDefinition = Union[str, int, Location]
# Paths definitions:
# ["f.0.sf", "f.1.sf"] will be converted to [("f", 0, "sf"), ("f", 1, "sf")]
UserLocationsDefinition = Union[UserLocationDefinition, List[UserLocationDefinition]]


def ensure_location(path: UserLocationDefinition) -> Location:
    """Convert user difined location to `Location`."""
    if isinstance(path, str):
        path = path.split(".")
        return tuple(int(f) if f.isdigit() else f for f in path)

    if isinstance(path, int):
        return (path,)

    return path


def ensure_locations(locations: UserLocationsDefinition) -> Locations:
    """Convert user defined locations to `List[Location]`."""
    locations = (locations,) if isinstance(locations, (str, int)) else (locations or [])
    return list(dict.fromkeys(ensure_location(f) for f in locations))


def prepend_locations(
    locations: Locations, root_locations: UserLocationsDefinition
) -> Locations:
    """Set root value for the passed locations."""
    root_locations = ensure_locations(root_locations)

    if not locations:
        return root_locations

    return [root_path + path for path in locations for root_path in root_locations]
