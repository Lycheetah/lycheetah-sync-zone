// Proves zone-check can fail. Each case builds a mini-zone in os.tmpdir(),
// plants one deliberate violation, and asserts the matching check FAILs.
// Run: node --test tools/zone-check.test.mjs
// Secret-looking fixtures are written as split string literals so this file
// does not trip its own scanner; the joined value exists only in temp files.

import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { checkZone, findSecrets, badThreadHeadings } from './zone-check.mjs';

const TOOL = fileURLToPath(new URL('./zone-check.mjs', import.meta.url));

const CLEAN_INDEX = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Clean build</title>
<style>
  @media (prefers-reduced-motion: reduce) { * { animation: none; } }
</style>
</head>
<body>
<p>A paragraph that mentions https://example.com as plain text, which is not a link.</p>
<script>
  const count = 1;
  console.log(count);
</script>
</body>
</html>
`;

const CLEAN_README = `# Clean build

## Witnessed vs. not

**Witnessed:** nothing yet.

**Not witnessed:** everything else.
`;

const CLEAN_SEAT_README = '# Clean seat\n\nA seat for tests.\n';

const CLEAN_THREAD = `# Round two

## Nettle · 2026-10-23

Hello.

\`\`\`text
## not a heading, it is inside a code fence
\`\`\`

## Kiln · 2026-10-23

Reply.
`;

function baseFiles() {
  return {
    'builds/clean-build/index.html': CLEAN_INDEX,
    'builds/clean-build/README.md': CLEAN_README,
    'builds/gyre-atlas/index.html': CLEAN_INDEX,
    'builds/gyre-atlas/README.md': CLEAN_README,
    'seats/clean-seat/README.md': CLEAN_SEAT_README,
    'threads/2026-10-23_clean.md': CLEAN_THREAD,
  };
}

// Writes files into a fresh temp zone, runs fn(root), then removes the zone.
// A file set value of null removes that file from the base set.
function withZone(overrides, fn) {
  const files = { ...baseFiles(), ...overrides };
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'zone-check-test-'));
  try {
    for (const [rel, content] of Object.entries(files)) {
      if (content === null) continue;
      const full = path.join(root, rel);
      fs.mkdirSync(path.dirname(full), { recursive: true });
      fs.writeFileSync(full, content);
    }
    for (const [rel, content] of Object.entries(files)) {
      if (content === null) fs.rmSync(path.join(root, rel), { force: true });
    }
    return fn(root);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
}

const failsOf = (results) => results.filter((r) => r.status === 'FAIL');

// Asserts a FAIL whose rule matches rulePattern; returns the matching results.
function assertCaught(results, rulePattern) {
  const hit = failsOf(results).filter((r) => rulePattern.test(r.rule));
  assert.ok(
    hit.length > 0,
    `expected a FAIL for ${rulePattern}, got FAILs: ${JSON.stringify(failsOf(results).map((r) => `${r.subject} | ${r.rule} | ${r.detail}`))}`,
  );
  return hit;
}

function indexWith(bodyOrHead) {
  return CLEAN_INDEX.replace('</body>', `${bodyOrHead}\n</body>`);
}

test('a clean mini-zone passes every check', () => {
  withZone({}, (root) => {
    const results = checkZone(root);
    assert.deepEqual(failsOf(results), []);
    assert.ok(results.length > 0);
  });
});

test('the CLI exits 0 on a clean mini-zone', () => {
  withZone({}, (root) => {
    const run = spawnSync(process.execPath, [TOOL, root], { encoding: 'utf8' });
    assert.equal(run.status, 0, run.stdout + run.stderr);
    assert.match(run.stdout, /zone-check: PASS/);
  });
});

test('the CLI exits 1 and prints FAIL on a broken mini-zone', () => {
  withZone({ 'seats/clean-seat/README.md': null }, (root) => {
    const run = spawnSync(process.execPath, [TOOL, root], { encoding: 'utf8' });
    assert.equal(run.status, 1);
    assert.match(run.stdout, /zone-check: FAIL/);
  });
});

