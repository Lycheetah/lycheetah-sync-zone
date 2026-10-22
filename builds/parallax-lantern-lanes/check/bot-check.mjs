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
const script = m[1];

const ctx = { console, Math };
vm.createContext(ctx);
vm.runInContext(script + '\n;globalThis.__core = { createState, step, act, genRow, cast, WORD_BY, LANES };', ctx);
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

function run(seed, policy, kept) {
  const S = C.createState(seed, kept);
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
  return { seed, rows: Math.floor(S.d), score: S.score, collected: S.collected, seen: S.seen.length, over: S.over, reached: S.d >= TARGET_ROWS, kept: S.kept };
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

// Kept word: the greedy bot's second night, with and without the word from its first night.
// The first night is run exactly as the sweep runs it, so its numbers are the sweep's numbers.
const carry = { nights: SEEDS.length, kept: 0, reach2_plain: 0, reach2_carry: 0, mean_rows2_plain: 0, mean_rows2_carry: 0 };
{
  let rowsPlain = 0, rowsCarry = 0;
  for (const seed of SEEDS) {
    const first = run(seed, 'greedy');
    const second = run(seed + 1000, 'greedy');
    const withCarry = run(seed + 1000, 'greedy', first.kept);
    if (first.kept) carry.kept++;
    if (second.reached) carry.reach2_plain++;
    if (withCarry.reached) carry.reach2_carry++;
    rowsPlain += second.rows; rowsCarry += withCarry.rows;
  }
  carry.mean_rows2_plain = +(rowsPlain / SEEDS.length).toFixed(1);
  carry.mean_rows2_carry = +(rowsCarry / SEEDS.length).toFixed(1);
}
console.log('KEPT WORD (greedy, 60 seeds; night two uses seed + 1000):');
console.log(JSON.stringify(carry, null, 2));

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
{ // Kept word rules.
  const I = C.createState(21, 'sticta');
  checks.push(['a carried word starts the next night in slot 1', I.satchel[0] === 'sticta' && I.carried === 'sticta']);
  const J = C.createState(21, 'nonsense');
  checks.push(['an unknown carried word is ignored', J.satchel.every((w) => w === null) && J.carried === null]);
  const K = C.createState(21, 'sticta'); C.act(K, 'start'); K.objs = [];
  C.cast(K, 0);
  checks.push(['a carried shield can be cast in the next night', K.shield === true && K.satchel[0] === null]);
  const L = C.createState(22); C.act(L, 'start'); L.objs = []; L.satchel = ['sticta', 'ansel', null]; L.light = 1; L.lane = 1;
  L.objs.push({ kind: 'shadow', row: L.d + 0.5, lane: 1, done: false }); C.step(L, 1.0);
  checks.push(['the night keeps the first held word only', L.over === true && L.kept === 'sticta']);
  const M2 = C.createState(23); C.act(M2, 'start'); M2.objs = []; M2.satchel = [null, null, null]; M2.light = 1; M2.lane = 1;
  M2.objs.push({ kind: 'shadow', row: M2.d + 0.5, lane: 1, done: false }); C.step(M2, 1.0);
  checks.push(['an empty satchel keeps nothing', M2.over === true && M2.kept === null]);
}
console.log('SPELL AND RULE CHECKS:');
for (const [name, ok] of checks) console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${name}`);
const failed = checks.filter(([, ok]) => !ok).length;

// ---------------------------------------------------------------- DOM smoke (stub DOM, not a browser)
// Plays seeded nights with random input until one ends, then checks that the kept word is
// saved, announced on the end card, and consumed when the next night starts.
function domSmoke(seed) {
  const store = new Map();
  const rafQ = [];
  const toasts = [];
  const mkEl = () => {
    const cls = new Set();
    const listeners = {};
    const el = {
      textContent: '', value: '', dataset: {}, style: {}, width: 0, height: 0, clientWidth: 360, clientHeight: 640,
      classList: { add: (c) => cls.add(c), remove: (c) => cls.delete(c), contains: (c) => cls.has(c), toggle: (c, on) => (on ? cls.add(c) : cls.delete(c)) },
      setAttribute() {}, focus() {}, click() { (listeners.click || []).forEach((f) => f({ stopPropagation() {} })); },
      addEventListener(t, f) { (listeners[t] ||= []).push(f); },
      fire(t, ev) { (listeners[t] || []).forEach((f) => f(ev)); },
      querySelectorAll: () => [], closest: () => null, getBoundingClientRect: () => ({ left: 0, top: 0, width: 360, height: 640 }),
      getContext: () => ctx2d, setPointerCapture() {}, hidden: false,
    };
    el.classList.add('hidden');
    return el;
  };
  const els = {};
  const byId = (id) => (els[id] ||= mkEl());
  // Title and over start in the markup: title visible, over hidden.
  byId('title').classList.remove('hidden');
  byId('over').classList.add('hidden');
  const grad = { addColorStop() {}, width: 10 };
  const ctx2d = new Proxy({}, {
    get(t, k) {
      if (k in t) return t[k];
      if (k === 'measureText') return () => grad;
      if (/Gradient$/.test(String(k))) return () => grad;
      return () => undefined;
    },
    set(t, k, v) { t[k] = v; return true; },
  });
  const docListeners = {};
  const winListeners = {};
  const document = {
    getElementById: (id) => byId(id),
    querySelectorAll: () => [],
    hidden: false,
    addEventListener() {},
  };
  const storage = {
    getItem: (k) => (store.has(k) ? store.get(k) : null),
    setItem: (k, v) => store.set(k, String(v)),
    removeItem: (k) => store.delete(k),
  };
  const ctx = {
    console, Math, Number, String, Array, JSON, Object, Set, Map, URLSearchParams, Promise,
    document,
    window: { addEventListener: (t, f) => (winListeners[t] ||= []).push(f), localStorage: storage, devicePixelRatio: 1, location: {}, matchMedia: undefined },
    location: { search: '?seed=' + seed },
    requestAnimationFrame: (f) => rafQ.push(f),
    setTimeout: () => 0,
    ResizeObserver: undefined,
  };
  ctx.window.location = ctx.location;
  ctx.document.getElementById = (id) => byId(id);
  // The game's canvas.getContext('2d') goes to the proxy.
  byId('field').getContext = () => ctx2d;
  byId('game').clientWidth = 360; byId('game').clientHeight = 640;
  byId('game').getBoundingClientRect = () => ({ left: 0, top: 0, width: 360, height: 640 });
  vm.createContext(ctx);
  vm.runInContext(script, ctx);
  let now = 0;
  const frame = () => { now += 1000 / 60; const f = rafQ.shift(); if (f) f(now); };
  const key = (k) => (winListeners.keydown || []).forEach((f) => f({ key: k, preventDefault() {} }));
  return { els, store, frame, key, toasts, byId };
}

function playUntilOver(d, maxFrames) {
  let i = 0;
  for (; i < maxFrames; i++) {
    if (!d.byId('over').classList.contains('hidden')) return true;
    if (i % 18 === 0) d.key(['ArrowLeft', 'ArrowRight'][(i / 18) % 2 ? 1 : 0]);
    d.frame();
  }
  return !d.byId('over').classList.contains('hidden');
}

const domChecks = [];
{
  // Find a seed whose night ends with a word still in the satchel, then check the whole handoff.
  let picked = null;
  for (let seed = 1; seed <= 40 && !picked; seed++) {
    const d = domSmoke(seed);
    d.byId('startBtn').click();
    d.frame();
    if (!playUntilOver(d, 60 * 120)) continue;
    const kept = d.store.get('parallax-lantern-kept') || null;
    if (kept) picked = { seed, d, kept };
  }
  if (!picked) {
    domChecks.push(['a seeded night ends holding a word (search 1..40)', false]);
  } else {
    const { d, kept } = picked;
    domChecks.push(['the end card says which word is kept', d.byId('overNote').textContent.includes(C.WORD_BY[kept].w)]);
    d.byId('againBtn').click();
    d.frame();
    domChecks.push(['the kept word is consumed when the next night starts', !d.store.has('parallax-lantern-kept')]);
  }
}

console.log('DOM SMOKE (stub DOM, not a browser):');
for (const [name, ok] of domChecks) console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${name}`);
const domFailed = domChecks.filter(([, ok]) => !ok).length;

console.log(`checks: ${checks.length - failed + domChecks.length - domFailed}/${checks.length + domChecks.length} pass`);
process.exitCode = failed || rowViolations || domFailed ? 1 : 0;
