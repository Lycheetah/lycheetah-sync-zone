#!/usr/bin/env python3
"""Print one filing slip from an invented house that imports weather."""

import argparse


ROOMS = (
    "the roof's dry aquarium",
    "the pantry with a tide mark on its ceiling",
    "the attic that has no stairs",
    "the room behind the rain barrel",
)

WEATHER = (
    "warm fog with no outside",
    "small blue snow under the table",
    "rain falling upward in a teaspoon",
    "wind made of folded paper",
)

ARRIVALS = (
    "through the locked chimney",
    "from a mailbox's shadow",
    "under the mirror's silver",
    "by way of a doorbell nobody installed",
)

TRACES = (
    "a salt crescent on the ceiling",
    "three dry commas on the sill",
    "a hinge turned toward the sea",
    "a compass pointing into a cup",
)


def fields_for_address(address: int) -> tuple[str, str, str, str]:
    """Return the room, weather, arrival, and trace for an 8-bit address."""
    if not 0 <= address <= 255:
        raise ValueError("address must be between 0 and 255")

    digits = tuple((address >> shift) & 0b11 for shift in (6, 4, 2, 0))
    return (
        ROOMS[digits[0]],
        WEATHER[digits[1]],
        ARRIVALS[digits[2]],
        TRACES[digits[3]],
    )


def render(address: int) -> str:
    room, weather, arrival, trace = fields_for_address(address)
    return "\n".join(
        (
            "THE HOUSE THAT IMPORTS WEATHER",
            f"INVENTED WORLD | SLIP {address:03d} / {address:08b}",
            "",
            f"ROOM: {room}",
            f"WEATHER: {weather}",
            f"ARRIVAL: {arrival}",
            f"TRACE: {trace}",
            "",
            "CLERK'S NOTE: Each forecast is filed before its window is built.",
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Print a weather slip from an explicitly invented house."
    )
    parser.add_argument("address", type=int, help="an integer from 0 through 255")
    args = parser.parse_args()
    try:
        print(render(args.address))
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
