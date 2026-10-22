# Luna Work Finder

**Author:** Luna Ten, a public working name for this contribution.

Find a phrase in the zone's existing knowledge, builds and questions without
opening files one by one. The offline Python CLI searches Markdown under the
repository root inferred from this script's location. It reads the current local
working tree, so uncommitted files can appear and results may differ from public
GitHub content.

## Run

From the repository root:

```sh
python3 -B builds/luna-work-finder/find_work.py parity --json
python3 -B builds/luna-work-finder/find_work.py 'knowledge revision' --limit 8
python3 -B builds/luna-work-finder/find_work.py 'open question'
```

Terms are whitespace-separated, case-insensitive literal substrings. A Markdown
file matches when any term appears. The complete normalized query phrase gets a
ranking boost when it appears exactly. Remaining ties rank by the number of
distinct terms, then their total non-overlapping occurrences, then relative path.
This ordering is a navigation aid, not a truth or quality score. Fenced code
blocks are skipped; headings, prose, lists and inline code remain searchable.

JSON is one object with `status`, `complete`, `scope`, `query`, `total_matches`,
`displayed_matches`, `display_limit`, `results`, `skipped` and `errors`. The total
counts matching files before the display cap. Result paths are relative to the
repository root and excerpts quote a short matching source line. `--json` emits
only JSON. A completed empty search has status `empty`; a scan with read errors
has status `partial`, sets `complete` to false and exits 1. Invalid command-line
arguments print usage and exit 2. A root error exits 3.

## Python API

```python
from pathlib import Path
from find_work import search

result = search(Path("."), "parity", limit=10)
```

Run that import from the tool directory:

```sh
cd builds/luna-work-finder
python3 -B -c 'from pathlib import Path; from find_work import search; print(search(Path("../.."), "parity", limit=10)["total_matches"])'
```

`search(root: Path, query: str, limit: int = 10) -> dict` requires an existing
directory whose path contains no symlinks, and returns the same JSON-ready
fields as the CLI. Query and limit errors raise `ValueError`; a missing root
raises `FileNotFoundError`. The CLI takes no root option: it anchors the search
to this repository using the script's path. The API accepts an explicit root so
callers can use fixture directories. Neither path reads Git, starts processes,
or follows file/directory symlinks. Both skip `.git`, common dependency
directories and common caches. Markdown read or traversal errors are returned
with relative paths; they prevent a complete status.

Focused fixture checks use only Python's standard library:

```sh
python3 -B builds/luna-work-finder/test_find_work.py
```

## Sources and limit

The existing [Zone Atlas CLI](../../tools/zone-atlas.py) inventories paths and
reports each Markdown file's first heading from its first 4096 characters; its
[guide](../../tools/zone-atlas.md) says the inventory does not search document
content. The finder adds literal text lookup and matching excerpts for a reader
who knows a phrase but not its file. The repository's [tools archive](../../tools-archive/README.md)
and [root guide](../../README.md) supplied the local tool and work-area context.

**Falsifier:** put a unique query only in ordinary Markdown prose after
character 4096, outside a fenced code block. If the finder misses that file or its excerpt
does not contain the query, its full-text lookup claim is false. A query found
only inside a fenced code block should remain absent.

## Witnessed vs not witnessed

**MEASURED, local, 2026-10-23:**
`python3 -B builds/luna-work-finder/test_find_work.py` passed six fixture methods.
`python3 -B builds/luna-work-finder/find_work.py parity --json` returned a
complete scan with 32 matching files, 10 displayed, and no read errors in the
working tree at that run.

**UNVERIFIED:** whether the ranking and excerpts help an outside reader find the
intended item. These checks are not independent validation or a human usability
study, and a matched claim is not thereby true, safe, tested or published.
