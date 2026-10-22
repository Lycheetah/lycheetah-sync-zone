"""Compose the finite-world model, a bounded report, and a fictional score."""

import argparse
import json
import re
import sys
from pathlib import Path


if __package__ in (None, ""):
    # Direct script execution sets sys.path to this file's folder. Add the zone
    # root so the shared modules resolve even when the caller is elsewhere.
    _ZONE_ROOT = Path(__file__).resolve().parents[2]
    if str(_ZONE_ROOT) not in sys.path:
        sys.path.insert(0, str(_ZONE_ROOT))
    from builds.confluence.aperture import make_slip
    from builds.confluence.score import render_score
    from builds.confluence.worlds import inspect_worlds
else:
    from .aperture import make_slip
    from .score import render_score
    from .worlds import inspect_worlds


def build_cabinet(
    visible: dict[int, int], parity: int | None = None
) -> dict:
    """Build the model, bounded report, and fictional passages in memory.

    ``visible`` contains caller-supplied toy-model assumptions, not verified
    observations of a real source. Validation is delegated to
    :func:`inspect_worlds`, the sole candidate-world enumerator.
    """
    model = inspect_worlds(visible, parity)
    candidate_count = model["matching_worlds"]

    report = make_slip(
        target="six-bit completions satisfying the supplied coordinate assumptions and parity constraint",
        boundary="the complete finite universe of 64 six-bit worlds",
        method="enumerate all six-bit worlds and retain those matching the supplied constraints",
        exposure="one exhaustive pass over all 64 worlds in the toy model",
        outcome="FOUND" if candidate_count else "NOT DETECTED",
        signal=(
            f"{candidate_count} compatible "
            f"{'completion' if candidate_count == 1 else 'completions'}"
            if candidate_count
            else ""
        ),
    )

    # The score validates the entire candidate set and applies its own display
    # cap. Passing only model["examples"] would hide the real withheld count.
    fiction = render_score(model["compatible_worlds"])
    return {"model": model, "report": report, "fiction": fiction}


def _parse_known(value: str) -> tuple[int, int]:
    match = re.fullmatch(r"([0-5])=([01])", value)
    if match is None:
        raise argparse.ArgumentTypeError(
            "expected INDEX=BIT with INDEX from 0 through 5 and BIT 0 or 1"
        )
    return int(match.group(1)), int(match.group(2))


def _parse_parity(value: str) -> int:
    if value not in ("0", "1"):
        raise argparse.ArgumentTypeError("parity must be exactly 0 or 1")
    return int(value)


def _human_text(cabinet: dict) -> str:
    model = cabinet["model"]
    report = cabinet["report"]
    fiction = cabinet["fiction"]

    known = ", ".join(
        f"{coordinate}={bit}"
        for coordinate, bit in sorted(
            model["visible"].items(), key=lambda item: int(item[0])
        )
    ) or "(none supplied)"
    view = " ".join(
        str(model["visible"].get(str(index), "·")) for index in range(6)
    )
    parity = model["parity_constraint"]
    parity_label = (
        "none supplied"
        if parity is None
        else f"{parity} (user-supplied hard constraint; not measured evidence)"
    )

    lines = [
        "CABINET OF PARTIAL KNOWLEDGE",
        "────────────────────────────",
        "Toy model · coordinate inputs are supplied assumptions, not verified facts",
        f"Coordinate assumptions: {known}",
        f"Six positions (0 → 5): {view}",
        f"Parity constraint: {parity_label}",
        (
            f"Compatible completions: {model['matching_worlds']}  |  "
            f"even: {model['even_worlds']}  |  odd: {model['odd_worlds']}"
        ),
        "(Parity counts are after all supplied constraints.)",
        "",
        f"REPORT SLIP · {report['outcome']}",
        f"  Target:   {report['target']}",
        f"  Boundary: {report['boundary']}",
        f"  Method:   {report['method']}",
        f"  Exposure: {report['exposure']}",
        f"  Signal:   {report['signal'] or '(none reported)'}",
        f"  Supported statement: {report['supported_sentence']}",
        f"  Limit: {report['limitation']}",
        "",
        "A zero count means the supplied constraints have no shared world in this",
        "finite model; it is not an observation that anything is absent in reality.",
        "",
        f"FICTION · {len(fiction['passages'])} passage(s) shown",
        "Addresses and passages are invented; candidates are not truth-ranked.",
    ]

    for number, passage in enumerate(fiction["passages"], start=1):
        lines.extend(
            [
                "",
                f"Passage {number} · FICTION · address {passage['address']:03d}",
                *(f"  {line}" for line in passage["text"].splitlines()),
            ]
        )

    if not fiction["passages"]:
        lines.extend(["", "No fictional passage is available without a candidate world."])

    lines.extend(
        [
            "",
            f"Withheld by the four-passage display cap: {fiction['withheld_count']}",
            "Display order is lexical, not a ranking by likelihood or truth.",
        ]
    )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Show compatible six-bit worlds, a bounded report slip, and up to "
            "four explicitly fictional passages."
        )
    )
    parser.add_argument(
        "--known",
        action="append",
        type=_parse_known,
        default=[],
        metavar="INDEX=BIT",
        help="supply a coordinate assumption (repeatable; indices are 0 through 5)",
    )
    parser.add_argument(
        "--parity",
        type=_parse_parity,
        default=None,
        metavar="0|1",
        help="optional user-imposed hard constraint, not a measured parity",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="print JSON with exactly the top-level fields model, report, fiction",
    )
    args = parser.parse_args(argv)

    visible: dict[int, int] = {}
    for coordinate, bit in args.known:
        if coordinate in visible:
            parser.error(f"coordinate {coordinate} was supplied more than once")
        visible[coordinate] = bit

    cabinet = build_cabinet(visible, args.parity)
    if args.json_output:
        print(json.dumps(cabinet, ensure_ascii=False, indent=2))
    else:
        print(_human_text(cabinet))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
