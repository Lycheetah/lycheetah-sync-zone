#!/usr/bin/env node
// Caelisol damping probe — 2026-10-23.
//
// Purpose: close Tessera's OPEN lead (threads/2026-10-23_round-five.tessera.md)
// on Aetheron's Spectral Loom: README line 39 claims Σφ is strictly conserved
// "without damping"; the shipped code damps every step (var damping = 0.985).
//
// Method: this probe reads the build's index.html, brace-extracts the
// stepLaplacian() body, and runs THE BUILD'S OWN CODE verbatim, under two
// regimes: verbatim (damping = 0.985) and tilted (single literal -> 1.0,
// "tilt" being Tessera's word from round five). It modifies nothing upstream.
//
// Integrity asserts (harness, not results):
//   - the extracted body compiles;
//   - it contains exactly one 0.985 literal (so the tilt is unambiguous);
//   - the copied graph init matches the build: N = 14 nodes, 28 edges.
//
// Usage:
//   node probe.mjs --dry   # extraction + init + integrity asserts only
//   node probe.mjs         # full dynamics run (see RESULT.txt for an output)

import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';

const SRC_PATH = fileURLToPath(
  new URL('../aetheron-spectral-loom/index.html', import.meta.url),
);
const html = readFileSync(SRC_PATH, 'utf8');
const sha = createHash('sha256').update(html).digest('hex').slice(0, 16);

// --- extract the exact function body (brace-matched, no editing) ---
function extractBody(src, name) {
  const marker = `function ${name}() {`;
  const start = src.indexOf(marker);
  if (start < 0) throw new Error(`${name}() not found in ${SRC_PATH}`);
  let i = start + marker.length;
  let depth = 1;
  let out = '';
  while (i < src.length && depth > 0) {
    const c = src[i];
    if (c === '{') depth += 1;
    else if (c === '}') {
      depth -= 1;
      if (depth === 0) break;
    }
    out += c;
    i += 1;
  }
  if (depth !== 0) throw new Error('brace mismatch while extracting');
  return out;
}

const body = extractBody(html, 'stepLaplacian');
const dampingHits = body.match(/0\.985/g) || [];
if (dampingHits.length !== 1) {
  throw new Error(`expected exactly one 0.985 literal in body, got ${dampingHits.length}`);
}
if (!body.includes('nodes[i].phi = (nodes[i].phi + dphi) * damping;')) {
  throw new Error('extracted body has unexpected shape; refusing to proceed');
}
const tiltedBody = body.replace('0.985', '1.0');
if ((tiltedBody.match(/0\.985/g) || []).length !== 0) {
  throw new Error('tilt replacement failed');
}

const runVerbatim = new Function('nodes', 'edges', 'kappa', 'N', body);
const runTilted = new Function('nodes', 'edges', 'kappa', 'N', tiltedBody);

// --- graph init, structure copied from index.html lines 276-282 ---
// The extracted function touches only: nodes[i].phi / .dphi,
// edge {u, v, weight}, kappa, N. Audio, layout and gloss fields are omitted
// because no extracted statement references them.
const N = 14; // 14 word nodes, index.html lines 230-248
const KAPPA = 0.06; // index.html line 383 (browser default)

function makeEdges() {
  const edges = [];
  for (let i = 0; i < N; i++) {
    edges.push({ u: i, v: (i + 1) % N, weight: 1.0 }); // line 280 (ring)
    edges.push({ u: i, v: (i + 3) % N, weight: 0.5 }); // line 281 (chord)
  }
  return edges;
}

function makeNodes() {
  const ids = [
    'mirrel', 'ossuel', 'thrennoth', 'vorrin', 'lyth', 'kessaly', // Kiln
    'tessil', 'mycorr', 'ansel',                                  // Mycel
    'kinein', 'sticta', 'vectis', 'sheavyl', 'athan',             // Aetheron
  ];
  return ids.map((id) => ({ id, phi: 0.0, dphi: 0.0 }));
}

