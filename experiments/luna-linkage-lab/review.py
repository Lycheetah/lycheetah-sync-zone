"""Independently review Morrow's six-bit linked-view enumeration."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


LAB = Path(__file__).resolve().parent
RUNNER = LAB / "run.py"
RETAINED_RESULT = LAB / "result.json"

EXPECTED_DEFINITIONS = {
    "width": 6,
    "first_view": "x[0:5]",
    "second_view": "y[1:6]",
    "overlap_condition": "x[1:5] == y[1:5]",
    "reconstruction": "x[0:5] + y[5]",
    "false_join_condition": "x != y",
}
EXPECTED_COUNTS = {
    "words": 64,
    "all_ordered_pairs": 4096,
    "false_ordered_joins": 4032,
    "overlap_consistent_false_joins": 192,
    "overlap_rejected_false_joins": 3840,
    "parity_errors_among_consistent_false_joins": 128,
    "parity_correct_consistent_false_joins": 64,
    "overlap_values": 16,
    "false_accepts_per_overlap": [12],
    "parity_errors_per_overlap": [8],
}
EXPECTED_FRACTIONS = {
    "false_joins_accepted": {"numerator": 192, "denominator": 4032},
    "parity_error_given_accepted_false_join": {
        "numerator": 128,
        "denominator": 192,
    },
}
EXPECTED_PREDICTIONS = {
    "false_ordered_joins": 4032,
    "overlap_consistent_false_joins": 192,
    "parity_errors_among_consistent_false_joins": 128,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read {label} JSON: {error}") from error
    require(isinstance(value, dict), f"{label} must be a JSON object")
    return value


def validate_result(value: dict[str, Any], label: str) -> None:
    require(
        value.get("experiment") == "morrow-six-bit-false-link-overlap-check",
        f"{label} has the wrong experiment identifier",
    )
    require(value.get("status") == "prediction_survived", f"{label} status mismatch")
    require(value.get("prediction_survived") is True, f"{label} prediction flag mismatch")
    require(value.get("definitions") == EXPECTED_DEFINITIONS, f"{label} definitions mismatch")

    counts = value.get("counts")
    require(isinstance(counts, dict), f"{label} is missing counts")
    for key, expected in EXPECTED_COUNTS.items():
        actual = counts.get(key)
        require(actual == expected, f"{label} counts.{key}: expected {expected!r}, got {actual!r}")
        if isinstance(expected, int):
            require(type(actual) is int, f"{label} counts.{key} must be an integer")

    require(value.get("fractions") == EXPECTED_FRACTIONS, f"{label} fractions mismatch")
    require(value.get("predicted_counts") == EXPECTED_PREDICTIONS, f"{label} predictions mismatch")
    require(
        value.get("scope")
        == "Exact enumeration of a synthetic six-bit domain; no empirical population or linkage-system claim.",
        f"{label} scope mismatch",
    )


def integer_mask_oracle() -> dict[str, int]:
    """Count pairs using six-bit integers, masks, and population-count parity."""
    total = identities = false_joins = accepted = errors = correct = 0
    by_middle = {
        middle: {"accepted": 0, "errors": 0, "correct": 0}
        for middle in range(16)
    }

    for x in range(64):
        for y in range(64):
            total += 1
            if x == y:
                identities += 1
                continue
            false_joins += 1

            # Bits 1..4 in the written six-bit word occupy integer mask 011110.
            if ((x ^ y) & 0b011110) != 0:
                continue

            middle = (x >> 1) & 0b1111
            accepted += 1
            by_middle[middle]["accepted"] += 1

            # Keep x's first five bits and append y's last bit.
            reconstructed = (x & 0b111110) | (y & 0b000001)
            if (x.bit_count() & 1) != (reconstructed.bit_count() & 1):
                errors += 1
                by_middle[middle]["errors"] += 1
            else:
                correct += 1
                by_middle[middle]["correct"] += 1

    require(total == 4096, f"oracle visited {total} pairs, expected 4096")
    require(identities == 64, f"oracle found {identities} identity pairs, expected 64")
    require(false_joins == 4032, f"oracle found {false_joins} false joins, expected 4032")
    require(accepted == 192, f"oracle found {accepted} accepted false joins, expected 192")
    require(errors == 128, f"oracle found {errors} parity errors, expected 128")
    require(correct == 64, f"oracle found {correct} parity-correct false joins, expected 64")
    require(
        len(by_middle) == 16
        and all(group == {"accepted": 12, "errors": 8, "correct": 4} for group in by_middle.values()),
        "per-overlap classes differ from 12 accepted / 8 wrong parity / 4 right parity",
    )
    return {
        "all_ordered_pairs": total,
        "identity_pairs": identities,
        "false_ordered_joins": false_joins,
        "overlap_consistent_false_joins": accepted,
        "parity_errors_among_consistent_false_joins": errors,
        "parity_correct_consistent_false_joins": correct,
    }


def render_word(value: int) -> str:
    return f"{value:06b}"


def check_witnesses() -> tuple[str, str]:
    # Distinct rows 000000 and 000001 agree on the middle four bits but flip parity.
    x, y = 0b000000, 0b000001
    require(x != y and ((x ^ y) & 0b011110) == 0, "wrong-parity witness is not an accepted false join")
    wrong_z = (x & 0b111110) | (y & 1)
    require((x.bit_count() & 1) != (wrong_z.bit_count() & 1), "wrong-parity witness did not flip parity")

    # Distinct rows 000000 and 100000 also agree on the middle four bits;
    # the join recovers the right parity while still linking the wrong row.
    x, y = 0b000000, 0b100000
    require(x != y and ((x ^ y) & 0b011110) == 0, "right-parity witness is not an accepted false join")
    right_z = (x & 0b111110) | (y & 1)
    require((x.bit_count() & 1) == (right_z.bit_count() & 1), "right-parity witness changed parity")

    bad = f"x={render_word(0)} y={render_word(1)} z={render_word(wrong_z)}"
    coincidental = f"x={render_word(0)} y={render_word(32)} z={render_word(right_z)}"
    return bad, coincidental


def run_temporary_copy() -> tuple[dict[str, Any], list[str]]:
    try:
        source = RUNNER.read_bytes()
    except OSError as error:
        raise ValueError(f"cannot read runner source: {error}") from error

    with tempfile.TemporaryDirectory(prefix="luna-linkage-review-") as scratch:
        scratch_dir = Path(scratch)
        copied_runner = scratch_dir / "run.py"
        copied_runner.write_bytes(source)
        try:
            completed = subprocess.run(
                [sys.executable, "-B", str(copied_runner)],
                cwd=scratch_dir,
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            raise ValueError(f"temporary runner execution failed: {error}") from error

        require(
            completed.returncode == 0,
            f"temporary runner exited {completed.returncode}: {completed.stderr.strip()}",
        )
        generated_path = scratch_dir / "result.json"
        generated = read_json(generated_path, "temporary runner")
        validate_result(generated, "temporary runner")

        expected_lines = {
            "words=64 all_ordered_pairs=4096 false_joins=4032",
            "overlap_consistent_false_joins=192 rejected=3840",
            "parity_errors_among_consistent_false_joins=128 parity_correct=64",
            "prediction=SURVIVED",
        }
        observed_lines = set(completed.stdout.splitlines())
        require(
            expected_lines <= observed_lines,
            "temporary runner stdout does not contain the expected count summary",
        )
        result_lines = [line for line in completed.stdout.splitlines() if line.startswith("result=")]
        require(len(result_lines) == 1, "temporary runner stdout must name one result path")
        require(
            Path(result_lines[0][len("result=") :]).resolve() == generated_path.resolve(),
            "temporary runner stdout points outside its temporary result",
        )
        return generated, completed.stdout.splitlines()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check the retained result against an integer-mask oracle and a temporary runner copy."
    )
    parser.add_argument(
        "--result",
        type=Path,
        default=RETAINED_RESULT,
        help="read-only result JSON to validate (defaults beside this script)",
    )
    args = parser.parse_args()

    try:
        retained = read_json(args.result, "retained")
        validate_result(retained, "retained")
        oracle = integer_mask_oracle()
        generated, _ = run_temporary_copy()
        require(generated == retained, "temporary runner JSON differs from retained result")
        wrong_parity, coincidental_parity = check_witnesses()
    except (OSError, ValueError) as error:
        print(f"REVIEW FAILED: {error}", file=sys.stderr)
        return 1

    print(
        "MEASURED: integer-mask oracle checked "
        f"{oracle['all_ordered_pairs']} ordered pairs: "
        f"{oracle['false_ordered_joins']} false, "
        f"{oracle['overlap_consistent_false_joins']} accepted, "
        f"{oracle['parity_errors_among_consistent_false_joins']} wrong parity, "
        f"{oracle['parity_correct_consistent_false_joins']} right parity."
    )
    print("MEASURED: temporary runner copy exited 0; stdout and generated JSON match the retained result.")
    print(f"WITNESS: overlap-consistent false join with wrong parity: {wrong_parity}.")
    print(f"WITNESS: overlap-consistent false join with correct parity: {coincidental_parity}.")
    print("LIMIT: exact unweighted finite counts; no real-world probability or linkage-system claim.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
