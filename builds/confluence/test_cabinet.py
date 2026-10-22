"""Adversarial contract tests for the shared Cabinet; standard library only."""

from __future__ import annotations

import importlib.util
import json
import os
from itertools import product
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ZONE_ROOT = Path(__file__).resolve().parents[2]
if str(ZONE_ROOT) not in sys.path:
    sys.path.insert(0, str(ZONE_ROOT))

DEFAULT_CABINET = Path(__file__).resolve().with_name("cabinet.py")
CABINET_PATH = Path(
    os.environ.get("CONFLUENCE_CABINET_PATH", str(DEFAULT_CABINET))
).resolve()

if not CABINET_PATH.is_file():
    raise FileNotFoundError(
        f"Cabinet implementation is required before this suite can run: {CABINET_PATH}"
    )

_CABINET_MODULE_NAME = "builds.confluence._cabinet_under_test"
_CABINET_SPEC = importlib.util.spec_from_file_location(
    _CABINET_MODULE_NAME, CABINET_PATH
)
if _CABINET_SPEC is None or _CABINET_SPEC.loader is None:
    raise ImportError(f"could not load Cabinet from {CABINET_PATH}")
_CABINET = importlib.util.module_from_spec(_CABINET_SPEC)
sys.modules[_CABINET_MODULE_NAME] = _CABINET
_CABINET_SPEC.loader.exec_module(_CABINET)

from builds.confluence.aperture import make_slip
from builds.confluence.score import render_score
from builds.confluence.worlds import inspect_worlds


def completion_oracle(
    visible: dict[int, int], parity: int | None
) -> tuple[list[str], int, int]:
    """Build completions from only hidden positions, independently of the module."""
    hidden = [coordinate for coordinate in range(6) if coordinate not in visible]
    compatible: list[str] = []

    for hidden_bits in product((0, 1), repeat=len(hidden)):
        bits: list[int | None] = [None] * 6
        for coordinate, bit in visible.items():
            bits[coordinate] = bit
        for coordinate, bit in zip(hidden, hidden_bits):
            bits[coordinate] = bit

        world = "".join(str(bit) for bit in bits)
        world_parity = world.count("1") % 2
        if parity is None or world_parity == parity:
            compatible.append(world)

    compatible.sort()
    even = sum(world.count("1") % 2 == 0 for world in compatible)
    odd = len(compatible) - even
    return compatible, even, odd


def assert_report_is_bounded(test: unittest.TestCase, report: dict) -> None:
    required = {
        "target",
        "boundary",
        "method",
        "exposure",
        "outcome",
        "signal",
        "supported_sentence",
        "limitation",
    }
    test.assertEqual(set(report), required)
    for name in ("target", "boundary", "method", "exposure"):
        test.assertIs(type(report[name]), str)
        test.assertTrue(report[name].strip(), name)
        test.assertIn(f"{name}=", report["supported_sentence"])
        test.assertIn(report[name], report["supported_sentence"])
    test.assertIn(report["outcome"], {
        "FOUND", "NOT DETECTED", "NO ACCESS", "AMBIGUOUS", "NO RECORD HERE"
    })
    test.assertIn("outcome=", report["supported_sentence"])
    test.assertIs(type(report["signal"]), str)
    if report["outcome"] == "FOUND":
        test.assertTrue(report["signal"])
        test.assertIn("signal=", report["supported_sentence"])
        test.assertIn(report["signal"], report["supported_sentence"])
    else:
        test.assertEqual(report["signal"], "")
    test.assertIn("supplied report", report["limitation"])
    test.assertIn("independent validation", report["limitation"])


def assert_fiction_matches(
    test: unittest.TestCase, fiction: dict, expected_worlds: list[str]
) -> None:
    shown = expected_worlds[:4]
    test.assertIs(fiction["fictional"], True)
    test.assertEqual(fiction["candidate_count"], len(expected_worlds))
    test.assertEqual(fiction["withheld_count"], len(expected_worlds) - len(shown))
    passages = fiction["passages"]
    test.assertEqual([passage["world"] for passage in passages], shown)
    test.assertLessEqual(len(passages), 4)
    for passage in passages:
        expected_address = 4 * int(passage["world"], 2) + (
            passage["world"].count("1") % 2
        )
        test.assertEqual(passage["address"], expected_address)
        test.assertIn("FICTION", passage["text"])
        test.assertIn(passage["world"], passage["text"])