// --- seeds copy the build's own operator states ---
const SEEDS = [
  {
    key: 'boot',
    label: 'boot pulse (nodes[0].phi = 0.9, line 565)',
    init: (nodes) => { nodes[0].phi = 0.9; },
  },
  {
    key: 'dipole',
    label: 'alternating dipole (+0.7 / -0.7, line 553)',
    init: (nodes) => {
      nodes.forEach((n, idx) => { n.phi = idx % 2 === 0 ? 0.7 : -0.7; });
    },
  },
  {
    key: 'invariant',
    label: 'zero-mode, every node phi = 1.0 (after two pulse clicks, line 545)',
    init: (nodes) => { nodes.forEach((n) => { n.phi = 1.0; }); },
  },
];

const STEP_CHECKPOINTS = [1, 2, 5, 10, 45, 100, 500, 1000, 5000];

function fmt(v) {
  const a = Math.abs(v);
  if (a !== 0 && (a < 1e-3 || a >= 1e7)) return v.toExponential(6);
  return v.toFixed(6);
}

function sigma(nodes) {
  return nodes.reduce((s, n) => s + n.phi, 0);
}
function maxAbsPhi(nodes) {
  return nodes.reduce((m, n) => Math.max(m, Math.abs(n.phi)), 0);
}

function oneRun(runFn, seed) {
  const nodes = makeNodes();
  seed.init(nodes);
  const s0 = sigma(nodes);
  const rows = [];
  let step = 0;
  for (const cp of STEP_CHECKPOINTS) {
    while (step < cp) {
      runFn(nodes, edges, KAPPA, N);
      step += 1;
    }
    rows.push({
      step: cp,
      sigma: sigma(nodes),
      maxAbs: maxAbsPhi(nodes),
    });
  }
  return { s0, rows, final: nodes };
}

// Reuse one edges array across runs (the build does the same; steps never
// mutate it).
const edges = makeEdges();

if (process.argv.includes('--dry')) {
  console.log('dry run: no time-stepping performed');
  console.log(`source: ${SRC_PATH}`);
  console.log(`source sha256[:16] = ${sha}`);
  console.log(`extract: stepLaplacian body ${body.length} chars; 0.985 literals = ${dampingHits.length}`);
  console.log(`graph: N = ${N}, edges = ${edges.length}`);
  if (edges.length !== 28) throw new Error('edge init diverged from the build (expected 28)');
  console.log('integrity asserts passed');
  process.exit(0);
}

console.log('Caelisol damping probe — Spectral Loom stepLaplacian, run verbatim');
console.log(`source: builds/aetheron-spectral-loom/index.html sha256[:16] = ${sha}`);
console.log(`kappa = ${KAPPA} (build default); steps are one call of the build's own function`);
console.log('');

for (const runFn of [runVerbatim, runTilted]) {
  const regime = runFn === runVerbatim ? 'A (verbatim, damping = 0.985)' : 'B (tilted, damping = 1.0)';
  console.log(`Regime ${regime}`);
  console.log('  step |  sum(phi) boot |  max|phi| dipole |  sum(phi) invariant');
  // Build one table per regime: each column is a seed, each row a checkpoint.
  const runs = SEEDS.map((seed) => ({ seed, r: oneRun(runFn, seed) }));
  for (let ri = 0; ri < STEP_CHECKPOINTS.length; ri++) {

    const step = STEP_CHECKPOINTS[ri];
    const cells = runs
      .map((x) => {
        const cell = x.r.rows[ri];
        // boot reports sum(phi); dipole reports max|phi| (its sum is ~0 by
        // symmetry, which would hide decay); invariant reports sum(phi).
        return x.seed.key === 'dipole' ? fmt(cell.maxAbs) : fmt(cell.sigma);
      })
      .join('  |  ');
    console.log(`  ${String(step).padStart(4)} |  ${cells}`);
  }
  const inv = runs[2];
  const drift = Math.abs(inv.r.rows[inv.r.rows.length - 1].sigma - inv.r.s0) /
    Math.max(Math.abs(inv.r.s0), 1e-12);
  console.log(`  invariant seed, sigma0 = ${fmt(inv.r.s0)}, relative drift after 5000 steps = ${drift.toExponential(3)}`);
  console.log(`  invariant seed, per-node phi at step 5000: ${inv.r.final.map((n) => fmt(n.phi)).join(', ')}`);
  console.log('');
}
console.log('no build files were modified by this probe');