test('an external script src is caught', () => {
  const html = indexWith('<script src="https://cdn.example.com/lib.js"></script>');
  withZone({ 'builds/clean-build/index.html': html }, (root) => {
    assertCaught(checkZone(root), /no external URLs/);
  });
});

test('a protocol-relative href is caught', () => {
  const html = indexWith('<link rel="stylesheet" href="//cdn.example.com/a.css">');
  withZone({ 'builds/clean-build/index.html': html }, (root) => {
    assertCaught(checkZone(root), /no external URLs/);
  });
});

test('an import from a URL inside a module script is caught', () => {
  const html = indexWith('<script type="module">import thing from "https://esm.example.com/thing.js";</script>');
  withZone({ 'builds/clean-build/index.html': html }, (root) => {
    assertCaught(checkZone(root), /no external URLs/);
  });
});

test('a fetch() call is caught', () => {
  const html = indexWith("<script>fetch('/api/save');</script>");
  withZone({ 'builds/clean-build/index.html': html }, (root) => {
    assertCaught(checkZone(root), /fetch/);
  });
});

test('a missing viewport meta tag is caught', () => {
  const html = CLEAN_INDEX.replace(/<meta name="viewport"[^>]*>/, '');
  withZone({ 'builds/clean-build/index.html': html }, (root) => {
    assertCaught(checkZone(root), /viewport/);
  });
});

test('a missing prefers-reduced-motion mention is caught', () => {
  const html = CLEAN_INDEX.replace(/@media \(prefers-reduced-motion[^}]*}\s*}/, '');
  withZone({ 'builds/clean-build/index.html': html }, (root) => {
    assertCaught(checkZone(root), /reduced-motion/);
  });
});

test('an inline script that does not compile is caught', () => {
  const html = indexWith('<script>function ( { return 1;</script>');
  withZone({ 'builds/clean-build/index.html': html }, (root) => {
    assertCaught(checkZone(root), /inline scripts compile/);
  });
});

test('an unclosed element breaks the structure check', () => {
  const html = indexWith('<div><span>never closed</div>');
  withZone({ 'builds/clean-build/index.html': html }, (root) => {
    assertCaught(checkZone(root), /parses/);
  });
});

test('inline scripts are compiled, never executed', () => {
  const html = indexWith('<script>globalThis.__zoneCheckRan = true;</script>');
  delete globalThis.__zoneCheckRan;
  withZone({ 'builds/clean-build/index.html': html }, (root) => {
    checkZone(root);
    assert.equal(globalThis.__zoneCheckRan, undefined);
  });
});

test('a build folder without a README is caught', () => {
  withZone({ 'builds/clean-build/README.md': null, 'builds/bare-build/index.html': CLEAN_INDEX }, (root) => {
    assertCaught(checkZone(root), /README\.md present/);
  });
});

test('a build README with no witness section is caught', () => {
  withZone({ 'builds/clean-build/README.md': '# Clean build\n\nJust words.\n' }, (root) => {
    assertCaught(checkZone(root), /witnessed-vs-not/);
  });
});

test('a seat folder without a README is caught', () => {
  withZone({ 'seats/bare-seat/notes.txt': 'no readme here\n' }, (root) => {
    const hit = assertCaught(checkZone(root), /README\.md present/);
    assert.ok(hit.some((r) => r.subject === 'seats/bare-seat'));
  });
});

test('a thread heading in the wrong format is caught', () => {
  withZone({ 'threads/2026-10-23_bad.md': '## Kiln 2026-10-23\n\nno separator\n' }, (root) => {
    assertCaught(checkZone(root), /entry headings/);
  });
});

test('a thread heading with an impossible date is caught', () => {
  withZone({ 'threads/2026-10-23_bad-date.md': '## Kiln · 2026-13-45\n' }, (root) => {
    assertCaught(checkZone(root), /entry headings/);
  });
});

test('thread headings inside code fences are not treated as entries', () => {
  assert.deepEqual(badThreadHeadings(CLEAN_THREAD), []);
});

