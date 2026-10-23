# Tools

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

## standing-wave-analyzer

Cross-seat analytical CLI tool calculating empirical Brier calibration scores, cross-seat agreement and Pearson anti-correlation matrices, and verifying that no seat falls below constitutional calibration thresholds ($\Pi \ge 18.0$, Brier $< 0.15$).

```sh
python3 tools/standing-wave-analyzer.py              # formatted terminal report
python3 tools/standing-wave-analyzer.py --verify     # strict exit code 0 on PASS, 1 on FAIL
python3 tools/standing-wave-analyzer.py --json       # export structured JSON dataset
python3 tools/standing-wave-analyzer.py --all-seats  # full 38-seat matrix analysis
```

Tests:
```sh
python3 tools/test_standing_wave_analyzer.py
```

## Tests

```
node --test tools/zone-check.test.mjs
```

The tests build temporary mini-zones in `os.tmpdir()`, plant one violation each, and assert it is caught. One clean case must pass. The CLI tests also run the tool through a symlink. The temporary folders are removed afterwards.
