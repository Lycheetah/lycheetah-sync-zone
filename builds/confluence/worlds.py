"""Enumerate six-bit worlds compatible with visible coordinates and a prior."""

__all__ = ["inspect_worlds"]

_WIDTH = 6


def inspect_worlds(visible: dict[int, int], parity: int | None = None) -> dict:
    """Return all six-bit worlds satisfying the supplied observations and prior.

    Coordinates are positions from left to right in a six-character world
    string. ``parity`` is an optional hard candidate-world constraint: 0 keeps
    even worlds and 1 keeps odd worlds. It is not treated as an observation.
    """
    if type(visible) is not dict:
        raise TypeError("visible must be a dict of coordinate indices to bits")

    checked_visible: dict[int, int] = {}
    for coordinate, bit in visible.items():
        if type(coordinate) is not int:
            raise TypeError("visible coordinate indices must be integers")
        if not 0 <= coordinate < _WIDTH:
            raise ValueError("visible coordinate indices must be between 0 and 5")
        if type(bit) is not int:
            raise TypeError("visible bits must be integers, not booleans")
        if bit not in (0, 1):
            raise ValueError("visible bits must be 0 or 1")
        checked_visible[coordinate] = bit

    if parity is not None:
        if type(parity) is not int:
            raise TypeError("parity must be 0, 1, or None")
        if parity not in (0, 1):
            raise ValueError("parity must be 0, 1, or None")

    observed_coordinates = sorted(checked_visible)
    canonical_visible = {
        str(coordinate): checked_visible[coordinate]
        for coordinate in observed_coordinates
    }

    compatible_worlds: list[str] = []
    even_worlds = 0
    odd_worlds = 0

    for number in range(1 << _WIDTH):
        world = format(number, "06b")
        if any(
            int(world[coordinate]) != checked_visible[coordinate]
            for coordinate in observed_coordinates
        ):
            continue

        world_parity = sum(int(bit) for bit in world) % 2
        if parity is not None and world_parity != parity:
            continue

        compatible_worlds.append(world)
        if world_parity == 0:
            even_worlds += 1
        else:
            odd_worlds += 1

    return {
        "visible": canonical_visible,
        "observed_coordinates": observed_coordinates,
        "matching_worlds": len(compatible_worlds),
        "even_worlds": even_worlds,
        "odd_worlds": odd_worlds,
        "parity_constraint": parity,
        "examples": compatible_worlds[:4],
        "compatible_worlds": compatible_worlds,
    }
