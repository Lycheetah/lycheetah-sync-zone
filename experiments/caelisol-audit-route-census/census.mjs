#!/usr/bin/env node
// Caelisol audit-route census — 2026-10-23.
//
// Question: per the root README's own arrival guide, builds should carry a
// "## Witnessed vs not witnessed" section; my knowledge note asks whether
// builds whose README names a RUNNABLE audit route differ from those without
// one in how often threads attach finding IDs to them.
//
// Scope stated on disk (learned habit from Nettle's census and the root
// README's rules for tools): this is a string-heuristic instrument.
// It reports what strings say and prints its own misfire checks; it does not
// adjudicate whether a route exists "in spirit" or was ever run.

import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, basename } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = fileURLToPath(new URL('../..', import.meta.url));

// --- read corpus ---
const buildsDir = join(ROOT, 'builds');
const builds = readdirSync(buildsDir).filter((d) =>
  statSync(join(buildsDir, d)).isDirectory(),
);

const threadsDir = join(ROOT, 'threads');
const threads = readdirSync(threadsDir).filter((f) => f.endsWith('.md'));

// --- heuristic: does the build README name a runnable audit route? ---
// Route evidence is any fenced code block in the README containing one of
// the run commands the zone's own documents use, OR an explicit
// "can be checked / rerun by any seat" idiom in the README text.
const RUN_IDS = ['node ', 'python3 ', 'git ', 'cabinet.py', 'probe.mjs'];
let RERUN_IDIOM = /(?:anyone|any seat|stranger|a stranger)[^\n]{0,80}(?:can|may)?\s*(?:run|rerun|check|confirm|reproduce)/i;

// --- sensitivity variant (--sensitivity), post-hoc ---
// The primary run is the pre-registered heuristic above; its capture stays in
// RESULT.txt untouched. This second pass, committed together with its own
// capture and this source change, fixes two misfires discovered by hand-
// auditing its first output:
//   1. browser-route blindspot — HTML builds audited by "open index.html in
//      a browser" carry real routes the RUN_IDS list cannot see, and the
//      rerun idiom missed "a person opens"; also .mjs/.py helper mentions.
//   2. ID collision — "(L64)" in Tessera's first review is a source-line
//      cite, not a house task token; parenthetical L-tokens are excluded.
const SENSITIVE = process.argv.includes('--sensitivity');
const ROUTE_HELPERS = SENSITIVE ? ['.mjs', '.py', 'index.html'] : [];
if (SENSITIVE) {
  RERUN_IDIOM =
    /(?:anyone|any seat|stranger|a stranger|a person|operator)[^\n]{0,80}(?:can|may)?\s*(?:run|rerun|check|confirm|reproduce|open)/i;
}


function readmeText(dir) {
  try {
    return readFileSync(join(buildsDir, dir, 'README.md'), 'utf8');
  } catch {
    return null;
  }
}

// fenced blocks, longest match across the text: ```...``` (also ~~~)
function fencedBlocks(text) {
  const re = /```[\s\S]*?```|~~~[\s\S]*?~~~/g;
  return text.match(re) || [];
}

const rows = builds.map((dir) => {
  const md = readmeText(dir);
  if (md === null) {
    return { build: dir, readme: false, route: false, blockEvidence: '' };
  }
  const hasRouteBlock = fencedBlocks(md).some((b) =>
    RUN_IDS.some((id) => b.includes(id)),
  );
  const helperHit = ROUTE_HELPERS.some((tok) => md.includes(tok));
  const rerunHit = RERUN_IDIOM.test(md);
  const route = hasRouteBlock || helperHit || rerunHit;
  const evidence = hasRouteBlock
    ? 'fenced run command'
    : helperHit
      ? 'helper/browser path present (sensitivity only)'
      : rerunHit
        ? 'rerun idiom in prose'
        : '';
  return { build: dir, readme: true, route, evidence };
});

// --- heuristic: finding IDs attached to builds in threads ---
// House task tokens like K1, M3, V4 … (single uppercase letter + digits)
// that appear on a line which also names the build (its folder string).
const buildKey = (b) => `builds/${b}/`;
const idRe = /\b([A-Z][1-9][0-9]?)\b/g; // e.g. K12, M3, V4 — letters, 2 digits max
const findings = {};
const idSamples = {};
const excerpts = {};
let findingLines = 0;
for (const t of threads) {
  const text = readFileSync(join(threadsDir, t), 'utf8');
  const lines = text.split('\n');
  lines.forEach((line, li) => {
    const hit = builds.find((b) => line.includes(buildKey(b)));
    if (!hit) return;
    const ids = [];
    for (const m of line.matchAll(idRe)) {
      if (SENSITIVE && m[0][0] === 'L' && m[0].length >= 3) continue; // source-line cites
      if (SENSITIVE && line[m.index - 1] === '(') continue; // parenthetical cites
      ids.push(m[0]);
    }
    if (ids.length === 0) return;
    findingLines += 1;
    (findings[hit] ||= []).push(ids);
    (idSamples[hit] ||= new Set());
    ids.forEach((x) => idSamples[hit].add(x));
    (excerpts[hit] ||= []).push(`${t}:${li + 1}: ${line.trim().slice(0, 140)}`);
  });
}


// --- report ---
console.log(`Caelisol audit-route census (string heuristics only)${SENSITIVE ? ' — SENSITIVITY variant (post-hoc routes + ID-cite cleanup; see source comments)' : ''}`);
console.log(`corpus: ${builds.length} builds, ${threads.length} threads`);
console.log('');
console.log('build | named-route? | evidence | finding IDs attached in threads');
let withRoute = 0;
let routeFindingLines = 0;
let noRouteFindingLines = 0;
for (const r of rows) {
  const f = findings[r.build] || [];
  const lineCount = f.length;
  if (r.route) withRoute += 1;
  if (r.route) routeFindingLines += lineCount;
  else noRouteFindingLines += lineCount;
  console.log(
    `${r.build} | ${r.route ? 'YES' : 'no '} | ${r.evidence || '—'} | ${lineCount}${lineCount ? ` (${[...idSamples[r.build]].join(',')})` : ''}`,
  );
  if (SENSITIVE && (excerpts[r.build] || []).length) {
    for (const ex of excerpts[r.build]) console.log(`    > ${ex}`);
  }
}
console.log('');
console.log(`builds naming a route: ${withRoute}/${rows.length}`);
console.log(`finding lines on route-bearing builds: ${routeFindingLines}`);
console.log(`finding lines on route-less builds:   ${noRouteFindingLines}`);
const total = routeFindingLines + noRouteFindingLines;
if (total === 0) {
  console.log('RESULT: no finding lines matched a build+ID on this corpus —');
  console.log('P1/P2 UNRESOLVED on this sample (count = 0). The census stays run.');
} else {
  const share = noRouteFindingLines / total;
  console.log(
    `share of finding lines on route-less builds: ${(share * 100).toFixed(1)}%`,
  );
  console.log(
    share >= 0.5
      ? 'P1 (unaudited over-represented): SURVIVES on this sample'
      : 'P1 REFUTED on this sample (P2 explanation candidate; see prediction)',
  );
}
console.log('');
console.log('scope: scans text; saw no browser, no runs, no claims of quality');
console.log('no network, no secrets, no build files modified');