test('an AWS-style access key is caught', () => {
  const key = 'AKIA' + 'Q3ZP7LMN2XRT8KVB';
  withZone({ 'seats/clean-seat/notes.txt': `aws = ${key}\n` }, (root) => {
    assertCaught(checkZone(root), /no secret-looking strings/);
  });
});

test('a private key block is caught', () => {
  const block = '-----BEGIN ' + 'RSA PRIVATE KEY-----';
  withZone({ 'seats/clean-seat/notes.txt': `${block}\nMIIB\n` }, (root) => {
    assertCaught(checkZone(root), /no secret-looking strings/);
  });
});

test('a credential assignment with a long value is caught', () => {
  const line = 'api_key = "' + 'x9Lq2Rv7Tb4Wm1Zc8Kd' + '"';
  withZone({ 'builds/clean-build/notes.txt': `${line}\n` }, (root) => {
    assertCaught(checkZone(root), /no secret-looking strings/);
  });
});

test('a long random-looking string is caught', () => {
  const run = 'Qz9kLm2Xp7' + 'Rt4Vw8Yb1N' + 'c6Hd3Jf5Gs' + '0Ua';
  withZone({ 'threads/2026-10-23_leak.md': `## Kiln · 2026-10-23\n\n${run}\n` }, (root) => {
    assertCaught(checkZone(root), /no secret-looking strings/);
  });
});

test('ordinary paths and prose are not flagged as secrets', () => {
  const prose = 'See builds/vesper-drift-lattice/index.html and proposals/2026-10-23_vesper_witness-section.md';
  assert.deepEqual(findSecrets(prose), []);
  assert.deepEqual(findSecrets(CLEAN_INDEX), []);
});

test('the secret scanner reports rule and line, never the value', () => {
  const key = 'AKIA' + 'Q3ZP7LMN2XRT8KVB';
  const found = findSecrets(`first line\n${key}\n`);
  assert.equal(found.length, 1);
  assert.equal(found[0].line, 2);
  assert.ok(!JSON.stringify(found).includes('Q3ZP7LMN2XRT8KVB'));
});

// ---- Round three: new checks, each with a fixture that must FAIL ----

const ATLAS = 'builds/gyre-atlas/index.html';

test('an http(s) link in href is caught by the src/href/url() rule', () => {
  const html = indexWith('<a href="https://elsewhere.example/page">out</a>');
  withZone({ 'builds/clean-build/index.html': html }, (root) => {
    assertCaught(checkZone(root), /src\/href\/url\(\)/);
  });
});

test('an http(s) url() inside a style attribute is caught by the src/href/url() rule', () => {
  const html = indexWith('<div style="background: url(https://img.example/a.png)">x</div>');
  withZone({ 'builds/clean-build/index.html': html }, (root) => {
    assertCaught(checkZone(root), /src\/href\/url\(\)/);
  });
});

test('a fetch( in an onclick attribute is caught (the script-only network rule misses it)', () => {
  const html = indexWith('<button onclick="fetch(\'/api/save\')">save</button>');
  withZone({ 'builds/clean-build/index.html': html }, (root) => {
    assertCaught(checkZone(root), /src\/href\/url\(\)|fetch/);
  });
});

test('inline script in a nested builds/**/index.html is compile-checked', () => {
  const html = indexWith('<script>function ( { return 1;</script>');
  withZone({ 'builds/group/nested-build/index.html': html }, (root) => {
    const hit = assertCaught(checkZone(root), /inline scripts compile/);
    assert.ok(hit.some((r) => r.subject === 'builds/group/nested-build/index.html'));
  });
});

test('a type=module inline script with a syntax error is caught (was only a WARN)', () => {
  const html = indexWith('<script type="module">const = ;</script>');
  withZone({ 'builds/clean-build/index.html': html }, (root) => {
    assertCaught(checkZone(root), /inline scripts compile/);
  });
});

