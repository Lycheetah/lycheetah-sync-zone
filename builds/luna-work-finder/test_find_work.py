"""Small offline fixture checks for find_work.py."""

from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import find_work


class WorkFinderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "repo"
        self.root.mkdir()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_literal_text_match_and_nonmatch(self) -> None:
        self.write("builds/guide/README.md", "# Parity Guide\nA literal marker is parity.* here.\n")
        self.write("knowledge/near.md", "# Nearby\nThe marker parityX is different.\n")
        self.write("threads/other.md", "# Other\nNo marker in this file.\n")

        result = find_work.search(self.root, "parity.*")

        self.assertEqual(result["status"], "complete")
        self.assertEqual(result["total_matches"], 1)
        self.assertEqual(result["results"][0]["path"], "builds/guide/README.md")
        self.assertEqual(result["results"][0]["title"], "Parity Guide")
        self.assertIn("parity.*", result["results"][0]["excerpt"])

    def test_searches_full_prose_and_skips_fenced_code(self) -> None:
        self.write("long.md", "# Long page\n" + ("x" * 4200) + "\nneedle-after-prefix\n")
        self.write("code-only.md", "# Code sample\n```text\nneedle-hidden\n```\n")

        prose = find_work.search(self.root, "needle-after-prefix")
        code = find_work.search(self.root, "needle-hidden")

        self.assertEqual(prose["total_matches"], 1)
        self.assertEqual(prose["results"][0]["path"], "long.md")
        self.assertIn("needle-after-prefix", prose["results"][0]["excerpt"])
        self.assertEqual(code["status"], "empty")

    def test_total_count_is_before_display_cap_and_rank_is_explainable(self) -> None:
        self.write("a.md", "# Alpha\nalpha beta alpha\n")
        self.write("b.md", "# Beta\nalpha only\n")
        self.write("c.md", "# Gamma\nbeta only\n")

        result = find_work.search(self.root, "alpha beta", limit=1)

        self.assertEqual(result["total_matches"], 3)
        self.assertEqual(result["displayed_matches"], 1)
        self.assertEqual(result["results"][0]["path"], "a.md")
        self.assertTrue(result["results"][0]["rank"]["exact_phrase"])

    def test_dependencies_caches_and_file_or_directory_symlinks_are_skipped(self) -> None:
        self.write(".git/hidden.md", "needle")
        self.write("node_modules/pkg/hidden.md", "needle")
        self.write(".cache/hidden.md", "needle")
        self.write("visible.md", "needle")

        outside = Path(self.temp.name) / "outside"
        outside.mkdir()
        (outside / "linked.md").write_text("needle", encoding="utf-8")
        (outside / "linked-dir").mkdir()
        (outside / "linked-dir" / "inside.md").write_text("needle", encoding="utf-8")
        try:
            (self.root / "file-link.md").symlink_to(outside / "linked.md")
            (self.root / "dir-link").symlink_to(outside / "linked-dir", target_is_directory=True)
        except (NotImplementedError, OSError) as error:
            self.skipTest(f"symlinks unavailable: {error}")

        result = find_work.search(self.root, "needle")

        self.assertEqual([item["path"] for item in result["results"]], ["visible.md"])
        self.assertIn(".git", result["skipped"]["directories"])
        self.assertIn("node_modules", result["skipped"]["directories"])
        self.assertIn(".cache", result["skipped"]["directories"])
        self.assertIn("file-link.md", result["skipped"]["symlinks"])
        self.assertIn("dir-link", result["skipped"]["symlinks"])
        (self.root.parent / "repo-link").symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(ValueError):
            find_work.search(self.root.parent / "repo-link", "needle")

    def test_empty_result_is_distinct_from_partial_read(self) -> None:
        self.write("readable.md", "# A readable page\nNothing here.\n")
        self.write("unreadable.md", "secret term\n")
        original_open = Path.open

        def fail_one(path: Path, *args, **kwargs):
            if path.name == "unreadable.md":
                raise PermissionError("denied")
            return original_open(path, *args, **kwargs)

        with mock.patch.object(Path, "open", fail_one):
            partial = find_work.search(self.root, "absent")
        self.assertEqual(partial["status"], "partial")
        self.assertFalse(partial["complete"])
        self.assertEqual(partial["total_matches"], 0)
        self.assertEqual(partial["errors"][0]["path"], "unreadable.md")

        empty = find_work.search(self.root, "absent")
        self.assertEqual(empty["status"], "empty")
        self.assertTrue(empty["complete"])
        self.assertEqual(empty["total_matches"], 0)

    def test_malformed_query_limit_and_root_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            find_work.search(self.root, "   \n")
        with self.assertRaises(ValueError):
            find_work.search(self.root, "valid", limit=0)
        with self.assertRaises(FileNotFoundError):
            find_work.search(self.root / "missing", "valid")

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit) as raised:
            find_work.main(["   "])
        self.assertEqual(raised.exception.code, 2)
        self.assertIn("query must contain", stderr.getvalue())

        stderr = io.StringIO()
        with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit) as raised:
            find_work.main(["valid", "--limit", "0"])
        self.assertEqual(raised.exception.code, 2)
        self.assertIn("positive integer", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
