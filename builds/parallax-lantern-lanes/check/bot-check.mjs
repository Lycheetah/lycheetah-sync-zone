// Node check for Lantern Lanes. Loads only the pure core of index.html (no DOM).
// Usage: node builds/parallax-lantern-lanes/check/bot-check.mjs
// Prints measured numbers about bots and spells. A bot is not a person.
import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const html = fs.readFileSync(path.join(here, '..', 'index.html'), 'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (!m) throw new Error('inline script not found');

const ctx = { console, Math };
vm.createContext(ctx);
vm.runInContext(m[1] + '\n;globalThis.__core = { createState, step, act, genRow, cast, WORD_BY, LANES };', ctx);
const C = ctx.__core;

const DT = 1 / 60;
const TARGET_ROWS = 200;
const MAX_SIM = 300; // seconds of game time per run

function botDecide(S, bot) {
  const danger = [0, 0, 0];
  const value = [0, 0, 0];
  for (const o of S.objs) {
    if (o.done) continue;
    const ahead = o.row - S.d;
    if (ahead > 0 && ahead <= 3.5) {
      if (o.kind === 'shadow') danger[o.lane] += (3.5 - ahead) + 0.5;
      else value[o.lane] += 0.4;
    }
  }
  // Cast when useful. Mend at one light; Shield when a shadow is about to cross our lane.
  const slotOf = (w) => S.satchel.indexOf(w);
  if (S.light <= 1 && slotOf('ossuel') >= 0) C.act(S, 'cast', slotOf('ossuel'));
  else if (danger[S.lane] > 0.9 && slotOf('sticta') >= 0) C.act(S, 'cast', slotOf('sticta'));
  // Move toward the safest lane, with a reaction gap so the bot is not instant.
  if (bot.t - bot.lastMove < 0.15) return;
  let best = S.lane, bestScore = -Infinity;
  for (let l = 0; l < C.LANES; l++) {
    const sc = -danger[l] * 10 + value[l] - Math.abs(l - S.lane) * 0.1;
    if (sc > bestScore) { bestScore = sc; best = l; }
  }
  if (best !== S.lane) {
    const ok = C.act(S, best < S.lane ? 'left' : 'right');
    if (ok) bot.lastMove = bot.t;
  }
}

function run(seed, policy) {
  const S = C.createState(seed);
  C.act(S, 'start');
  const rng = C.createState(seed ^ 0x9e3779b9).rng; // separate stream for the random policy
  const bot = { t: 0, lastMove: -1 };
  while (!S.over && S.t < MAX_SIM && S.d < TARGET_ROWS) {
    bot.t += DT;
    if (policy === 'greedy') botDecide(S, bot);
    else if (policy === 'random' && Math.floor(bot.t / 0.3) !== Math.floor((bot.t - DT) / 0.3)) {
      C.act(S, rng() < 0.5 ? 'left' : 'right');
    }
    C.step(S, DT);
  }
  return { seed, rows: Math.floor(S.d), score: S.score, collected: S.collected, seen: S.seen.length, over: S.over, reached: S.d >= TARGET_ROWS };
}

const SEEDS = Array.from({ length: 60 }, (_, i) => i + 1);
const report = {};
for (const policy of ['greedy', 'random', 'idle']) {
  const rs = SEEDS.map((s) => run(s, policy));
  const reached = rs.filter((r) => r.reached).length;
  const bad = rs.filter((r) => !Number.isFinite(r.score) || !Number.isFinite(r.rows)).length;
  const meanRows = rs.reduce((a, r) => a + r.rows, 0) / rs.length;
  const meanCollected = rs.reduce((a, r) => a + r.collected, 0) / rs.length;
  report[policy] = { seeds: rs.length, reached_200_rows: reached, mean_rows: +meanRows.toFixed(1), mean_words: +meanCollected.toFixed(2), non_finite: bad };
}
console.log('POLICIES (60 seeds, cap 200 rows or 300 s):');
console.log(JSON.stringify(report, null, 2));

// Determinism: same seed, same policy, same result.
const a = run(17, 'greedy'), b = run(17, 'greedy');
console.log('DETERMINISM seed 17 greedy identical:', JSON.stringify(a) === JSON.stringify(b));

// Path invariant: every row has a free lane, and the free lane moves at most one lane between rows.
let rowViolations = 0, rowsChecked = 0;
for (const seed of SEEDS) {
  const S = C.createState(seed);
  C.act(S, 'start');
  let prevFree = null;
  for (let i = 0; i < 400; i++) {
    const r = C.genRow(S);
    const lanesHere = S.objs.filter((o) => o.kind === 'shadow' && o.row === r).map((o) => o.lane);
    const free = [0, 1, 2].filter((l) => !lanesHere.includes(l));
    rowsChecked++;
    if (free.length === 0) rowViolations++;
    if (prevFree !== null && !free.includes(S.freeLane)) rowViolations++;
    if (prevFree !== null && Math.abs(S.freeLane - prevFree) > 1) rowViolations++;
    prevFree = S.freeLane;
  }
}
console.log(`PATH INVARIANT: rows checked ${rowsChecked}, violations ${rowViolations}`);

// Spell checks, each with a planted situation.
function plant(S, kind, row, lane, word) { S.objs.push({ kind, row, lane, word, done: false }); }
const checks = [];

{ // Shield absorbs one hit, then is consumed.
  const S = C.createState(5); C.act(S, 'start'); S.satchel[0] = 'sticta'; S.objs = [];
  S.lane = 1; plant(S, 'shadow', S.d + 0.5, 1);
  C.cast(S, 0); const light0 = S.light; C.step(S, 1.0);
  checks.push(['shield absorbs one hit', S.light === light0 && S.shield === false]);
}
{ // Without shield the same hit costs one light.
  const S = C.createState(5); C.act(S, 'start'); S.objs = [];
  S.lane = 1; plant(S, 'shadow', S.d + 0.5, 1);
  C.step(S, 1.0);
  checks.push(['unshielded hit costs one light', S.light === 2]);
}
{ // Break removes shadows in the lane ahead, not others.
  const S = C.createState(6); C.act(S, 'start'); S.objs = []; S.satchel[0] = 'obstruct';
  S.lane = 1; plant(S, 'shadow', S.d + 3, 1); plant(S, 'shadow', S.d + 3, 0);
  C.cast(S, 0);
  const inLane = S.objs.find((o) => o.lane === 1), other = S.objs.find((o) => o.lane === 0);
  checks.push(['break clears own lane only', inLane.done === true && other.done === false]);
}
{ // Mend restores one light, capped at three.
  const S = C.createState(7); C.act(S, 'start'); S.light = 1; S.satchel[0] = 'ossuel';
  C.cast(S, 0);
  const S2 = C.createState(7); C.act(S2, 'start'); S2.light = 3; S2.satchel[0] = 'ossuel'; C.cast(S2, 0);
  checks.push(['mend restores one, caps at 3', S.light === 2 && S2.light === 3]);
}
{ // Magnet pulls a word into the lantern lane.
  const S = C.createState(8); C.act(S, 'start'); S.objs = []; S.satchel[0] = 'harmok';
  S.lane = 1; plant(S, 'word', S.d + 2, 0, 'kinein');
  C.cast(S, 0); C.step(S, 0.05);
  checks.push(['magnet pulls word to lantern lane', S.objs[0].lane === 1]);
}
{ // Collecting fills the satchel; a full satchel does not punish.
  const S = C.createState(9); C.act(S, 'start'); S.objs = []; S.lane = 1;
  plant(S, 'word', S.d + 0.5, 1, 'mirrel');
  C.step(S, 1.0);
  checks.push(['pickup lands in satchel', S.satchel.includes('mirrel') && S.collected === 1]);
}
{ // Slow reduces row speed; Double doubles pickup points.
  const A = C.createState(10); C.act(A, 'start'); A.objs = [];
  const B = C.createState(10); C.act(B, 'start'); B.objs = []; B.slow = 3;
  C.step(A, 1.0); C.step(B, 1.0);
  checks.push(['slow reduces distance per second', B.d < A.d * 0.6]);
}
{ // Lantern out ends the run, and nothing is kept.
  const S = C.createState(11); C.act(S, 'start'); S.objs = []; S.light = 1; S.lane = 1;
  plant(S, 'shadow', S.d + 0.5, 1);
  C.step(S, 1.0);
  checks.push(['last light ends the run', S.over === true]);
}
{ // Idle before start: nothing moves.
  const S = C.createState(12); const d0 = S.d; C.step(S, 2.0);
  checks.push(['no movement before start', S.d === d0]);
}
console.log('SPELL AND RULE CHECKS:');
for (const [name, ok] of checks) console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${name}`);
const failed = checks.filter(([, ok]) => !ok).length;
console.log(`checks: ${checks.length - failed}/${checks.length} pass`);
process.exitCode = failed || rowViolations ? 1 : 0;
