// Node check for Dusk Moth. Loads index.html twice:
//   1. the pure core (no DOM), for bot runs and rule checks;
//   2. the page script against a small stub DOM, for a smoke test of the input layer.
// Usage: node builds/parallax-dusk-moth/check/bot-check.mjs
// Prints measured numbers. A bot is not a person, and the stub is not a browser.
import fs from 'node:fs';
import vm from 'node:vm';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const html = fs.readFileSync(path.join(here, '..', 'index.html'), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)?.[1];
if (!script) throw new Error('inline script not found');
const MAX_SHADOWS = Number(script.match(/MAX_SHADOWS = (\d+)/)[1]);
const PULSE_R = Number(script.match(/PULSE_R = (\d+)/)[1]);
const PULSE_COST = Number(script.match(/PULSE_COST = (\d+)/)[1]);
const W = 360;

// ---------------------------------------------------------------- core load
const coreCtx = { console, Math };
vm.createContext(coreCtx);
vm.runInContext(script, coreCtx);
const M = coreCtx.DUSK_MOTH;
if (!M) throw new Error('DUSK_MOTH did not load in Node');
const DT = 1 / 60;
const CAP = 300; // seconds of game time per run

function mulberry(a) {
  return function () {
    a |= 0; a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

// Shortest horizontal difference, wrapping only on the tide night (mirrors gap()).
function dxOf(night, a, b) {
  let d = a - b;
  if (night === 'tide') { if (d > W / 2) d -= W; else if (d < -W / 2) d += W; }
  return d;
}

// ---------------------------------------------------------------- policies
// Every policy only sends move and pulse input. Mirror Moon reverses horizontal
// input in the engine, so a bot that aims must invert it, as a player must.
function aim(g, tx, ty) {
  let mx = tx, my = ty;
  const m = Math.hypot(mx, my);
  if (m > 1e-6) { mx /= m; my /= m; } else { mx = 0; my = 0; }
  if (g.night === 'inverse') mx = -mx;
  return { mx, my };
}

const POLICIES = {
  // The bot the README describes: fly to the nearest ember, pulse when a shadow is close.
  // It does not dodge.
  greedy: (g, p, sight) => {
    let best = null, bd = Infinity;
    for (const e of g.embs) {
      if (e.taken) continue;
      const dx = dxOf(g.night, e.x, g.px), dy = e.y - g.py;
      const d = Math.hypot(dx, dy);
      if (d < sight && d < bd) { bd = d; best = { dx, dy }; }
    }
    let close = false;
    for (const s of g.shads) {
      const d = Math.hypot(dxOf(g.night, s.x, g.px), s.y - g.py);
      if (d < sight && d < PULSE_R * 0.85) close = true;
    }
    const out = best ? aim(g, best.dx, best.dy) : { mx: 0, my: 0 };
    out.pulse = close && g.pulseCool <= 0 && g.dusk > PULSE_COST;
    return out;
  },
  // Greedy, plus a crude dodge: if a shadow is directly ahead, step sideways away from it.
  dodger: (g, p) => {
    let threat = null;
    for (const s of g.shads) {
      const dx = dxOf(g.night, g.px, s.x), dy = s.y - g.py;
      if (dy > -10 && dy < 110 && Math.abs(dx) < 26) { threat = { dx, dy }; break; }
    }
    if (threat) {
      const side = threat.dx === 0 ? (p.r() < 0.5 ? -1 : 1) : Math.sign(threat.dx);
      return { mx: side * (g.night === 'inverse' ? -1 : 1), my: 0, pulse: false };
    }
    return POLICIES.greedy(g, p, Infinity);
  },
  random: (g, p) => {
    if (p.t >= p.next) { p.t = 0; p.next = 0.3; p.dir = [-1, 0, 1][Math.floor(p.r() * 3)]; p.dy = [-1, 0, 1][Math.floor(p.r() * 3)]; }
    p.t += DT;
    return { mx: p.dir || 0, my: p.dy || 0, pulse: false };
  },
  idle: () => ({ mx: 0, my: 0, pulse: false }),
};
// Sighted greedy: the bot can only see things inside a 72 px radius (the Blind Lantern circle).
const SIGHT = 72;

function runGame(seed, policyName, sight = Infinity) {
  const g = M.createGame(seed);
  const rnd = mulberry(seed ^ 0x51ed270b);
  const p = { r: rnd, t: 0, next: 0, dir: 0, dy: 0 };
  let maxShads = 0, framesAtCap = 0, frames = 0, finite = true;
  while (g.state === 'play' && g.t < CAP) {
    const inp = POLICIES[policyName](g, p, sight);
    M.step(g, inp, DT);
    frames++;
    if (!Number.isFinite(g.px) || !Number.isFinite(g.py) || !Number.isFinite(g.dusk) || !Number.isFinite(g.score)) finite = false;
    maxShads = Math.max(maxShads, g.shads.length);
    if (g.shads.length >= MAX_SHADOWS) framesAtCap++;
  }
  const outcome = g.state === 'play' ? 'timeout' : g.state;
  return {
    seed, night: g.nightName, id: g.night, outcome, embers: g.embers, seconds: +g.t.toFixed(1),
    score: Math.round(g.score), frames, finite, maxShads, framesAtCap,
  };
}

// ---------------------------------------------------------------- bot sweep
const SEEDS = Array.from({ length: 60 }, (_, i) => i + 1);
const SEEDS_BY_NIGHT = {};
for (const s of SEEDS) (SEEDS_BY_NIGHT[M.nightFor(s).id] ||= []).push(s);

const sweep = {};
for (const name of ['greedy', 'dodger', 'random', 'idle']) {
  const rs = SEEDS.map((s) => runGame(s, name));
  sweep[name] = summarise(rs);
}
// Sighted greedy on the Blind Lantern nights only.
const blindSeeds = SEEDS.filter((s) => M.nightFor(s).id === 'blind');
const blindSighted = blindSeeds.map((s) => runGame(s, 'greedy', SIGHT));
const blindFull = blindSeeds.map((s) => runGame(s, 'greedy'));

function summarise(rs) {
  const dawn = rs.filter((r) => r.outcome === 'dawn').length;
  const mean = (f) => +(rs.reduce((a, r) => a + f(r), 0) / rs.length).toFixed(1);
  return {
    seeds: rs.length,
    dawn,
    dusk: rs.filter((r) => r.outcome === 'dusk').length,
    timeout: rs.filter((r) => r.outcome === 'timeout').length,
    mean_seconds: mean((r) => r.seconds),
    mean_embers: mean((r) => r.embers),
    non_finite: rs.filter((r) => !r.finite).length,
  };
}

function perNight(rs) {
  const out = {};
  for (const r of rs) {
    out[r.night] ||= { seeds: 0, dawn: 0 };
    out[r.night].seeds++;
    if (r.outcome === 'dawn') out[r.night].dawn++;
  }
  return out;
}

const results = {
  cap_seconds: CAP,
  policies: sweep,
  greedy_per_night: perNight(SEEDS.map((s) => runGame(s, 'greedy'))),
  dodger_per_night: perNight(SEEDS.map((s) => runGame(s, 'dodger'))),
  blind_nights: {
    seeds: blindSeeds.length,
    greedy_full_sight_dawn: blindFull.filter((r) => r.outcome === 'dawn').length,
    greedy_72px_sight_dawn: blindSighted.filter((r) => r.outcome === 'dawn').length,
  },
  echo_shadows: (() => {
    const ECHO_SEEDS = Array.from({ length: 400 }, (_, i) => i + 1).filter((s) => M.nightFor(s).id === 'echo');
    const echo = ECHO_SEEDS.map((s) => runGame(s, 'idle'));
    const echoG = ECHO_SEEDS.map((s) => runGame(s, 'greedy'));
    const all = [...echo, ...echoG];
    return {
      cap: MAX_SHADOWS,
      seeds_run: all.length,
      max_on_screen: Math.max(...all.map((r) => r.maxShads)),
      frames_at_cap: all.reduce((a, r) => a + r.framesAtCap, 0),
      frames_total: all.reduce((a, r) => a + r.frames, 0),
    };
  })(),
};

// ---------------------------------------------------------------- rule checks
const checks = [];
{ // Determinism: same seed and policy, same result.
  const a = JSON.stringify(runGame(17, 'greedy')), b = JSON.stringify(runGame(17, 'greedy'));
  checks.push(['same seed and policy give the same run', a === b]);
}
{ // Every seed resolves to exactly one night, and all six nights occur in 1..60.
  const ids = new Set(SEEDS.map((s) => M.nightFor(s).id));
  checks.push(['all six nights occur in seeds 1..60', ids.size === M.NIGHTS.length]);
}
{ // Tide wraps; plain does not.
  const t = M.createGame(seedWhere('tide'));
  t.px = 2; M.step(t, { mx: -1, my: 0, pulse: false }, 0.05);
  const p = M.createGame(seedWhere('plain'));
  p.px = 2; M.step(p, { mx: -1, my: 0, pulse: false }, 0.05);
  checks.push(['tide wraps the left wall', t.px > 300 && t.px < W]);
  checks.push(['plain clamps at the wall', p.px === 10]);
}
{ // Mirror Moon reverses horizontal input only.
  const m = M.createGame(seedWhere('inverse'));
  const x0 = m.px; M.step(m, { mx: 1, my: 0, pulse: false }, 0.1);
  checks.push(['mirror moon moves the moth left on right input', m.px < x0]);
}
{ // Pulse costs dusk and starts a cooldown.
  const g = M.createGame(seedWhere('plain'));
  const d0 = g.dusk; M.step(g, { mx: 0, my: 0, pulse: true }, DT);
  checks.push(['pulse costs dusk (net of drain)', d0 - g.dusk > PULSE_COST - 1 && g.pulseCool > 0]);
}
{ // Fourteen embers end the run as dawn; zero dusk ends it as dusk.
  const g = M.createGame(seedWhere('plain')); g.embers = 14; M.step(g, {}, DT);
  checks.push(['fourteen embers end in dawn', g.state === 'dawn']);
  const k = M.createGame(seedWhere('plain')); k.dusk = 0.01; M.step(k, {}, DT);
  checks.push(['dusk at zero ends the run as dusk', k.state === 'dusk']);
}
{ // Heavy Tithe drains twice as fast.
  const a = M.createGame(seedWhere('plain')), b = M.createGame(seedWhere('tithe'));
  M.step(a, {}, DT); M.step(b, {}, DT);
  checks.push(['heavy tithe drains twice as fast', Math.abs((100 - b.dusk) - 2 * (100 - a.dusk)) < 1e-6]);
}

function seedWhere(id) {
  for (let s = 1; s < 100000; s++) if (M.nightFor(s).id === id) return s;
  throw new Error('no seed for ' + id);
}

// ---------------------------------------------------------------- DOM smoke (stub, not a browser)
function domSmoke({ hash = '', script: sc, drive }) {
  const texts = [];
  const translates = [];
  const rafQ = [];
  const listeners = new Map();
  const grad = { addColorStop() {}, width: 10 };
  const ctx2d = new Proxy({}, {
    get(t, k) {
      if (k in t) return t[k];
      if (k === 'measureText') return () => grad;
      if (/Gradient$/.test(String(k))) return () => grad;
      return (...a) => {
        if (k === 'fillText') texts.push(String(a[0]));
        if (k === 'translate') translates.push([a[0], a[1]]);
        return undefined;
      };
    },
    set(t, k, v) { t[k] = v; return true; },
  });
  const mkEl = (id) => {
    const el = {
      id, hidden: false, textContent: '', dataset: {}, style: {}, clientWidth: 360, clientHeight: 640,
      width: 0, height: 0, tagName: 'DIV',
      classList: { add() {}, remove() {}, toggle() {}, contains: () => false },
      focus() {}, click() {}, setAttribute() {}, setPointerCapture() {},
      getBoundingClientRect: () => ({ left: 0, top: 0, width: 360, height: 640 }),
      getContext: () => ctx2d,
      addEventListener(t, f) { if (!listeners.has(el)) listeners.set(el, {}); (listeners.get(el)[t] ||= []).push(f); },
      querySelectorAll: () => [],
    };
    return el;
  };
  const els = {};
  const document = { getElementById: (id) => (els[id] ||= mkEl(id)), addEventListener() {} };
  const winL = {};
  const windowObj = {
    innerWidth: 360, innerHeight: 640, devicePixelRatio: 1,
    addEventListener(t, f) { (winL[t] ||= []).push(f); },
  };
  const ctx = {
    console, Math, Number, String, Array, JSON, Object, Set, Map, Proxy,
    window: windowObj, document, location: { hash, search: '' },
    performance: { now: () => clock }, requestAnimationFrame: (f) => rafQ.push(f),
  };
  let clock = 0;
  ctx.globalThis = ctx;
  vm.createContext(ctx);
  vm.runInContext(sc, ctx);

  const frame = (ms) => { clock = ms; const cb = rafQ.shift(); if (cb) cb(ms); };
  const fire = (el, type, ev = {}) => {
    const l = listeners.get(el)?.[type] || [];
    for (const f of l) f({ preventDefault() {}, target: undefined, ...ev });
  };
  const key = (k) => { for (const f of winL.keydown || []) f({ key: k, preventDefault() {}, target: undefined }); };
  let t = 0;
  const tick = (n) => { for (let i = 0; i < n; i++) { t += 1000 / 60; frame(t); } };
  return { els, texts, translates, tick, fire, key, rafQ, drive, run: () => drive({ tick, fire, key, els, texts, translates, fire }) };
}

const smokes = [];
{ // P2: a Space pressed on the end card must not pulse the next night.
  const sc = script;
  const smoke = domSmoke({
    script: sc,
    drive: ({ tick, fire, key, els, texts }) => {
      tick(2);
      key('Enter'); // begin, then play with no input until the end card shows
      let guard = 0;
      while (els.end.hidden && guard++ < 60 * 300) tick(1);
      key(' ');     // Space on the end card
      fire(els.same, 'click'); // This night again
      texts.length = 0;
      tick(1);
      const cool = texts.find((x) => x.startsWith('pulse '));
      smokes.push({ name: 'space on end card does not pulse next night', ok: cool === 'pulse ready', detail: cool });
    },
  });
  smoke.run();
}
{ // P3: a drag held to the right of the moth on the tide night should wrap left, not travel right.
  const seed = seedWhere('tide');
  const smoke = domSmoke({
    hash: '#seed=' + seed,
    script: script,
    drive: ({ tick, fire, els, translates }) => {
      tick(1);
      // "This night again" keeps the hash seed (Begin would roll a fresh one).
      const onTide = /Wrapping Tide/.test(els.preview.textContent);
      fire(els.same, 'click');
      tick(1);
      // Drag left until the moth sits near x=3 (it starts at x=180), at the left seam.
      fire(els.field, 'pointerdown', { pointerId: 1, clientX: 180, clientY: 400 });
      fire(els.field, 'pointermove', { pointerId: 1, clientX: 3, clientY: 400 });
      tick(120);
      // Now drag to x=300. The short way is left, across the seam (about 63 px).
      // The long way is right (297 px). Three frames tell them apart.
      fire(els.field, 'pointermove', { pointerId: 1, clientX: 300, clientY: 400 });
      translates.length = 0;
      tick(3);
      const last = translates.filter((x) => x[1] !== undefined).pop();
      const x = last ? ((last[0] % W) + W) % W : NaN;
      const shortWay = x > 300; // moved left, across the seam
      smokes.push({ name: 'tide drag wraps the short way', ok: shortWay && onTide, detail: `tide night ${onTide}; moth x after 3 frames: ` + x.toFixed(1) });
    },
  });
  smoke.run();
}

// ---------------------------------------------------------------- report
console.log('SWEEP (60 seeds, cap 300 s game time):');
console.log(JSON.stringify(results, null, 2));
console.log('RULE CHECKS:');
for (const [name, ok] of checks) console.log(`  ${ok ? 'PASS' : 'FAIL'}  ${name}`);
console.log('DOM SMOKE (stub DOM, not a browser):');
for (const s of smokes) console.log(`  ${s.ok ? 'PASS' : 'FAIL'}  ${s.name}  [${s.detail}]`);
const failed = checks.filter(([, ok]) => !ok).length + smokes.filter((s) => !s.ok).length;
console.log(`checks: ${checks.length + smokes.length - failed}/${checks.length + smokes.length} pass`);
process.exitCode = failed ? 1 : 0;
