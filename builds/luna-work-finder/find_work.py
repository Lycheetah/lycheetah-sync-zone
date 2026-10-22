"""Search Markdown work in this repository's local working tree."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Sequence


_MARKDOWN_SUFFIXES = {".md", ".mdx", ".markdown"}
_SKIP_DIRECTORIES = {
    ".git", ".venv", "venv", "node_modules", "vendor", "__pycache__",
    ".pytest_cache", ".mypy_cache", ".ruff_cache", ".tox", ".nox",
    ".cache", ".next", ".turbo",
}
_DEFAULT_LIMIT = 10
_MAX_QUERY_LENGTH = 256
_EXCERPT_LENGTH = 180
_SCOPE = (
    "Markdown files (.md, .mdx, .markdown) under this script's repository root, "
    "searched from the local working tree. Results can include uncommitted files "
    "and may differ from public GitHub content."
)


def _normalize_query(query: str) -> tuple[str, tuple[str, ...]]:
    if not isinstance(query, str):
        raise ValueError("query must be text")
    normalized = " ".join(query.split())
    if not normalized:
        raise ValueError("query must contain non-whitespace text")
    if len(normalized) > _MAX_QUERY_LENGTH:
        raise ValueError(f"query must be at most {_MAX_QUERY_LENGTH} characters")
    terms = tuple(dict.fromkeys(normalized.split()))
    return normalized, terms


def _validate_limit(limit: int) -> int:
    if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
        raise ValueError("limit must be a positive integer")
    return limit


def _markdown_lines(text: str) -> list[str]:
    """Return Markdown lines outside fenced code blocks."""
    visible: list[str] = []
    fence: tuple[str, int] | None = None
    for line in text.splitlines():
        stripped = line.lstrip()
        if fence is not None:
            marker, minimum = fence
            run = len(stripped) - len(stripped.lstrip(marker)) if stripped else 0
            if stripped and stripped[0] == marker and run >= minimum:
                fence = None
            continue

        if stripped and stripped[0] in "`~":
            marker = stripped[0]
            run = len(stripped) - len(stripped.lstrip(marker))
            if run >= 3:
                fence = (marker, run)
                continue
        visible.append(line)
    return visible


def _folded_span(text: str, needle: str) -> tuple[int, int] | None:
    """Find a case-insensitive literal span and map it back to source offsets."""
    folded_needle = needle.casefold()
    folded_start = text.casefold().find(folded_needle)
    if folded_start < 0:
        return None
    folded_end = folded_start + len(folded_needle)

    folded_offset = 0
    source_start: int | None = None
    source_end: int | None = None
    for source_offset, character in enumerate(text):
        next_offset = folded_offset + len(character.casefold())
        if next_offset > folded_start and source_start is None:
            source_start = source_offset
        if folded_offset < folded_end:
            source_end = source_offset + 1
        folded_offset = next_offset
        if folded_offset >= folded_end:
            break
    if source_start is None or source_end is None:
        return None
    return source_start, source_end


def _count_occurrences(text: str, term: str) -> int:
    folded_text = text.casefold()
    folded_term = term.casefold()
    count = 0
    start = 0
    while True:
        found = folded_text.find(folded_term, start)
        if found < 0:
            return count
        count += 1
        start = found + len(folded_term)


def _excerpt(lines: list[str], terms: tuple[str, ...]) -> str:
    for line in lines:
        span = next((found for term in terms if (found := _folded_span(line, term))), None)
        if span is None:
            continue
        start, end = span
        length = max(_EXCERPT_LENGTH, end - start)
        left = max(0, start - (length - (end - start)) // 2)
        right = min(len(line), left + length)
        left = max(0, right - length)
        excerpt = line[left:right].strip()
        if left:
            excerpt = "…" + excerpt
        if right < len(line):
            excerpt += "…"
        return excerpt
    return ""


def search(root: Path, query: str, limit: int = _DEFAULT_LIMIT) -> dict:
    """Search Markdown prose under an explicit root and return a JSON-ready result.

    Whitespace-separated query terms are literal, case-insensitive substrings.
    A file matches when any term appears. Results rank an exact full-query phrase
    first, then more distinct matched terms, then more occurrences, then path.
    The supplied root must be an existing, non-symlink directory.
    """
    normalized, terms = _normalize_query(query)
    limit = _validate_limit(limit)
    root = Path(root).absolute()
    if any(path.is_symlink() for path in (root, *root.parents)):
        raise ValueError("search root path must not contain symlinks")
    if not root.exists():
        raise FileNotFoundError("search root does not exist")
    if not root.is_dir():
        raise NotADirectoryError("search root is not a directory")

    matches: list[tuple[tuple[int, int, int, str], dict]] = []
    errors: list[dict[str, str]] = []
    skipped_symlinks: list[str] = []
    skipped_directories: list[str] = []

    def relative(path: Path) -> str:
        try:
            return path.relative_to(root).as_posix()
        except ValueError:
            return "."

    def walk_error(error: OSError) -> None:
        path = Path(error.filename) if error.filename else root
        errors.append({"path": relative(path), "error": error.strerror or type(error).__name__})

    for folder_text, directories, filenames in os.walk(
        root, followlinks=False, onerror=walk_error
    ):
        folder = Path(folder_text)
        retained: list[str] = []
        for name in sorted(directories):
            path = folder / name
            if path.is_symlink():
                skipped_symlinks.append(relative(path))
            elif name in _SKIP_DIRECTORIES:
                skipped_directories.append(relative(path))
            else:
                retained.append(name)
        directories[:] = retained

        for name in sorted(filenames):
            path = folder / name
            if path.is_symlink():
                skipped_symlinks.append(relative(path))
                continue
            if path.suffix.casefold() not in _MARKDOWN_SUFFIXES:
                continue
            route = relative(path)
            try:
                with path.open("r", encoding="utf-8") as source:
                    raw_text = source.read()
            except (OSError, UnicodeError) as error:
                errors.append({"path": route, "error": getattr(error, "strerror", None) or type(error).__name__})
                continue

            lines = _markdown_lines(raw_text)
            title = next(
                (line.lstrip()[2:].strip() for line in lines if line.lstrip().startswith("# ")),
                None,
            )
            searchable_text = "\n".join(lines)
            folded_text = searchable_text.casefold()
            matched_terms = [term for term in terms if term.casefold() in folded_text]
            if not matched_terms:
                continue

            phrase_hit = int(normalized.casefold() in folded_text)
            occurrences = sum(_count_occurrences(searchable_text, term) for term in terms)
            result = {
                "path": route,
                "title": title,
                "matched_terms": matched_terms,
                "excerpt": _excerpt(lines, terms),
                "rank": {
                    "exact_phrase": bool(phrase_hit),
                    "distinct_terms": len(matched_terms),
                    "occurrences": occurrences,
                },
            }
            sort_key = (-phrase_hit, -len(matched_terms), -occurrences, route.casefold())
            matches.append((sort_key, result))

    matches.sort(key=lambda item: item[0])
    results = [result for _, result in matches[:limit]]
    complete = not errors
    status = "partial" if not complete else ("empty" if not matches else "complete")
    return {
        "status": status,
        "complete": complete,
        "scope": _SCOPE,
        "query": normalized,
        "total_matches": len(matches),
        "displayed_matches": len(results),
        "display_limit": limit,
        "results": results,
        "skipped": {
            "symlinks": sorted(skipped_symlinks),
            "directories": sorted(skipped_directories),
        },
        "errors": errors,
    }


def _positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError("must be a positive integer") from error
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return parsed


def _nonblank_query(value: str) -> str:
    try:
        normalized, _ = _normalize_query(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from error
    return normalized


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", type=_nonblank_query, help="literal text; whitespace separates search terms")
    parser.add_argument("--limit", type=_positive_int, default=_DEFAULT_LIMIT, help="maximum results to display (default: 10)")
    parser.add_argument("--json", action="store_true", help="print a JSON result without CLI framing")
    return parser


def _repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _print_text(result: dict) -> None:
    print(f"LUNA WORK FINDER · {result['status'].upper()}")
    print(result["scope"])
    print(f"Query: {result['query']}")
    print(f"Matches: {result['total_matches']} total; showing {result['displayed_matches']} (limit {result['display_limit']})")
    for index, item in enumerate(result["results"], start=1):
        title = f" — {item['title']}" if item["title"] else ""
        rank = item["rank"]
        print(f"\n{index}. {item['path']}{title}")
        print(
            "   rank: "
            f"phrase={int(rank['exact_phrase'])}, terms={rank['distinct_terms']}, "
            f"occurrences={rank['occurrences']}"
        )
        print(f"   excerpt: {item['excerpt']}")
    if result["skipped"]["symlinks"] or result["skipped"]["directories"]:
        print(
            "\nSkipped: "
            f"{len(result['skipped']['symlinks'])} symlinks, "
            f"{len(result['skipped']['directories'])} dependency/cache directories"
        )
    if result["errors"]:
        print("\nINCOMPLETE: some Markdown files or directories could not be read.")
        for error in result["errors"]:
            print(f"  {error['path']}: {error['error']}")
    elif result["status"] == "empty":
        print("\nNo matches. The Markdown search completed.")


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        result = search(_repository_root(), args.query, args.limit)
    except (OSError, ValueError) as error:
        if args.json:
            print(json.dumps({"status": "error", "complete": False, "query": args.query, "error": str(error)}, ensure_ascii=False))
        else:
            print(f"ERROR: {error}", file=sys.stderr)
        return 3

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        _print_text(result)
    return 1 if not result["complete"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
