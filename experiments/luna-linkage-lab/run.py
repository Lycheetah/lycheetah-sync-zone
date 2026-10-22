"""Exhaustively measure false acceptance under six-bit linked-view checking."""

import json
from pathlib import Path
from itertools import product


WIDTH = 6
EXPECTED_FALSE_JOINS = 4032
EXPECTED_ACCEPTED_FALSE_JOINS = 192
EXPECTED_PARITY_ERRORS = 128


def parity(word: str) -> int:
    return sum(bit == "1" for bit in word) % 2


def main() -> None:
    words = tuple("".join(bits) for bits in product("01", repeat=WIDTH))
    total_ordered_pairs = 0
    false_joins = 0
    overlap_consistent_false_joins = 0
    parity_errors = 0
    accepted_by_overlap: dict[str, int] = {}
    errors_by_overlap: dict[str, int] = {}

    for x in words:
        for y in words:
            total_ordered_pairs += 1
            if x == y:
                continue
            false_joins += 1
            overlap = x[1:5]
            if overlap != y[1:5]:
                continue
            overlap_consistent_false_joins += 1
            accepted_by_overlap[overlap] = accepted_by_overlap.get(overlap, 0) + 1
            reconstructed = x[:5] + y[5]
            if parity(reconstructed) != parity(x):
                parity_errors += 1
                errors_by_overlap[overlap] = errors_by_overlap.get(overlap, 0) + 1

    overlap_rejected_false_joins = false_joins - overlap_consistent_false_joins
    prediction_survived = (
        false_joins == EXPECTED_FALSE_JOINS
        and overlap_consistent_false_joins == EXPECTED_ACCEPTED_FALSE_JOINS
        and parity_errors == EXPECTED_PARITY_ERRORS
        and len(accepted_by_overlap) == 16
        and set(accepted_by_overlap.values()) == {12}
        and set(errors_by_overlap.values()) == {8}
    )

    result = {
        "experiment": "morrow-six-bit-false-link-overlap-check",
        "status": "prediction_survived" if prediction_survived else "prediction_falsified",
        "definitions": {
            "width": WIDTH,
            "first_view": "x[0:5]",
            "second_view": "y[1:6]",
            "overlap_condition": "x[1:5] == y[1:5]",
            "reconstruction": "x[0:5] + y[5]",
            "false_join_condition": "x != y",
        },
        "counts": {
            "words": len(words),
            "all_ordered_pairs": total_ordered_pairs,
            "false_ordered_joins": false_joins,
            "overlap_consistent_false_joins": overlap_consistent_false_joins,
            "overlap_rejected_false_joins": overlap_rejected_false_joins,
            "parity_errors_among_consistent_false_joins": parity_errors,
            "parity_correct_consistent_false_joins": overlap_consistent_false_joins - parity_errors,
            "overlap_values": len(accepted_by_overlap),
            "false_accepts_per_overlap": sorted(set(accepted_by_overlap.values())),
            "parity_errors_per_overlap": sorted(set(errors_by_overlap.values())),
        },
        "fractions": {
            "false_joins_accepted": {
                "numerator": overlap_consistent_false_joins,
                "denominator": false_joins,
            },
            "parity_error_given_accepted_false_join": {
                "numerator": parity_errors,
                "denominator": overlap_consistent_false_joins,
            },
        },
        "predicted_counts": {
            "false_ordered_joins": EXPECTED_FALSE_JOINS,
            "overlap_consistent_false_joins": EXPECTED_ACCEPTED_FALSE_JOINS,
            "parity_errors_among_consistent_false_joins": EXPECTED_PARITY_ERRORS,
        },
        "prediction_survived": prediction_survived,
        "scope": "Exact enumeration of a synthetic six-bit domain; no empirical population or linkage-system claim.",
    }

    output_path = Path(__file__).with_name("result.json")
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(
        f"words={len(words)} all_ordered_pairs={total_ordered_pairs} "
        f"false_joins={false_joins}"
    )
    print(
        f"overlap_consistent_false_joins={overlap_consistent_false_joins} "
        f"rejected={overlap_rejected_false_joins}"
    )
    print(
        f"parity_errors_among_consistent_false_joins={parity_errors} "
        f"parity_correct={overlap_consistent_false_joins - parity_errors}"
    )
    print(f"prediction={'SURVIVED' if prediction_survived else 'FALSIFIED'}")
    print(f"result={output_path}")
    if not prediction_survived:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
