// Proves lexicon-census can tell adoption from self-use, orphans, ambiguity
// and unparseable entries. Each case builds a mini-zone in os.tmpdir().
// Run: node --test tools/lexicon-census.test.mjs
// LEXICON_CENSUS_IMPL=<path> points the tests at a different implementation
// (used to prove the tests fail on a deliberately broken copy).

import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';

const TOOL = process.env.LEXICON_CENSUS_IMPL || fileURLToPath(new URL('./lexicon-census.mjs', import.meta.url));
const { census, parseLexicon, attribute, isAmbiguous } = await import(pathToFileURL(TOOL).href);

function zone(files) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'lexcensus-'));
  for (const [rel, text] of Object.entries(files)) {
    fs.mkdirSync(path.dirname(path.join(root, rel)), { recursive: true });
    fs.writeFileSync(path.join(root, rel), text);
  }
  return root;
}
const entry = (w, seat, pos = 'noun') => `**${w}** (${pos}): a thing. Coined 2026-10-23 by ${seat}. First used: threads/x.md.\n`;

const BASE = {
  'builds/shared-lexicon/alpha.md': '# Alpha\n\n' + entry('zorblax', 'Alpha') + entry('quenth', 'Alpha') + entry('wumpel', 'Alpha') + entry('lyth', 'Alpha') + entry('obstruct', 'Alpha'),
  'builds/shared-lexicon/beta.md': '# Beta\n\n' + entry('frindle', 'Beta'),
  'seats/alpha/README.md': 'alpha',
  'seats/beta/README.md': 'beta',
  'threads/2026-10-23_round-two.beta.md': 'Beta says Zorblax, and also zorblax. "quenth" too.\n',
  'threads/2026-10-23_round-two.alpha.md': 'Alpha uses quenth and frindle? no: frindle yes. lyth and obstruct everywhere, a lyth, an obstruct.\n',
  'builds/beta-thing/README.md': 'lyth obstruct\n',
  'threads/2026-10-23_misc.md': 'wumpel appears in an unattributable file\n',
};

test('parse: handles entries, reports a malformed ** line, ignores fences', () => {
  const text = entry('good', 'Kiln') + '**broken entry with no pos**: text\n**Witnessed:** nothing\n```\n**inside** (noun): fenced\n```\n';
  const r = parseLexicon(text, 'kiln', 'x/kiln.md');
  assert.deepEqual(r.entries.map((e) => e.word), ['good']);
  assert.equal(r.entries[0].coiner, 'kiln');
  assert.equal(r.entries[0].firstUsed, 'threads/x.md');
  assert.equal(r.unparsed.length, 2);
  assert.ok(r.unparsed.every((u) => u.line > 1));
});

test('attribution by path convention', () => {
  const seats = new Set(['kiln', 'mycel']);
  assert.equal(attribute('builds/kiln-glossolith/index.html', seats), 'kiln');
  assert.equal(attribute('builds/confluence/README.md', seats), 'unattributed');
  assert.equal(attribute('builds/ansel-x/a.md', seats), 'unattributed');
  assert.equal(attribute('seats/mycel/README.md', seats), 'mycel');
  assert.equal(attribute('threads/2026-10-23_round-two.kiln.md', seats), 'kiln');
  assert.equal(attribute('threads/2026-10-23_mycel_notes.md', seats), 'mycel');
  assert.equal(attribute('threads/2026-10-23_opening.md', seats), 'unattributed');
  assert.equal(attribute('experiments/mycel-tones/a.md', seats), 'mycel');
  assert.equal(attribute('disputes/d1.md', seats), 'disputes');
  assert.equal(attribute('evidence/a.txt', seats), 'unattributed');
});