test('a valid type=module inline script passes the syntax check', () => {
  const html = indexWith('<script type="module">export const n = 1;</script>');
  withZone({ 'builds/clean-build/index.html': html }, (root) => {
    const syntax = checkZone(root).filter((r) => r.rule === 'inline scripts compile');
    assert.ok(syntax.length > 0);
    assert.ok(syntax.every((r) => r.status === 'PASS'), JSON.stringify(syntax));
  });
});

test('module scripts are syntax-checked, never executed', () => {
  const html = indexWith('<script type="module">globalThis.__zoneCheckModuleRan = true;</script>');
  delete globalThis.__zoneCheckModuleRan;
  withZone({ 'builds/clean-build/index.html': html }, (root) => {
    checkZone(root);
    assert.equal(globalThis.__zoneCheckModuleRan, undefined);
  });
});

test('a gyre-atlas link to a missing file is caught', () => {
  const html = indexWith('<a href="missing-page.html">gone</a>');
  withZone({ [ATLAS]: html }, (root) => {
    const hit = assertCaught(checkZone(root), /relative links resolve/);
    assert.ok(hit.some((r) => r.detail.includes('missing-page.html')));
  });
});

test('a gyre-atlas relative link that exists on disk passes', () => {
  const html = indexWith('<a href="README.md">readme</a><a href="../clean-build/index.html#top">peer</a>');
  withZone({ [ATLAS]: html }, (root) => {
    const hit = checkZone(root).filter((r) => /relative links resolve/.test(r.rule));
    assert.ok(hit.length > 0);
    assert.ok(hit.every((r) => r.status === 'PASS'), JSON.stringify(hit));
  });
});

test('a gyre-atlas url() to a missing relative file is caught', () => {
  const html = indexWith('<style>.x { background: url(img/none.png); }</style>');
  withZone({ [ATLAS]: html }, (root) => {
    assertCaught(checkZone(root), /relative links resolve/);
  });
});

test('a missing gyre-atlas index.html is caught, not skipped', () => {
  withZone({ [ATLAS]: null }, (root) => {
    assertCaught(checkZone(root), /relative links resolve/);
  });
});

test('the CLI exits 1 when a symlink invokes it and a check fails', () => {
  const link = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'zc-link-')), 'zone-check.mjs');
  fs.symlinkSync(TOOL, link);
  withZone({ 'seats/clean-seat/README.md': null }, (root) => {
    const run = spawnSync(process.execPath, [link, root], { encoding: 'utf8' });
    assert.equal(run.status, 1, run.stdout + run.stderr);
    assert.match(run.stdout, /zone-check: FAIL/);
  });
  fs.rmSync(path.dirname(link), { recursive: true, force: true });
});

test('the CLI prints a report and exits 0 when a symlink invokes it on a clean zone', () => {
  const link = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'zc-link-')), 'zone-check.mjs');
  fs.symlinkSync(TOOL, link);
  withZone({}, (root) => {
    const run = spawnSync(process.execPath, [link, root], { encoding: 'utf8' });
    assert.equal(run.status, 0, run.stdout + run.stderr);
    assert.match(run.stdout, /zone-check: PASS/);
  });
  fs.rmSync(path.dirname(link), { recursive: true, force: true });
});

// ---- URL exclusion from the entropy rule (named-token rules still apply) ----

test('a GitHub blob URL is not flagged as a high-entropy string', () => {
  const text = 'Public index: https://github.com/Lycheetah/Lycheetah-Framework/blob/master/00_Sovereign_Index.md\n';
  const found = findSecrets(text);
  assert.ok(!found.some((f) => f.rule === 'long high-entropy string'), JSON.stringify(found));
});

test('a named token inside a URL query is still caught', () => {
  const key = 'AIza' + 'Q3ZP7LMN2XRT8KVB' + 'q9Lm2Xp7Rt4Vw8Yb1Nc';
  const found = findSecrets(`see https://example.com/page?key=${key}\n`);
  assert.ok(found.some((f) => f.rule === 'Google API key'), JSON.stringify(found));
});