def cli_run(*arguments: str, cwd: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", str(CABINET_PATH), *arguments],
        cwd=cwd,
        text=True,
        capture_output=True,
        check=False,
    )


class CabinetContractTests(unittest.TestCase):
    @classmethod
    def tearDownClass(cls) -> None:
        print(
            "Scenario coverage: 729 partial observations; 2,187 observation/parity "
            "models (729 with no parity, 729 per prior).",
            file=sys.stderr,
        )

    def test_all_partial_observations_against_completion_oracle(self) -> None:
        """Exercise every coordinate as hidden, observed zero, and observed one."""
        scenarios = 0
        for observation in product((None, 0, 1), repeat=6):
            visible = {
                coordinate: bit
                for coordinate, bit in enumerate(observation)
                if bit is not None
            }
            for parity in (None, 0, 1):
                with self.subTest(observation=observation, parity=parity):
                    expected_worlds, even, odd = completion_oracle(visible, parity)
                    result = _CABINET.build_cabinet(visible, parity)
                    self.assertEqual(set(result), {"model", "report", "fiction"})

                    expected_model = {
                        "visible": {
                            str(coordinate): visible[coordinate]
                            for coordinate in sorted(visible)
                        },
                        "observed_coordinates": sorted(visible),
                        "matching_worlds": len(expected_worlds),
                        "even_worlds": even,
                        "odd_worlds": odd,
                        "parity_constraint": parity,
                        "examples": expected_worlds[:4],
                        "compatible_worlds": expected_worlds,
                    }
                    self.assertEqual(result["model"], expected_model)
                    assert_report_is_bounded(self, result["report"])
                    assert_fiction_matches(self, result["fiction"], expected_worlds)
                scenarios += 1

        self.assertEqual(scenarios, 2187)

    def test_cabinet_and_worlds_reject_invalid_types_ranges_and_booleans(self) -> None:
        class DictSubclass(dict):
            pass

        invalid_cases = (
            ((), None, TypeError),
            (DictSubclass({0: 0}), None, TypeError),
            ({True: 0}, None, TypeError),
            ({"0": 0}, None, TypeError),
            ({-1: 0}, None, ValueError),
            ({6: 0}, None, ValueError),
            ({0: True}, None, TypeError),
            ({0: "0"}, None, TypeError),
            ({0: -1}, None, ValueError),
            ({0: 2}, None, ValueError),
            ({}, True, TypeError),
            ({}, "0", TypeError),
            ({}, -1, ValueError),
            ({}, 2, ValueError),
        )
        for visible, parity, error in invalid_cases:
            for function in (inspect_worlds, _CABINET.build_cabinet):
                with self.subTest(
                    function=function.__name__, visible=visible, parity=parity
                ):
                    with self.assertRaises(error):
                        function(visible, parity)

    def test_score_validates_the_entire_input_before_its_four_passage_cap(self) -> None:
        valid_prefix = ["000000", "000001", "000010", "000011"]
        with self.assertRaises(ValueError):
            render_score(valid_prefix + ["00X100"])
        with self.assertRaises(ValueError):
            render_score(valid_prefix + ["000001"])
        with self.assertRaises(TypeError):
            render_score(valid_prefix + [None])

    def test_score_gives_all_64_worlds_unique_artistic_addresses(self) -> None:
        addresses: dict[int, str] = {}
        for number in range(64):
            world = format(number, "06b")
            with self.subTest(world=world):
                result = render_score([world])
                self.assertEqual(result["candidate_count"], 1)
                self.assertEqual(result["withheld_count"], 0)
                self.assertEqual(len(result["passages"]), 1)
                address = result["passages"][0]["address"]
                self.assertGreaterEqual(address, 0)
                self.assertLessEqual(address, 253)
                self.assertNotIn(address, addresses)
                addresses[address] = world

        self.assertEqual(len(addresses), 64)

    def test_score_reports_candidate_and_withheld_counts(self) -> None:
        for count in (0, 1, 4, 5, 8, 64):
            worlds = [format(number, "06b") for number in range(count)]
            with self.subTest(count=count):
                result = render_score(worlds)
                shown_count = min(count, 4)
                self.assertEqual(result["candidate_count"], count)
                self.assertEqual(len(result["passages"]), shown_count)
                self.assertEqual(result["withheld_count"], count - shown_count)
                self.assertEqual(
                    [passage["world"] for passage in result["passages"]],
                    sorted(worlds)[:4],
                )

    def test_all_aperture_outcomes_preserve_the_supplied_scope(self) -> None:
        outcomes = (
            "FOUND",
            "NOT DETECTED",
            "NO ACCESS",
            "AMBIGUOUS",
            "NO RECORD HERE",
        )
        for outcome in outcomes:
            supplied = {
                "target": "the caller's named signal",
                "boundary": "the stated six-bit model",
                "method": "a reported finite enumeration",
                "exposure": "one caller-described pass",
                "outcome": outcome,
            }
            if outcome == "FOUND":
                supplied["signal"] = "one caller-reported compatible world"
            result = make_slip(**supplied)
            with self.subTest(outcome=outcome):
                assert_report_is_bounded(self, result)
                self.assertEqual(result["outcome"], outcome)
                self.assertEqual(result["target"], supplied["target"])
                self.assertEqual(result["boundary"], supplied["boundary"])
                self.assertEqual(result["method"], supplied["method"])
                self.assertEqual(result["exposure"], supplied["exposure"])
                self.assertIn(supplied["boundary"], result["supported_sentence"])

    def test_empty_intersection_is_valid_not_detected_and_has_no_passage(self) -> None:
        visible = {coordinate: (coordinate % 2) for coordinate in range(6)}
        observed_parity = sum(visible.values()) % 2
        impossible_parity = 1 - observed_parity
        result = _CABINET.build_cabinet(visible, impossible_parity)

        self.assertEqual(result["model"]["compatible_worlds"], [])
        self.assertEqual(result["model"]["matching_worlds"], 0)
        self.assertEqual(result["report"]["outcome"], "NOT DETECTED")
        self.assertEqual(result["fiction"]["candidate_count"], 0)
        self.assertEqual(result["fiction"]["passages"], [])
        self.assertEqual(result["fiction"]["withheld_count"], 0)

    def test_cli_json_works_from_a_foreign_directory_without_extra_output(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cabinet-foreign-cwd-") as foreign_cwd:
            result = cli_run("--known", "0=1", "--known", "5=0", "--json", cwd=foreign_cwd)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        decoded = json.loads(result.stdout)
        self.assertEqual(set(decoded), {"model", "report", "fiction"})
        self.assertEqual(decoded["model"]["visible"], {"0": 1, "5": 0})

    def test_cli_without_observations_starts_with_all_64_worlds(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cabinet-foreign-cwd-") as foreign_cwd:
            result = cli_run("--json", cwd=foreign_cwd)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        decoded = json.loads(result.stdout)
        self.assertEqual(decoded["model"]["matching_worlds"], 64)
        self.assertEqual(len(decoded["model"]["compatible_worlds"]), 64)
        self.assertEqual(decoded["fiction"]["candidate_count"], 64)
        self.assertEqual(decoded["fiction"]["withheld_count"], 60)

    def test_cli_rejects_malformed_and_duplicate_coordinates_with_status_two(self) -> None:
        with tempfile.TemporaryDirectory(prefix="cabinet-foreign-cwd-") as foreign_cwd:
            malformed = cli_run("--known", "six=1", "--json", cwd=foreign_cwd)
            duplicate = cli_run(
                "--known", "2=0", "--known", "2=1", "--json", cwd=foreign_cwd
            )
            out_of_range = cli_run("--known", "6=1", "--json", cwd=foreign_cwd)

        for result in (malformed, duplicate, out_of_range):
            with self.subTest(stderr=result.stderr):
                self.assertEqual(result.returncode, 2)
                self.assertNotEqual(result.stderr, "")

    def test_cli_zero_compatible_worlds_remains_a_valid_not_detected_report(self) -> None:
        visible = {coordinate: (coordinate % 2) for coordinate in range(6)}
        wrong_parity = 1 - (sum(visible.values()) % 2)
        arguments: list[str] = []
        for coordinate in range(6):
            arguments.extend(("--known", f"{coordinate}={visible[coordinate]}"))
        arguments.extend(("--parity", str(wrong_parity), "--json"))

        with tempfile.TemporaryDirectory(prefix="cabinet-foreign-cwd-") as foreign_cwd:
            result = cli_run(*arguments, cwd=foreign_cwd)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        decoded = json.loads(result.stdout)
        self.assertEqual(decoded["report"]["outcome"], "NOT DETECTED")
        self.assertEqual(decoded["model"]["compatible_worlds"], [])
        self.assertEqual(decoded["fiction"]["passages"], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
