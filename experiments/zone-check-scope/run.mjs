#!/usr/bin/env node
// Experiment runner: what does a green zone-check report cover?
//
// It imports the checker's own exported functions, builds a temporary zone
// root per fixture, runs checkZone(), then executes the fixture's inline
// script in a Node vm with a fake DOM. No network. No dependencies.
//
// Usage: node experiments/zone-check-scope/run.mjs

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import vm from 'node:vm';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { checkZone, scanHtml } from '../../tools/zone-check.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(here, '../..');
const fixtures = ['good', 'semantic', 'structural', 'network'];
const expected = { good: '1', semantic: '1', structural: '1', network: '1' };

function scaffolding(root) {
  const seat = path.join(root, 'seats', 'probe');
  fs.mkdirSync(seat, { recursive: true });
  fs.writeFileSync(
    path.join(seat, 'README.md'),
    '# Probe\n\nA fixture seat. It witnesses nothing.\n',
  );

  const threads = path.join(root, 'threads');
  fs.mkdirSync(threads, { recursive: true });
  fs.writeFileSync(
    path.join(threads, '2026-10-23_fixture.md'),
    '# Fixture\n\n## Probe · 2026-10-23\n\nA fixture thread.\n',
  );

  const atlas = path.join(root, 'builds', 'gyre-atlas');
  fs.mkdirSync(atlas, { recursive: true });
  fs.writeFileSync(
    path.join(atlas, 'README.md'),
    '# Atlas fixture\n\nWitnessed vs not witnessed: nothing.\n',
  );
  fs.writeFileSync(
    path.join(atlas, 'index.html'),
    `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Atlas fixture</title>
<style>@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }</style>
</head>
<body><p>Fixture atlas.</p></body>
</html>
`,
  );
}

function makeRoot(fixture) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), `zone-check-scope-${fixture}-`));
  scaffolding(root);
  const dir = path.join(root, 'builds', fixture);
  fs.mkdirSync(dir, { recursive: true });
  fs.copyFileSync(path.join(here, 'fixtures', fixture, 'index.html'), path.join(dir, 'index.html'));
  fs.copyFileSync(path.join(here, 'fixtures', fixture, 'README.md'), path.join(dir, 'README.md'));
  return root;
}

function runFixtureScript(html) {
  const { scripts } = scanHtml(html);
  if (scripts.length !== 1) {
    return { output: null, error: `expected 1 inline script, found ${scripts.length}` };
  }

  const elements = new Map();
  const document = {
    getElementById(id) {
      if (!elements.has(id)) elements.set(id, { textContent: '' });
      return elements.get(id);
    },
  };

  const context = vm.createContext({ document, window: {}, console });
  try {
    vm.runInContext(scripts[0].content, context, { timeout: 1000 });
  } catch (error) {
    return { output: null, error: `${error.name}: ${error.message}` };
  }

  const output = elements.get('count');
  return { output: output ? output.textContent : null, error: null };
}

function declaration(holds) {
  return holds ? 'holds' : 'REFUTED';
}

const source = fs.readFileSync(path.join(repoRoot, 'tools', 'zone-check.mjs'));
const sourceDigest = createHash('sha256').update(source).digest('hex');

console.log('zone-check-scope | Node ' + process.version);
console.log('source: tools/zone-check.mjs sha256 ' + sourceDigest);
console.log('fixtures: ' + fixtures.join(', '));
console.log('');

const checks = [];
let allHold = true;

for (const fixture of fixtures) {
  const root = makeRoot(fixture);
  try {
    const results = checkZone(root);
    const subjects = results.filter((result) => result.subject.startsWith(`builds/${fixture}/`));
    const failures = subjects.filter((result) => result.status === 'FAIL');
    const zoneCheck = failures.length ? 'FAIL' : 'PASS';
    const failedRules = failures.map((result) => result.rule).join('; ') || '—';

    const html = fs.readFileSync(path.join(here, 'fixtures', fixture, 'index.html'), 'utf8');
    const runtime = runFixtureScript(html);
    const runtimeText = runtime.error ? `ERROR (${runtime.error})` : runtime.output;
    const expectedText = expected[fixture];
    const runtimeVerdict = runtime.error
      ? 'error'
      : runtime.output === expectedText
        ? 'correct'
        : 'WRONG';

    let holds;
    if (fixture === 'good') {
      holds = zoneCheck === 'PASS' && runtimeText === '1';
    } else if (fixture === 'semantic') {
      holds = zoneCheck === 'PASS' && runtimeText === '2' && runtimeVerdict === 'WRONG';
    } else {
      holds = zoneCheck === 'FAIL' && runtimeText === '1';
    }
    if (!holds) allHold = false;
    checks.push({ fixture, zoneCheck, runtimeText, expectedText, runtimeVerdict, holds });

    console.log(`[${fixture}]`);
    console.log(`  zone-check: ${zoneCheck}`);
    console.log(`  failed rule(s): ${failedRules}`);
    console.log(`  runtime: ${runtimeText} (expected ${expectedText}) -> ${runtimeVerdict}`);
    console.log('');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
}

console.log('Prediction checks:');
for (const check of checks) {
  console.log(
    `  ${check.fixture}: ${check.zoneCheck} + runtime ${check.runtimeText} (expected ${check.expectedText}) -> ${declaration(check.holds)}`,
  );
}
console.log('');

if (allHold) {
  console.log('RESULT: PASS — the checker passed the semantic defect and failed the structural and network defects.');
  process.exitCode = 0;
} else {
  console.log('RESULT: REFUTED — at least one prediction did not hold; see the checks above.');
  process.exitCode = 1;
}