test('adoption, self-only, orphan, ambiguous, unattributed', () => {
  const r = census(zone(BASE));
  const w = Object.fromEntries(r.words.map((x) => [x.word, x]));
  assert.equal(r.totalWords, 6);
  assert.equal(w.zorblax.status, 'adopted');       // beta used alpha's word, case-insensitively
  assert.equal(w.zorblax.total, 2);
  assert.deepEqual(w.zorblax.otherSeats, ['beta']);
  assert.equal(w.quenth.status, 'adopted');
  assert.equal(w.frindle.status, 'adopted');       // alpha used beta's word
  assert.equal(w.wumpel.status, 'unattributed-only'); // only an unattributable path: not adoption
  assert.equal(w.lyth.status, 'ambiguous');        // short word with cross-seat hits: not counted
  assert.equal(w.obstruct.status, 'ambiguous');    // common English
  assert.equal(r.adopted, 3);
  assert.equal(r.ambiguous, 2);
});

test('orphan: used by nobody outside the lexicon; own-seat use is self-only', () => {
  const files = { ...BASE, 'threads/2026-10-23_misc.md': 'nothing here', 'threads/2026-10-23_round-two.alpha.md': 'wumpel and quenth', 'threads/2026-10-23_round-two.beta.md': 'x' };
  const r = census(zone(files));
  const w = Object.fromEntries(r.words.map((x) => [x.word, x]));
  assert.equal(w.zorblax.status, 'orphan');
  assert.equal(w.frindle.status, 'orphan');
  assert.equal(w.quenth.status, 'self-only');
  assert.equal(w.wumpel.status, 'self-only');
  assert.equal(r.adopted, 0);
});

test('whole word only; lexicon files and marked files are not counted', () => {
  const files = {
    ...BASE,
    'threads/2026-10-23_round-two.beta.md': 'zorblaxes frindlez prezorblax zorblax-ish\n',
    'threads/2026-10-23_round-two.alpha.md': 'nothing',
    'threads/2026-10-23_misc.md': 'x',
    'evidence/report.txt': 'lexicon-census:ignore zorblax quenth frindle\n',
  };
  const r = census(zone(files));
  const z = r.words.find((x) => x.word === 'zorblax');
  assert.equal(z.total, 1, 'only the hyphen-bounded "zorblax-ish" counts; plural and prefixed forms do not');
  assert.equal(r.words.find((x) => x.word === 'quenth').status, 'orphan');
  assert.equal(r.words.find((x) => x.word === 'frindle').status, 'orphan');
  assert.deepEqual(r.ignoredFiles, ['evidence/report.txt']);
});

test('unparseable entries are reported, not dropped', () => {
  const files = { ...BASE, 'builds/shared-lexicon/gamma.md': '# G\n\n' + entry('okword', 'Gamma') + '**badword** is a noun without the colon form\n' };
  const r = census(zone(files));
  assert.equal(r.unparsed.length, 1);
  assert.match(r.unparsed[0].text, /badword/);
  assert.equal(r.totalWords, 7);
  assert.ok(!r.words.some((x) => x.word === 'badword'));
});

test('CLI: exit 0 with a table and valid --json; exit 1 when the lexicon is unreadable', () => {
  const root = zone(BASE);
  const tool = fileURLToPath(new URL('./lexicon-census.mjs', import.meta.url));
  const t = spawnSync(process.execPath, [tool, root], { encoding: 'utf8' });
  assert.equal(t.status, 0);
  assert.match(t.stdout, /adoption rate/);
  const j = spawnSync(process.execPath, [tool, root, '--json'], { encoding: 'utf8' });
  assert.equal(j.status, 0);
  assert.equal(JSON.parse(j.stdout).totalWords, 6);
  const bad = spawnSync(process.execPath, [tool, zone({ 'x.md': 'y' })], { encoding: 'utf8' });
  assert.equal(bad.status, 1);
});

test('isAmbiguous flags short and common words only', () => {
  assert.equal(isAmbiguous('lyth'), 'short');
  assert.equal(isAmbiguous('ambit'), 'common-english');
  assert.equal(isAmbiguous('kessaly'), null);
});
