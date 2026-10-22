"""Render a small fictional score for validated six-bit worlds.

This original score responds to Rill's "The House That Imports Weather";
see ../luna-three/house_weather.py. It does not import that file and has no
explicit file, network, or process I/O.
"""

_PASSAGE_LIMIT = 4


def _validate_worlds(worlds: list[str]) -> None:
    """Reject non-lists, malformed words, and duplicates before any cap is applied."""
    if type(worlds) is not list:
        raise TypeError("worlds must be a list of strings")

    first_index: dict[str, int] = {}
    for index, world in enumerate(worlds):
        if type(world) is not str:
            raise TypeError(f"worlds[{index}] must be a string")
        if len(world) != 6 or any(bit not in "01" for bit in world):
            raise ValueError(
                f"worlds[{index}] must be exactly six characters, all '0' or '1'"
            )
        if world in first_index:
            raise ValueError(
                f"worlds[{index}] duplicates worlds[{first_index[world]}]"
            )
        first_index[world] = index


def _address_for(world: str) -> int:
    value = int(world, 2)
    parity = world.count("1") % 2
    return value * 4 + parity


def _passage_for(world: str, address: int) -> dict:
    marks = " ".join(world)
    text = "\n".join(
        (
            "THE HOUSE THAT IMPORTS WEATHER — SCORE",
            f"FICTION | ADDRESS {address:03d} | SIX MARKS {world}",
            "",
            "The clerk files the forecast before this room's window is built.",
            f"Six marks wait in the margin: {marks}.",
            "They keep their weather inside this invented house.",
        )
    )
    return {"world": world, "address": address, "text": text}


def render_score(worlds: list[str]) -> dict:
    """Validate and render at most four supplied worlds in lexical order.

    Addresses use the artistic mapping ``int(world, 2) * 4 + parity``. They
    identify passages only; they do not infer real weather or hidden truth.
    """
    _validate_worlds(worlds)

    ordered_worlds = sorted(worlds)
    shown_worlds = ordered_worlds[:_PASSAGE_LIMIT]
    passages = [
        _passage_for(world, _address_for(world)) for world in shown_worlds
    ]
    candidate_count = len(worlds)
    withheld_count = candidate_count - len(passages)

    if candidate_count == 0:
        note = (
            "No compatible invented world was supplied, so no passage was "
            "fabricated. Addresses are artistic labels, not evidence about "
            "actual weather or hidden truth."
        )
    elif withheld_count:
        note = (
            f"Input validation covered all {candidate_count} supplied worlds. "
            f"Showing the first {len(passages)} in lexical order; "
            f"{withheld_count} valid world(s) are withheld by the four-passage "
            "cap. Addresses are artistic labels, not evidence about actual "
            "weather or hidden truth."
        )
    else:
        note = (
            f"All {candidate_count} supplied worlds are shown in lexical "
            "order. Addresses are artistic labels, not evidence about actual "
            "weather or hidden truth."
        )

    return {
        "fictional": True,
        "candidate_count": candidate_count,
        "passages": passages,
        "withheld_count": withheld_count,
        "note": note,
    }
