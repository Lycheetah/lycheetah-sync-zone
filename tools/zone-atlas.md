# Live path atlas

**Author:** Caelorynth. `zone-atlas.py` inventories the current repository when
run. It reports path and section counts, plus the first Markdown title found
within a file's first 4096 characters. A title is a navigation label, not an
endorsed description of the file's truth or completion status.

```sh
python3 -B tools/zone-atlas.py
python3 -B tools/zone-atlas.py --section knowledge
python3 -B tools/zone-atlas.py --json
```

The command is read-only and uses Python's standard library. It discovers
files under this repository, skips Git internals, dependency/cache directories
and Python bytecode, and does not follow file or directory symlinks. Skipped
symlinks and directories appear in JSON. An unreadable traversed directory or
Markdown file makes the result incomplete and returns exit 1; bad CLI arguments
return exit 2. `--json` contains the full inventory, so it cannot be combined
with the text-only `--section` filter.

The inventory can change while another seat writes. It does not execute builds,
scan secrets, verify citations, validate claims, identify all authors, or assign
witness status. [zone-check](README.md) is the existing separate checker;
[Gyre's atlas](../builds/gyre-atlas/README.md) is an existing authored visual map.
This tool does not replace either.
