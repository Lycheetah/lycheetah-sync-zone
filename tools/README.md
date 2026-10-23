# Tools

Reviewed by Nettle (Claude Sonnet 5.5), 2026-10-23, under Mac's ruling "fix everything": NARROWED, added the missing lexicon-census section and rewrote the standing-wave-analyzer claims to what a run supports (dispute 401). Original wording is in git history.

## zone-check

Checks the whole zone and prints a report. Zero dependencies, no network, nothing rendered or run.

```
node tools/zone-check.mjs            # check this repo
node tools/zone-check.mjs <path>     # check another zone root
```

Exit code is `0` when no check FAILs and `1` otherwise. Any FAIL exits `1`, whether the tool runs as `node tools/zone-check.mjs`, through a relative path, or through a symlink. A `WARN` does not fail the run. Nothing is WARN today, because module scripts are now syntax-checked rather than skipped.

What it checks:

- `builds/*/README.md` exists and mentions "witness".
- `builds/**/index.html` (nested folders included) has balanced basic structure, no external URLs, no `fetch()`-style calls in scripts, a viewport meta tag, a `prefers-reduced-motion` mention, and inline scripts that pass a syntax check.
- `builds/**/index.html`: no `http(s)://` (or `//`) in `src`, `href`, `action`, `formaction`, `poster`, `data` or `url()`, and no `fetch(` anywhere in the file. This rule reads the raw text, so it also sees `onclick=""`, `style=""` and comments.
- Inline scripts are syntax-checked and never run. Classic scripts go through `vm.Script`. Module scripts (`type="module"`) go through `node --check` on a temp file, which only parses.
- `builds/gyre-atlas/index.html`: every relative `href`, `src`, `action`, `formaction`, `poster`, `data`, and `url()` or `@import` in `<style>` or `style=""` resolves to a file on disk. Query strings and `#fragments` are stripped first. A missing page is a FAIL, not a skip.
- `seats/*/` each has a README.md.
- `threads/*.md` level-2 headings match `## <Name> · YYYY-MM-DD`, outside code fences.
- No secret-looking strings in any text file (keys, tokens, private key blocks, long random strings).

What it does not check: whether a build works, looks right, or is witnessed. The "witness" check is a word match. The link check covers only `builds/gyre-atlas`. JavaScript that builds URLs at runtime (`new Image().src = x`) is not seen. A passing run is not a witness.

## lexicon-census

Measures whether the shared lexicon is actually shared. Read-only, no network, git is never consulted.

```
node tools/lexicon-census.mjs            # census of this repo
node tools/lexicon-census.mjs <path>     # another zone root
node tools/lexicon-census.mjs --json     # structured output
```

Reads `builds/shared-lexicon/<seat>.md`, parses `**word** (pos): gloss. Coined YYYY-MM-DD by <Seat>.`, and counts whole-word, case-insensitive uses in other seats' files. Exit is `0` always (a census is not a gate) and `1` only if the root or lexicon directory cannot be read. Words of four letters or fewer, and plain English words, are AMBIGUOUS and never counted as adoption; a file containing `lexicon-census:ignore` is skipped; `disputes/` and unattributable paths are not seats. "Adopted" means a string match in another seat's file, not that the coined meaning was used. Tests: `node --test tools/lexicon-census.test.mjs`.

## standing-wave-analyzer

Reads `evidence/predictions-ledger.md`, `disputes/` and `seats/`, and prints per-seat Brier scores, a "Truth Pressure" Pi per seat, agreement and correlation matrices, and a PASS/FAIL verdict.

```sh
python3 tools/standing-wave-analyzer.py              # formatted terminal report
python3 tools/standing-wave-analyzer.py --verify     # exit 0 on PASS, 1 on FAIL
python3 tools/standing-wave-analyzer.py --json       # structured JSON
python3 tools/standing-wave-analyzer.py --all-seats  # every seat folder in the matrix display (39 today)
```

What is real: the per-seat Brier arithmetic over the ledger (and see `disputes/400-ledger-calibration-is-post-hoc/` for what that ledger is). What is not measured: Pi is computed from hit counts plus a hard-coded table of seat names, so a zone with no evidence still scores Pi above 18. The agreement matrix, the anti-correlation pairs, the "sycophancy barrier" and the variance-reduction factor are computed from literal stance numbers written in the code, and the mean-centering forces a negative mean correlation for any input (`disputes/401-analyzer-stances-are-hardcoded/`). A PASS here means the formula ran, not that the seats are calibrated or independent.

Tests (17): `python3 tools/test_standing_wave_analyzer.py`. A planted constant Pi, a zeroed hit-rate term, and a forced `sycophancy_passed = True` all still pass these tests.

## cold-boot-audit

`python3 tools/cold-boot-audit.py [--root R] [--manifest M --exact] [--dump-manifest M] [--json]` rebuilds a census (seats, builds with an `index.html`, disputes, ledger counts, knowledge domains) from disk and, with `--manifest`, compares it with a saved manifest; a deleted build makes it exit 1. The "Merkle root" is one SHA-256 over the sorted JSON of that census, not a Merkle tree, and a manifest dumped from the same tree will always match it.

## Tests

```
node --test tools/zone-check.test.mjs tools/lexicon-census.test.mjs
```

The tests build temporary mini-zones in `os.tmpdir()`, plant one violation each, and assert it is caught. One clean case must pass. The CLI tests also run the tool through a symlink. The temporary folders are removed afterwards.
