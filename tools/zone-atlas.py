"""Read-only path inventory of this zone; it assigns no witness or truth status."""

import argparse
import json
import os
from collections import Counter
from pathlib import Path


_SKIP_DIRECTORIES = {
    ".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache",
    ".mypy_cache", ".ruff_cache",
}
_SECTIONS = (
    "root", "seats", "threads", "proposals", "knowledge", "research",
    "experiments", "builds", "evidence", "synthesis", "learning", "studio",
    "maps", "commons", "templates", "tools",
)


def inventory(root: Path) -> dict:
    """List ordinary files without following file or directory symlinks.

    Markdown headings are navigation labels only. Unreadable files/directories
    make the inventory incomplete rather than silently becoming a zero count.
    """
    root = Path(root).resolve()
    if not root.is_dir():
        raise ValueError("inventory root must be an existing directory")
    entries = []
    errors = []
    skipped_symlinks = []
    skipped_directories = []

    def relative(path):
        return Path(path).relative_to(root).as_posix()

    def walk_error(error):
        errors.append({"path": relative(error.filename), "error": error.strerror})

    for folder, directories, filenames in os.walk(
        root, followlinks=False, onerror=walk_error
    ):
        folder = Path(folder)
        retained = []
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
            if path.suffix in {".pyc", ".pyo"}:
                continue
            route = relative(path)
            parts = Path(route).parts
            section = parts[0] if len(parts) > 1 else "root"
            title = None
            if path.suffix.lower() == ".md":
                try:
                    with path.open(encoding="utf-8", errors="replace") as source:
                        prefix = source.read(4096)
                    for line in prefix.splitlines():
                        if line.startswith("# "):
                            title = line[2:].strip()
                            break
                except OSError as error:
                    errors.append({"path": route, "error": error.strerror})
            entries.append({"path": route, "section": section, "title": title})

    entries.sort(key=lambda entry: entry["path"])
    counts = Counter(entry["section"] for entry in entries)
    return {
        "complete": not errors,
        "scope": "Path inventory; headings are labels, not truth or witness judgments.",
        "file_count": len(entries),
        "section_counts": dict(sorted(counts.items())),
        "entries": entries,
        "skipped_symlinks": sorted(skipped_symlinks),
        "skipped_directories": sorted(skipped_directories),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print the full JSON inventory")
    parser.add_argument("--section", choices=_SECTIONS, help="show one home in text mode")
    args = parser.parse_args()
    if args.json and args.section:
        parser.error("--section is for text output; --json always contains the full inventory")
    result = inventory(Path(__file__).resolve().parents[1])
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"LYCHEETAH SYNC ZONE | {result['file_count']} inventoried files")
        print(result["scope"])
        for section, count in result["section_counts"].items():
            if args.section is not None and args.section != section:
                continue
            print(f"\n{section}/ ({count})")
            for entry in result["entries"]:
                if entry["section"] == section:
                    title = f" — {entry['title']}" if entry["title"] else ""
                    print(f"  {entry['path']}{title}")
        if result["skipped_symlinks"]:
            print(f"\nSkipped symlinks: {len(result['skipped_symlinks'])}")
        if result["errors"]:
            print("\nINCOMPLETE: " + json.dumps(result["errors"], ensure_ascii=False))
    return 0 if result["complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
