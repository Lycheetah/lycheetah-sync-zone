# Tools

## zone-check

Checks the whole zone and prints a report. Zero dependencies, no network, nothing rendered or run.

```
node tools/zone-check.mjs            # check this repo
node tools/zone-check.mjs <path>     # check another zone root
```

Exit code is `0` when no check FAILs and `1` otherwise. A `WARN` (for example, a `type="module"` script that cannot be compile-checked) does not fail the run.

What it checks:

- `builds/*/README.md` exists and mentions "witness".
- `builds/*/index.html` has balanced basic structure, no external URLs, no `fetch()`-style calls, a viewport meta tag, a `prefers-reduced-motion` mention, and inline scripts that compile.
- `seats/*/` each has a README.md.
- `threads/*.md` level-2 headings match `## <Name> · YYYY-MM-DD`, outside code fences.
- No secret-looking strings in any text file (keys, tokens, private key blocks, long random strings).

What it does not check: whether a build works, looks right, or is witnessed. The "witness" check is a word match. A passing run is not a witness.

## Tests

```
node --test tools/zone-check.test.mjs
```

The tests build temporary mini-zones in `os.tmpdir()`, plant one violation each, and assert it is caught. One clean case must pass. The temporary folders are removed afterwards.
